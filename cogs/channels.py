import random

import discord
from discord.ext import commands


class Channels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def our_custom_check():
        async def predicate(ctx):
            return ctx.guild is not None \
                and ctx.author.guild_permissions.manage_channels \
                and ctx.me.guild_permissions.manage_channels
        return commands.check(predicate)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(
        name="channelstats",
        aliases=["cs"],
        description="Sends a nice fancy embed with some channel stats",
    )
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def channelstats(self, ctx):
        channel = ctx.channel

        embed = discord.Embed(
            title=f"Stats de **{channel.name}**",
            description=f"{'Categoria: {}'.format(channel.category.name) if channel.category else 'Este canal no está en una categoría.'}",
            color=random.choice(self.bot.color_list),
        )
        embed.add_field(name="Servidor del canal", value=ctx.guild.name, inline=False)
        embed.add_field(name="Id del canal", value=channel.id, inline=False)
        embed.add_field(
            name="Topico del canal",
            value=f"{channel.topic if channel.topic else 'No topic.'}",
            inline=False,
        )
        embed.add_field(name="Posición del canal", value=channel.position, inline=False)
        embed.add_field(
            name="Retardo del modo lento", value=channel.slowmode_delay, inline=False
        )
        embed.add_field(name="Canal es nsfw?", value=channel.is_nsfw(), inline=False)
        embed.add_field(name="Canal es de anuncios?", value=channel.is_news(), inline=False)
        embed.add_field(
            name="Fecha de creación del canal", value=channel.created_at, inline=False
        )
        embed.add_field(
            name="Permisos de canal sincronizados",
            value=channel.permissions_synced,
            inline=False,
        )
        embed.add_field(name="Hash de canal", value=hash(channel), inline=False)

        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    @our_custom_check()
    async def new(self, ctx):
        await ctx.send("Sub-comando invalido.")

    @new.command(
        name="category",
        description="Create a new category",
        usage="<role> <Category name>",
    )
    @our_custom_check()
    async def category(self, ctx, role: discord.Role, *, name):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True),
        }
        category = await ctx.guild.create_category(name=name, overwrites=overwrites)
        await ctx.send(f"Hey! cree la categoria {category.name} por ti!")

    @new.command(
        name="channel",
        description="Create a new channel",
        usage="<role> <channel name>",
    )
    @our_custom_check()
    async def channel(self, ctx, role: discord.Role, *, name):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True),
        }
        channel = await ctx.guild.create_text_channel(
            name=name,
            overwrites=overwrites,
            category=self.bot.get_channel(707945693582590005),
        )
        await ctx.send(f"Hey! cree el canal {channel.name} por ti!")

    @commands.group(invoke_without_command=True)
    @our_custom_check()
    async def delete(self, ctx):
        await ctx.send("Invalid sub-command passed")

    @delete.command(
        name="category", description="Delete a category", usage="<category> [reason]"
    )
    @our_custom_check()
    async def _category(self, ctx, category: discord.CategoryChannel, *, reason=None):
        await category.delete(reason=reason)
        await ctx.send(f"hey! Elimine {category.name} por ti")

    @delete.command(
        name="channel", description="Delete a channel", usage="<channel> [reason]"
    )
    @our_custom_check()
    async def _channel(self, ctx, channel: discord.TextChannel = None, *, reason=None):
        channel = channel or ctx.channel
        await channel.delete(reason=reason)
        await ctx.send(f"hey! Elimine {channel.name} por ti")


def setup(bot):
    bot.add_cog(Channels(bot))
