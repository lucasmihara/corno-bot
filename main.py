import discord
from discord.ext import commands, tasks
import os
import music
from datetime import datetime
import json
import random

cogs = [music]

client = commands.Bot(command_prefix="~~", help_command=None)

for i in range(len(cogs)):
  cogs[i].setup(client)


@client.event
async def on_ready():
  print("Connected as {0.user}".format(client))

@client.command()
async def hello(ctx):
  await ctx.send("Olá " + str(ctx.author))

# @tasks.loop(minutes=1.0)
# async def check_3am():
#   print("A")
#   now = datetime.now().strftime("%H:%M:%S")
#   print(now)
#   if str(now).startswith('05:1'):
#     client.get_channel(764322455732879420).send('10 minutos para as 3:00')
#     #764322455732879420
    
@client.command()
async def say(ctx, *args):
  arg = ''
  for word in args:
    arg += word + ' '
  await ctx.message.delete()
  if len(arg) > 0:
    await ctx.send(arg)

@client.command()
async def randonisio(ctx, *args):
  n = len(args)
  await ctx.send(args[random.randint(0, n-1)])
  

@client.command()
async def help(ctx):
  await ctx.send("""```
Comandos:\n
join - entra no canal de voz
play [nome da música] - pesquisa uma música no youtube e adiciona à fila
playskip [nome da música] - pesquisa uma música no youtube e a toca imediatamente
skip - passa para a próxima música da fila
queue - exibe a fila de reprodução
changeposition [posição da música] [posição destino] - troca a posição da música selcionada para a posição destino
leave - desconecta o bot do canal ```""")


config_file = open("config.json")
config = json.load(config_file)
client.run(config['token'])