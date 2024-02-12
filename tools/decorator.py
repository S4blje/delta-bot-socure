import discord, datetime, humanize
from discord.ext import commands

async def send_pages(ctx, embeds):
    current_page = 0
    message = await ctx.send(embed=embeds[current_page])

    reactions = ['⬅️', '➡️']

    for reaction in reactions:
        await message.add_reaction(reaction)

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in reactions

    while True:
        try:
            reaction, _ = await ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            break

        if str(reaction.emoji) == '⬅️':
            current_page = max(0, current_page - 1)
        elif str(reaction.emoji) == '➡️':
            current_page = min(len(embeds) - 1, current_page + 1)

        await message.edit(embed=embeds[current_page])
        await message.remove_reaction(reaction.emoji, ctx.author)



def is_reskin():
 async def predicate(ctx: commands.Context): 
  check = await ctx.bot.db.fetchrow("SELECT * FROM reskin_toggle WHERE guild_id = $1", ctx.guild.id)
  if not check: await ctx.warn("Reskin is **not** enabled")
  return check is not None 
 return commands.check(predicate)