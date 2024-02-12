import discord
from discord.ext import commands
import button_paginator as pg

class VapeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(help="fun", description="play with vape lol", aliases=["v"], invoke_without_command=True)
    async def vape(self, ctx):
        return await ctx.create_pages()

    @vape.command()
    async def list(self, ctx):
        hits_data = await self.bot.db.fetch('SELECT user_id, hit_count FROM vape')

        if hits_data:
            formatted_data = [f"<@{user_id}>: {hit_count} hits" for user_id, hit_count in hits_data]
            embeds = pg.embed_creator("\n".join(formatted_data), 1995)

            paginator = pg.Paginator(self.bot, embeds, ctx, invoker=ctx.author.id)
            paginator.add_button('prev', emoji='<:left:1100418278272290846>')
            paginator.add_button('next', emoji='<:right:1100418264028426270>')
            await paginator.start()
        else:
            embed = discord.Embed(color=self.bot.color, description="No vape hits recorded yet.")
            await ctx.send(embed=embed)




    @vape.command()
    async def buy(self, ctx):
        user_id = ctx.author.id
        has_vape = await self.bot.db.fetchval('SELECT has_vape FROM vape WHERE user_id=$1', user_id)

        if has_vape:
            embed = discord.Embed(color=self.bot.color, description="You already have a vape!")
            await ctx.send(embed=embed)
        else:
            await self.bot.db.execute('INSERT INTO vape (user_id, has_vape) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET has_vape=$2', user_id, True)
            embed = discord.Embed(color=self.bot.color, description="Congratulations! You bought a vape.")
            await ctx.send(embed=embed)

    @vape.command()
    async def hit(self, ctx):

        user_id = ctx.author.id
        has_vape = await self.bot.db.fetchval('SELECT has_vape FROM vape WHERE user_id=$1', user_id)

        if has_vape:
            await self.bot.db.execute('UPDATE vape SET hit_count = hit_count + 1 WHERE user_id = $1', user_id)
            hit_count = await self.bot.db.fetchval('SELECT hit_count FROM vape WHERE user_id = $1', user_id)
            embed = discord.Embed(color=self.bot.color, description=f"You hit the vape! Total hits: {hit_count}")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=self.bot.color, description="You need to buy a vape first. Use `*vape buy`.")
            await ctx.send(embed=embed)

    @vape.command()
    async def sell(self, ctx):

        user_id = ctx.author.id
        has_vape = await self.bot.db.fetchval('SELECT has_vape FROM vape WHERE user_id=$1', user_id)

        if has_vape:
            await self.bot.db.execute('DELETE FROM vape WHERE user_id = $1', user_id)
            embed = discord.Embed(color=self.bot.color, description="You sold your vape. It's time to quit!")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=self.bot.color, description="You don't have a vape to sell.")
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(VapeCog(bot))

