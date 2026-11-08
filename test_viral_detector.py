from app.viral_detector import score_text, detect_moments

def test_impactful_text_scores():
    assert score_text("¡No puede ser! Esto es increíble, nadie lo esperaba") > 0.2

def test_empty_segments():
    assert detect_moments([]) == []

def test_detects_30_to_60_second_window():
    segments = [
        {"start": i * 5, "end": i * 5 + 5, "text": "¡No puede ser! Esto es increíble, una sorpresa"}
        for i in range(8)
    ]
    found = detect_moments(segments, threshold=0.2)
    assert found
    assert all(30 <= x.end - x.start <= 60 for x in found)
