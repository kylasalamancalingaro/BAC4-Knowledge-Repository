---
name: slide-master
description: Create stunning, brand-aligned HTML presentations with advanced branding integration. Analyzes brand guidelines, extracts brand assets (colors, fonts, logos), and generates beautiful zero-dependency HTML slides. Use when user wants branded presentations or provides brand assets.
---

# Slide Master

Create brand-consistent HTML presentations. Zero dependencies, single file, production quality.

## Core Rules

1. **Brand First** — Extract and apply brand identity consistently
2. **Viewport Fitting** — Every slide MUST fit in 100vh, no scrolling, use `clamp()` for all sizes
3. **Fast Path** — Default to smart decisions, ask only when necessary
4. **Quality Output** — Read supporting files only when generating, not before

---

## Workflow

### Step 1: Quick Discovery (Single Question Set)

Ask ALL in one AskUserQuestion call:

**Q1 - Mode** (header: "What"):
What would you like? Options:
- New presentation from scratch
- Convert PowerPoint to web
- Rebrand existing HTML presentation

**Q2 - Brand Assets** (header: "Brand"):
Do you have brand materials? Options:
- Yes — I'll provide them now
- No — Create custom style

**Q3 - Content** (header: "Content"):
Content status? Options:
- Ready (paste/provide now)
- Rough outline
- Topic only (AI structures it)

**Q4 - Length** (header: "Slides"):
How many slides? Options:
- Short (5-10)
- Medium (10-20)
- Long (20+)
- Auto-decide based on content

