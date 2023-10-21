import discord
from discord import app_commands
from discord.ext import commands
from config import TOKEN
import logging
import logging.handlers
import json
import typing

# loads the card information from JSON file
with open('wotgcards.json') as cards_file:
	cards = json.load(cards_file)
	names = cards.keys()

# run command for the bot, named open_eye for aesthetics 
def open_eye():
	### set up logging ###
	logger = logging.getLogger('discord')
	logger.setLevel(logging.INFO)

	handler = logging.handlers.RotatingFileHandler(
		filename="discord.log",
		encoding="utf-8",
		maxBytes= 32 * 1024 * 1024,
		backupCount=5,
	)
	dt_fmt = '%Y-%m-%d %H:%M:%S'
	formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	### end logging setup ###

	# instance a Bot
	eye = commands.Bot(command_prefix="!", intents=discord.Intents.all())

	# on ready event
	@eye.event
	async def on_ready():
		print(f"The Arcane Eye has opened.")
		try:
			synced = await eye.tree.sync()
			print(f"Synced {len(synced)} command(s)")
		except Exception as e:
			print(e) 

	### /card command ###
	@eye.tree.command(name="card", description="Display an image of the requested card. Spelling must be exact, but the name isn't case sensitive.")
	@app_commands.describe(card_name="The exact name of the card.")
	@app_commands.rename(card_name="name")
	@app_commands.describe(public = "Optional. Enter true to have the bot publically respond with the card. False will be just to you. Defaults to true.")
	async def show_card(interaction: discord.Interaction, card_name: str, public: typing.Literal['true','false'] = None):
		if public is None:
			ephem = False
		else:
			ephem = True if public.lower() == "false" else False
		if card_name in cards: #sends image if card name is valid
			await interaction.response.send_message(f"{cards[card_name.lower()]['Link']}", ephemeral=ephem)
		else: #responds to just the caller to let them know a card wasn't found if name is invalid
			await interaction.response.send_message(f"I can't find a card named {card_name}.", ephemeral=True)

	# autocomplete function for /card
	@show_card.autocomplete("card_name")
	async def sc_autocomp(interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
		matches = []
		for cname in names:
			if current.lower() in cname: #adds card name to choices if the current string is a substring of the name
				matches.append(app_commands.Choice(name=cname.title(), value=cname))
				if len(matches) >= 25: #can only return max 25 choices at a time
					break
		
		return matches
	### /card command end ###

	### /gallery command ###
	@eye.tree.command(name="gallery", description="Provides link to the imgur gallery of card images.")
	@app_commands.describe(public = "Optional. Enter true to have the bot publically respond with the link. False will be just to you. Defaults to false.")
	async def share_gallery(interaction: discord.Interaction, public: typing.Literal['true','false'] = None):
		if public is None:
			ephem = True
		else:
			ephem = False if public.lower() == "true" else True
		await interaction.response.send_message("https://imgur.com/a/X0mNcbZ", ephemeral=ephem)
	### /gallery command end ###

	#log_handler set to None as we set up our own logging above
	eye.run(TOKEN, log_handler=None)
