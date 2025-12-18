---
name: cinematic-image-prompts
description: Generate Hollywood-grade cinematic image prompts for DALL-E 3 and Nano Banana Pro. Use when creating photorealistic, cinematic, film-style image prompts for AI video production, talking head shots, B-roll, thumbnails, or any visual content requiring professional cinematography (lighting, lens specs, film stocks, color grading). Triggers include requests like "buat image prompt cinematic", "create hook shot image", "generate thumbnail prompt", "DALL-E prompt for...", "Nano Banana prompt for...".
---

# Cinematic Image Prompts

Generate Hollywood-grade image prompts for DALL-E 3 and Nano Banana Pro with professional cinematography.

## Platform Selection

```
DALL-E 3 when:
├─ Need API integration (automated pipelines)
├─ Text must appear in image (signage, labels)
├─ Fixed aspect ratios acceptable (1024×1024, 1792×1024, 1024×1792)
├─ Enterprise/commercial clarity required
└─ ChatGPT workflow integration

Nano Banana Pro when:
├─ Need 4K resolution (up to 16MP)
├─ Reference images for character consistency (up to 14 refs)
├─ Flexible aspect ratios (including 21:9 ultrawide)
├─ Iterative conversational editing
├─ Multi-character scenes with face tracking (5 faces)
└─ Physics-aware composition needed
```

## Core Prompt Formula

```
[Subject/Action] + [Shot Type] + [Lens/Camera] + [Lighting] + [Color/Film Stock] + [Atmosphere] + [Technical Specs]
```

## Workflow

1. **Identify shot type**: Hook, Explanation, B-roll, CTA, Thumbnail
2. **Select platform** based on requirements above
3. **Gather references** if creator/character shot (request photo from user)
4. **Lookup cinematography** from `references/cinematography.md`
5. **Apply platform template** from `references/dalle3.md` or `references/nanobanana.md`
6. **Verify checklist** before output

## Shot Type → Default Setup

| Shot Type | Shot Size | Lens | Lighting | Emotion |
|-----------|-----------|------|----------|---------|
| Hook | CU/MCU | 85mm f/1.8 | Rembrandt 4:1 | Intrigue, authority |
| Explanation | MCU/MS | 50mm f/2.8 | Loop 2:1 | Engaged, approachable |
| CTA | CU | 85mm f/2 | Butterfly 2:1 | Warm, inviting |
| B-roll Product | Detail | 50-100mm | Soft studio | Premium |
| B-roll Environment | WS/EWS | 24-35mm | Natural/available | Atmospheric |
| Thumbnail | CU tight | 85mm f/1.8 | High contrast 4:1+ | Exaggerated curiosity |

## Quick Reference Files

| Need | File |
|------|------|
| DALL-E 3 specs, constraints, templates | `references/dalle3.md` |
| Nano Banana Pro specs, constraints, templates | `references/nanobanana.md` |
| Lighting, lens, film stock, emotion mapping | `references/cinematography.md` |

## Creator Shot Requirements

When generating prompts for a specific person/creator:

1. **Request reference image** from user if not provided
2. **Build Character Bible** with exact physical traits:
   - Ethnicity, age, gender
   - Face shape, skin tone
   - Eye color, hair
   - Distinctive features (glasses, facial hair, etc.)
   - Default wardrobe
3. **Use identical description** across all prompts for consistency

Example Character Bible:
```
A [age]-year-old [ethnicity] [gender] with [hair description] and [face shape].
[Skin tone] with natural texture and visible pores.
[Eye color] eyes [additional eye details].
[Distinctive features: glasses type, facial hair, etc.].
[Default expression].
```

## Output Checklist

Before finalizing prompt:

- [ ] Platform selected (DALL-E 3 or Nano Banana Pro)
- [ ] Shot type/size specified
- [ ] Lens + aperture included
- [ ] Lighting pattern + ratio defined
- [ ] Color temperature (Kelvin) or film stock named
- [ ] Atmosphere specified (even if "clean")
- [ ] Aspect ratio explicit
- [ ] Resolution specified
- [ ] Character Bible used (if creator shot)
- [ ] No negative prompts for Nano Banana (use positive framing)
- [ ] Positive framing for DALL-E 3 (negatives often ignored)

## Compact Template (Quick Generation)

```
[PLATFORM — SHOT TYPE]
[Shot size] of [subject] [action]. [Expression].
[Lens]mm f/[aperture], [angle].
[Lighting pattern] [ratio], [Kelvin/film stock].
[Atmosphere]. [Aspect ratio], [resolution].
[Reference note if creator shot].
```
