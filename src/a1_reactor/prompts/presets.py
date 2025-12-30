from __future__ import annotations

PRESETS = {
    "cinematic": "cinematic lighting, shallow depth of field, natural film grain, realistic textures",
    "studio": "soft studio lighting, clean seamless background, sharp details",
    "noir": "noir lighting, high contrast, moody atmosphere, deep shadows",
    "anime": "anime style, clean linework, vibrant colors, consistent character design",
}

NEGATIVE_DEFAULT = "low quality, blurry, watermark, text, artifacts, distorted face, extra limbs"

def apply_preset(prompt: str, preset: str | None) -> tuple[str, str]:
    if not preset:
        return prompt, NEGATIVE_DEFAULT
    addon = PRESETS.get(preset.lower(), "")
    merged = (prompt + ", " + addon).strip(", ").strip()
    return merged, NEGATIVE_DEFAULT
