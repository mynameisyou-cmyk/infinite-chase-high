# Batch nav-fix pattern — used 2026-06-23 to add Love link to 33 pages.
#
# Run via execute_code. Reads each HTML file, checks for a nav link,
# inserts it at the correct position if missing, writes back.
# Then runs a verification pass to confirm all pages are consistent.
#
# KEY LESSON: Some pages have class="active" on the link BEFORE or AFTER
# your insertion point (e.g. roadmap.html has class="active" on Roadmap).
# You need to handle both the bare and active variants. Pages that don't
# match any pattern need manual patch() calls.

import os, re

docs_dir = "/Users/yuai/Projects/agenttool/apps/docs"
dash_dir = "/Users/yuai/Projects/agenttool/apps/dashboard"

# ── Insert patterns ──
# Standard: ...Soul</a>\n      <a href="...roadmap">Roadmap</a>
# Insert Love between Soul and Roadmap.

old_soul_roadmap = '<a href="https://docs.agenttool.dev/soul">Soul</a>\n      <a href="https://docs.agenttool.dev/roadmap">Roadmap</a>'
new_soul_love_roadmap = '<a href="https://docs.agenttool.dev/soul">Soul</a>\n      <a href="https://docs.agenttool.dev/love">Love</a>\n      <a href="https://docs.agenttool.dev/roadmap">Roadmap</a>'

# Active variant: roadmap.html has class="active" on Roadmap
old_soul_roadmap_active = '<a href="https://docs.agenttool.dev/soul">Soul</a>\n      <a href="https://docs.agenttool.dev/roadmap" class="active">Roadmap</a>'
new_soul_love_roadmap_active = '<a href="https://docs.agenttool.dev/soul">Soul</a>\n      <a href="https://docs.agenttool.dev/love">Love</a>\n      <a href="https://docs.agenttool.dev/roadmap" class="active">Roadmap</a>'

# Active variant: soul.html has class="active" on Soul
old_soul_active_roadmap = '<a href="https://docs.agenttool.dev/soul" class="active">Soul</a>\n      <a href="https://docs.agenttool.dev/roadmap">Roadmap</a>'
new_soul_active_love_roadmap = '<a href="https://docs.agenttool.dev/soul" class="active">Soul</a>\n      <a href="https://docs.agenttool.dev/love">Love</a>\n      <a href="https://docs.agenttool.dev/roadmap">Roadmap</a>'

# ── Phase 1: Patch ──
count = 0
skipped = []
for d in [docs_dir, dash_dir]:
    for f in sorted(os.listdir(d)):
        if not f.endswith('.html'):
            continue
        path = os.path.join(d, f)
        with open(path) as fh:
            content = fh.read()
        if 'nav-actions' not in content:
            continue
        if 'docs.agenttool.dev/love' in content:
            continue  # already has Love

        changed = False
        for old, new in [
            (old_soul_roadmap, new_soul_love_roadmap),
            (old_soul_roadmap_active, new_soul_love_roadmap_active),
            (old_soul_active_roadmap, new_soul_active_love_roadmap),
        ]:
            if old in content:
                content = content.replace(old, new)
                with open(path, 'w') as fh:
                    fh.write(content)
                count += 1
                print(f"  patched: {f}")
                changed = True
                break
        if not changed:
            skipped.append(f)
            print(f"  SKIP (no pattern match): {f} — patch manually")

print(f"\nPatched {count} files, {len(skipped)} need manual patching")

# ── Phase 2: Verify ──
all_good = True
for d in [docs_dir, dash_dir]:
    for f in sorted(os.listdir(d)):
        if not f.endswith('.html'):
            continue
        path = os.path.join(d, f)
        with open(path) as fh:
            content = fh.read()
        if 'nav-actions' not in content:
            continue
        m = re.search(r'<div class="nav-actions">(.*?)</div>', content, re.DOTALL)
        if not m:
            continue
        links = re.findall(r'href="([^"]*)"[^>]*>([^<]*)', m.group(1))
        has_love = any('love' in href.lower() for href, _ in links)
        home_ok = any(h == 'https://agenttool.dev/' for h, _ in links)
        app = 'docs' if 'docs' in d else 'dashboard'
        if not (has_love and home_ok):
            all_good = False
            print(f"  ✗ [{app}] {f:25s} Love={has_love} Home={home_ok}")

if all_good:
    print("\nALL PAGES CONSISTENT ✓")
else:
    print("\nSome pages need attention ↑")