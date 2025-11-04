# Mortalidad Colombia 2019 - Dash

## Configuración
1. Python 3.11+
2. `pip install -r requirements.txt`
3. Coloca los archivos en `/data`.
4. `python app/app.py` y abre `http://localhost:8050`.

## Despliegue en Render
- Nuevo servicio Web -> "Deploy from Git".
- Runtime: Python.
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app.app:server`
- Variable `PORT` gestionada por Render.

## Despliegue en Railway
- Nuevo proyecto -> Deploy GitHub repo.
- Add Variable: `PORT=8000` (Railway suele inyectar, pero explícalo si es necesario).
- Start command: `gunicorn app.app:server --bind 0.0.0.0:$PORT`.

## Google App Engine (opcional)
- `app.yaml`: