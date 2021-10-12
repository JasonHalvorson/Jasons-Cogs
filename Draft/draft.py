import discord
from redbot.core import commands, Config
from random import choice
import asyncio
import aiohttp

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
                await self.config.user(ctx.author).draft_champs.set(False)
            else:
                await self.config.guild(ctx.guild).last_draft.set(players)
                await self.config.guild(ctx.guild).draft_champs.set(False)

            team_a, team_b = await self.create_teams(players)

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
            draft_champs = await self.config.user(ctx.author).draft_champs()
        else:
            last_draft = await self.config.guild(ctx.guild).last_draft()
            draft_champs = await self.config.guild(ctx.guild).draft_champs()

        if not last_draft:
            await ctx.send(f"Previous draft not found. Please use `{ctx.clean_prefix}draft` instead.")

        else:
            team_a, team_b = await self.create_teams(last_draft, draft_champs)

            em = await self.create_embed(ctx, team_a, team_b)

            await ctx.send(embed=em)

    @commands.command(aliases=["rd"])
    async def randdraft(self, ctx, *playerlist):

        players = list(playerlist)

        if len(players) < 2:
            await ctx.send(f"You must specify at least 2 players. Example: `{ctx.clean_prefix}draft @person1 @person2 @person3 ...`")
        else:

            if isinstance(ctx.channel, discord.channel.DMChannel):
                await self.config.user(ctx.author).last_draft.set(players)
                await self.config.user(ctx.author).draft_champs.set(True)
            else:
                await self.config.guild(ctx.guild).last_draft.set(players)
                await self.config.guild(ctx.guild).draft_champs.set(True)

            async with ctx.typing():

                team_a, team_b = await self.create_teams(players, True)
            
                em = await self.create_embed(ctx, team_a, team_b)

            await ctx.send(embed=em)
        
    async def create_teams(self, players, draft_champs=False):
        team_a = []
        team_b = []

        if (draft_champs):
            async with aiohttp.ClientSession() as session:
                async with session.get("https://ddragon.leagueoflegends.com/api/versions.json") as resp:

                    latest = (await resp.json())[0]
                    async with session.get(f"https://ddragon.leagueoflegends.com/cdn/{latest}/data/en_US/champion.json") as resp:

                        corrected_champs = {
                            "AurelionSol": "Aurelion Sol",
                            "Chogath": "Cho'Gath",
                            "DrMundo": "Dr. Mundo",
                            "JarvanIV": "Jarvan IV",
                            "Khazix": "Kha'Zix",
                            "KogMaw": "Kog'Maw",
                            "Leblanc": "LeBlanc",
                            "LeeSin": "Lee Sin",
                            "MasterYi": "Master Yi",
                            "MissFortune": "Miss Fortune",
                            "MonkeyKing": "Wukong",
                            "Nunu": "Nunu & Willump",
                            "RekSai": "Rek'Sai",
                            "TahmKench": "Tahm Kench",
                            "TwistedFate": "Twisted Fate",
                            "Velkoz": "Vel'Koz",
                            "XinZhao": "Xin Zhao"
                        }

                        champs = list((await resp.json())["data"].keys())

                        champs = [corrected_champs.get(champ, champ) for champ in champs]

                        while len(players) > 0:
                            player_a = choice(players)
                            champ_a = choice(champs)

                            team_a.append(f"**{player_a}** - {champ_a}")
                            
                            players.remove(player_a)
                            champs.remove(champ_a)

                            if players == []:
                                break
                                
                            player_b = choice(players)
                            champ_b = choice(champs)
                            
                            team_b.append(f"**{player_b}** - {champ_b}")

                            players.remove(player_b)
                            champs.remove(champ_b)

        else:
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