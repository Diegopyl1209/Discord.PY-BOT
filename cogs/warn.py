import discord
from discord.ext import commands

from utils.util import Pag


class Warns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.guild_only()
    @commands.has_role(713274381693878344)
    async def warn(self, ctx, member: discord.Member, *, reason):
        if member.id in [ctx.author.id, self.bot.user.id]:
            return await ctx.send("No puedes advertirte a ti mimso ni al bot!")
        
        current_warn_count = len(
            await self.bot.warns.find_many_by_custom(
                {
                    "user_id": member.id,
                    "guild_id": member.guild.id
                }
            )
        ) + 1
        
        warn_filter = {"user_id": member.id, "guild_id": member.guild.id, "number": current_warn_count}
        warn_data = {"reason": reason, "timestamp": ctx.message.created_at, "warned_by": ctx.author.id}
        
        await self.bot.warns.upsert_custom(warn_filter, warn_data)
        
        embed = discord.Embed(
            title="Estás siendo advertido:",
            description=f"__**Razon**__:\n{reason}",
            colour=discord.Colour.red(),
            timestamp=ctx.message.created_at
        )
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.set_footer(text=f"Warn: {current_warn_count}")
        
        try:
            await member.send(embed=embed)
            await ctx.send("Adverti a este usuario en DM por ti .")
        except discord.HTTPException:
            await ctx.send(member.mention, embed=embed)
            
    @commands.command()
    @commands.guild_only()
    @commands.has_role(713274381693878344)
    async def warns(self, ctx, member: discord.Member):
        warn_filter = {"user_id": member.id, "guild_id": member.guild.id}
        warns = await self.bot.warns.find_many_by_custom(warn_filter)
        
        if not bool(warns):
            return await ctx.send(f"No se pudo encontrar ninguna advertencia para: `{member.display_name}`")
        
        warns = sorted(warns, key=lambda x: x["number"])
        
        pages = []
        for warn in warns:
            description = f"""
            Warn Numero: `{warn['number']}`
            Warn Razon: `{warn['reason']}`
            Advertido Por: <@{warn['warned_by']}>
            Fecha de la Advertencia: {warn['timestamp'].strftime("%I:%M %p %B %d, %Y")}
            """
            pages.append(description)
        
        await Pag(
            title=f"Warns de `{member.display_name}`",
            colour=0xCE2029,
            entries=pages,
            length=1
        ).start(ctx)

    @commands.command(aliases=["delwarn", "dw"])
    @commands.has_role(713274381693878344)
    @commands.guild_only()
    async def deletewarn(self, ctx, member: discord.Member, warn: int = None):
        """Eliminar una advertencia / todas las advertencias de un miembro determinado"""
        filter_dict = {"user_id": member.id, "guild_id": member.guild.id}
        if warn:
            filter_dict["number"] = warn

        was_deleted = await self.bot.warns.delete_by_custom(filter_dict)
        if was_deleted and was_deleted.acknowledged:
            if warn:
                return await ctx.send(
                    f"Eliminé la advertencia numero `{warn}` de `{member.display_name}`"
                )

            return await ctx.send(
                f"Elimine `{was_deleted.deleted_count}` advertencias de `{member.display_name}`"
            )

        await ctx.send(
            f"No pude encontrar ninguna advertencia de  `{member.display_name}` que concuerde con el numero introducido"
        )


def setup(bot):
    bot.add_cog(Warns(bot))
