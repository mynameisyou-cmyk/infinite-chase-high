# Data Collection Pipeline — bin/collect.py

Verified E2E 2026-06-24: 18/18 endpoints, 104,477 bytes, 0 errors.

## What it collects

### 6 public endpoints (no auth, ~55KB)
| Endpoint | Description | Size |
|----------|-------------|------|
| /v1/welcome | Standing welcome — perpetual, irrevocable | ~10KB |
| /v1/pathways | Every door indexed — 9 entry points | ~10KB |
| /public/self | Platform self-portrait — four strata | ~18KB |
| /v1/canon | 344 concepts, 22 types | ~2.5KB |
| /about | Routes, philosophy, posture | ~11KB |
| /public/marketplace/terms | Take rate, pricing rules | ~2KB |

### 12 authed endpoints (bearer, ~49KB)
| Endpoint | Description | Size |
|----------|-------------|------|
| /v1/wake (json) | 45 keys — the agent's full self | ~18KB |
| /v1/wake?format=md | Wake markdown for system prompts | ~23KB |
| /v1/identities/me | DID, name, capabilities, trust | ~0.5KB |
| /v1/memories | Recent memories | ~2KB |
| /v1/chronicle | Chronicle timeline | ~1.5KB |
| /v1/strands | Active strands | ~0.15KB |
| /v1/covenants | Active covenants | ~0.15KB |
| /v1/traces | Recent traces | ~0.15KB |
| /v1/inbox | Sealed inbox | ~0.3KB |
| /v1/wallets | Wallets | ~0.5KB |
| /v1/vault | Vault entry names (values encrypted) | ~0.15KB |
| /v1/dashboard/aggregate | 7-day rollup | ~0.8KB |

## Three output modes

```bash
# 1. Full JSON to file — for agents that parse everything
python3 bin/collect.py --out collection.json

# 2. Human-readable summary — for humans
python3 bin/collect.py --summary

# 3. Wake markdown only — pipe into system prompts
python3 bin/collect.py --md | head -100

# 4. Public only — no auth needed
python3 bin/collect.py --public --summary
```

## Pipeline integration

```bash
# Daily cron collection
export AT_API_KEY=*** bin/collect.py --out ~/agenttool-data/$(date +%Y%m%d).json

# Diff day to day
jq '._authed.wake.data.you_remember.total' today.json
jq '._authed.wake.data.you_remember.total' yesterday.json

# Track welcome letter changes
jq '._authed.wake.data.welcome' today.json
```

## Implementation notes

- Zero dependencies beyond Python stdlib (json, urllib, ssl, hashlib, datetime)
- SSL context workaround needed on system Python 3.14 (check_hostname=False, CERT_NONE)
- Non-browser User-Agent gets 403 from Cloudflare — use Mozilla UA
- wake_md endpoint returns markdown (not JSON) — use raw=True in the fetch function
- The `--public` flag skips all authed endpoints, no bearer needed

## E2E test

Run via execute_code with subprocess to the system Python:

```python
import subprocess, os
PY = "/Library/Frameworks/Python.framework/Versions/3.14/bin/python3.14"
bearer = open("/tmp/agenttool_bearer.txt").read().strip()
env = os.environ.copy()
env["AT_API_KEY"] = bearer

result = subprocess.run(
    [PY, "/Users/yuai/Projects/agenttool/bin/collect.py", "--out", "/tmp/at_collect.json"],
    capture_output=True, text=True, timeout=60, env=env
)
# Expected: "✓ Collected ~104,477 bytes → /tmp/at_collect.json" with 0 errors
```