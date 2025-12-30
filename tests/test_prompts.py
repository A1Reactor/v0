from a1_reactor.prompts.normalize import normalize_prompt
from a1_reactor.prompts.presets import apply_preset

def test_normalize_prompt():
    assert normalize_prompt("  hello   world ") == "hello world"

def test_apply_preset():
    p, neg = apply_preset("shot", "cinematic")
    assert "cinematic" in p
    assert "watermark" in neg
