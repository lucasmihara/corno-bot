import discord
from discord.ext import commands

import youtube_dl

class music(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.music_queue = []
    self.ctx = None

  @commands.command()
  async def join(self, ctx):
    if ctx.author.voice == None:
      await ctx.send("Conecte-se em um canal primeiro")
      return
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
      await voice_channel.connect()
    else:
      await ctx.voice_client.move_to(voice_channel)

  @commands.command()
  async def leave(self, ctx):
    if ctx.voice_client is not None:
      self.music_queue = []
      await ctx.voice_client.disconnect()

  async def get_video(self, ctx, arg):
    if ctx.voice_client is None:
      await ctx.send('Não estou conectado em nenhum canal, use o comando join primeiro')
      return
    
    YDL_OPTIONS = {'format': 'bestaudio', 'ignoreerrors': True, 'age_limit': 0, 'noplaylist': True}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if arg.startswith('https:'):
      info =  youtube_dl.YoutubeDL(YDL_OPTIONS).extract_info(arg, download=False)
      if info and '_type' in info and info['_type'] == 'playlist':
        for video in info['entries']:
          if video:
            url2 = video['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            video.update({"source": source})
            await ctx.send('Adicionado à fila: ' + video['title'])
            self.music_queue.append(video)
        return None
    else:
      info =  youtube_dl.YoutubeDL(YDL_OPTIONS).extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
    if not info:
      await ctx.send('Falha ao carregar o vídeo')
      return None
    url2 = info['formats'][0]['url']
    source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
    info.update({"source": source})
    return info
    
  
  @commands.command()
  async def play(self, ctx, *args):
    if not args:
      await ctx.send(f"Comando inválido")
      return
    arg = ''
    for word in args:
      arg += word + ' '
    
    song = await self.get_video(ctx, arg)
    if song:
      await ctx.send('Adicionado à fila: ' + song['title'])
      self.music_queue.append(song)
    print(ctx)
    if not ctx.voice_client.is_playing():
      self.play_next(ctx)
  
  @commands.command()
  async def playskip(self, ctx, *args):
    if not args:
      await ctx.send(f"Comando inválido")
      return
    arg = ''
    for word in args:
      arg += word + ' '
    
    song = await self.get_video(ctx, arg)
    if song:
      await ctx.send('Tocando agora: ' + song['title'])
      self.music_queue.insert(0, song)
    if not ctx.voice_client.is_playing():
      self.play_next(ctx)
    else:
      ctx.voice_client.stop()

  def play_next(self, ctx):
    print('next')
    if self.music_queue:
      self.ctx = ctx
      song = self.music_queue.pop(0)
      ctx.voice_client.play(song['source'], after=self.after_play)
    else:
      ctx.voice_client.stop()

  def after_play(self, error):
    self.play_next(self.ctx)

  @commands.command()
  async def skip(self, ctx):
    await ctx.send(f"Pulando música atual")
    ctx.voice_client.stop()

  @commands.command()
  async def queue(self, ctx):
    i = 1
    if not self.music_queue:
      await ctx.send(f"Sem músicas na fila")
    else:
      for song in self.music_queue:
        await ctx.send(f"{i} - {song['title']}")
        i += 1


  @commands.command()
  async def clearqueue(self, ctx):
    self.music_queue = []
    await ctx.send(f"Fila esvaziada")

  @commands.command()
  async def changeposition(self, ctx, *args):
    if not args or len(args) != 2:
      await ctx.send(f"Comando inválido")
      return
    try:
      ini_index = int(args[0]) - 1
      dest_index = int(args[1]) - 1
    except:
      await ctx.send(f"Comando inválido")
    if ini_index < 0 or ini_index >= len(self.music_queue) or dest_index < 0 or dest_index >= len(self.music_queue):
      await ctx.send(f"Posições inválidas")
      return
    self.music_queue.insert(dest_index ,self.music_queue.pop(ini_index))


  # @commands.command()
  # async def play(self, ctx, *args):
  #   if ctx.voice_client is None:
  #     await ctx.send('Não estou conectado em nenhum canal, use o comando join primeiro')
  #     return
  #   FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
  #   YDL_OPTIONS = {'format': 'bestaudio'}
  #   vc = ctx.voice_client

  #   arg = ''
  #   for word in args:
  #     arg += word + ' '
  #   with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
  #     info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
  #     await ctx.send('Adicionado à fila: ' + info['title'])
  #     url2 = info['formats'][0]['url']
  #     source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
  #     self.music_queue.append(source)
    
  #     if not vc.is_playing():
  #       print("not playing")
  #       self.play_next(ctx)



def setup(client):
  client.add_cog(music(client))
