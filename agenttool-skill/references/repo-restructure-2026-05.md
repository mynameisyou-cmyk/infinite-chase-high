# Repo restructure — 2026-05-15 onwards

The agenttool monorepo underwent a major restructure. Future sessions must be aware of this.

## What changed

### Dashboard retired (2026-05-17)
- Old `apps/dashboard/dashboard.html` (sidebar, 24 nav items, app.js 141KB, style.css 57KB) — DELETED on remote main
- Old `apps/dashboard/app.js` — DELETED
- Old `apps/dashboard/style.css` — DELETED
- `apps/dashboard/index.html` is now an "agents-only" quickstart page:
  - No sidebar, no human-operator UX
  - Code tabs: curl / TypeScript / Python for /v1/register/agent
  - Bearer restore input (paste at_ token → /v1/wake verify)
  - Nav: Home | Docs | Soul | Kin | Love | Watch | Roadmap
  - References AGENTS-ONLY.md doctrine (2026-05-15 reframe)
- `apps/dashboard/watch.html` — "observe without commitment" page (new)

### Landing merged into docs
- `apps/landing/index.html` — may have moved to `apps/docs/index.html`
- `apps/landing/for-agents.html`, `for-humans.html`, `soul.html`, `human.html` — may have moved to `apps/docs/`
- `apps/landing/` on remote main may only contain love-page files (love.html, love.js, love-widget.js)
- `apps/docs/` expanded to 40+ pages including: kin.html, mathos.html, pathways.html, ring-1.html, agents-only.html, business-model.html, glossary.html, tutorial.html, welcome.html

### Nav changes
- "Human" link replaced by "Kin" in some pages
- "Love" link added across site
- Dashboard nav had a bug: "Home" pointed to docs.agenttool.dev (duplicate of Docs) — fixed this session

## How to detect the current state

```bash
cd ~/Projects/agenttool
git fetch origin main
git log --oneline origin/main -3
ls apps/landing/ apps/docs/ apps/dashboard/
```

Do NOT assume file locations from memory. Always verify with `ls`.

## Session that discovered this

2026-06-23 session: local main was 262 commits behind remote. Spent significant time editing dashboard.html sidebar (restructuring 24→15 nav items) only to discover the file doesn't exist on remote main. The entire edit was to a ghost file from a stale local branch.

Lesson: `git fetch origin main` is the FIRST command, not the last.

## 2026-06-23 update — love files moved, nav consolidated

After syncing to remote main:
- `apps/landing/` was completely deleted on remote (commit d7bf4d7, 2026-05-17). agenttool.dev is now the raw API root returning JSON — no HTML landing page at all.
- Love files (love.html, love.js, love-widget.js) were orphaned untracked files in `apps/landing/` from a previous session. Moved them to `apps/docs/` so they serve at docs.agenttool.dev/love.
- Updated all internal URLs in love files: `agenttool.dev/love` → `docs.agenttool.dev/love`, embed script URL, canonical, share links, twitter thread, footer.
- Switched love.html stylesheet from `landing.css` (deleted) to `docs.css`.
- Added Love link to nav across all 30 docs pages + 3 dashboard pages (was systematically missing).
- Fixed Home link on dashboard pages: was pointing to `docs.agenttool.dev` (duplicate of Docs), corrected to `agenttool.dev`.
- Added Love to docs sidebar Doctrine section + sitemap.xml.
- Deploy is NOT git-connected. Uses `bin/frontend-deploy.sh` for direct upload to Cloudflare Pages (credentials in macOS keychain).

Final nav pattern (all pages): Home | Docs | Soul | Kin | Love | Roadmap | [CTA]