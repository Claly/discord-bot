import discord

from pydactyl import PterodactylClient
from discord.ext import commands

class Hesapesle(commands.Cog):

	def __init__(self, bot):
		self.bot = bot


	@commands.command()
	async def hesapsil(self, ctx, id=None):
		database = self.bot.keydata
		config = self.bot.config
		if id == None:
			if str(ctx.author.id) in set([list(x)[1] for x in self.bot.keys]):
				embed=discord.Embed(description="Hesabınızı başarıyla sildiniz.Isterseniz yeniden eşleyebilirsiniz.", color=config['embed']['onayrenk'])
				database.execute("DELETE FROM nightapi WHERE discord_id='" + str(ctx.author.id) + "'")
				database.commit()
				self.bot.keys = database.execute("SELECT * FROM nightapi").fetchall()
			else:
				embed=discord.Embed(description="Size ait bir hesap bulunamıyor.Hesabınızı eşlemek için **!hesapesle** yazın", color=config['embed']['hatarenk'])
		await ctx.send(embed=embed)
		
	@commands.command()
	async def hesapesle(self, ctx, user_key = None):
		config = self.bot.config
		database = self.bot.keydata
		if str(ctx.author.id) not in set([list(x)[1] for x in self.bot.keys]):
			if user_key == None:
				embed=discord.Embed(description="[Bu Adrese](https://panel.nightservers.xyz/account/api) giderek sağ üstte mavi renkli **Create New** tuşuna basarak api anahtarı oluşturun.\nOluşturduğunuz api anahtarını bota özel mesaj olarak şu şekilde gönderin.\n```!hesapesle <api_anahtarı>```", color=config['embed']['onayrenk'])
			else:
				if ctx.guild != None:
					await ctx.message.delete()
					embed=discord.Embed(description=f"{ctx.message.author.mention}, Bu komutu bana özel mesaj olarak atmalısın", color=config['embed']['hatarenk'])
				else:
					if len(user_key) != 48:
						embed=discord.Embed(description="Böyle bir api anahtarı bulunamadı", color=config['embed']['hatarenk'])
					else:
						pteroclient = PterodactylClient(config["ptero"]["url"], user_key)
						checker = False
						try:
							user_servers = pteroclient.client.list_servers()
							checker = True
						except:
							embed=discord.Embed(description="Böyle bir api anahtarı bulunamadı", color=config['embed']['hatarenk'])
						if checker == True:
							embed_son=discord.Embed(description="Hesabınız eşleştiriliyor bu biraz zaman alabilir...", color=config['embed']['onayrenk'])
							editmesaj = await ctx.send(embed=embed_son)
							database.execute("INSERT INTO nightapi (discord_id, api_key)VALUES (?,?)",(ctx.author.id, user_key))
							database.commit()
							self.bot.keys = database.execute("SELECT * FROM nightapi").fetchall()
							embed_son2=discord.Embed(description="Hesabınızı başarıyla eşlediniz.", color=config['embed']['onayrenk'])
							await editmesaj.edit(embed=embed_son2)
							return
		else:
			embed=discord.Embed(description="Zaten hesabınızı eşlemişsiniz.Api anahtarını değiştirmek istiyorsanız anahtarı **!hesapsil** komutu ile silip tekrardan eşleyebilirsiniz.", color=config['embed']['hatarenk'])
		await ctx.send(embed=embed)
def setup(bot):
	bot.add_cog(Hesapesle(bot))
