from .bigmoji import Bigmoji

async def setup(bot):
    await bot.add_cog(Bigmoji())