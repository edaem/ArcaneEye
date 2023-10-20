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
	bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

	# on ready event
	@bot.event
	async def on_ready():
		print(f"The Arcane Eye has opened.")
		try:
			synced = await bot.tree.sync()
			print(f"Synced {len(synced)} command(s)")
		except Exception as e:
			print(e) 

	### /card command ###
	@bot.tree.command(name="card", description="Display an image of the requested card. Spelling must be exact, but the name isn't case sensitive.")
	@app_commands.describe(card_name="The exact name of the card.")
	@app_commands.rename(card_name="name")
	async def show_card(interaction: discord.Interaction, card_name: str):
		if card_name in cards: #sends image if card name is valid
			await interaction.response.send_message(f"{cards[card_name.lower()]['Link']}")
		else: #responds to just the caller to let them know a card wasn't found if name is invalid
			await interaction.response.send_message(f"I can't find a card named {card_name}.", ephemeral=True)

	# autocomplete function for /card
	@show_card.autocomplete("card_name")
	async def sc_autocomp(interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
		matches = []
		for cname in names:
			if current.lower() in cname:
				matches.append(app_commands.Choice(name=cname.title(), value=cname))
				if len(matches) >= 25:
					break
		
		return matches
	### /card command end ###

	#log_handler set to None as we set up our own logging above
	bot.run(TOKEN, log_handler=None)
