import discord
from redbot.core import commands

BaseCog = getattr(commands, "Cog", object)

class Bigmoji(BaseCog):
    """Send a bigger emoji."""

    @commands.command()
    async def bigmoji(self, ctx, emoji: discord.Emoji):
        """Send a big emoji."""

        em = discord.Embed(colour=ctx.author.colour if not isinstance(ctx.channel, discord.channel.DMChannel) else await ctx.embed_colour())
        em.set_image(url=emoji.url)

        await ctx.send(embed=em)
