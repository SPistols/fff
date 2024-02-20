import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import datetime
import humanfriendly
import asyncio
import json

bot = commands.Bot(command_prefix= '-', intents=nextcord.Intents.all())

# Connecter la base de d
with open('report.json', encoding='utf-8') as f:
  try:
    report = json.load(f)
  except ValueError:
    report = {}
    report['users'] = []

# Mise en ligne du bot
@bot.event
async def on_ready():
    print('Bot Online !')
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.streaming, name="Final Boss Theme", url="https://youtu.be/U0TXIXTzJEY?si=7ZvUUEgxd0PGeeQz"))

# Ajouter les WARNS a la base de données
async def addwarn(ctx, reason, user):
    for current_user in report['users']:
        if current_user['name'] == user.name:
            current_user['reasons'].append(reason)
            break
    else:
        report['users'].append({
            'name': user.name,
            'reasons': [reason, ]
        })
    with open('report.json', 'w+') as f:
        json.dump(report, f)

# Commande WARN
@bot.command()
@commands.has_permissions(manage_guild= True)
async def warn(ctx: commands.Context, member: nextcord.Member, *, reason: str="No reason"):
    channel = nextcord.ChannelType
    if reason == "No reason":
        await ctx.send("** :x: Veuillez fournir raison valide :x: **")
    else:
        await addwarn(ctx, reason, member)
        await member.send(f'Vous avez été warn dans {channel} car {reason}')
        await ctx.send(f"**{member.mention}** a été warn car **{reason}**")

# Supprimer le WARN de la bd
@bot.command()
@commands.has_permissions(manage_guild = True)
async def removewarn(ctx: commands.Context, member: nextcord.Member):
    for current_user in report['users']:
        if current_user['name'] == member.name:
            current_user['reasons'].pop()
            break
        else:
            await ctx.send("**Aucun warn a supprimer**")
    with open('report.json', 'w+') as f:
        json.dump(report, f)

# Afficher la liste de WARNING
@bot.command()
async def warnings(ctx, user:nextcord.User):
  for current_user in report['users']:
    if user.name == current_user['name']:
      await ctx.send(f"**{user.name} a été warn {len(current_user['reasons'])}: {','.join(current_user['reasons'])}**")
  else:
    await ctx.send(f"**{user.name} n' a jamais été warn**")



@bot.slash_command(guild_ids=[1203727221584568320])
async def darija(interaction: Interaction):
    await interaction.response.send_message("wa sir t9wd")

# Command MUTE et UNMUTE
@bot.command()
@commands.has_permissions(manage_guild=True)
async def tempmute(ctx, member: nextcord.Member, time, *, reason: str="No reason"):
    time = humanfriendly.parse_timespan(time)
    if reason == "No reason":
        await ctx.send('** :x: Veuillez fournir une raison :x: **')
    else:
       await member.edit(timeout=nextcord.utils.utcnow() + datetime.timedelta(seconds=time))
       await ctx.send(f"** :hourglass_flowing_sand: {member.mention}** a été mute car **{reason}** pour **{time / 60} min :hourglass_flowing_sand: **")

@bot.command()
@commands.has_permissions(manage_guild =True)
async def unmute(ctx, member: nextcord.Member):
    await member.edit(timeout=None)
    await ctx.send(f"** :hourglass_flowing_sand: {member.mention} a été unmute :hourglass_flowing_sand: **")

@bot.command()
async def ping(ctx):
    await ctx.send(f':ping_pong: Pong ! Ma latence actuelle est {bot.latency} ms')








bot.run("MTIwNTkwMjA0NTcxMDc3ODQwOA.GC3SFL.aNZWxDDZ_xzM3t9rxrV3mwpvDt5LF2gQpfVsPM")