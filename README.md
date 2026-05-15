# Slide Master - Claude Code Skill

Create stunning, brand-aligned HTML presentations with advanced branding integration. Analyzes brand guidelines, extracts brand assets (colors, fonts, logos), and generates beautiful zero-dependency HTML slides.

## What This Skill Does

- **Brand Intelligence** — Analyzes PDFs, logos, and brand guidelines to extract colors, fonts, and personality
- **Style Options** — Choose from 12 curated presets or generate custom styles
- **Zero Dependencies** — Creates single HTML files that work anywhere, forever
- **Fast & Lean** — Optimized for speed (325 lines, 12KB)
- **Multiple Modes** — Create from scratch, convert PowerPoint, or rebrand existing HTML
- **Export Ready** — Deploy to Vercel or export to PDF

## Features

✅ **Brand Asset Analysis**
- Extracts colors from PDFs and images
- Maps fonts to Google Fonts/Fontshare
- Analyzes brand personality (3-word assessment)
- Base64 logo embedding

✅ **Professional Output**
- Viewport fitting (100vh, no scrolling)
- Responsive design (clamp() everywhere)
- WCAG AA accessible
- Inline editing optional
- Animations on scroll

✅ **Fast Workflow**
- Single question set (all at once)
- Optional preview generation
- Smart defaults
- Lazy file loading

## Installation

### Prerequisites

- [Claude Code](https://claude.ai/claude-code) CLI installed
- Access to the frontend-slides repository for supporting files

### Quick Install

```bash
# Create the skills directory if it doesn't exist
mkdir -p ~/.claude/skills/slide-master

# Copy the skill file
cp Skill.md ~/.claude/skills/slide-master/

# Restart Claude Code
```

### Verify Installation

After restarting Claude Code, check that the skill appears:

```bash
# In Claude Code, the skill should appear in the available skills list
/slide-master
```

You should see it listed in the system skills.

## Usage

Invoke the skill in Claude Code:

```
/slide-master

> "Create a pitch deck for our AI startup with our brand guidelines"
```

The skill will:
1. **Collect info** — Ask about mode, brand assets, content, length, style, editing
2. **Analyze brand** — Extract colors, fonts, personality from your assets
3. **Generate previews** (optional) — Show 3 styled options with your brand
4. **Create presentation** — Single HTML file with your brand integrated
5. **Deliver** — Open in browser, provide customization guide

## Example Use Cases

### Corporate Pitch Deck
```
/slide-master

> "Create a Series A pitch deck. Here's our brand guide PDF and logo."
```

### Product Launch
```
/slide-master

> "Build a product launch presentation. 
   Colors: #FF006E (primary), #FFBE0B (accent)
   Font: Archivo Black"
```

### Convert PowerPoint
```
/slide-master

> "Convert quarterly-review.pptx and apply our brand"
```

## Requirements

The skill requires access to supporting files from the [frontend-slides](https://github.com/zarazhangrui/frontend-slides) repository:

- `viewport-base.css` — Mandatory responsive CSS
- `html-template.md` — HTML structure patterns
- `animation-patterns.md` — Animation library
- `STYLE_PRESETS.md` — 12 curated visual styles

### Setup Supporting Files

If you don't have the frontend-slides repository:

```bash
# Clone the repository
git clone https://github.com/zarazhangrui/frontend-slides.git ~/slde-master/frontend-slides

# Or update the paths in Skill.md to point to your local copy
```

The skill expects files at:
```
/Users/michaelalvarado/slde-master/frontend-slides/
├── viewport-base.css
├── html-template.md
├── animation-patterns.md
├── STYLE_PRESETS.md
└── scripts/
    ├── extract-pptx.py
    ├── deploy.sh
    └── export-pdf.sh
```

**Update paths if different:** Edit the Skill.md file and replace the paths with your actual locations.

## Configuration

### Brand Assets

The skill can analyze:
- Logo files (SVG, PNG, JPG)
- Brand guideline PDFs
- Color palettes (hex codes, screenshots)
- Font specifications
- Website URLs (for extraction)

### Export Options

**Deploy to URL (Vercel):**
```bash
bash scripts/deploy.sh presentation.html
```

**Export to PDF:**
```bash
bash scripts/export-pdf.sh presentation.html

# Or compact mode (smaller file)
bash scripts/export-pdf.sh presentation.html --compact
```

## Performance

- **With previews:** ~2-3 minutes total
- **Without previews:** ~60-90 seconds
- **Simple (no brand):** ~30-45 seconds

## Style Presets

The skill includes 12 curated styles:

**Dark Themes:**
- Bold Signal — Confident, high-impact
- Electric Studio — Clean, professional
- Creative Voltage — Energetic, retro-modern
- Dark Botanical — Elegant, sophisticated

**Light Themes:**
- Notebook Tabs — Editorial, organized
- Pastel Geometry — Friendly, modern
- Split Pastel — Playful, creative
- Vintage Editorial — Witty, personality-driven

**Specialty:**
- Neon Cyber — Futuristic, techy
- Terminal Green — Developer-focused
- Swiss Modern — Minimal, Bauhaus
- Paper & Ink — Literary, thoughtful

## Output Quality

Every presentation includes:
- ✅ Single self-contained HTML file
- ✅ Viewport fitting (no scrolling)
- ✅ Responsive design
- ✅ Brand colors in CSS variables
- ✅ Brand fonts with fallbacks
- ✅ Accessible (WCAG AA, keyboard nav)
- ✅ Smooth animations
- ✅ Clear comments

## Troubleshooting

### Skill Not Appearing

1. Verify file is in correct location: `~/.claude/skills/slide-master/Skill.md`
2. Check filename is exactly `Skill.md` (capital S)
3. Restart Claude Code completely
4. Check for syntax errors in frontmatter (YAML between `---`)

### Supporting Files Not Found

Update the paths in `Skill.md`:

```markdown
**Read these files NOW (not before):**
- `/path/to/your/frontend-slides/viewport-base.css`
- `/path/to/your/frontend-slides/html-template.md`
- `/path/to/your/frontend-slides/animation-patterns.md`
```

### Slow Performance

1. Skip preview generation (choose "Just generate")
2. Use provided colors directly (no extraction)
3. Skip logo optimization
4. Generate fewer slides initially

## Companion Skill: slide-export

For exporting presentations to PDF, install the companion `slide-export` skill:

- Validates slides before export
- Two methods: Image (perfect fidelity) or Text (selectable)
- Quality optimization
- Works seamlessly with slide-master output

## Credits

Created by analyzing the [frontend-slides](https://github.com/zarazhangrui/frontend-slides) project by [@zarazhangrui](https://github.com/zarazhangrui).

Optimized for Claude Code performance:
- 71% smaller than original (325 lines vs 1,116 lines)
- Lazy file loading
- Batched questions
- Smart defaults
- Optional previews

## License

MIT — Use it, modify it, share it.

## Version

**v1.0** - Optimized for speed while maintaining quality
- Initial release: May 2026
- Size: 325 lines / 12KB
- Performance: 5-10x faster than verbose version

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify supporting files are accessible
3. Review the skill's Decision Matrix for guidance
4. Ensure Claude Code is up to date

## What's Next?

After installation, try creating your first presentation:

```
/slide-master

> "Create a quick 5-slide presentation about [your topic]"
```

Choose "Just generate" for the fastest experience, or "Show me 3 options" to see style previews.

Enjoy creating beautiful presentations! 🎨✨
