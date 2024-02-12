import discord
from discord.ext import commands
import aiohttp

class IconCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setpfp(self, ctx, image_url):
            if not ctx.author.id in self.bot.owner_ids: return await ctx.send("nono")
            async with aiohttp.ClientSession() as session:
             async with session.get(image_url) as response:
                try:
                    image_data = await response.read()
                    await self.bot.user.edit(avatar=image_data)
                    await ctx.send("Bot profile picture updated successfully!")
                except Exception as e:
                    await ctx.send(f"An error occurred: {e}")

    @commands.group(aliases=["ge"], invoke_without_command=True)
    async def guildedit(self, ctx):
     return await ctx.create_pages()

    @guildedit.command(help="config", description="change the server vanity", usage="[name]")
    async def vanity(self, ctx, vanity_url: str):
        if ctx.author.guild_permissions.manage_guild:
            if ctx.guild.premium_subscription_count >= 14:  # Check for at least 14 boosts
                # Check if the vanity URL is available
                vanity_info = await ctx.guild.vanity_invite()
                if vanity_info is None or vanity_info.code == vanity_url:
                    try:
                        await ctx.guild.edit(vanity_code=vanity_url)
                        await ctx.send_success("Server vanity URL updated successfully.")
                    except discord.HTTPException as e:
                        await ctx.send(f"An error occurred: {e}")
                else:
                    await ctx.send_warning("The vanity URL is already taken.")
            else:
                await ctx.send_warning("You need at least 14 server boosts to change the vanity URL.")
        else:
            await ctx.send_warning("You don't have permission to change the server vanity URL.")


    @guildedit.command(help="config", description="change the server splash", usage="[link]")
    async def splash(self, ctx, url: str):
        if ctx.author.guild_permissions.manage_guild:
            if ctx.guild.premium_subscription_count >= 2:  # Check for at least 2 boosts
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as response:
                            if response.status == 200:
                                splash_data = await response.read()
                                await ctx.guild.edit(splash=splash_data)
                                await ctx.send_success("Server splash image updated successfully.")
                            else:
                                await ctx.send_warning("Failed to download the image. Please check the URL.")
                except Exception as e:
                    await ctx.send_warning(f"An error occurred: {e}")
            else:
                await ctx.send_warning("You need at least 2 server boosts to change the splash image.")
        else:
            await ctx.send_warning("You don't have permission to change the server splash image.")

    @guildedit.command(help="config", description="change the server description", usage="[description]")
    async def description(self, ctx, *, description: str):
        if ctx.author.guild_permissions.manage_guild:
            if "COMMUNITY" in ctx.guild.features:
                try:
                    await ctx.guild.edit(description=description)
                    await ctx.send_success("Server description updated successfully.")
                except Exception as e:
                    await ctx.send_warning(f"An error occurred: {e}")
            else:
                await ctx.send_warning("The server must have the `COMMUNITY` feature to change the description.")
        else:
            await ctx.send_warning("You don't have permission to change the server description.")

    @guildedit.command(help="config", description="change the server banner", usage="[link]")
    async def banner(self, ctx, url: str):
        if ctx.author.guild_permissions.manage_guild:
            if ctx.guild.premium_subscription_count >= 7:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as response:
                            if response.status == 200:
                                banner_data = await response.read()
                                await ctx.guild.edit(banner=banner_data)
                                await ctx.send_success("Server banner updated successfully.")
                            else:
                                await ctx.send_warning("Failed to download the image. Please check the URL.")
                except Exception as e:
                    await ctx.send_warning(f"An error occurred: {e}")
            else:
                await ctx.send_warning("You need at least 7 server boosts to change the server banner.")
        else:
            await ctx.send_warning("You don't have permission to change the server banner.")

    @guildedit.command(help="config", description="change the server icon", usage="[link]")
    async def icon(self, ctx, url: str):
        if ctx.author.guild_permissions.manage_guild:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            icon_data = await response.read()
                            await ctx.guild.edit(icon=icon_data)
                            await ctx.send_success("Server icon updated successfully.")
                        else:
                            await ctx.send_warning("Failed to download the image. Please check the URL.")
            except Exception as e:
                await ctx.send_warning(f"An error occurred: {e}")
        else:
            await ctx.send_warning("You don't have permission to change the server icon.")

async def setup(bot) -> None:
    await bot.add_cog(IconCog(bot))   
