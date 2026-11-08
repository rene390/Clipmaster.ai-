import subprocess
from pathlib import Path
from faster_whisper import WhisperModel
from .config import MODEL_SIZE
from .viral_detector import detect_moments

_model = None

def get_model():
    global _model
    if _model is None:
        _model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
    return _model

def transcribe(path: Path):
    model = get_model()
    segments, _ = model.transcribe(str(path), language="es", word_timestamps=True, vad_filter=True)
    rows, words = [], []
    for seg in segments:
        rows.append({"start": seg.start, "end": seg.end, "text": seg.text})
        if seg.words:
            for w in seg.words:
                words.append({"start": w.start, "end": w.end, "word": w.word})
    return rows, words

def render_clip(source: Path, start: float, end: float, srt: Path, output: Path):
    # FFmpeg must be installed in the deployment environment.
    vf = "scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,setsar=1,subtitles=" + str(srt).replace(":", "\\:")
    cmd = ["ffmpeg", "-y", "-ss", str(start), "-i", str(source), "-t", str(end-start),
           "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(output)]
    subprocess.run(cmd, check=True, capture_output=True)
    return output

def process_video(path: Path, output_dir: Path):
    rows, words = transcribe(path)
    moments = detect_moments(rows)
    results = []
    for idx, moment in enumerate(moments, 1):
        clip_words = [w for w in words if w["end"] >= moment.start and w["start"] <= moment.end]
        adjusted = [{"start": max(0, w["start"]-moment.start), "end": max(0, w["end"]-moment.start), "word": w["word"]} for w in clip_words]
        srt = output_dir / f"clip_{idx:02}.srt"
        write_srt(adjusted, srt)
        output = output_dir / f"clip_{idx:02}.mp4"
        render_clip(path, moment.start, moment.end, srt, output)
        results.append({"start": moment.start, "end": moment.end, "score": moment.score, "file": output.name})
    return results
