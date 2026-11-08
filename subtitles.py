def srt_timestamp(seconds: float) -> str:
    ms = max(0, int(round(seconds * 1000)))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def write_srt(words, output_path, max_words=5):
    lines = []
    chunks, current = [], []
    for word in words:
        current.append(word)
        if len(current) >= max_words or str(word.get("word", "")).endswith((".", "!", "?", ",")):
            chunks.append(current)
            current = []
    if current:
        chunks.append(current)
    for idx, chunk in enumerate(chunks, 1):
        start = float(chunk[0]["start"])
        end = float(chunk[-1]["end"])
        text = "".join(str(w.get("word", "")) for w in chunk).strip()
        lines.extend([str(idx), f"{srt_timestamp(start)} --> {srt_timestamp(end)}", text, ""])
    output_path.write_text("\n".join(lines), encoding="utf-8")
