import discord
from redbot.core import commands
from redbot.core.data_manager import bundled_data_path
from PIL import Image, ImageOps
from io import BytesIO

BaseCog = getattr(commands, "Cog", object)

class Without(BaseCog):
    """Turn someone's avatar into a Chainsaw Man meme"""

    @commands.command()
    async def without(self, ctx, user: discord.User=None):

        async with ctx.typing():

            if not user:
                user = (await ctx.channel.history(limit=2).flatten())[1].author

            result = await self.create_meme(user)

            result.seek(0)

        await ctx.send(file=discord.File(result))

    async def get_avatar(self, user):
        try:
            res = BytesIO()
            await user.avatar_url_as(format="png", size=1024).save(res, seek_begin=True)
            return res
        except:
            async with self._session.get(user.avatar_url_as(format="png", size=1024)) as r:
                img = await r.content.read()
                return BytesIO(img)

    async def create_meme(self, user):
        meme_image = Image.open(str(bundled_data_path(self)) + '/without.png')

        avatar = await self.get_avatar(user)
        avatar_image = Image.open(avatar)
        resized_avatar = avatar_image.resize([175, 175])
        mask = Image.open(str(bundled_data_path(self)) + '/mask.png').resize(resized_avatar.size).convert('L')

        meme_image.paste(resized_avatar, (334, 734), mask)

        temp = BytesIO()
        meme_image.save(temp, format="PNG")
        temp.name = "profile.png"
        return temp