import asyncio
from bot import get_prefix
import platform
import random


import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(
        name="stats", description="A useful command that displays bot statistics."
    )
    async def stats(self, ctx):
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))

        embed = discord.Embed(
            title=f"{self.bot.user.name} Stats",
            description="\uFEFF",
            colour=ctx.author.colour,
            timestamp=ctx.message.created_at,
        )

        embed.add_field(name="Bot Version:", value=self.bot.version)
        embed.add_field(name="Python Version:", value=pythonVersion)
        embed.add_field(name="Discord.Py Version", value=dpyVersion)
        embed.add_field(name="Total Servidores:", value=serverCount)
        embed.add_field(name="Total Usuarios:", value=memberCount)
        embed.add_field(name="Bot Developer:", value="<@409485667291234306>")

        embed.set_footer(text=f"Carpe Noctem | {self.bot.user.name}")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(
        name="echo",
        description="A simple command that repeats the users input back to them.",
    )
    async def echo(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(
            title="Por favor dime que quieres que repita!",
            description="||Esta solicitud expirará después de 1 minuto..||",
        )
        sent = await ctx.send(embed=embed)

        try:
            msg = await self.bot.wait_for(
                "message",
                timeout=60,
                check=lambda message: message.author == ctx.author
                and message.channel == ctx.channel,
            )
            if msg:
                await sent.delete()
                await msg.delete()
                await ctx.send(msg.content)
        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send("Cancelling", delete_after=10)

    @commands.command(name="toggle", description="Enable or disable a command!")
    @commands.is_owner()
    async def toggle(self, ctx, *, command):
        command = self.bot.get_command(command)

        if command is None:
            await ctx.send("No pude encontrar un comando con ese nombre!")

        elif ctx.command == command:
            await ctx.send("No puede sabilitar ese comando.")

        else:
            command.enabled = not command.enabled
            ternary = "Habilitado" if command.enabled else "Desabilitado"
            await ctx.send(f"Tengo {ternary} el comando {command.qualified_name} por ti!")


    @commands.group(invoke_without_command=True, aliases=['user', 'uinfo', 'info', 'ui'])
    async def userinfo(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.message.author

        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(color=0xdfa3ff, description=user.mention)
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Fecha de ingreso", value=user.joined_at.strftime(date_format))
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Posicion de ingreso", value=str(members.index(user)+1))
        embed.add_field(name="Fecha de registro", value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
        embed.set_footer(text='ID: ' + str(user.id))
        return await ctx.send(embed=embed)
                
            
        await ctx.message.delete()

    @userinfo.command()
    async def avi(self, ctx, txt: str = None):
        """View bigger version of user's avatar. Ex: [p]info avi @user"""
        if txt:
            try:
                user = ctx.message.mentions[0]
            except IndexError:
                user = ctx.guild.get_member_named(txt)
            if not user:
                user = ctx.guild.get_member(int(txt))
            if not user:
                user = self.bot.get_user(int(txt))
            if not user:
                await ctx.send('No pude encontrar al usuario.')
                return
        else:
            user = ctx.message.author

        if user.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi = user.avatar_url.rsplit("?", 1)[0]
        else:
            avi = user.avatar_url_as(static_format='png')

            em = discord.Embed(colour=0x708DD0)
            em.set_image(url=avi)
            await ctx.send(embed=em)

    @commands.group(name="setlog",description="set log channel")
    async def setlog(self, ctx, *, channel: discord.guild.TextChannel = None):
        if channel:
            await self.bot.log_channel.upsert({"_id": ctx.guild.id, "channel_id": channel.id})
            await ctx.send(f"El canal de logs se a establecido en **{channel}**")
        else:
            await ctx.send("Debes especificar un canal")
        

def setup(bot):
    bot.add_cog(Misc(bot))
