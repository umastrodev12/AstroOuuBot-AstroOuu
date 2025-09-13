import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Configurações
mute_automatico = True
moderadores_ids = []  # Adicione IDs de moderadores aqui

# Eventos
@bot.event
async def on_ready():
    activity = discord.Game(name="Powered by DreamsArt Bot | /help")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    try:
        synced = await bot.tree.sync()
        print(f"Sincronizados {len(synced)} comandos de barra.")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")
    print(f'Bot conectado como {bot.user}')


@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.id in moderadores_ids:
        await bot.process_commands(message)
        return

    # Exemplo de mute automático se mencionar bots
    if mute_automatico and any(user.bot for user in message.mentions):
        await message.delete()
        mutado = discord.utils.get(message.guild.roles, name="Mutado")
        if mutado:
            await message.author.add_roles(mutado, reason="Mencionou bot")
            await message.channel.send(f"{message.author.mention} mutado por 5min por mencionar bot.")
            await asyncio.sleep(300)
            await message.author.remove_roles(mutado, reason="Castigo acabou")
            await message.channel.send(f"{message.author.mention} desmutado.")
        return

    await bot.process_commands(message)


# Comandos
@bot.tree.command(name='ping', description='Responde com Pong!')
async def ping(ctx):
    await ctx.response.send_message(f"Pong! Latência: {round(bot.latency*1000)}ms")


@bot.tree.command(name='mute', description='Mute um membro manualmente por 5 minutos')
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member):
    mutado = discord.utils.get(ctx.guild.roles, name="Mutado")
    if mutado:
        await member.add_roles(mutado, reason="Mute manual")
        await ctx.response.send_message(f"{member.mention} foi mutado por 5min")
        await asyncio.sleep(300)
        await member.remove_roles(mutado, reason="Mute expirado")
        await ctx.channel.send(f"{member.mention} desmutado.")
    else:
        await ctx.response.send_message("Cargo 'Mutado' não encontrado.")


@bot.tree.command(name='ban', description='Bane um membro temporariamente')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, tempo: int = 10, motivo: str = "Ban temporário"):
    await member.ban(reason=motivo)
    await ctx.response.send_message(f"{member.mention} banido por {tempo} minutos. Motivo: {motivo}")
    await asyncio.sleep(tempo*60)
    await ctx.guild.unban(member, reason="Ban expirado")
    await ctx.response.send_message(f"{member.mention} foi desbanido automaticamente.")


@bot.tree.command(name='unmute', description='Desmuta um membro manualmente')
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    mutado = discord.utils.get(ctx.guild.roles, name="Mutado")
    if mutado in member.roles:
        await member.remove_roles(mutado, reason="Unmute manual")
        await ctx.response.send_message(f"{member.mention} foi desmutado manualmente.")
    else:
        await ctx.response.send_message(f"{member.mention} não está mutado.")
