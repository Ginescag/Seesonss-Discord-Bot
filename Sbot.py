# Sbot.py
import os
import re
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import time
from testDiscount import create_discount_code  # Importar las funciones necesarias
import threading
import asyncio
from testDiscount import monitor_stock_changes

# Definir el orden de los roles
ROLE_RANKS = {"s'cout": 1, "s'oldier": 2, "s'enior": 3, "s'iso": 4}
DISCOUNT_AMOUNTS = {
    5: 0.4,  # 40% de probabilidad
    10: 0.5,  # 40% de probabilidad
    15: 0.15,  # 15% de probabilidad
    20: 0.05  # 5% de probabilidad
}

probability = 0.01  # Probabilidad inicial de generar un código de descuento
# cooldown_time = 60  # Tiempo de enfriamiento en segundos
# timeout_duration = 3600  # Duración del timeout en segundos (1 hora)
# last_generated = {}  # Diccionario para almacenar el tiempo de la última generación de código por usuario
# spam_attempts = {}  # Diccionario para almacenar los intentos de spam por usuario

# Cargar variables de entorno desde el archivo .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Definir los intents necesarios
intents = discord.Intents.default()
intents.message_content = True  # Necesario para leer el contenido de los mensajes
intents.members = True  # Necesario para recibir eventos de actualización de miembros

# Crear una instancia del bot con un prefijo para los comandos
bot = commands.Bot(command_prefix='!', intents=intents)

def handle_stock_increase(stock_increases):
    text = "@everyone Stock update!\n"
    for item_name, amount in stock_increases:
        text += f'{item_name}: {amount} more available\n'
    asyncio.run_coroutine_threadsafe(send_stock_message(text), bot.loop)

async def send_stock_message(text):
    # Buscar el canal por nombre "flare-raffles"
    channel = discord.utils.get(bot.get_all_channels(), name="flare-raffles")
    if channel:
        await channel.send(text)

# Evento que se ejecuta cuando el bot está listo
@bot.event
async def on_ready():
    print(f'¡Conectado como {bot.user.name} - {bot.user.id}!')
    # Iniciar el monitoreo de stock en otro hilo
    threading.Thread(
        target=monitor_stock_changes,
        args=(20, handle_stock_increase), #CAMBIAR ARGUMENTO DE 20 A 3600
        daemon=True
    ).start()

# Comando simple: !hola
@bot.command(name='hola', help='Responde con un saludo')
async def hola(ctx):
    await ctx.send('¡Hola! ¿Cómo estás?')

# Comando simple: !ping
@bot.command(name='ping', help='Responde con Pong!')
async def ping(ctx):
    await ctx.send('Pong! 🏓')

# Evento para detectar actualización de miembros (como asignación de roles)
@bot.event
async def on_member_update(before, after):
    # Convertir las listas de roles en conjuntos para facilitar la comparación
    before_roles = set(before.roles)
    after_roles = set(after.roles)

    # Identificar roles añadidos y eliminados
    added_roles = after_roles - before_roles
    removed_roles = before_roles - after_roles

    # Filtrar roles que están en ROLE_RANKS
    added_roles_filtered = [
        role for role in added_roles if role.name in ROLE_RANKS
    ]
    removed_roles_filtered = [
        role for role in removed_roles if role.name in ROLE_RANKS
    ]

    # Obtener el rol de menor rango antes de la actualización
    before_relevant_roles = [
        role for role in before.roles if role.name in ROLE_RANKS
    ]
    if before_relevant_roles:
        # Obtener el rol con el mayor rango antes de la actualización
        current_rank_before = max(
            [ROLE_RANKS[role.name] for role in before_relevant_roles])
    else:
        current_rank_before = 0  # No tenía ningún rol relevante

    # Obtener el rol de mayor rango después de la actualización
    after_relevant_roles = [
        role for role in after.roles if role.name in ROLE_RANKS
    ]
    if after_relevant_roles:
        current_rank_after = max(
            [ROLE_RANKS[role.name] for role in after_relevant_roles])
    else:
        current_rank_after = 0  # No tiene ningún rol relevante

    # Verificar si el usuario ha ascendido
    if current_rank_after > current_rank_before:
        # Determinar qué rol ha sido añadido
        # Si antes no tenía ningún rol, determinar el nuevo rol
        if current_rank_before == 0:
            new_roles = [
                role for role in after_relevant_roles
                if ROLE_RANKS[role.name] == current_rank_after
            ]
            if new_roles:
                new_role = new_roles[0]
                mensaje = (
                    f'¡Felicidades {after.mention}! Has recibido el rol **{new_role.name}** en el servidor **{after.guild.name}**.\n'
                    'Has ganado acceso al grupo de WhatsApp exclusivo para compradores <:imagen_20241120_153809765:1308803577250054216>\n'
                    'En este grupo tendrás acceso anticipado antes que nadie, leaks de próximos lanzamientos/eventos, descuentos exclusivos... <:imagen_20241120_154102450:1308804300817956875>\n'
                    'Únete al grupo aquí: https://chat.whatsapp.com/JwGYYnUDKqKGAlyazwiXTJ'
                )
                try:
                    await after.send(mensaje)
                    print(f'Mensaje enviado a {after.name}: {mensaje}')
                except discord.Forbidden:
                    print(
                        f'No pude enviar un DM a {after.name} sobre el nuevo rol.'
                    )
        else:
            # Si tenía un rol antes, determinar el nuevo rol superior
            # Identificar el rol añadido que corresponde al nuevo rango
            possible_new_roles = [
                role for role in added_roles_filtered
                if ROLE_RANKS[role.name] == current_rank_after
            ]
            if possible_new_roles:
                new_role = possible_new_roles[0]
                # Identificar el rol anterior de menor rango
                old_roles = [
                    role for role in before_relevant_roles
                    if ROLE_RANKS[role.name] < current_rank_after
                ]
                if old_roles:
                    old_role_rank = max(
                        [ROLE_RANKS[role.name] for role in old_roles])
                    old_roles_filtered = [
                        role for role in before_relevant_roles
                        if ROLE_RANKS[role.name] == old_role_rank
                    ]
                    if old_roles_filtered:
                        old_role = old_roles_filtered[0]
                        mensaje = f'¡Felicidades {after.mention}! Has ascendido de **{old_role.name}** a **{new_role.name}** en el servidor **{after.guild.name}**.'
                        try:
                            await after.send(mensaje)
                            print(
                                f'Mensaje de ascenso enviado a {after.name}: {mensaje}'
                            )
                        except discord.Forbidden:
                            print(
                                f'No pude enviar un DM a {after.name} sobre el ascenso de rol.'
                            )

