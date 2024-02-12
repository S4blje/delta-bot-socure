import discord
from discord.ext import commands
import button_paginator as pg

class deltaos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="roleplay", description="check the the newest news on delta twitter")
    async def phone(self, ctx):
        guild = ctx.guild 
        embeds = []
        embeds.append(discord.Embed(color=self.bot.color, description="").set_author(name="Welcome to DeltaOS 7", icon_url=self.bot.user.display_avatar.with_format('png')).add_field(name=f"", value=">>> **<:deltahome:1203405139839549552> Home Page**\n**<:deltatwitter:1203405143400259624> Twitter**\n**<:Page:1203415628665323584> Location**", inline=False))
        embeds.append(discord.Embed(color=self.bot.color, description=">>> **New tweet from @marian**\n \n**Welcome to DeltaOS 7!**").add_field(name=f"Updated Tweet", value=">>> **This is the next update i hope you like idea by @encq**", inline=False).set_author(
            name="", icon_url=self.bot.user.display_avatar.with_format('png')).set_footer(icon_url="https://cdn.discordapp.com/attachments/1201252642865827922/1203407309573726229/deltatwitter.png?ex=65d0fb64&is=65be8664&hm=105a7f259308aff96a662298cf960115f82c7b8ec7cc01bebcfdb9229ac7347a&", text=f"Twitter Notification (+1)"))
        embeds.append(discord.Embed(color=self.bot.color, description=f">>> **You are now in {guild.name}**\n \n**Around {guild.member_count} people**").set_author(
            name="delta", icon_url=self.bot.user.display_avatar.with_format('png')).set_footer(icon_url="https://cdn.discordapp.com/attachments/1201461002848448522/1203416237141663875/Page.png?ex=65d103b5&is=65be8eb5&hm=58e44b039dece05dc35c0ebc4e59880a9de6bdf4a400ce238f11d2c1e3221841&", text=f"Location Share"))
        paginator = pg.Paginator(self.bot, embeds, ctx, invoker=ctx.author.id)
        paginator.add_button('prev', emoji='<:left:1100418278272290846>')
        paginator.add_button('next', emoji='<:right:1100418264028426270>')
        await paginator.start()

async def setup(bot):
    await bot.add_cog(deltaos(bot))
