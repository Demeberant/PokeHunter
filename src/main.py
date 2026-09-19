import discord
from discord import app_commands
from discord.ext import commands, tasks
from .config import load_settings
from .providers.http_json import HttpJsonProvider
from .store import AlertStore

settings = load_settings()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
provider = HttpJsonProvider(settings.feed_url, settings.timeout_seconds)
alerts = AlertStore()
seen: set[str] = set()

def matches(s, pokemon, iv=None, size=None):
    if s.pokemon.casefold() != pokemon.casefold():
        return False
    if iv is not None and (s.iv is None or s.iv != iv):
        return False
    if size and (s.size or "").upper() != size.upper():
        return False
    return True

def render(s):
    attrs = []
    if s.iv is not None: attrs.append(f"IV {s.iv:g}")
    if s.level is not None: attrs.append(f"L{s.level:g}")
    if s.cp is not None: attrs.append(f"CP {s.cp}")
    if s.size: attrs.append(s.size)
    return f"**{s.pokemon}** — {' · '.join(attrs) or 'datos básicos'}\n`{s.latitude:.6f},{s.longitude:.6f}`"

async def fetch_matches(pokemon, iv=None, size=None):
    rows = await provider.fetch()
    return [s for s in rows if matches(s, pokemon, iv, size)]

@bot.event
async def on_ready():
    if settings.guild_id:
        guild = discord.Object(id=settings.guild_id)
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
    else:
        await bot.tree.sync()
    if not alert_loop.is_running():
        alert_loop.start()
    print(f"Ready: {bot.user}")

@bot.tree.command(name="buscar", description="Busca coordenadas en el feed configurado")
@app_commands.describe(pokemon="Nombre, ej. Slaking", iv="IV exacto", size="Tamaño, ej. XXL")
async def buscar(interaction: discord.Interaction, pokemon: str, iv: float | None = None, size: str | None = None):
    await interaction.response.defer(ephemeral=True)
    try:
        found = (await fetch_matches(pokemon, iv, size))[:10]
    except Exception as e:
        await interaction.followup.send(f"Feed no disponible: {type(e).__name__}", ephemeral=True)
        return
    await interaction.followup.send("\n\n".join(map(render, found)) if found else "Sin coincidencias activas.", ephemeral=True)

@bot.tree.command(name="hundo", description="Busca IV100 de un Pokémon")
async def hundo(interaction: discord.Interaction, pokemon: str):
    await interaction.response.defer(ephemeral=True)
    try:
        found = (await fetch_matches(pokemon, 100, None))[:10]
    except Exception as e:
        await interaction.followup.send(f"Feed no disponible: {type(e).__name__}", ephemeral=True)
        return
    await interaction.followup.send("\n\n".join(map(render, found)) if found else "Sin hundos activos.", ephemeral=True)

@bot.tree.command(name="alerta", description="Crea una alerta")
async def alerta(interaction: discord.Interaction, pokemon: str, iv: float | None = None, size: str | None = None):
    a = alerts.add({"user_id": interaction.user.id, "channel_id": interaction.channel_id, "pokemon": pokemon, "iv": iv, "size": size})
    await interaction.response.send_message(f"Alerta #{a['id']} creada para {pokemon}.", ephemeral=True)

@bot.tree.command(name="alertas", description="Muestra tus alertas")
async def listar(interaction: discord.Interaction):
    mine = [x for x in alerts.items if x["user_id"] == interaction.user.id]
    msg = "\n".join(f"#{x['id']} {x['pokemon']} IV={x.get('iv') or '*'} size={x.get('size') or '*'}" for x in mine)
    await interaction.response.send_message(msg or "No tienes alertas.", ephemeral=True)

@bot.tree.command(name="borrar_alerta", description="Elimina una alerta")
async def borrar(interaction: discord.Interaction, id: int):
    ok = alerts.remove(id, interaction.user.id)
    await interaction.response.send_message("Alerta eliminada." if ok else "No encontré esa alerta.", ephemeral=True)

@bot.tree.command(name="estado", description="Comprueba el estado de PokeHunter")
async def estado(interaction: discord.Interaction):
    msg = "PokeHunter online. Feed configurado." if settings.feed_url else "PokeHunter online. Falta configurar POKEMON_FEED_URL."
    await interaction.response.send_message(msg, ephemeral=True)

@tasks.loop(seconds=settings.poll_seconds)
async def alert_loop():
    try:
        rows = await provider.fetch()
    except Exception:
        return
    for a in list(alerts.items):
        for s in rows:
            key = f"{a['id']}:{s.id}"
            if key in seen or not matches(s, a["pokemon"], a.get("iv"), a.get("size")):
                continue
            seen.add(key)
            try:
                channel = bot.get_channel(a["channel_id"]) or await bot.fetch_channel(a["channel_id"])
                await channel.send(f"<@{a['user_id']}> 🔔 {render(s)}")
            except discord.DiscordException:
                pass
    if len(seen) > 10000:
        seen.clear()

@alert_loop.before_loop
async def before_alerts():
    await bot.wait_until_ready()

bot.run(settings.token)
