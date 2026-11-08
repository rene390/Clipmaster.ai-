from dataclasses import dataclass
from typing import Iterable

@dataclass
class Segment:
    start: float
    end: float
    text: str
    score: float

KEYWORDS = {
    "impact": ["increíble", "no puede ser", "jamás", "nunca", "por primera vez", "secreto", "verdad"],
    "conflict": ["mentira", "estás loco", "cállate", "discutir", "problema", "traición", "engaño"],
    "humor": ["jajaja", "ja ja", "😂", "chiste", "broma", "gracioso"],
    "surprise": ["qué", "sorpresa", "no lo esperaba", "de repente", "resulta que"],
    "emotion": ["te amo", "perdóname", "me duele", "no puedo más", "gracias", "familia"],
}

def score_text(text: str) -> float:
    t = text.lower()
    score = min(len(t.split()) / 35.0, 1.0) * 0.25
    for weight, words in [(0.18, KEYWORDS["impact"]), (0.22, KEYWORDS["conflict"]),
                          (0.15, KEYWORDS["humor"]), (0.18, KEYWORDS["surprise"]),
                          (0.12, KEYWORDS["emotion"])]:
        if any(word in t for word in words):
            score += weight
    if "!" in text or "?" in text:
        score += 0.08
    return round(min(score, 1.0), 3)

def detect_moments(segments: Iterable[dict], min_duration=30, max_duration=60, threshold=0.22):
    rows = list(segments)
    if not rows:
        return []
    candidates = []
    for i, first in enumerate(rows):
        start = float(first["start"])
        picked, text_parts, end = [], [], start
        for row in rows[i:]:
            row_start, row_end = float(row["start"]), float(row["end"])
            if row_end - start > max_duration:
                break
            if row_start - start > max_duration:
                break
            picked.append(row)
            text_parts.append(str(row.get("text", "")))
            end = row_end
            duration = end - start
            if min_duration <= duration <= max_duration:
                text = " ".join(text_parts).strip()
                score = score_text(text)
                if score >= threshold:
                    candidates.append(Segment(start, end, text, score))
    candidates.sort(key=lambda x: x.score, reverse=True)
    chosen = []
    for item in candidates:
        if all(item.end <= other.start or item.start >= other.end for other in chosen):
            chosen.append(item)
    return sorted(chosen, key=lambda x: x.start)
