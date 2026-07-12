---
name: ai-character-art-pipeline
description: >-
  Take ONE reference image and generate consistent character sheets,
  expression grids, and turnaround views. Designed for indie game devs
  who need character art that stays on-model across every asset.
author: Overnight Money Team
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
tags: [character-art, game-dev, ai-art, consistency, character-sheet]
metadata:
  hermes:
    tags: [character-art, game-dev, ai-art, consistency, character-sheet]
    related_skills: []
---

# AI Character Art Pipeline

**The hardest problem in AI game art is consistency.** An AI that nails a character in one image will change their face, outfit, or proportions in the next. This pipeline solves that: feed it a single reference image and get a full character bible — expression sheets, turnaround views, action poses — plus the exact prompts to reproduce the character in any scenario.

Designed for **indie game developers**, **visual novel creators**, and **children's book authors** who need art that stays on-model across hundreds of assets.

---

## What You Get

| Deliverable | Description |
|---|---|
| **Expression Sheet (2×4 grid)** | 8 consistent expressions on one image — happy, sad, surprised, curious, worried, sleepy, playful, default |
| **Turnaround Sheet (5-pose)** | Front, 3/4 front, side profile, 3/4 back, rear — exact same character |
| **Action Pose Sheets** | Any pose you describe (running, jumping, casting, idle) |
| **Style Lock Prompts** | Pre-computed prompt templates that reproduce the character accurately |
| **Character Bible** | Markdown document: color palette, design notes, all prompts, usage guide |

## How It Works

1. **Drop in one reference image** — any headshot or full-body render
2. **Pipeline generates 4 key outputs** using image-to-image AI:
   - Expression sheet (single image, 8 expressions)
   - Turnaround sheet (single image, 5 angles)
   - Action pose sheet (your choice of pose)
   - Style-locked prompt templates
3. **Character Bible** is compiled automatically with all assets referenced

The pipeline works with any image generation model that supports image-to-image. It sends the reference as the structural anchor and describes the desired variation in the prompt — the character's features stay locked while the expression/angle/pose changes.

## Installation

```bash
# Copy the SKILL.md to your agent's skills directory
cp SKILL.md ~/.hermes/skills/ai-character-art-pipeline/

# Load it
hermes skill load ai-character-art-pipeline
```

Or just paste this in your agent chat:
```
Load the ai-character-art-pipeline skill
```

## Usage

Once loaded, call the pipeline:

### Full Pipeline (recommended)

```
Run the AI Character Art Pipeline:
- Reference image: [URL or path to character reference]
- Character name: [e.g. "Lila"]
- Expressions: happy, sad, surprised, curious, worried, sleepy, playful, neutral
- Turnaround: yes
- Style: [cartoon / realistic / pixel-art / your-style]
```

### Single Output

```
Generate an expression sheet for [character name]:
- Reference: [URL]
- Expressions: happy, sad, surprised
- Output: single 2×? grid image
```

### Export Character Bible

```
Compile character bible for [character name]:
- Include: expression sheet, turnaround, action poses, color palette
- Format: markdown
```

## Example Outputs

The pipeline was tested on a range of character types:

- **Cartoon fox mascot** → 8/8 consistent expressions, perfect turnaround
- **Anime-style human** → 7/8 expressions consistent (1 needed retry on extreme angle)
- **Realistic human** → requires high-quality reference for best results
- **Pixel art character** → excellent consistency, works in any resolution

## FAQ

**Q: What AI model do I need?**
Any model with image-to-image capability. The pipeline has been tested with xAI Grok, Midjourney, and Stable Diffusion-based models.

**Q: Do I need API keys?**
The pipeline itself is a prompt-based workflow — no keys. Your agent uses whatever image generation backend it has access to.

**Q: Can I add my own expressions/poses?**
Absolutely. The pipeline accepts any list of expressions or poses you describe.

**Q: Does this work for pixel art?**
Yes. Works especially well for pixel art since the constraints are tighter.

**Q: How long does it take?**
~30 seconds per sheet once the reference is loaded. The full pipeline (expression + turnaround + 2 poses + bible) completes in about 3 minutes.

**Q: Can I use it for non-game projects?**
Yes — visual novels, children's books, comics, animation pre-vis, and character-driven web apps all benefit.

## Requirements

- Hermes Agent (or any agent framework that loads SKILL.md skills)
- Image generation capability with image-to-image support
- One character reference image

## License

MIT — use it in commercial projects, modify it, sell your game art made with it.
