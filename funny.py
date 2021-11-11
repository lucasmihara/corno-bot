from PIL import Image, ImageDraw, ImageFont
import textwrap
import json
import discord
from discord.ext import commands
from tempfile import TemporaryFile

class funny(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def mememaker(self, ctx, meme, *texts):
        try:
            with open('memes/dict.json') as json_file:
                dict = json.load(json_file)
        except:
            await ctx.send("Meme inválido")

        img = Image.open(dict[meme]["file"])

        d1 = ImageDraw.Draw(img)
        font = ImageFont.truetype(font="fonts/calibri.ttf", size=30, encoding="utf-8")
        for position, text in zip( dict[meme]["positions"], texts):
            text = textwrap.TextWrapper(width=30, break_long_words=False).fill(text)
            d1.multiline_text(position, text, fill=(0,0,0), font=font, anchor="mm")
        fp = open(f"TempFile.{img.format}", "wb+")
        img.save(fp, img.format)
        fp.seek(0)
        await ctx.send(file=discord.File(fp))
        fp.close()
    
def setup(client):
    client.add_cog(funny(client))