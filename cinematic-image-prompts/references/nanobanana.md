# Nano Banana Pro Reference

## Technical Specs

| Parameter | Value |
|-----------|-------|
| Official Name | Gemini 3 Pro Image |
| API Model ID | `gemini-3-pro-image-preview` |
| Fast Model | `gemini-2.5-flash-image` |
| Max Resolution | 4K (16 megapixels) |
| Reference Images | Up to 14 simultaneous |
| Face Tracking | 5 distinct characters |
| Object References | 6 high-fidelity objects |
| Generation Speed | Under 10 seconds |

## Resolution Tiers

| Tier | Resolution | Use Case |
|------|------------|----------|
| 1K | Standard | Quick iteration |
| 2K | High Definition | Production quality |
| 4K | Ultra HD (16MP) | Hero shots, print |

## Aspect Ratios Supported

- 1:1 (square)
- 2:3 / 3:2
- 3:4 / 4:3
- 4:5 / 5:4
- 9:16 / 16:9 (vertical/horizontal video)
- 21:9 (ultrawide cinematic)

## Pricing

| Access | Cost |
|--------|------|
| Free (Gemini app) | ~3 images/day, 1MP, watermarked |
| Google AI Plus | $9.99/mo, limited Pro |
| Google AI Pro | $19.99/mo, 2K access |
| Google AI Ultra | $34.99/mo, full 4K |
| API Standard | $0.134/image |
| API 4K | $0.24/image |
| Third-party (Kie.ai) | $0.02-0.12/image |

## Critical Constraints

### NO Negative Prompts
Nano Banana Pro does NOT support negative prompt fields. Use **positive/semantic framing**:
- ❌ "no blur" → ✅ "sharp focus throughout"
- ❌ "no people" → ✅ "empty road, desolate sidewalk"
- ❌ "bad hands" → ✅ "natural hand positions, correct finger count"

### No Temperature Slider
Control creativity through prompt specificity. More detail = more controlled output.

### Text Rendering Limitations
- 1-3 words: ~75% accuracy
- 4-8 words: ~40% accuracy
- 9+ words: ~15% accuracy
- **Best practice**: Generate without text, add in post-production

### Character Drift
Features may drift after 4+ generations. Re-anchor by re-uploading reference image.

## What Works Well

✅ Natural language prompts (like Creative Director brief)
✅ Reference images for character consistency (14 max)
✅ Multi-character scenes with face tracking
✅ Physics-aware composition
✅ Iterative conversational editing
✅ Camera/lens specs (85mm f/1.8, etc.)
✅ Film stock references
✅ Cinematographer style references (Deakins, Fincher)

## Reference Image Best Practices

### Character Consistency ("Identity Locking")

1. **Create DNA reference**: Side-by-side image with close-up face (left) + full body (right)
2. **Key phrase**: "featuring the same character shown in the reference image"
3. **Re-anchor every 3-4 generations** by re-uploading reference

### Multi-Character Scenes

Upload multiple references, explicitly identify each:
```
"Character A from first reference (warrior with copper hair) faces 
Character B from second reference (merchant with grey beard)."
```

### Reference Types

- Face/identity references
- Style guide references
- Pose references
- Brand/logo references
- Environment references

## Prompt Structure

**Natural language, not tag soup:**
```
Subject + Action + Environment + Art Style + Lighting + Technical Details
```

**ICS Framework:**
- **I**mage type (portrait, product shot, diagram)
- **C**ontent (subject, action, context)
- **S**tyle (aesthetic, mood, technical)

## Prompt Template — Creator Shot (with Reference)

