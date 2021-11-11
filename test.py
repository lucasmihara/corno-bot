from PIL import Image, ImageDraw, ImageFont
import textwrap
import json

meme = "step_shit"
texts = ["Lorem ipsum dolor", "sit amet, consectetur adipiscing elit.", "Curabitur sed ligula fermentum,","tincidunt leo nec, scelerisque sapie"]

with open('memes/dict.json') as json_file:
    dict = json.load(json_file)
img = Image.open(dict[meme]["file"])

d1 = ImageDraw.Draw(img)
font = ImageFont.truetype(font="fonts/calibri.ttf", size=30, encoding="utf-8")
for position, text in zip( dict[meme]["positions"], texts):
    text = textwrap.TextWrapper(width=30, break_long_words=False).fill(text)
    d1.multiline_text(position, text, fill=(0,0,0), font=font, anchor="mm")
# img.show()