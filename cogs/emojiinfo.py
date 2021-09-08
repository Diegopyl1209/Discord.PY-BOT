import discord
from discord.ext import commands


class EmojiInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name="emojiinfo", aliases=["ei"])
    async def emoji_info(self, ctx, emoji: discord.Emoji = None):
        if not emoji:
            return await ctx.invoke(self.bot.get_command("help"), entity="emojiinfo")

        try:
            emoji = await emoji.guild.fetch_emoji(emoji.id)
        except discord.NotFound:
            return await ctx.send("I could not find this emoji in the given guild.")

        is_managed = "Yes" if emoji.managed else "No"
        is_animated = "Yes" if emoji.animated else "No"
        requires_colons = "Yes" if emoji.require_colons else "No"
        creation_time = emoji.created_at.strftime("%I:%M %p %B %d, %Y")
        can_use_emoji = (
            "Everyone"
            if not emoji.roles
            else " ".join(role.name for role in emoji.roles)
        )

        description = f"""
        **General:**
        **- Nombre:** {emoji.name}
        **- Id:** {emoji.id}
        **- URL:** [Link To Emoji]({emoji.url})
        **- Autor:** {emoji.user.mention}
        **- Fecha de creacion:** {creation_time}
        **- Usable por:** {can_use_emoji}
        
        **Other:**
        **- Animado:** {is_animated}
        **- Managed:** {is_managed}
        **- Requiere dos puntos:** {requires_colons}
        **- Nombre servidor:** {emoji.guild.name}
        **- Id servidor:** {emoji.guild.id}
        """

        embed = discord.Embed(
            title=f"**Informacion del Emoji:** `{emoji.name}`",
            description=description,
            colour=0xADD8E6,
        )
        embed.set_thumbnail(url=emoji.url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(EmojiInfo(bot))