```
[NANO BANANA PRO — CREATOR SHOT]

Create a photorealistic cinematic [shot type] featuring the same character 
shown in the reference image.

Face Consistency: Keep facial features exactly matching the reference.

Expression: [emotion — specific, detailed]
Action/Pose: [description]
Wardrobe: [specific clothing, colors, textures]

Camera: [shot size], [lens]mm f/[aperture], [angle]
Composition: [rule of thirds / centered]

Lighting: [pattern] lighting, [ratio] ratio
Key light from [direction], [hard/soft] quality, [Kelvin]K color temperature.
[Fill, rim, practical lights as needed]

Color Grade: [film stock or grading style]
Atmosphere: [haze/particles/clean]

Environment: [setting description]
Background: [depth, blur level, elements]

Style: Cinematic photorealistic, natural skin texture with visible pores,
Hollywood production value. [Cinematographer reference if applicable]

Technical: [Aspect ratio], [resolution tier], sharp focus.
Natural hand positions if visible.
```

## Prompt Template — Creator Shot (Text-Only, No Reference)

```
[NANO BANANA PRO — CREATOR (TEXT BIBLE)]

Create a photorealistic cinematic [shot type] of:

[FULL CHARACTER BIBLE]:
A [age]-year-old [ethnicity] [gender] with [hair]. [Face shape], 
[skin tone] with natural texture and visible pores. [Eye color] eyes
[eye details]. [Distinctive features]. [Expression type].

Wardrobe: [specific clothing]
Action/Pose: [description]

[Continue with Camera, Lighting, Color, Environment, Style, Technical 
as above]
```

## Prompt Template — B-Roll

```
[NANO BANANA PRO — B-ROLL]

Create a photorealistic cinematic [shot type] of [subject/scene].

[Detailed scene description — focus on visual storytelling]

Camera: [shot size], [lens]mm, [angle]
Movement suggestion: [static / implied pan / etc.]

Lighting: [natural/artificial], [time of day], [quality]
Atmosphere: [volumetric haze / dust particles / fog / clean]

Color: [film stock], [grade style]
Mood: [emotional tone]

Technical: [Aspect ratio], [resolution], sharp focus throughout.
```

## Prompt Template — Thumbnail

```
[NANO BANANA PRO — THUMBNAIL]

Create a high-impact thumbnail composition featuring the same character
from the reference image:

PRIMARY SUBJECT (50-60% of frame):
Character with [EXAGGERATED expression] creating curiosity gap —
wide eyes, raised eyebrows, [specific mouth position], energy that says
"you need to see this."
Position: [left/right/center], facing [direction]

TOPIC VISUAL:
[Description of topic element] positioned [spatial relationship to character].
Color contrast: [warm character vs cool topic / etc.]

Camera: Tight close-up, 85mm f/1.8
Angle: Eye-level with slight dutch tilt (5-10°) for dynamic energy

Lighting: High-contrast dramatic, Rembrandt or split, 4:1+ ratio
Warm key on face (3200K), contrasting topic element

Color: HIGH SATURATION, vibrant teal-orange grade
Maximum contrast for small-screen visibility

Composition: Character dominant [side], topic [opposite side]
TEXT SAFE ZONE: Keep [top/bottom 20%] clear for title overlay

Technical: 9:16 vertical, 2K+ resolution, punchy and readable at 100×100px.
```

## Iterative Editing

Nano Banana Pro excels at conversational refinement:

1. Generate base image
2. Request specific changes: "Make the lighting warmer" / "Shift expression to more confident"
3. Model maintains context and applies edits
4. Re-anchor character reference if drift occurs

**Best practice**: Change ONE variable at a time to isolate improvements.

## Cinematographer Style References

| Reference | Style | Use Case |
|-----------|-------|----------|
| "Roger Deakins style" | Naturalistic, motivated sources, atmospheric | Drama, sci-fi |
| "Fincher style" | Desaturated, green tint, high contrast | Thriller, tension |
| "Wes Anderson style" | Pastel, symmetrical, whimsical | Stylized, quirky |
| "Lubezki style" | Natural light, ethereal, long takes | Poetic, immersive |
| "Blade Runner 2049 look" | Desaturated, orange-teal, volumetric | Sci-fi, dystopian |
