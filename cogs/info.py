import discord, random, psutil
from discord.ext import commands
from discord.ui import View, Button
import button_paginator as pg

class info(commands.Cog):
   def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot        
 
   @commands.command(help="info", description="see the shards info")
   async def shards(self, ctx):
        embed = discord.Embed(title="Shard Information", color=self.bot.color)

        for shard_id in range(self.bot.shard_count):
            server_count = sum(1 for guild in self.bot.guilds if guild.shard_id == shard_id)
            embed.add_field(name=f"Shard {shard_id}", value=f"Server Count: {server_count}", inline=False)

        await ctx.send(embed=embed)


   @commands.command(help="info", description="check the bot info", aliases=["bi"])
   async def botinfo(self, ctx):
    avatar_url = self.bot.user.avatar.url
    embed = discord.Embed(color=self.bot.color,title="delta",description=f"Start create your server with **delta**\n. Analyze `{len(self.bot.guilds)}` **servers** and `{sum(g.member_count for g in self.bot.guilds):,}` **users**").set_thumbnail(url=f'{avatar_url}')
    embed.add_field(name="System", value=f"`{discord.__version__}` **discord.py**\n`{psutil.virtual_memory()[2]}%` **memory**", inline=False).add_field(name="Client", value=f"`{self.bot.ping}` **ms**\n`{len(self.bot.cogs)}` **cogs**", inline=False)
    await ctx.reply(embed=embed)
    

    
   @commands.hybrid_command(description="check bot connection", help="info")
   async def ping(self, ctx):
    embed=discord.Embed(color=self.bot.color, description=f"🛰 `{self.bot.ping}`ms")
    await ctx.reply(embed=embed)

   @commands.hybrid_command(description="invite the bot", help="info", aliases=["support", "inv"])
   async def invite(self, ctx):
    avatar_url = self.bot.user.avatar.url
    embed = discord.Embed(color=self.bot.color, description="Add the bot in your server!")
    embed.set_author(name=self.bot.user.name, icon_url=f"{avatar_url}")
    button1 = Button(label="invite", url=f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot%20applications.commands")
    button2 = Button(label="support", url="https://discord.gg/NMj58fsjEa")
    view = View()
    view.add_item(button1)
    view.add_item(button2)
    await ctx.reply(embed=embed, view=view)

async def setup(bot) -> None:
    await bot.add_cog(info(bot))      
