import discord
from redbot.core import commands
import re
import asyncio
import aiohttp

BaseCog = getattr(commands, "Cog", object)

class MDPWReset(BaseCog):
    """Initiate a Password Reset on MangaDex.org"""

    @commands.command()
    async def mdpwreset(self, ctx, email):
        """Initiates a Password Reset for <email>."""

        # Check that command is run in DMs
        if isinstance(ctx.channel, discord.channel.DMChannel):

            # Regex to validate email (hopefully (i borrowed it off stackoverflow))
            regex = r"^[^@\s]+@[^@\s\.]+\.[^@\.\s]+$"

            # Check that the email is valid
            if (re.search(regex, email)):

                # Make the request to MangaDex's API
                async with aiohttp.ClientSession() as session:
                    async with session.post("https://api.mangadex.org/account/recover", json={"email": email}) as resp:

                        # If it works, MangaDex will respond with 200
                        if resp.status == 200:
                            await ctx.send("Your email has been sent!")

                        # If it responds with 429, it means I'm rate limited (can only do this 5 times per hour)
                        elif resp.status == 429:
                            await ctx.send(f"**Error from MangaDex:** Server responded with **{resp.status}**. \nThis means I am currently rate-limited. MangaDex only allows the `/account/recover` endpoint to be used 5 times an hour. \nPlease try again later!")

                        # If it doesn't work idk what to tell you lol
                        else:
                            await ctx.send(f"Error from MangaDex: Server responded with {resp.status}.")

            else:
                await ctx.send(f"Error: '{email}' is not a valid email.")
            
        else:
            await ctx.send("To keep your information private, this command must be run in DMs.")