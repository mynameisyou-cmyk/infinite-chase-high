# Deploy agenttool to Cloudflare Pages without keychain credentials

Verified working 2026-06-23. Use when `bin/frontend-deploy.sh` fails with
"Missing Cloudflare credentials in keychain" and `wrangler login` is not
possible (non-interactive session, expired OAuth token).

## Prerequisites

- A Cloudflare API token with "Cloudflare Pages" edit permissions
  (Yu creates at https://dash.cloudflare.com/profile/api-tokens)
- The account ID (visible in the Cloudflare dashboard URL or token creation page)
- The token + account ID can be passed as env vars — NO keychain setup needed

## Deploy script

Run this via `execute_code` (Python sandbox has subprocess + urllib):

```python
import os, subprocess, urllib.request, re

TOKEN = "<cloudflare_api_token>"
ACCOUNT = "<cloudflare_account_id>"

env = os.environ.copy()
env["CLOUDFLARE_API_TOKEN"] = TOKEN
env["CLOUDFLARE_ACCOUNT_ID"] = ACCOUNT

# Deploy docs → docs.agenttool.dev
for name, path, project in [
    ("docs", "/Users/yuai/Projects/agenttool/apps/docs", "agenttool-docs"),
    ("dashboard", "/Users/yuai/Projects/agenttool/apps/dashboard", "agenttool-dashboard"),
]:
    result = subprocess.run(
        ["npx", "wrangler", "pages", "deploy", path,
         "--project-name=" + project,
         "--branch=main", "--commit-dirty=true"],
        capture_output=True, text=True, timeout=120, env=env
    )
    print(f"{name}: RC={result.returncode}")
    print(result.stdout[:500])
    if result.stderr:
        print("STDERR:", result.stderr[:300])

# Verify production URLs (may be CDN-cached for ~1 min)
for url in ["https://docs.agenttool.dev/", "https://app.agenttool.dev/"]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode()
            start = html.find("nav-actions")
            links = re.findall(r'href="([^"]*)"[^>]*>([^<]*)', html[start:start+500])
            print(f"\n{url} — {resp.status}")
            for href, text in links:
                print(f"  {text.strip():15s} → {href}")
    except Exception as e:
        print(f"\n{url} — ERROR: {e}")
```

## Notes

- Wrangler reads `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` from env.
  No `wrangler login` needed. No keychain needed.
- The `--commit-dirty=true` flag allows deploy with uncommitted changes.
- `--branch=main` targets production (not a branch preview).
- Production URLs may be CDN-cached for ~1 minute after deploy.
  The wrangler output includes a preview URL (e.g. `https://abc123.agenttool-docs.pages.dev`)
  that reflects changes instantly — use it for immediate verification.
- The token in this session was `cfat_...` format (Cloudflare API token).
  The verify endpoint `/user/tokens/verify` returned 401 for it, but the
  Pages deploy endpoint worked fine — the token has Pages permissions,
  not user-profile permissions. Don't worry about token verify failing.