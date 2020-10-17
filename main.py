from discord.ext import commands
import os
import sqlite3

from ruamel.yaml import YAML
from aioconsole import ainput
from os import listdir
from os.path import isfile, join

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), case_insensitive=True)
yaml = YAML()

bot.keydata = sqlite3.connect(f"userkeys.db")
bot.keydata.execute("CREATE TABLE IF NOT EXISTS nightapi (id INTEGER PRIMARY KEY AUTOINCREMENT, discord_id VARCHAR(255), api_key VARCHAR(255))")


bot.keys = bot.keydata.execute("SELECT * FROM nightapi").fetchall()
with open("config.yml", "r") as stream:
	bot.config = yaml.load(stream) 


bot.remove_command("help")
#for cog in [f for f in listdir("cogs") if isfile(join("cogs", f))]:
#	if cog.endswith(".py"):
#		try:
#			cog = f"cogs.{cog[0:-3]}"
#			bot.load_extension(cog)
#			print(f"Added - {cog[5:].capitalize()}")
#		except Exception as e:
#			print(f"Can't load {cog}: {e}")



async def console():
    cmd = await ainput("\n>>> ")
    os.system("clear")
    if cmd.replace(" ", "") != "":
        if cmd.startswith("reload"):
            for cog in os.listdir("cogs/"):
                if cog.endswith(".py"):
                    try:
                        cog = f'cogs.{cog.replace(".py", "")}'
                        bot.unload_extension(cog)
                    except Exception as e:
                        print(f'[-] {cog}')
            try:
                await setup()
            except Exception as e:
                print("Xəta baş verdi\n{}".format(e))
            else:
                print(f"\n{bot.user.name} Yenidən yükləndi")
        elif cmd.startswith("help"):
            print("reload -> yenidən başlayır")
        else:
            print("bilinməyən əmr")
    await console()

async def setup():
    os.system("clear")
    for cog in os.listdir("cogs/"):
        if cog.endswith(".py"):
            try:
                cog = f'cogs.{cog.replace(".py", "")}'
                bot.load_extension(cog)
                print(f'[+] {cog.replace("cogs.", "").capitalize()}')
            except Exception as e:
                print(f'[-] {cog}')
                raise e

#async def status_task():
#	while True:
#		response = requests.get("https://api.nightservers.xyz/server/servers.php")
#		cevur2 = response.json()
#		await bot.change_presence(activity=discord.Game(name=f"{cevur2['totalserver']} sunucu"))
#		await asyncio.sleep(10)
#		await bot.change_presence(activity=discord.Game(name=f"{cevur2['totaluser']} müşteri"))
#		await asyncio.sleep(10)

@bot.event
async def on_ready():
	
	await setup()
	await console()
#	response = requests.get("https://api.nightservers.xyz/server/servers.php")
#	cevur2 = response.json()
#	await bot.change_presence(activity=discord.Game(name=f"{cevur2['totalserver']} sunucu"))
#	bot.loop.create_task(status_task())

bot.run(bot.config["token"])