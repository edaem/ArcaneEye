# Arcane Eye
Arcane Eye is a discord bot that serves information about the strategy card game Wizards of the Grimoire  

## /card
    /card card_name public

`card_name` = any card name from Wizards of the Grimoire.  
`public` = Optional argument. Expects a value of either true or false. If true, the bot will publically reply. Otherwise, it will respond with an ephemeral message (only you can see it). Defaults to true.  

Returns an image of the requested card. Please note that the spelling must be correct, but the card name is not case sensitive. There is also auto complete for this function.  

## /card_text
    /card_text card_name public

`card_name` = any card name from Wizards of the Grimoire.  
`public` = Optional argument. Expects a value of either true or false. If true, the bot will publically reply. Otherwise, it will respond with an ephemeral message (only you can see it). Defaults to true.  

Returns information about the requested card as text. Please note that the spelling must be correct, but the card name is not case sensitive. There is also auto complete for this function.  

## /gallery
    /gallery public

`public` = Optional argument. Expects a value of either true or false. If true, the bot will publically reply. Otherwise, it will respond with an ephemeral message (only you can see it). Defaults to false.  

Returns a link to the imgur gallery of all cards (https://imgur.com/a/X0mNcbZ).
