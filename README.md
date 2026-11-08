# CLIPMASTER AI — paquete de despliegue

API inicial para cargar videos propios/autorizados, transcribir en español, puntuar ventanas de 30–60 segundos y exportar clips MP4 verticales 9:16 con subtítulos incrustados.

## Qué incluye
- API FastAPI: `GET /`, `POST /process`, `GET /download/{job_id}/{filename}`.
- Transcripción con Faster-Whisper y marcas de tiempo por palabra.
- Detector heurístico de frases impactantes, discusiones, bromas, sorpresas y emoción.
- Render con FFmpeg a 2160×3840 (4K vertical), con subtítulos SRT quemados.
- Dockerfile y `render.yaml` para desplegar en Render.

## Requisitos locales
- Python 3.11+
- FFmpeg instalado y disponible como comando `ffmpeg`.
- Dependencias de `requirements.txt`.

## Ejecutar
```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Abre `http://127.0.0.1:8000/docs` para probar la API.

## Pruebas
```bash
pytest -q
```

## Publicar desde el iPhone
1. Descomprime `CLIPMASTER_AI.zip`.
2. Entra en GitHub y crea un repositorio nuevo llamado `clipmaster-ai`.
3. Usa **Add file → Upload files** y sube el contenido de esta carpeta (no la carpeta ZIP).
4. Guarda los cambios con **Commit changes**.
5. Entra en Render y elige **New + → Web Service**.
6. Conecta GitHub, selecciona `clipmaster-ai` y elige despliegue mediante Docker.
7. Render detectará el `Dockerfile`; pulsa **Deploy Web Service**.
8. Cuando termine, Render mostrará la URL pública.

## Límites importantes
- Este paquete procesa archivos de video cargados por el usuario. No descarga videos de YouTube.
- Usa únicamente videos propios o para los que tengas permiso de uso.
- El detector actual usa reglas y palabras clave; no es un modelo entrenado que entienda contexto, sarcasmo o emociones con fiabilidad.
- El recorte vertical es centrado; no incluye seguimiento automático de rostros.
- 4K significa salida 2160×3840; ampliar un video de menor resolución no recupera detalle original.
- El modelo de voz se descarga al primer uso y puede consumir memoria/CPU. En Render, usa un plan con recursos suficientes.
- Esta es una versión inicial: no incluye cuentas, cola de trabajos, almacenamiento permanente ni eliminación automática de archivos. No es recomendable exponerla públicamente con videos sensibles sin añadir autenticación y límites de carga.
