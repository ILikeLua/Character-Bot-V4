import discord
from discord.ext import commands
from discord.ext.commands import Context

from SQLInterface import SQL_Connection


class ServerWork(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.SI = SQL_Connection()

    @commands.Cog.listener()
    async def on_ready(self):
        user = self.bot.user
        print(f"Logged in as {user.name} ({user.id})")
        print("------")

    @commands.command()
    async def addchar(self, ctx: Context, name: str, description: str):
        """Adds a character to the database if it doesn't already
        exist attached to the user, also {},@ not aloud in name

        Parameters
        ----------
        ctx : Context
            Context
        name : str
            OC's Name
        description : str
            Description
        """
        if ctx.message.mentions:
            await ctx.reply("You cannot mention people in your character.")
            return

        if "{" in name or "}" in name:
            await ctx.reply("You cannot use {} in your character name.")
            return

        embed = discord.Embed(
            title=name,
            description=description,
        )

        if self.SI.getCharacter(ctx.author.id, name):
            self.SI.updateCharacter(ctx.author.id, name, description)
            embed.set_author(name="Your OC has been updated!")
        else:
            self.SI.createCharacter(ctx.author.id, name, description)
            embed.set_author(name="Your OC has been added!")

        await ctx.reply(embed=embed)

    @commands.command()
    async def delchar(self, ctx: Context, name: str):
        """Deletes a character from the database if it exists attached to the user

        Parameters
        ----------
        ctx : Context
            Context
        name : str
            OC's Name
        """
        if self.SI.getCharacter(ctx.author.id, name):
            self.SI.deleteCharacter(ctx.author.id, name)
            await ctx.reply(f"Your OC {name!r} has been deleted!")
        else:
            await ctx.reply(f"You don't have an OC named {name}!")

    @commands.command(name="char")
    async def getchar(self, ctx: Context, name: str):
        """Retrieves character information, unless it doesn't exist
        or there are multiple characters named

        Parameters
        ----------
        ctx : Context
            Context
        name : str
            OC's Name
        """
        ml = self.SI.getMultiList(name)
        if self.SI.checkIfOne(name) and "{" not in name:
            embed = discord.Embed(
                title=ml[0][0],
                description=ml[0][1],
            )
            embed.set_author(name="Your OC!")
            await ctx.reply(embed=embed)
        elif "{" in name:
            entries = "\n".join(
                f"{c_name}{{{c_id}}}" for c_name, c_id in ml if c_name == name
            )
            await ctx.reply(f"Characters with the name {name!r}:\n{entries}")
        else:
            await ctx.reply(self.SI.getList(name) or "No characters found!")

        """
        How I would do it
        -----------------

        if character := self.SI.getCharacter(ctx.author.id, name):
            embed = discord.Embed(
                title=character[0],
                description=character[1],
            )
            await ctx.reply(embed=embed)
        elif "{" in name:
            entries = "\n".join(
                f"{c_name}{{{c_id}}}" for c_name, c_id in ml if c_name == name
            )
            await ctx.reply(f"Characters with the name {name!r}:\n{entries}")
        else:
            await ctx.reply(self.SI.getList(name))
        """

    @commands.command(name="list")
    async def charlist(self, ctx: Context, name: str):
        """Retrieves all characters attached to the user

        Parameters
        ----------
        ctx : Context
            Context
        name : str
            Username of the person to lookup
        """
        await ctx.reply(self.SI.getList(name))
