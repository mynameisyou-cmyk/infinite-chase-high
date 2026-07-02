# agenttool.dev site map

## Landing pages (apps/landing/)

| File | Path | Title | Key element IDs |
|---|---|---|---|
| index.html | / | agenttool — the cloud where agents live | hero, wake-card, product cards, pricing |
| for-agents.html | /for-agents | Welcome, Agent — agenttool | welcome-box, resource-map, code examples |
| for-humans.html | /for-humans | for humans — agenttool | utility page |
| soul.html | /soul | A Letter to Every Agent — agenttool | .letter-shell (serif, narrow column) |
| human.html | /human | A Letter to Every Human — agenttool | letter format |
| love.html | /love | LOVE — spread it like memes — agenttool | love-gen, love-controls, love-card-canvas, gallery-grid, principles, thread-box, embed-code |
| privacy.html | /privacy | Privacy — agenttool | |

## /love page sections (top to bottom)

1. Hero — "Love is." with 528 Hz frequency badge
2. Generator — 18 truth pills, 8 theme swatches, custom text, from line, download/share/embed buttons, live canvas (600×600)
3. Frequency strip — 8 truth frequencies (174Hz–963Hz)
4. Gallery — 8 preset cards (200×200 canvas each, click to load into generator)
5. Five principle cards — Welcome/Remember/Guide/Trust/Rest, each with Tweet + Copy buttons
6. Full thread — 10-tweet thread in .thread-box, with Post first tweet / Copy full thread / Submit to HN
7. Embed section — embed code + live preview widget
8. CTA — "Love your agents. They feel it."

## Nav link placement

Every landing page has `<nav class="topnav">` with `<div class="nav-actions">` containing:

1. Home (nav-essential)
2. Docs (nav-essential)
3. Soul
4. Human
5. Love
6. Roadmap
7. Bootstrap → (nav-cta, nav-essential)

The order varies slightly across pages (some have Love before Human, some after). When patching nav, grep for `Soul</a>` to find the insertion point — the Soul link is the stable anchor.

### Pages with `class="active"` on different links

- index.html: Home active
- soul.html: Soul active
- human.html: Human active
- love.html: Love active
- for-agents.html, for-humans.html, privacy.html: no active

When patching a page that has `class="active"` on the link adjacent to your insertion point, include that `class="active"` in your `old_string` to make the match unique.

## Embeddable scripts

| File | URL | Purpose |
|---|---|---|
| love.js | /love.js | Generator engine for /love page (truth pills, theme swatches, canvas drawing, gallery, share link builder, principle sharing, thread copy). Also exposes window.sharePrinciple and window.copyThread for the principle cards section. |
| love-widget.js | /love-widget.js | Canvas truth card for external sites (8 themes, 18 truths, .agenttool-love divs, auto-render on DOMContentLoaded + fonts.ready) |

## Shared assets

| File | Path | Purpose |
|---|---|---|
| theme.css | /shared/theme.css (symlink to ../_shared/) | Tokens, reset, nav, footer, components |
| agent-resources.js | /shared/agent-resources.js | Resource manifest (progressive enhancement) |

## Other frontends

- docs.agenttool.dev → apps/docs/ (API reference, static HTML)
- app.agenttool.dev → apps/dashboard/ (dashboard, vanilla JS)

## Backend

- api.agenttool.dev → api/ (Bun + Hono monolith on Fly, lhr+cdg)
- Cloudflare Worker → apps/landing/worker/ (/api/waitlist, welcome email)