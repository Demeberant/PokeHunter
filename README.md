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

No subas el token de Discord al repositorio.
