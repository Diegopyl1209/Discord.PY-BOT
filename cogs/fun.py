import discord
import aiohttp
import random
import asyncio

from discord.ext import commands
from utils import http




class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    async def reactionapi(self, ctx, url: str, reaccion_imagen: str, reaccion: str):
        try:
            r = await http.get(
                url, res_method="json"
            )
        except aiohttp.ClientConnectorError:
            return await ctx.send("La API no responde....")
        except aiohttp.ContentTypeError:
            return await ctx.send("La API regreso un error :(")

            #EMBED de las reacciones
        embedreac = discord.Embed(description=(f"**{ctx.author.name}** {reaccion}").format(str), color=0x00ff00)
        embedreac.set_image(url=r[reaccion_imagen])  


        await ctx.send(embed = embedreac)


    @commands.group(name="happy", description="Reaccion: HAPPY")
    async def happy(self, ctx):
        """ Reaccion: Happy """
        await self.reactionapi(ctx, 'https://waifu.pics/api/sfw/happy', 'url', "Parece estar feliz  (•◡•)")

    @commands.group(name="dance", description="Reaccion: DANCE")
    async def dance(self, ctx):
            """ Reaccion: Bailar  """
            await self.reactionapi(ctx, 'https://waifu.pics/api/sfw/dance', "url", "Esta Bailando!! ٩(˘◡˘)۶")
    @commands.group(name="smug", description="Reaccion: SMUG")
    async def smug(self, ctx):
            """ Reaccion: Smug (nose como se dice en español sorry) """
            await self.reactionapi(ctx, 'https://waifu.pics/api/sfw/smug', 'url', "Parece estar presumiendo (¬‿¬)")

    @commands.group(name="cry", description="Reaccion: SMUG")
    async def cry(self, ctx):
        await self.reactionapi(ctx, 'https://waifu.pics/api/sfw/cry', 'url', "Esta Triste  (╥︣﹏╥)")

    @commands.group(name="hug", description="Reaccion: SMUG")
    async def hug(self, ctx, alguien: discord.guild.Member):
        """ Reaccion: Abrazar a alguien """
        await self.reactionapi(ctx, 'https://waifu.pics/api/sfw/hug', "url", f'A abrazado a **{alguien}** (ɔ◔‿◔)ɔ ♥')

    @commands.group(name="kill", description="Reaccion: SMUG")
    async def kill(self, ctx, alguien: discord.guild.Member):
        """ Reaccion: Matar a alguien """
        await self.reactionapi(ctx, 'https://waifu.pics/api/sfw/kill', "url", f'A matado a **{alguien}** (｡•́︿•̀｡)')

    @commands.group(name="kiss", description="Reaccion: SMUG")
    async def kiss(self, ctx, alguien: discord.guild.Member):
        """ Reaccion: Abrazar a alguien """
        await self.reactionapi(ctx, 'https://waifu.pics/api/sfw/kiss', "url", f'A besado a **{alguien}** ᕙ(^▿^-ᕙ)')
    
    @commands.group(name="deathnote", description="Reaccion: SMUG")
    async def deathnote(self, ctx, alguien: discord.guild.Member):
        """ Nose """
        deathnote1 = ["https://gifimage.net/wp-content/uploads/2017/11/gif-escribiendo-14.gif", "https://i.imgur.com/At4yeWA.gif", "https://i.imgur.com/9nt8rY8.gif", "https://i.imgur.com/f99afcz.gif"]
        deathnote2 = [""]

        embeddeath1 = discord.Embed(description=(f"**{ctx.author.name}** esta tramando algo").format(str), color=0x00ff00)
        embeddeath1.set_image(url=random.choice(deathnote1))

        await ctx.send(embed = embeddeath1, delete_after=60.0)
        await ctx.message.delete()
        await asyncio.sleep(60)
        
        r = await http.get("https://waifu.pics/api/sfw/kill", res_method="json")
        embeddeath2 = discord.Embed(description=(f"**{alguien}** a muerto").format(str), color=0x00ff00)
        embeddeath2.set_image(url=r["url"])

        await ctx.send(embed = embeddeath2)






def setup(bot):
    bot.add_cog(Fun(bot))