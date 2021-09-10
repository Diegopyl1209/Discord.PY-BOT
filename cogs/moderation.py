import re
import datetime
from copy import deepcopy

import asyncio
import discord
from discord.ext import commands, tasks
from dateutil.relativedelta import relativedelta

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)
            except KeyError:
                raise commands.BadArgument(
                    f"{value} es una clave de tiempo no válida! h|m|s|d son argumentos validos"
                )
            except ValueError:
                raise commands.BadArgument(f"{key} no es un numero!")
        return round(time)


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mute_task = self.check_current_mutes.start()

    def cog_unload(self):
        self.mute_task.cancel()

    @tasks.loop(minutes=5)
    async def check_current_mutes(self):
        currentTime = datetime.datetime.now()
        mutes = deepcopy(self.bot.muted_users)
        for key, value in mutes.items():
            if value['Duracion'] is None:
                continue

            unmuteTime = value['Silenciado el'] + relativedelta(seconds=value['Duracion'])

            if currentTime >= unmuteTime:
                guild = self.bot.get_guild(value['Id del servidor'])
                member = guild.get_member(value['_id'])

                role = discord.utils.get(guild.roles, name="😶 Muteado 😶")
                if role in member.roles:
                    await member.remove_roles(role)
                    print(f"Unmuted: {member.display_name}")

                await self.bot.mutes.delete(member.id)
                try:
                    self.bot.muted_users.pop(member.id)
                except KeyError:
                    pass

    @check_current_mutes.before_loop
    async def before_check_current_mutes(self):
        await self.bot.wait_until_ready()

    @commands.command(
        name='mute',
        description="Silencia a un usuario por x tiempo!",
        ussage='<user> [time]'
    )
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, time: TimeConverter=None):
        role = discord.utils.get(ctx.guild.roles, name="😶 Muteado 😶")
        if not role:
            await ctx.send("No se encontro el rol `😶 Muteado 😶`")
            return

        try:
            if self.bot.muted_users[member.id]:
                await ctx.send("Este usuario ya esta muteado")
                return
        except KeyError:
            pass

        data = {
            '_id': member.id,
            'Silenciado el': datetime.datetime.now(),
            'Duracion': time or None,
            'Silenciado por': ctx.author.id,
            'Id del servidor': ctx.guild.id,
        }
        await self.bot.mutes.upsert(data)
        self.bot.muted_users[member.id] = data

        await member.add_roles(role)

        if not time:
            await ctx.send(f"Muteado {member.display_name}")
        else:
            minutes, seconds = divmod(time, 60)
            hours, minutes = divmod(minutes, 60)
            if int(hours):
                await ctx.send(
                    f"Muteado {member.display_name} por {hours} horas, {minutes} minutos y {seconds} segundos"
                )
            elif int(minutes):
                await ctx.send(
                    f"Muteado {member.display_name} por {minutes} minutos y {seconds} segundos"
                )
            elif int(seconds):
                await ctx.send(f"Muteado {member.display_name} por {seconds} seconds")

        if time and time < 300:
            await asyncio.sleep(time)

            if role in member.roles:
                await member.remove_roles(role)
                await ctx.send(f"Desmuteado `{member.display_name}`")

            await self.bot.mutes.delete(member.id)
            try:
                self.bot.muted_users.pop(member.id)
            except KeyError:
                pass

    @commands.command(
        name='unmute',
        description="Unmuted a member!",
        usage='<user>'
    )
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="😶 Muteado 😶")
        if not role:
            await ctx.send("No se encontro el rol `😶 Muteado 😶`")
            return

        await self.bot.mutes.delete(member.id)
        try:
            self.bot.muted_users.pop(member.id)
        except KeyError:
            pass

        if role not in member.roles:
            await ctx.send("Este miembro no esta muteado.")
            return

        await member.remove_roles(role)
        await ctx.send(f"Desmuteado `{member.display_name}`")

    @commands.command(
        name="kick",
        description="A command which kicks a given user",
        usage="<user> [reason]",
    )
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.kick(user=member, reason=reason)

        # Using our past episodes knowledge can we make the log channel dynamic?
        embed = discord.Embed(
            title=f"{ctx.author.name} Expulsado: {member.name}", description=reason
        )
        await ctx.send(embed=embed)

    @commands.command(
        name="ban",
        description="A command which bans a given user",
        usage="<user> [reason]",
    )
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):

        await ctx.guild.ban(user=member, reason=reason)

        # Using our past episodes knowledge can we make the log channel dynamic?
        embed = discord.Embed(
            title=f"{ctx.author.name} baneado: {member.name}", description=reason
        )
        await ctx.send(embed=embed)

    @commands.command(
        name="hackban",
        description="Banea un usuario por id (aunque no sea del server)",
        usage="<user> [reason]",
    )
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def hackban(self, ctx, user: discord.User, *, reason=None):
        if user in ctx.guild.members:
            embed = discord.Embed(description=+f"Sin éxito, el usuario está en este servidor.", color=discord.Color.orange())
            await ctx.reply(embed=embed, mention_author=False)

        else:
            await ctx.guild.ban(user)
            await ctx.reply("Se baneo con exito a "+f"**{user}**", mention_author=False)


    @commands.command(
        name="unban",
        description="A command which unbans a given user",
        usage="<user> [reason]",
    )
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx, member, *, reason=None):
        member = await self.bot.fetch_user(int(member))
        await ctx.guild.unban(member, reason=reason)

        embed = discord.Embed(
            title=f"{ctx.author.name} Desbaneado: {member.name}", description=reason
        )
        await ctx.send(embed=embed)

    @commands.command(
        name="purge",
        description="A command which purges the channel it is called in",
        usage="[amount]",
    )
    @commands.guild_only()
    @commands.is_owner()
    async def purge(self, ctx, amount=15):
        await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed(
            title=f"{ctx.author.name} purged: {ctx.channel.name}",
            description=f"{amount} mensajes fueron limpíados",
        )
        await ctx.send(embed=embed, delete_after=15)


def setup(bot):
    bot.add_cog(Moderation(bot))
