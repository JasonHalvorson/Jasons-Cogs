import discord
from redbot.core import commands, Config
from random import choice

BaseCog = getattr(commands, "Cog", object)

class Draft(BaseCog):
    """Draft random teams"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=921840132, force_registration=True)

    @commands.command()
    async def draft(self, ctx, *playerlist):

        players = list(playerlist)

        if len(players) < 2:
            await ctx.send(f"You must specify at least 2 players. Example: `{ctx.clean_prefix}draft @person1 @person2 @person3 ...`")

        else:
            if isinstance(ctx.channel, discord.channel.DMChannel):
                await self.config.user(ctx.author).last_draft.set(players)
            else:

                await self.config.guild(ctx.guild).last_draft.set(players)

            team_a, team_b = await self.randomize_teams(players)

            em = await self.create_embed(ctx, team_a, team_b)
            em.set_footer(text=f"Use {ctx.clean_prefix}redraft to draft again with the same players!")

            await ctx.send(embed=em)

    # @commands.command()
    # async def clear(self, ctx):
    #     await self.config.clear_all()
    #     await ctx.send("Cleared config")

    @commands.command()
    async def redraft(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            last_draft = await self.config.user(ctx.author).last_draft()
        else:
            last_draft = await self.config.guild(ctx.guild).last_draft()

        if not last_draft:
            
            await ctx.send(f"Previous draft not found. Please use `{ctx.clean_prefix}draft` instead.")

        else:
            team_a, team_b = await self.randomize_teams(last_draft)

            em = await self.create_embed(ctx, team_a, team_b)

            await ctx.send(embed=em)

    async def randomize_teams(self, players):
        team_a = []
        team_b = []

        while len(players) > 0:
            player_a = choice(players)
            team_a.append(player_a)
            players.remove(player_a)

            if players == []:
                break

            player_b = choice(players)
            team_b.append(player_b)
            players.remove(player_b)

        return (team_a, team_b)

    async def create_embed(self, ctx, team_a, team_b):
        em = discord.Embed(colour=ctx.author.colour if not isinstance(ctx.channel, discord.channel.DMChannel) else await ctx.embed_colour(), title="Teams")
        em.add_field(name="Team A", value=str("\n".join(team_a)), inline=True)
        em.add_field(name="Team B", value=str("\n".join(team_b)), inline=True)

        return em