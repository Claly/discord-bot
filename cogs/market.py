import discord
import json
import requests
import math

from pydactyl import PterodactylClient
from discord.ext import commands

class NightMarket(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def sil(self,ctx,srvid):
		config = self.bot.config
		if ctx.author.id == 253937964193677323:
			response = requests.get(f"{config['api']['server']['info_url']}{srvid}")
			serverinfo = response.json()
			pteroclient = PterodactylClient(config["ptero"]["url"], config['ptero']['api_key'])
			pteroclient.servers.delete_server(serverinfo['id'])
	
	@commands.command()
	async def olustur(self,ctx):
		config = self.bot.config
		if ctx.author.id == 253937964193677323:
			pteroclient = PterodactylClient(config["ptero"]["url"], config['ptero']['api_key'])
			pteroclient.servers.create_server(name=f"Fenish Test", user_id=1135, nest_id=1, egg_id=3, memory_limit=5000, swap_limit=0, disk_limit=5000, database_limit=0, allocation_limit=0, docker_image="quay.io/pterodactyl/core:java", location_ids=[2], io_limit=500, cpu_limit=100, dedicated_ip=False, port_range=[], start_on_completion=False)
	
	@commands.command(aliases=['NightMarket'])
	async def market(self,ctx,srvid=None):
		config = self.bot.config
		database = self.bot.keydata
		if str(ctx.author.id) in set([list(x)[1] for x in self.bot.keys]):
			kod = [x[2] for x in self.bot.keys if x[1] == str(ctx.author.id)][0]
			pteroclient = PterodactylClient(config["ptero"]["url"], kod)
			server_list = pteroclient.client.list_servers()
			if srvid == None:
				embed=discord.Embed(title="🛍️ Sunucu Marketi", description="Lütfen sunucu id'nizi kullanarak komutu tekrardan çalıştırınız.\n**Örnek:** !market feN15h01", color=config['embed']['market']['huba'])
				if len([x.data for x in server_list][0]) != 0:
					for x in server_list:
						srv_ram = [str(y['attributes']['limits']['memory']/1000) + " GB" for y in x.data]
						srv_names = [y['attributes']['name'] for y in x.data]
						srv_ids = ["`"+y['attributes']['identifier']+"`" for y in x.data]
					embed.add_field(name="Sunucu ID", value="\n".join(srv_ids), inline= True)
					embed.add_field(name="Sunucu Adı", value="\n".join(srv_names), inline= True)
					embed.add_field(name="Sunucu Belleği", value="\n".join(srv_ram), inline= True)
				else:
					embed=discord.Embed(title="Bir hata oluştu :x:",description="Size ait bir sunucu bulunamıyor.", color=config['embed']['hatarenk'])
			else:
				response = requests.get(f"{config['api']['server']['info_url']}{srvid}")
				info = response.json()
				if "error" not in info:
					for server in server_list:
						if srvid not in [y['attributes']['identifier'] for y in server.data]:
							embed=discord.Embed(title="Bir hata oluştu :x:",description="Bu sunucu size ait değil!", color=config['embed']['hatarenk'])
							await ctx.send(embed=embed)
							return
					embed=discord.Embed(title="🛍️ Sunucu Marketi",
						description=f"""
						**Sunucu ID:** `{srvid}`
						**Sunucu Adı:** `{info['name']}`

						Aşağıda sunucunuzun özellikleri yazmaktadır.Arttırmak istediğiniz özelliği emojiler ile seçtikten sonra onaylayınız.
						""",
						color=config['embed']['market']['huba'])
					embed.set_thumbnail(url=ctx.author.avatar_url)
					embed.add_field(name="Ram", value=f"**{info['memory']/1000} GB**",inline=True)
					embed.add_field(name="Disk", value=f"**{info['disk']/1000} GB**",inline=True)
					embed.add_field(name="İşlemci", value=f"**{math.floor(info['cpu']/100)} Çekirdek**",inline=True)

					embed.add_field(name="\u200b", value="Aşağıdan ürünlerin fiyatını görebilirsiniz.Satın almak istediğiniz ürünün yanında yazan emojiye 1 kere tıklayın.Tıkladığınız zaman satın alma gerçekleştirilecektir.Yanlışıkla bastım diyip geri yükleme istemeyiniz.\n\n**Ürünler** 🛒",inline=False)
					embed.add_field(name="☄️- 1 GB Ram", value="1 Night Coin", inline=True)
					embed.add_field(name="⚙️- 1 Çekirdek", value="1 Bağış Puanı", inline=True)
				
				else:
					embed=discord.Embed(title="Bir hata oluştu :x:",description="Böyle bir sunucu bulunamadı.", color=config['embed']['hatarenk'])
		else:
			embed=discord.Embed(title="Bir hata oluştu :x:",description="Size ait bir hesap bulunamıyor.Hesabınızı eşlemek için **!hesapesle** yazın", color=config['embed']['hatarenk'])
		
		await ctx.send(embed=embed)


	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		config = self.bot.config
		if isinstance(error, commands.CommandInvokeError):
			if "Forbidden for url" in str(error):
				if str(ctx.author.id) in set([list(x)[1] for x in self.bot.keys]):
					database = self.bot.keydata
					kod = [x[2] for x in self.bot.keys if x[1] == str(ctx.author.id)][0]
					pteroclient = PterodactylClient(config["ptero"]["url"], kod)
					checker = False
					try:
						user_servers = pteroclient.client.list_servers()
						checker = True
					except:
						embed=discord.Embed(title="Bir hata oluştu :x:",description="Görünüşe göre yanlışıkla api anahtarınızı silmişsiniz.Yeniden eşlemek için **!hesapesle** komutunu kullanınız.", color=config['embed']['hatarenk'])
						await ctx.send(embed=embed)
						database.execute("DELETE FROM nightapi WHERE discord_id='" + str(ctx.author.id) + "'")
						database.commit()
						self.bot.keys = database.execute("SELECT * FROM nightapi").fetchall()
						return

		if not isinstance(error, commands.CommandNotFound):
			await ctx.send(embed=discord.Embed(title="Bir hata oluştu :x:",description=str(error), color=config['embed']['hatarenk']))
			return
		print(error)
def setup(bot):
	bot.add_cog(NightMarket(bot))
