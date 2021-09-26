import youtube_dl
import json

url = input()

YDL_OPTIONS = {'format': 'bestaudio', 'ignoreerrors': True, 'age_limit': 0, 'noplaylist': True}
try:
    info =  youtube_dl.YoutubeDL(YDL_OPTIONS).extract_info(url, download=False)
    with open('data.json', 'w') as outfile:
        json.dump(info, outfile)
    print(info)
except:
    print("indisponivel")