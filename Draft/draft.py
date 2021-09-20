import discord
from redbot.core import commands
from random import choice

BaseCog = getattr(commands, "Cog", object)

class Draft(BaseCog):
    """Draft random teams"""

    @commands.command()
    async def draft(self, ctx, *playerlist: discord.User):

        players = []
        for player in playerlist:
            players.append(player)

        if len(players) < 2:
            await ctx.send("You must specify at least 2 players. Example: `!draft @person1 @person2 @person3 ...`")
            
        else:

            teamA = []
            teamB = []

            while len(players) > 0:
                playerA = choice(players)
                teamA.append(playerA.mention)
                players.remove(playerA)

                if players == []:
                    break

                playerB = choice(players)
                teamB.append(playerB.mention)
                players.remove(playerB)

            em = discord.Embed(colour=ctx.author.colour, title="Teams")
            em.add_field(name="Team A", value=str("\n".join(teamA)), inline=True)
            em.add_field(name="Team B", value=str("\n".join(teamB)), inline=True)

            await ctx.send(embed=em)