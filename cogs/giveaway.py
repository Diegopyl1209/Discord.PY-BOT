import re
import random
import asyncio

import discord
from discord.ext import commands

from utils.util import GetMessage

time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


def convert(argument):
    args = argument.lower()
    matches = re.findall(time_regex, args)
    time = 0
    for key, value in matches:
        try:
            time += time_dict[value] * float(key)
        except KeyError:
            raise commands.BadArgument(
                f"{value} es una clave de tiempo no válida! h|m|s|d son argumentos válidos"
            )
        except ValueError:
            raise commands.BadArgument(f"{key} no es un numero!")
    return round(time)


class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="giveaway",
        description="Crea un sorteo!"
    )
    @commands.guild_only()
    async def giveaway(self, ctx):
        await ctx.send("Comencemos este sorteo, responde las preguntas que hago y procederemos.")

        questionList = [
            ["¿En qué canal debería estar?", "Menciona el canal"],
            ["¿Cuánto tiempo debería durar este sorteo?", "`d|h|m|s`"],
            ["¿Qué estás regalando?", "EJ: Tu Alma.."]
        ]
        answers = {}

        for i, question in enumerate(questionList):
            answer = await GetMessage(self.bot, ctx, question[0], question[1])

            if not answer:
                await ctx.send("No respondiste, responde más rápido la próxima vez.")
                return

            answers[i] = answer

        embed = discord.Embed(name="Giveaway content")
        for key, value in answers.items():
            embed.add_field(name=f"Pregunta: `{questionList[key][0]}`", value=f"Answer: `{value}`", inline=False)

        m = await ctx.send("¿Son todos válidos?", embed=embed)
        await m.add_reaction("✅")
        await m.add_reaction("🇽")

        try:
            reaction, member = await self.bot.wait_for(
                "reaction_add",
                timeout=60,
                check=lambda reaction, user: user == ctx.author
                and reaction.message.channel == ctx.channel
            )
        except asyncio.TimeoutError:
            await ctx.send("Fallo de confirmación. Inténtalo de nuevo.")
            return

        if str(reaction.emoji) not in ["✅", "🇽"] or str(reaction.emoji) == "🇽":
            await ctx.send("Cancelando el sorteo!")
            return

        channelId = re.findall(r"[0-9]+", answers[0])[0]
        channel = self.bot.get_channel(int(channelId))

        time = convert(answers[1])

        giveawayEmbed = discord.Embed(
            title="🎉 __**Giveaway**__ 🎉",
            description=answers[2]
        )
        giveawayEmbed.set_footer(text=f"Este sorteo termina en {time} segundos desde este mensaje.")
        giveawayMessage = await channel.send(embed=giveawayEmbed)
        await giveawayMessage.add_reaction("🎉")

        await asyncio.sleep(time)

        message = await channel.fetch_message(giveawayMessage.id)
        users = await message.reactions[0].users().flatten()
        users.pop(users.index(ctx.guild.me))
        users.pop(users.index(ctx.author))

        if len(users) == 0:
            await channel.send("No se decidió ningún ganador")
            return

        winner = random.choice(users)

        await channel.send(f"**felicitaciones {winner.mention}!**\nPor favor contacta a {ctx.author.mention} para recibir tu premio.")


def setup(bot):
    bot.add_cog(Giveaway(bot))
