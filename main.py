from pathlib import Path
from uuid import uuid4
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from .config import UPLOAD_DIR, OUTPUT_DIR
from .processor import process_video

app = FastAPI(title="CLIPMASTER AI", version="0.2.0",
              description="Detecta momentos destacados y crea clips verticales con subtítulos en español.")
ALLOWED = {".mp4", ".mov", ".mkv", ".webm"}

@app.get("/")
def home():
    return {"app": "CLIPMASTER AI", "status": "online", "message": "Sube un video para detectar momentos de 30 a 60 segundos."}

@app.post("/process")
async def process(file: UploadFile = File(...)):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED:
        raise HTTPException(400, "Formato no admitido. Usa MP4, MOV, MKV o WEBM.")
    job = uuid4().hex
    source = UPLOAD_DIR / f"{job}{suffix}"
    out_dir = OUTPUT_DIR / job
    out_dir.mkdir(parents=True, exist_ok=True)
    source.write_bytes(await file.read())
    try:
        clips = process_video(source, out_dir)
    except FileNotFoundError as exc:
        raise HTTPException(500, "No se encontró FFmpeg. Debe instalarse en el servidor.") from exc
    except Exception as exc:
        raise HTTPException(500, f"No se pudo procesar el video: {exc}") from exc
    return {"job_id": job, "clips": clips, "message": "Proceso terminado"}

@app.get("/download/{job_id}/{filename}")
def download(job_id: str, filename: str):
    if "/" in filename or "\\" in filename or ".." in filename:
        raise HTTPException(400, "Nombre de archivo no válido")
    path = OUTPUT_DIR / job_id / filename
    if not path.is_file() or path.suffix.lower() != ".mp4":
        raise HTTPException(404, "Clip no encontrado")
    return FileResponse(path, media_type="video/mp4", filename=filename)
