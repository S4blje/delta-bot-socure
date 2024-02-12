import sys, os, discord
from discord.ext import commands
from typing import Union

class EmbedBuilder:

  def ordinal(num: str) -> str:
   """Convert from number to ordinal (10 - 10th)""" 
   num = str(num) 
   if num in ["11", "12", "13"]:
       return num + "th"
   if num.endswith("1"):
      return num + "st"
   elif num.endswith("2"):
      return num + "nd"
   elif num.endswith("3"): 
       return num + "rd"
   else: return num + "th" 
  
  async def send_callback(interaction: discord.Interaction, ctx: commands.Context, modal: discord.ui.Modal) -> None: 
    if interaction.user.id != ctx.author.id: return await interaction.client.ext.send_warning(interaction, "You are not the author of this embed", ephemeral=True)          
    await interaction.response.send_modal(modal)
  
  async def send_personal_embed(bot: commands.Bot, destination: discord.TextChannel, member: discord.Member, embed: str, lastfm: bool=False) -> discord.Message or None: 
   check = await bot.db.fetchrow("SELECT * FROM embeds WHERE object_id = $1 AND embedname = $2 AND mode = $3", member.id, embed, "personal")  
   if not check: return None 
   text = check["emb"]
   con = check["content"]
   if lastfm is True: 
     re = await bot.db.fetchrow("SELECT * FROM lastfm WHERE user_id = $1", member.id)
     if not re: pass
     user = re["username"]
     lastfmhandler = Handler("43693facbb24d1ac893a7d33846b15cc")
     a = await lastfmhandler.get_tracks_recent(user, 1) 
     userinfo = await lastfmhandler.get_user_info(user)
     userpfp = userinfo["user"]["image"][2]["#text"]
     artist = a['recenttracks']['track'][0]['artist']['#text']
     albumplays = await lastfmhandler.get_album_playcount(user, a['recenttracks']['track'][0]) or "N/A"
     artistplays = await lastfmhandler.get_artist_playcount(user, artist) 
     trackplays = await lastfmhandler.get_track_playcount(user, a['recenttracks']['track'][0]) or "N/A"
     album = a["recenttracks"]['track'][0]['album']['#text'].replace(" ", "+") or "N/A"     
     if con: con = con.replace('{track}', a['recenttracks']['track'][0]['name']).replace('{trackurl}', a['recenttracks']['track'][0]['url']).replace('{artist}', a['recenttracks']['track'][0]['artist']['#text']).replace('{artisturl}', f"https://last.fm/music/{artist.replace(' ', '+')}").replace('{trackimage}', str((a['recenttracks']['track'][0])['image'][3]['#text']).replace('{https', "https")).replace('{artistplays}', str(artistplays)).replace('{albumplays}', str(albumplays)).replace('{trackplays}', str(trackplays)).replace('{album}', a['recenttracks']['track'][0]['album']['#text'] or "N/A").replace('{albumurl}', f"https://www.last.fm/music/{artist.replace(' ', '+')}/{album.replace(' ', '+')}" or "https://none.none").replace('{username}', user).replace('{scrobbles}', a['recenttracks']['@attr']['total']).replace('{useravatar}', userpfp) 
     if text: text = text.replace('{track}', a['recenttracks']['track'][0]['name']).replace('{trackurl}', a['recenttracks']['track'][0]['url']).replace('{artist}', a['recenttracks']['track'][0]['artist']['#text']).replace('{artisturl}', f"https://last.fm/music/{artist.replace(' ', '+')}").replace('{trackimage}', str((a['recenttracks']['track'][0])['image'][3]['#text']).replace('{https', "https")).replace('{artistplays}', str(artistplays)).replace('{albumplays}', str(albumplays)).replace('{trackplays}', str(trackplays)).replace('{album}', a['recenttracks']['track'][0]['album']['#text'] or "N/A").replace('{albumurl}', f"https://www.last.fm/music/{artist.replace(' ', '+')}/{album.replace(' ', '+')}" or "https://none.none").replace('{username}', user).replace('{scrobbles}', a['recenttracks']['@attr']['total']).replace('{useravatar}', userpfp)  
   x = EmbedBuilder.str_to_dict(member, text, con)
   return await destination.send(content=x[1], embed=x[0])

  async def send_embed(bot: commands.Bot, destination: discord.TextChannel, member: discord.Member, embed: str, view: discord.ui.View=None) -> bool:
    check = await bot.db.fetchrow("SELECT * FROM embeds WHERE object_id = $1 AND embedname = $2 AND mode = $3", member.guild.id, embed, "server")
    if not check: return False 
    text = check['emb']
    con = check['content']          
    x = EmbedBuilder.str_to_dict(member, text, con)
    await destination.send(content=x[1], embed=x[0], view=view)
    return True

  def str_to_dict(user: discord.Member, emb: str=None, content: str=None) -> tuple: 
   embed_text = EmbedBuilder.embed_replacement(user, emb)  
   content_text = EmbedBuilder.embed_replacement(user, content)     
   embed = discord.Embed.from_dict(ast.literal_eval(embed_text)) or None
   return (embed, content_text)

  def replace_images(user: discord.Member, params: str=None): 
    if params is None: return None 
    if "https://imgs.search.brave.com/fUEzoOqyU93IlIkwKFZqWm9Mzx8tZZC1OxuqwefxwTA/rs:fit:735:728:1/g:ce/aHR0cHM6Ly9pLnBp/bmltZy5jb20vNzM2/eC9jMC9jMi8xNi9j/MGMyMTZiMzc0M2M2/Y2I5ZmQ2N2FiN2Rm/NmIyYzMzMC5qcGc" in params: params=params.replace("https://imgs.search.brave.com/fUEzoOqyU93IlIkwKFZqWm9Mzx8tZZC1OxuqwefxwTA/rs:fit:735:728:1/g:ce/aHR0cHM6Ly9pLnBp/bmltZy5jb20vNzM2/eC9jMC9jMi8xNi9j/MGMyMTZiMzc0M2M2/Y2I5ZmQ2N2FiN2Rm/NmIyYzMzMC5qcGc", "{useravatar}")
    if "https://imgs.search.brave.com/IT1jjIm_87vsIET7-l_DMYokRMbZrUJLI7sHk-yrSHQ/rs:fit:900:900:1/g:ce/aHR0cHM6Ly95dDMu/Z2dwaHQuY29tL2Ev/QUFUWEFKeURpZm1Y/ZS1QU1NFUS1NRkpO/VVdMaVRVajJLbnBV/bEJ5dGRBPXM5MDAt/Yy1rLWMweGZmZmZm/ZmZmLW5vLXJqLW1v" in params: params=params.replace('https://imgs.search.brave.com/IT1jjIm_87vsIET7-l_DMYokRMbZrUJLI7sHk-yrSHQ/rs:fit:900:900:1/g:ce/aHR0cHM6Ly95dDMu/Z2dwaHQuY29tL2Ev/QUFUWEFKeURpZm1Y/ZS1QU1NFUS1NRkpO/VVdMaVRVajJLbnBV/bEJ5dGRBPXM5MDAt/Yy1rLWMweGZmZmZm/ZmZmLW5vLXJqLW1v', '{trackimage}')
    if user.display_avatar.url in params: params=params.replace(user.display_avatar.url, "{user.avatar}")
    if user.guild.icon.url in params: params=params.replace(user.guild.icon.url, "{guild.icon}")
    return params
  
  def embed_replacement(user: discord.Member, params: str=None):
    if params is None: return None
    if '{user}' in params:
        params=params.replace('{user}', str(user.name) + "#" + str(user.discriminator))
    if '{user.mention}' in params:
        params=params.replace('{user.mention}', user.mention)
    if '{user.name}' in params:
        params=params.replace('{user.name}', user.name)
    if '{user.avatar}' in params:
        params=params.replace('{user.avatar}', str(user.display_avatar.url))
    if '{user.joined_at}' in params:
        params=params.replace('{user.joined_at}', discord.utils.format_dt(user.joined_at, style='R'))
    if '{user.created_at}' in params:
        params=params.replace('{user.created_at}', discord.utils.format_dt(user.created_at, style='R'))
    if '{user.discriminator}' in params:
        params=params.replace('{user.discriminator}', user.discriminator)
    if '{guild.name}' in params:
        params=params.replace('{guild.name}', user.guild.name)
    if '{guild.count}' in params:
        params=params.replace('{guild.count}', str(user.guild.member_count))
    if '{guild.count.format}' in params:
        params=params.replace('{guild.count.format}', EmbedBuilder.ordinal(len(user.guild.members)))
    if '{guild.id}' in params:
        params=params.replace('{guild.id}', user.guild.id)
    if '{guild.created_at}' in params:
        params=params.replace('{guild.created_at}', discord.utils.format_dt(user.guild.created_at, style='R'))
    if '{guild.boost_count}' in params:
        params=params.replace('{guild.boost_count}', str(user.guild.premium_subscription_count))
    if '{guild.booster_count}' in params:
        params=params.replace('{guild.booster_count}', str(len(user.guild.premium_subscribers)))
    if '{guild.boost_count.format}' in params:
        params=params.replace('{guild.boost_count.format}', EmbedBuilder.ordinal(user.guild.premium_subscription_count))
    if '{guild.booster_count.format}' in params:
        params=params.replace('{guild.booster_count.format}', EmbedBuilder.ordinal(len(user.guild.premium_subscribers)))
    if '{guild.boost_tier}' in params:
        params=params.replace('{guild.boost_tier}', str(user.guild.premium_tier))
    if '{guild.vanity}' in params: 
        params=params.replace('{guild.vanity}', "/" + user.guild.vanity_url_code or "none")     
    if '{useravatar}' in params: 
        params=params.replace('{useravatar}', "https://imgs.search.brave.com/fUEzoOqyU93IlIkwKFZqWm9Mzx8tZZC1OxuqwefxwTA/rs:fit:735:728:1/g:ce/aHR0cHM6Ly9pLnBp/bmltZy5jb20vNzM2/eC9jMC9jMi8xNi9j/MGMyMTZiMzc0M2M2/Y2I5ZmQ2N2FiN2Rm/NmIyYzMzMC5qcGc")    
    if '{trackimage}' in params: 
        params=params.replace('{trackimage}', "https://imgs.search.brave.com/IT1jjIm_87vsIET7-l_DMYokRMbZrUJLI7sHk-yrSHQ/rs:fit:900:900:1/g:ce/aHR0cHM6Ly95dDMu/Z2dwaHQuY29tL2Ev/QUFUWEFKeURpZm1Y/ZS1QU1NFUS1NRkpO/VVdMaVRVajJLbnBV/bEJ5dGRBPXM5MDAt/Yy1rLWMweGZmZmZm/ZmZmLW5vLXJqLW1v")    
    if '{invisible}' in params: 
        params=params.replace('{invisible}', '2f3136') 
    if '{botcolor}' in params: 
        params=params.replace('{botcolor}', '6d827d')       
    if '{guild.icon}' in params:
      if user.guild.icon:
        params=params.replace('{guild.icon}', user.guild.icon.url)
      else: 
        params=params.replace('{guild.icon}', "https://none.none")        

    return params
  
  class EmbedFieldModal(discord.ui.Modal, title="add a field to your embed"): 
    name = discord.ui.TextInput(label="field name", placeholder="the name of your field", required=True, style=discord.TextStyle.short)
    val = discord.ui.TextInput(label="value", placeholder="the value of your field", required=True, style=discord.TextStyle.paragraph)
    inline = discord.ui.TextInput(label="inline", placeholder="This is true by default", required=False, max_length=5)

    async def on_submit(self, interaction: discord.Interaction) -> None: 
      embed = self.message.embeds[0]
      if self.inline.value == '': field_inline = True  
      else: field_inline = bool(self.inline.value.lower() == "true") 
      embed.add_field(name=self.name.value, value=self.val.value, inline=field_inline)
      await self.message.edit(embed=embed)
      await interaction.client.ext.send_success(interaction, "Added a field", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception): 
      await interaction.client.ext.send_warning(interaction, f"Something went wrong while trying to edit the add fields - {error}", ephemeral=True)   

  class EmbedFooterModal(discord.ui.Modal, title="edit the embed footer"): 
    text = discord.ui.TextInput(label="footer text", placeholder="the footer text", required=False, style=discord.TextStyle.short)
    icon = discord.ui.TextInput(label="footer icon", placeholder="this should be an image ur or a variable", required=False, style=discord.TextStyle.short)
    
    async def on_submit(self, interaction: discord.Interaction) -> None:
      embed = interaction.message.embeds[0]
      
      footer_text = None 
      footer_icon = None 
      if self.text.value == "none": footer_text = None 
      elif self.text.value == "": footer_text = embed.footer.text 
      else: footer_text = self.text.value 

      if self.icon.value == "none": footer_icon = None 
      elif self.icon.value == "": footer_icon = embed.footer.icon_url
      else: footer_icon = self.icon.value 
      
      embed.set_footer(text=footer_text, icon_url=EmbedBuilder.embed_replacement(interaction.user, footer_icon))
      await interaction.response.edit_message(embed=embed)
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
      print(error) 
      await interaction.client.ext.send_warning(interaction, f"The links or variables passed are not available", ephemeral=True) 

  class EmbedAuthorModal(discord.ui.Modal, title="edit the embed author"): 
    name = discord.ui.TextInput(label="author name", placeholder="the author name", required=False, style=discord.TextStyle.short)
    icon = discord.ui.TextInput(label="author icon", placeholder="this should be an image ur or a variable", required=False, style=discord.TextStyle.short)
    
    async def on_submit(self, interaction: discord.Interaction) -> None:
      embed = interaction.message.embeds[0]
      
      author_name = None 
      author_icon = None
      if self.name.value == "none": author_name = None 
      elif self.name.value == "": author_name = embed.author.name 
      else: author_name = self.name.value 

      if self.icon.value == "none": author_icon = None 
      elif self.icon.value == "": author_icon = embed.author.icon_url
      else: author_icon = self.icon.value 
      embed.set_author(name=author_name, icon_url=EmbedBuilder.embed_replacement(interaction.user, author_icon))
      await interaction.response.edit_message(embed=embed)
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
      print(error) 
      await interaction.client.ext.send_warning(interaction, f"The links or variables passed are not available", ephemeral=True) 

  class EmbedImagesModal(discord.ui.Modal, title="edit the embed images"):
   thumbnail = discord.ui.TextInput(label="thumbnail", placeholder="this should be an image url or a variable", required=False, style=discord.TextStyle.short)
   image = discord.ui.TextInput(label="image", placeholder="this should be an image url or a variable", required=False, style=discord.TextStyle.short)

   async def on_submit(self, interaction: discord.Interaction) -> None:
    embed = interaction.message.embeds[0]

    if self.thumbnail.value == "none": embed.set_thumbnail(url=None) 
    elif self.thumbnail.value == "": embed.set_thumbnail(url=embed.thumbnail.url) 
    else: embed.set_thumbnail(url=EmbedBuilder.embed_replacement(interaction.user, self.thumbnail.value)) 

    if self.image.value == "none": embed.set_image(url=None)  
    elif self.image.value == "": embed.set_image(url=embed.image.url)  
    else: embed.set_image(url=EmbedBuilder.embed_replacement(interaction.user, self.image.value)) 

    await interaction.response.edit_message(embed=embed)

   async def on_error(self, interaction: discord.Interaction, error: Exception):
      print(error) 
      await interaction.client.ext.send_warning(interaction, f"The links or variables passed are not available", ephemeral=True) 

  class EmbedBasicsModal(discord.ui.Modal, title="edit the basic embed parts"): 
    content = discord.ui.TextInput(label="content", placeholder="the content of the embed", required=False, style=discord.TextStyle.paragraph)
    tit = discord.ui.TextInput(label="title", placeholder="the title of the embed", required=False, max_length=100)
    description = discord.ui.TextInput(label="description", placeholder="the description of the embed", required=False, style=discord.TextStyle.long)
    color = discord.ui.TextInput(label="color", placeholder="the color of the embed", required=False, max_length=11)

    async def on_submit(self, interaction: discord.Interaction): 
      embed = interaction.message.embeds[0]

      if self.content.value == "": content = interaction.message.content 
      elif self.content.value.lower() == "none": content = None 
      else: content = self.content.value 

      if self.tit.value == "none": embed.title=None 
      else: embed.title = self.tit.value if self.tit.value != "" else embed.title

      embed.description = self.description.value or embed.description 

      try: embed.color = int(EmbedBuilder.embed_replacement(interaction.user, self.color.value.replace("#", "")), 16) 
      except: pass

      await interaction.response.edit_message(content=content, embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception): 
      await interaction.client.ext.send_warning(interaction, f"Something went wrong while trying to edit the **basic info** - {error}", ephemeral=True)   

  class EmbedButtons(discord.ui.View): 
   def __init__(self, ctx: commands.Context, embedname: str): 
    super().__init__(timeout=None)
    self.ctx = ctx
    self.embedname = embedname

   @discord.ui.button(label="basics", custom_id="basics:button")  
   async def basics_button(self, interaction: discord.Interaction, button: discord.ui.Button): 
    await EmbedBuilder.send_callback(interaction, self.ctx, EmbedBuilder.EmbedBasicsModal())
   
   @discord.ui.button(label="images", custom_id="images:button")
   async def images_button(self, interaction: discord.Interaction, button: discord.ui.Button): 
    await EmbedBuilder.send_callback(interaction, self.ctx, EmbedBuilder.EmbedImagesModal())
   
   @discord.ui.button(label="author", custom_id="author:button")
   async def author_button(self, interaction: discord.Interaction, button: discord.ui.Button): 
    await EmbedBuilder.send_callback(interaction, self.ctx, EmbedBuilder.EmbedAuthorModal())
   
   @discord.ui.button(label="footer", custom_id="footer:button")
   async def footer_button(self, interaction: discord.Interaction, button: discord.ui.Button): 
    await EmbedBuilder.send_callback(interaction, self.ctx, EmbedBuilder.EmbedFooterModal())

   @discord.ui.button(label="fields", custom_id="field:button", row=1)
   async def field_button(self, interaction: discord.Interaction, button: discord.ui.Button): 
    if interaction.user.id != self.ctx.author.id: return await interaction.client.ext.send_warning(interaction, "You are not the author of this embed")          
    v = discord.ui.View()
    add = discord.ui.Button(label="add", style=discord.ButtonStyle.green)
    remove = discord.ui.Button(label="remove", disabled=bool(len(interaction.message.embeds[0].fields) == 0), style=discord.ButtonStyle.red)
    
    async def add_callback(inter: discord.Interaction): 
      modal = EmbedBuilder.EmbedFieldModal()
      modal.message = interaction.message
      await inter.response.send_modal(modal)

    add.callback = add_callback 

    async def remove_callback(inter: discord.Interaction):
     embed = interaction.message.embeds[0] 
     if len(embed.fields) == 0: return await inter.client.ext.send_warning(interaction, "This embed has no fields")
     e = discord.Embed(color=interaction.client.color, description=f"🔍 Which field do you want to remove?")
     select = discord.ui.Select(options=[discord.SelectOption(label=f"field {embed.fields.index(field)+1} | {field.name}", value=str(embed.fields.index(field))) for field in embed.fields]) 
    
     async def select_callback(intere: discord.Interaction): 
      embed.remove_field(int(select.values[0]))
      await interaction.message.edit(embed=embed)
      await intere.response.edit_message(view=None, embed=discord.Embed(color=intere.client.color, description="{} {}: Deleted field {}".format(interaction.client.yes, interaction.user.mention, str(int(int(select.values[0])+1))))) 
     select.callback = select_callback 
     view = discord.ui.View()
     view.add_item(select)
     await inter.response.send_message(embed=e, view=view, ephemeral=True) 
    
    remove.callback = remove_callback

    v.add_item(add)
    v.add_item(remove)
    await interaction.response.send_message(content="", view=v, ephemeral=True) 

   @discord.ui.button(label="preview", custom_id="preview:button", row=1)
   async def preview_button(self, interaction: discord.Interaction, button: discord.ui.Button): 
    text = str(interaction.message.embeds[0].to_dict())
    x = EmbedBuilder.str_to_dict(interaction.user, text, interaction.message.content)
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="embed preview", disabled=True))
    view.add_item(discord.ui.Button(label="need help?", url="https://discord.gg/pretend"))
    await interaction.response.send_message(content=x[1], embed=x[0], view=view, ephemeral=True)

   @discord.ui.button(label="save", custom_id="save:button", row=1)
   async def save_button(self, interaction: discord.Interaction, button: discord.ui.Button): 
    if interaction.user.id != self.ctx.author.id: return await interaction.client.ext.send_warning(interaction, "You are not the author of this embed")          
    text = EmbedBuilder.replace_images(interaction.user, str(interaction.message.embeds[0].to_dict()))
    embed = discord.Embed(color=interaction.client.color, description=f"🔍 Save `{self.embedname}` as")
    button1 = discord.ui.Button(label="personal")
    button2 = discord.ui.Button(label="server", disabled=bool(not await Perms.has_perms(self.ctx, "manage_guild")))
    async def save_func(label, inter: discord.Interaction): 
      check = await interaction.client.db.fetchrow("SELECT embedname FROM embeds WHERE embedname = $1 AND object_id = $2 AND mode = $3", self.embedname, interaction.guild.id if label == "server" else interaction.user.id, label)
      if check: 
       embs = await interaction.client.db.fetch("SELECT * FROM embeds WHERE object_id = $1 AND mode = $2", interaction.guild.id if label == "server" else interaction.user.id, label)
       if len(embs) >= 10: 
        if label == "server": 
          don = await interaction.client.db.fetchrow("SELECT * FROM auth WHERE guild_id = $1 AND tags = $2", interaction.guild.id, "true")
          if not don: return await self.bot.ext.send_warning(interaction, "You **cannot** create more than **10** embeds in a non premium guild")    
        elif label == "personal": 
          don = await interaction.client.db.fetchrow("SELECT * FROM donor WHERE user_id = $1", interaction.user.id)
          if not don: return await self.bot.ext.send_warning(interaction, "You **cannot** create more than **10** embeds if you are not a donator")       
       await interaction.client.db.execute("UPDATE embeds SET emb = $1 WHERE object_id = $2 AND embedname = $3 AND mode = $4", text, interaction.guild.id if label == "server" else interaction.user.id, self.embedname, label)
       await interaction.client.db.execute("UPDATE embeds SET content = $1 WHERE object_id = $2 AND embedname = $3 AND mode = $4", interaction.message.content if interaction.message.content != "" else None, interaction.guild.id if label == "server" else interaction.user.id, self.embedname, label)   
      else: await interaction.client.db.execute("INSERT INTO embeds VALUES ($1,$2,$3,$4,$5)", interaction.guild.id if label == "server" else interaction.user.id, self.embedname, text, interaction.message.content if interaction.message.content != "" else None, label)
      await inter.response.edit_message(content=None, embed=discord.Embed(color=interaction.client.color, description="{} {}: Saved your **{}** embed as **{}**".format(interaction.client.yes, interaction.user.mention, label, self.embedname)), view=None)    
      await interaction.message.edit(view=None)

    async def button1_callback(inter: discord.Interaction):
      await save_func("personal", inter)
    
    async def button2_callback(inter: discord.Interaction): 
      await save_func("server", inter)
    
    button1.callback = button1_callback
    button2.callback = button2_callback
    view = discord.ui.View()
    view.add_item(button1)
    view.add_item(button2)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

   @discord.ui.button(label="cancel", custom_id="cancel:button", row=1)
   async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button): 
     if interaction.user.id != self.ctx.author.id: return await interaction.client.ext.send_warning(interaction, "You are not the author of this embed")          
     embed = discord.Embed(color=interaction.client.color, description="Are you sure you want to **cancel** the embed creation?\nChanges won't be saved")
     yes = discord.ui.Button(emoji=interaction.client.yes)
     no = discord.ui.Button(emoji=interaction.client.no)

     async def yes_callback(inter: discord.Interaction): 
      await interaction.message.delete()
      await inter.response.edit_message(embed=discord.Embed(color=interaction.client.color, description="{} {}: Canceled the embed creation".format(interaction.client.yes, interaction.user.mention)), view=None)

     async def no_callback(inter: discord.Interaction): 
      await inter.response.edit_message(embed=discord.Embed(color=interaction.client.color, description="{} {}: Aborting closure".format(interaction.client.yes, interaction.user.mention)), view=None) 

     yes.callback = yes_callback
     no.callback = no_callback
     view = discord.ui.View()
     view.add_item(yes)
     view.add_item(no)
     await interaction.response.send_message(embed=embed, view=view, ephemeral=True) 