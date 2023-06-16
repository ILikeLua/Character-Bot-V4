import asyncio
import json

import discord
from discord.ext import commands

with open("BOTInfo.json", "r") as JsonHold:
    DATA = json.load(JsonHold)


class Helper(commands.HelpCommand):
    async def send_bot_help(self, _):
        target = self.get_destination()
        await target.send(
            "\n".join(
                [
                    "* To add a character use",
                    " * **!addchar <name>\n<description>**",
                    "* To delete a character use",
                    " * **!delchar <name>**",
                    "* To list a character use",
                    " * **!char <name>**",
                    "* To list all your characters in the bot use",
                    " * **!List**",
                ]
            )
        )


bot = commands.Bot(
    command_prefix="!",
    help_command=Helper(),
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions(
        users=False,
        roles=False,
        everyone=False,
        replied_user=True,
    ),
)


if __name__ == "__main__":
    bot.load_extension("cogs.serverwork")
    asyncio.run(bot.start(token=DATA["token"]))
