# PokeHunter

Bot de Discord para consultar y recibir alertas desde un feed JSON de coordenadas autorizado/público.

## Comandos
- `/buscar pokemon:Slaking iv:100 size:XXL`
- `/hundo pokemon:Slaking`
- `/alerta pokemon:Slaking iv:100 size:XXL`
- `/alertas`
- `/borrar_alerta id:1`
- `/estado`

## Configuración
1. Python 3.12+
2. `pip install -r requirements.txt`
3. Copia `.env.example` a `.env`.
4. Define `DISCORD_TOKEN` y un `POKEMON_FEED_URL` autorizado/público.
5. Ejecuta `python -m src.main`.

## Despliegue en Railway
1. Crea un proyecto desde este repositorio.
2. Configura `DISCORD_TOKEN`, `DISCORD_GUILD_ID` y `POKEMON_FEED_URL` como variables.
3. Railway construirá la imagen con `Dockerfile` y ejecutará el bot como servicio worker.

No subas el token de Discord al repositorio.
