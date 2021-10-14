import discord
from redbot.core import commands

BaseCog = getattr(commands, "Cog", object)

class Avatar(BaseCog):
    """Get a user's Avatar"""

    @commands.command()
    async def avatar(self, ctx, *, user: discord.Member=None):
        """Get a user's Avatar, defaults to yourself if user isn't given"""

        author = ctx.author

        if not user:
            user = author

        if user.is_avatar_animated():
            url = user.avatar_url_as(format="gif")

        if not user.is_avatar_animated():
            url = user.avatar_url_as(static_format="png")

        em = discord.Embed(colour=user.colour)
        em.set_author(name=str(user) + "'s Avatar", url=url)
        em.set_image(url=url)

        await ctx.send(embed=em)
