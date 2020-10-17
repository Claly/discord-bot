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

@bot.event
async def on_ready():
	await setup()
	await console()

bot.run(bot.config["token"])
