import discord
import requests
import pydactyl

from discord.ext import commands
from discord.utils import get

class Create(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='create')
    async def create(self, ctx, *args):
        """
        Args:
            0: Mention
            1: E-Mail
            2: User
            3: Password
        """

        config = self.bot.config
        if ctx.author.id in config["admin"]:
            if len(args) >= 4:
                regex = re.fullmatch(r"<@!?(\d+)>", args[0])
                if regex is not None:
                    member = ctx.guild.get_member(int(regex.group(1)))
                    pteroclient = PterodactylClient(config["ptero"]["url"], config["ptero"]["app_key"])
                    result = pteroclient.user.create_user(email=args[1], username=args[2], password=args[3], language="tr", first_name="Night", last_name="Servers")
                    if "errors" in result:
                        embed = discord.Embed(description=f"❌ {result['errors']['0']['email']}", color=0xfc0303)
                        await ctx.channel.send(embed=embed)
                    else:
                        server = pteroclient.servers.create_server(name=f"NightServers - {args[2]}", user_id=result['attributes']['id'], nest_id=1, egg_id=3, memory_limit=1000, swap_limit=0, disk_limit=5000, database_limit=0, allocation_limit=0, docker_image="quay.io/pterodactyl/core:java", location_ids=[2], io_limit=500, cpu_limit=100, dedicated_ip=False, port_range=[], start_on_completion=False)
                        output = server.json()
                        embed = discord.Embed(description=f"{args[0]} hesabınız ve sunucunuz oluşturuldu. Daha çok RAM elde etmek için **başkalarını davet edebilir** veya [bağış yapabilirsiniz](https://nightservers.xyz/index.php?threads/bagis-oeduelleri-ve-gereksimleri.113/). Destek talebinde işiniz bittiyse **!kapat** komutuyla talebi kapatabilirsiniz.", color=0x03fc28)
                        embed.add_field(name="Diğer", value="**Site:** [Tıkla](https://nightservers.xyz/)\n**Wiki:** [Tıkla](https://wiki.nightservers.xyz/)", inline=True)
                        embed.add_field(name="​", value="**Panel:** [Tıkla](https://panel.nightservers.xyz/)\n**Durum:** [Tıkla](https://status.nightservers.xyz/)", inline=True)
                        embed.add_field(name="Hesap bilgileri", value=f"Sunucu ID: **{output['attributes']['identifier']}**\nE-Posta: **{args[1]}**\nKullanıcı adı: **{args[2]}**\nŞifre: **{args[3]}**")
                        embed.set_author(name="NightServers | Sunucu Oluşturuldu", icon_url='https://cdn.nightservers.xyz/nslogo.png')
                        role = get(ctx.guild.roles, name="🤠│Müşteri")
                        await ctx.message.delete()
                        await ctx.channel.send(embed=embed)
                        await member.add_roles(role)
                        await member.edit(nick=f"{member.display_name} ({output['attributes']['identifier']})")
                else:
                    embed = discord.Embed(description=f"Kullanıcı geçersiz", color=0xfc0303)
                    await ctx.channel.send(embed=embed)
                    pass
            else:
                embed = discord.Embed(description=f"Kullanım !create <mention> <email> <username> <password>", color=0xfc0303)
                await ctx.channel.send(embed=embed)
                pass
        else:
            embed = discord.Embed(description="Bu komutu kullanamazsın.", color=0xfc0303)
            await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Create(bot))