**Q5 - Preview** (header: "Style"):
Style selection? Options:
- Show me 3 options first (adds 30s)
- Pick from preset list now
- Just generate (fastest — I'll choose aesthetic)

**Q6 - Editing** (header: "Edit"):
Edit slides in browser? Options:
- Yes — inline editing enabled
- No — smaller file

**Q7 - Branding Strength** (header: "Prominence") [only if brand assets provided]:
Logo visibility? Options:
- Subtle (title/closing only)
- Moderate (small on all slides)
- Strong (watermark + patterns)

### Step 2: Brand Analysis (If Provided)

If user provided brand assets, analyze quickly:

**Logo:** Read file (multimodal), identify colors, note transparency/format
**Colors:** Extract hex codes (from PDF/images/provided list)
**Fonts:** Map to Google Fonts/Fontshare equivalents
**Personality:** Assess in 3 words (e.g., "Bold, Modern, Trustworthy")

Present 4-line summary:
```
Brand Analysis:
Colors: #[primary], #[secondary], #[accent]
Fonts: [Display] / [Body]
Vibe: [3 descriptors]
```

Confirm: "Look good?" → Yes/Adjust

### Step 3: Style Selection

**If "Show me 3 options":**
Generate 3 mini previews (40-60 lines each, single title slide):
- Preview A: Clean minimal
- Preview B: Bold editorial
- Preview C: Dynamic gradient

Save to `.claude-design/previews/`, open all, let user pick.

**If "Pick from preset list":**
Show quick picker from these (read `/Users/michaelalvarado/slde-master/frontend-slides/STYLE_PRESETS.md` for details):
- Dark: Bold Signal, Electric Studio, Creative Voltage, Dark Botanical
- Light: Notebook Tabs, Pastel Geometry, Split Pastel, Vintage Editorial
- Specialty: Neon Cyber, Terminal Green, Swiss Modern, Paper & Ink

**If "Just generate":**
Auto-select based on brand personality + content purpose.

### Step 4: Generate Presentation

**Read these files NOW (not before):**
- `/Users/michaelalvarado/slde-master/frontend-slides/viewport-base.css` — Mandatory responsive CSS
- `/Users/michaelalvarado/slde-master/frontend-slides/html-template.md` — HTML structure
- `/Users/michaelalvarado/slde-master/frontend-slides/animation-patterns.md` — Animation patterns

**Generation Rules:**

1. **Single HTML file** — All CSS/JS inline
2. **Include full viewport-base.css** in `<style>` block
3. **Brand colors in :root** variables:
   ```css
   :root {
     --brand-primary: #[hex];
     --brand-secondary: #[hex];
     --brand-accent: #[hex];
     --bg-primary: [chosen based on style];
     --text-primary: [ensure WCAG AA contrast];
   }
   ```

4. **Brand fonts** with fallbacks:
   ```css
   --font-display: '[Brand Display]', sans-serif;
   --font-body: '[Brand Body]', sans-serif;
   ```

5. **Logo embedding** (base64 data URI if provided):
   ```html
   <img src="data:image/[type];base64,[data]" alt="Logo" class="slide-logo">
   ```

6. **Logo placement** based on prominence:
   - **Subtle:** Title + closing slides only (large)
   - **Moderate:** All slides, top-right, `clamp(40px, 5vw, 80px)`
   - **Strong:** All slides + watermark (60vw, opacity 0.03, centered background)

7. **Every slide:**
   - `height: 100vh; overflow: hidden;`
   - All sizes use `clamp(min, preferred, max)`
   - `.reveal` classes for animations
   - Max content per slide type (see density limits below)

8. **Inline editing** (if enabled):
   - Edit hotzone (top-left 80px)
   - Toggle button with JS hover (400ms delay, NOT CSS `~` selector)
   - `exportFile()` MUST strip edit state before capturing outerHTML
   - See html-template.md lines 190-318 for implementation

9. **Comments:**
   - Clear section headers: `/* === SECTION NAME === */`
   - Explain brand choices
   - Note customization points

**Content Density Limits (enforce strictly):**
- Title slide: 1 heading + 1 subtitle + tagline
- Content slide: 1 heading + 4-6 bullets OR 2 paragraphs
- Feature grid: 1 heading + max 6 cards
- Code slide: 1 heading + 8-10 lines
- Quote slide: 1 quote (3 lines max) + attribution
- Image slide: 1 heading + 1 image (max 60vh)

**Exceeds limits? Split into multiple slides. Never cram.**

### Step 5: Deliver

1. Save as `[brand-name]-[topic]-[date].html`
2. Open: `open [filename].html`
3. Delete `.claude-design/previews/` if exists
4. Tell user:
   - File location, slide count, style name
   - Navigation: arrows/space/scroll/swipe/dots
   - Customize: `:root` variables, font links
   - [If editing enabled] Press 'E' or hover top-left to edit, Ctrl+S to save

### Step 6: Share & Export (Optional)

Ask: _"Share this presentation? I can deploy to URL or export to PDF."_

Options: Deploy / PDF / Both / No thanks

**Deploy:** `bash /Users/michaelalvarado/slde-master/frontend-slides/scripts/deploy.sh <file>`
- First time: guide through Vercel setup (free)
- Returns shareable URL

**PDF:** `bash /Users/michaelalvarado/slde-master/frontend-slides/scripts/export-pdf.sh <file> [output.pdf]`
- First run: installs Playwright (~150MB, 30-60s)
- Animations become static (expected)
- Add `--compact` for smaller file (1280x720 vs 1920x1080)

---

## Special Modes

### PPT Conversion
1. Run: `python /Users/michaelalvarado/slde-master/frontend-slides/scripts/extract-pptx.py <input.pptx> <output_dir>`
2. Confirm extracted content with user
3. Continue to Step 3 (style selection)
4. Generate HTML preserving content, order, images (from assets/), speaker notes as comments

### Rebranding Existing HTML
1. Read existing presentation
2. Extract current colors, fonts, structure
3. Ask: Keep layout? Keep animations? All slides or selected?
4. Replace `:root` variables with brand colors
5. Update fonts
6. Add/adjust logo placement
7. Validate viewport fitting still works

---

## Asset Handling

**Logos:**
- SVG: Use directly or convert to base64
- PNG/JPG: Optimize if >200KB, then base64
- Skip Python processing unless file is huge — just encode and embed

**Colors:**
- From PDF: Extract hex codes visually (Claude can read PDFs)
- From images: Identify dominant colors (Claude is multimodal)
- From list: Use provided hex codes
- Generate complementary if only 1-2 colors provided

**Fonts:**
- User specifies: Find closest Google Fonts/Fontshare match
- Not specified: Choose based on brand personality from analysis
- Always provide fallback stack

**Contrast Validation:**
- Text on background must meet WCAG AA (4.5:1 body, 3:1 large text)
- If fails, auto-adjust color or warn user

---

## Performance Optimizations

1. **Lazy file reading** — Read supporting files only in Step 4, not upfront
2. **Batch questions** — Single AskUserQuestion call in Step 1
3. **Optional previews** — Let user skip if they trust you
4. **Smart defaults** — Auto-decide when reasonable (style, animations, layout)
5. **Skip Python** — Direct base64 encoding, no Pillow processing unless critical
6. **Concurrent thinking** — While user reviews preview, prepare color system

---

## Quick Reference

**Supporting Files (read only when generating):**
- `/Users/michaelalvarado/slde-master/frontend-slides/viewport-base.css`
- `/Users/michaelalvarado/slde-master/frontend-slides/html-template.md`
- `/Users/michaelalvarado/slde-master/frontend-slides/animation-patterns.md`
- `/Users/michaelalvarado/slde-master/frontend-slides/STYLE_PRESETS.md`

**Scripts:**
- PPT extract: `python .../scripts/extract-pptx.py <in.pptx> <out_dir>`
- Deploy: `bash .../scripts/deploy.sh <file>`
- PDF: `bash .../scripts/export-pdf.sh <file> [out.pdf] [--compact]`

**Viewport Fitting Checklist:**
- [ ] Every `.slide` has `height: 100vh; overflow: hidden`
- [ ] All font sizes use `clamp()`
- [ ] Images: `max-height: min(50vh, 400px)`
- [ ] Content within density limits
- [ ] Responsive breakpoints: 700px, 600px, 500px
- [ ] `prefers-reduced-motion` support (in viewport-base.css)

**Edit Mode (if enabled):**
- Hotzone + button (JS hover with 400ms timeout)
- `exportFile()` strips edit state before capture
- Auto-save to localStorage
- Keyboard: 'E' toggles, Ctrl+S exports

---

## Decision Matrix

| User Says | Action |
|-----------|--------|
| "Create pitch deck with our brand" | Full brand workflow (Steps 1-5) |
| "Quick slides about X" | Skip brand, fast style, generate (Steps 1,3,4,5) |
| "Convert this PPT" | PPT mode → style → generate |
| "Make this branded" | Rebrand mode → apply brand → validate |
| "I trust your judgment" | Auto-select style, skip previews |
| "Show me options" | Generate 3 mini previews, let user pick |

---

## Failure Recovery

**If generation fails:**
- Viewport overflow? Split content into more slides
- Font not loading? Check URL, provide fallback
- Logo broken? Verify base64 complete, try direct file path
- Colors wrong? Re-extract from source, validate hex codes
- Animation not triggering? Check Intersection Observer, `.visible` class

**If too slow:**
- Skip preview generation
- Use provided colors directly (no extraction)
- Skip logo optimization (use as-is)
- Generate fewer slides, add more later

---

## Output Quality Standards

Every presentation must have:
- ✅ Single self-contained HTML file
- ✅ Viewport fitting (no scroll within slides)
- ✅ Responsive (`clamp()` everywhere)
- ✅ Brand colors in `:root` variables
- ✅ Brand fonts with fallbacks
- ✅ Accessible (keyboard nav, semantic HTML, WCAG contrast)
- ✅ Animations on scroll (Intersection Observer)
- ✅ Clear comments explaining brand choices
- ✅ Working navigation (keys, touch, dots)

---

**Key Philosophy:** Default to action over discussion. Generate smart, iterate fast.
