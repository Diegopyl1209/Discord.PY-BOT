import discord
import asyncio

from discord.ext import commands

embedhelp = discord.Embed(title=":shield: | Ayuda", description="Bot con funciones de Moderación", color=0x00ff00)
embedhelp.set_footer(text="Reacciones:\n🎮 = Comandos de STAFF\n📜 = Comandos de info y miselaneos\n😝 = Comandos Reacciones\n🌎 = Indice")

embedstaff = discord.Embed(title=":shield: | Ayuda", description="Comandos STAFF", color=0x00ff00)
embedstaff.add_field(name="Ban", value="Banea a un miembro del servidor", inline=False)
embedstaff.add_field(name="Hackban", value="Banea a un usuario de discord por su ID", inline=False)
embedstaff.add_field(name="Unban", value="Desbanea a alguien", inline=False)
embedstaff.add_field(name="Kick", value="Expulsa a alguien del servidor", inline=False)
embedstaff.add_field(name="Warn", value="Advierte a un usuario del servidor", inline=False)
embedstaff.add_field(name="Deletewarn", value="Elimina una advertencia de algun usuario", inline=False)
embedstaff.add_field(name="Purge", value="Elimina una cantidad de mensajes en algun canal del servidor", inline=False)
embedstaff.add_field(name="Mute", value="Silencia a algun usuario", inline=False)
embedstaff.add_field(name="Unmute", value="Quita el silencio a algun usuario", inline=False)
embedstaff.add_field(name="New <channel - category>", value="Crea un canal o una categoria dando un rol y un nombre", inline=False)
embedstaff.add_field(name="Delete <channel - category>", value="Elimina un canal o categoria dando un ID", inline=False)

embedinfo = discord.Embed(title=":shield: | Ayuda", description="Comandos INFO", color=0x00ff00)
embedinfo.add_field(name="Help", value="El comando de ayuda", inline=False)
embedinfo.add_field(name="UserInfo", value="Envia un embed con informacion relevante de un usuario", inline=False)
embedinfo.add_field(name="opgg", value="Envia informacion sobre el perfil de opgg de alguien **PROXIMAMENTE**", inline=False)

embedreaction = discord.Embed(title=":shield: | Ayuda")
embedreaction.add_field(name="Happy", value="Reaccion: HAPPY", inline=False)
embedreaction.add_field(name="Cry", value="Reaccion: CRY", inline=False)
embedreaction.add_field(name="Hug", value="Reaccion: HUG", inline=False)
embedreaction.add_field(name="Kill", value="Reaccion: KILL", inline=False)
embedreaction.add_field(name="Kiss", value="Reaccion: KISS", inline=False)
embedreaction.add_field(name="Smug", value="Reaccion: SMUG", inline=False)
embedreaction.add_field(name="Dance", value="Reaccion: DANCE", inline=False)
embedreaction.add_field(name="Deathnote", value="Reaccion: DEATHNOTE", inline=False)




class Help(commands.Cog, name="Help command"):
    def __init__(self, bot):
        self.bot = bot
        self.cmds_per_page = 6


    @commands.group(
        name="help", aliases=["h", "commands"], description="The help command!"
    )
    async def help(self, ctx):
            pages = 4
            cur_page = 1
            message = await ctx.send(embed = embedhelp)
            # getting the message object for editing and reacting

            await message.add_reaction("🎮")
            await message.add_reaction("📜")
            await message.add_reaction("😝")
            await message.add_reaction("🌎")

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["📜", "🎮", "😝", "🌎"]
            # This makes sure nobody except the command sender can interact with the "menu"

            while True:
                try:
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
            # waiting for a reaction to be added - times out after x seconds, 60 in this
            # example

                    if str(reaction.emoji) == "📜":
                        cur_page += 1
                        await message.edit(embed = embedinfo)
                        await message.remove_reaction(reaction, user)

                    elif str(reaction.emoji) == "🎮":
                        cur_page -= 1
                        await message.edit(embed = embedstaff)
                        await message.remove_reaction(reaction, user)
                    elif str(reaction.emoji) == "😝":
                        cur_page -= 1
                        await message.edit(embed = embedreaction)
                        await message.remove_reaction(reaction, user)
                    elif str(reaction.emoji) == "🌎":
                        cur_page -= 1
                        await message.edit(embed = embedhelp)
                        await message.remove_reaction(reaction, user)

                    else:
                        await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
                except asyncio.TimeoutError:
                    await message.delete()
                    break
def setup(bot):
    bot.add_cog(Help(bot))