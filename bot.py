from dotenv import load_dotenv
import os
import requests
from pexels_api import API
import discord
import json

load_dotenv()

TOKEN=os.getenv("DISCORD_TOKEN")
GUILD=os.getenv("GUILD")
PEXELS_API=os.getenv("PEXELS_API")
search_term=""
intents = discord.Intents.all()
client=discord.Client(intents=intents)

class ImageScraper():
    def __init__(self,search_term):
        self.search=search_term
        self.img_count=0
        self.photos=[]
        self.pexels_api_key=PEXELS_API
        self.unsplash_api=f"https://unsplash.com/napi/search?query={self.search}&per_page=20&xp="
    def pexels(self,i_count):
        self.img_count=i_count
        with requests.session() as r:
            api=API(self.pexels_api_key)
            api.search(self.search,results_per_page=10)
            photos=api.get_entries()
            for i in range(int(self.img_count)):
                self.photos.append(photos[i].original)
            print(self.photos)
            return self.photos
    def unsplash(self,i_count):
        self.img_count=i_count
        with requests.session() as r:
            response=r.get(self.unsplash_api)
            photos_json=json.loads(response.text)
            for i in range(int(self.img_count)):
                self.photos.append(photos_json["photos"]["results"][i]["urls"]["raw"])
            return self.photos

@client.event
async def on_ready():
    print(f"{client.user} has connected to the server")
    for guild in client.guilds:
        if guild.name==GUILD:
            break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@client.event
async def on_message(message):
    if(message.author == client.user):
        return
    if(message.content.split(" ")[0].lower()=="picot"):
        search_term =" ".join(message.content.split(" ")[1:-1])
        imgs = ImageScraper(search_term)
        if (message.content.split(" ")[1] == "help"):
            await message.channel.send('`picot "search query" number_of_images(optional, default is 10)`')
            return
        if (message.content.split[-1].isnumeric() == True):
            imgs.pexels(int(int(message.content.split(" ")[-1])/2.0))
            imgs.unsplash(int(int(message.content.split(" ")[-1])/2.0))
            for photo in imgs.photos:
                await message.channel.send(photo)
        else:
            imgs.pexels(5)
            imgs.unsplash(5)
            for photo in imgs.photos:
                await message.channel.send(photo)

client.run(TOKEN)