# Manejar errores de comandos
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            'Este comando no existe. Usa `!help` para ver los comandos disponibles.'
        )
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('No tienes permisos para usar este comando.')
    else:
        await ctx.send('Ocurrió un error al ejecutar el comando.')
        print(f'Error: {error}')

# Evento para detectar mensajes en los canales "general" y "fitpics" y generar códigos de descuento
@bot.event
async def on_message(message):
    global probability, DISCOUNT_AMOUNTS, last_generated, spam_attempts

    if message.author == bot.user:
        return


    # # Verificar si el usuario está en el periodo de enfriamiento
    # if user_id in last_generated and current_time - last_generated[user_id] < cooldown_time:
    #     await message.channel.send(f'{message.author.mention}, por favor espera antes de intentar generar otro código de descuento.')
    #     return

    # # Verificar si el usuario está en el periodo de timeout
    # if user_id in spam_attempts and current_time - spam_attempts[user_id] < timeout_duration:
    #     return  # No enviar mensaje al canal

    # Verificar si el mensaje se envió en los canales "general", "fitpics" o "aycd"
    if message.channel.name in ["general", "fitpics", "flare-raffles"]:
        # Intentar generar un código de descuento
        if random.random() < probability:
            # Seleccionar el porcentaje de descuento basado en las probabilidades definidas
            discount_percentage = random.choices(
                list(DISCOUNT_AMOUNTS.keys()), weights=list(DISCOUNT_AMOUNTS.values()), k=1
            )[0]
            discount_code = create_discount_code(discount_percentage)
            await message.channel.send(
                f'A wild discount code has spawned **{discount_code}** with {discount_percentage}% off! Fast, claim it before it disappears!'
            )
            # Reiniciar la probabilidad después de generar un código
            probability = 0.01
            # Registrar el tiempo de generación del código
            # last_generated[user_id] = current_time
        else:
            # Incrementar la probabilidad si no se genera un código
            probability += 0.005

    # Verificar si el mensaje se envió en el canal "bot" y sigue el formato especificado
    if message.channel.name == "bot":
        match = re.match(r"Enhorabuena @(\w+), has alcanzado el nivel (\d+)!", message.content)
        if match:
            username = match.group(1)
            level = int(match.group(2))
            if level == 5:
                discount_code = create_discount_code(10)
                user = discord.utils.get(message.guild.members, name=username)
                if user:
                    try:
                        await user.send(
                            f'¡Felicidades {user.name}! Has alcanzado el nivel 5 y has ganado un código de descuento del 10%: **{discount_code}**'
                        )
                    except discord.Forbidden:
                        await message.channel.send(f'No pude enviar un DM a {user.mention} sobre el código de descuento.')
            elif level == 10:
                discount_code = create_discount_code(20)
                user = discord.utils.get(message.guild.members, name=username)
                if user:
                    try:
                        await user.send(
                            f'¡Felicidades {user.name}! Has alcanzado el nivel 10 y has ganado un código de descuento del 20%: **{discount_code}**'
                        )
                    except discord.Forbidden:
                        await message.channel.send(f'No pude enviar un DM a {user.mention} sobre el código de descuento.')
    
    await bot.process_commands(message)

# Ejecutar el bot
bot.run(TOKEN)