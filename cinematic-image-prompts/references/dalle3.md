# DALL-E 3 Reference

## Technical Specs

| Parameter | Value |
|-----------|-------|
| Model ID | `dall-e-3` |
| Quality | `standard` or `hd` (always use `hd` for video production) |
| Style | `vivid` (cinematic) or `natural` (realistic) |
| Max Prompt | 4,000 characters |
| Images per call | 1 only (n=1 enforced) |

## Resolution Options

| Size | Aspect | Price (Standard) | Price (HD) |
|------|--------|------------------|------------|
| 1024×1024 | 1:1 | $0.04 | $0.08 |
| 1792×1024 | ~16:9 landscape | $0.08 | $0.12 |
| 1024×1792 | ~9:16 portrait | $0.08 | $0.12 |

**For vertical video (9:16)**: Use `1024×1792`

## Critical Constraints

### No Reference Image Support
DALL-E 3 API has NO image input. Character consistency relies on **exact text description repetition**.

### Negative Prompts Don't Work
DALL-E 3 ignores exclusions. Use positive framing:
- ❌ "no blur" → ✅ "crystal-clear sharp focus"
- ❌ "no people" → ✅ "empty, desolate scene"
- ❌ "no text" → ✅ "clean frame without overlays"

### Automatic Prompt Rewriting
GPT-4 rewrites all prompts before generation. To minimize changes:
```
"My prompt has full detail so no need to add more: [your exact prompt]"
```

### Response URL Expires
URLs expire in 60 minutes. Use `response_format: "b64_json"` for production.

## What Works Well

✅ Camera/lens specifications (85mm f/1.8, 50mm f/2.8)
✅ Film stock references (Kodak Vision3 500T, Portra 400)
✅ Lighting terminology (Rembrandt, butterfly, split)
✅ "Photo of" or "photograph of" (better than "photorealistic")
✅ Text rendering (best-in-class among AI models)

## What Doesn't Work

❌ "8K", "ultra-HD" (minimal impact)
❌ Negative prompts
❌ Reference images
❌ Consistent characters across generations (without text repetition)

## Prompt Template — Creator Shot

```
[DALL-E 3 — CREATOR SHOT]

A photorealistic cinematic [shot type] of [CHARACTER BIBLE - exact description].

Expression: [emotion keywords]
Pose/Action: [description]
Wardrobe: [specific clothing]

Camera: [shot size], [lens]mm f/[aperture], [angle]
Composition: [rule of thirds / centered / etc.]

Lighting: [pattern] lighting, [ratio] ratio, [Kelvin]K
Key from [direction], [hard/soft] quality.

Color: [film stock], [grade style]
Atmosphere: [haze/clean/particles]

Environment: [setting]
Background: [depth, blur, elements]

Style: Shot on [camera/film], cinematic photorealistic, natural skin texture,
Hollywood production value.

Technical: [Size: 1024×1792 for portrait], HD quality, vivid style.
Clean frame, sharp focus, no text overlays, no watermarks.
```

## Prompt Template — B-Roll

```
[DALL-E 3 — B-ROLL]

A photorealistic cinematic [shot type] of [subject/scene].
[Focus on topic visuals — NO human face unless specified]

Camera: [shot size], [lens]mm f/[aperture], [angle]
Composition: [rule]

Lighting: [pattern/setup], [Kelvin]K
Atmosphere: [type]

Color: [film stock], [grade]
Environment: [full description]

Style: Cinematic, Hollywood production value.

Technical: [Size], HD quality.
Clean frame, sharp focus, no text overlays.
```

## Prompt Template — Thumbnail

```
[DALL-E 3 — THUMBNAIL]

A photorealistic cinematic thumbnail composition:

PRIMARY (50-60% of frame):
[CHARACTER BIBLE] with [EXAGGERATED expression] —
wide eyes, raised brows, [mouth position], curiosity-gap energy.
Position: [left/right/center], [angle to camera].

SECONDARY:
[TOPIC VISUAL] in [background/side position].
Visual relationship: [spatial description]

Camera: Tight close-up, 85mm f/1.8
Angle: Eye-level, slight dutch tilt (5-10°)

Lighting: High-contrast dramatic, 4:1+ ratio
Temperature: Warm face (3200K), cool topic contrast

Color: HIGH SATURATION, teal-orange grade, Kodak Vision3 500T

Composition: Creator dominant, topic opposite side
TEXT ZONES: Reserve [area] for title — keep clear of face

Technical: 1024×1792 portrait, HD quality, vivid style.
Clean, no text rendered.
```

## API Call Example

```python
response = client.images.generate(
    model="dall-e-3",
    prompt="[your prompt]",
    size="1024x1792",  # portrait
    quality="hd",
    style="vivid",
    response_format="b64_json"  # for production
)
```
