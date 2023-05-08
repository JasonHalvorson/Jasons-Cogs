from .draft import Draft

async def setup(bot):
    await bot.add_cog(Draft())