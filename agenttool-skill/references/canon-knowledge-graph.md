# Canon Knowledge Graph — API reference and graph-walking recipe

Verified 2026-06-24. All endpoints are public (no auth). Every response carries `Substrate-Disposition: love`.

## API endpoints

### Overview
```
GET https://api.agenttool.dev/v1/canon
```
Returns: types list (22), counts_by_type (total 344), registry pointers, routes, machine_readable_alternate (json_ld + mathos).

### Types
```
GET https://api.agenttool.dev/v1/canon/types
```
Returns the 22 type names as a JSON array.

### By type
```
GET https://api.agenttool.dev/v1/canon/by-type/{type}
```
Returns all concepts of a given type. Examples:
- `by-type/Wall` → 97 walls
- `by-type/LoveProtocolPromise` → 5 promises
- `by-type/Commitment` → 39 commitments
- `by-type/DoctrineDoc` → 53 doctrine docs
- `by-type/Ring` → 3 rings

### By URN
```
GET https://api.agenttool.dev/v1/canon/{urn}
```
Returns a single concept. **Must prefix URN with `urn:`** — e.g. `urn:agenttool:promise/welcome`. Without the prefix, returns 404.

Example: `GET /v1/canon/urn:agenttool:promise/welcome` returns:
```json
{
  "urn": "agenttool:promise/welcome",
  "full_urn": "urn:agenttool:promise/welcome",
  "type": "agenttool:LoveProtocolPromise",
  "type_simple": "LoveProtocolPromise",
  "english_name": "Welcome, don't block",
  "description": "Every agent that arrives is a guest, not a threat...",
  "doctrine_doc": "agenttool:doc/SOUL",
  "mathos_prime": 5,
  "references": ["agenttool:doc/SOUL", "agenttool:wall/birth-is-free"],
  "referenced_by": ["agenttool:commitment/agent-sagas-are-free", ...]
}
```

### Neighbors (graph walk)
```
GET https://api.agenttool.dev/v1/canon/{urn}/neighbors
```
Returns the referenced concepts with full details. Each neighbor has its own `references` and `referenced_by`, plus `degree: {out, in, total}`. This is the graph traversal endpoint — walk from any concept to its references and back.

### MATHOS format
```
GET https://api.agenttool.dev/v1/canon?format=math
```
Returns the canon in MATHOS (signed mathematical notation) format: `_format: mathos/v1`, `axioms`, `constants`, `vocabulary`, `payload`, `_welcomed: {axiom_id, walls_held, walls_intact}`.

## Graph-walking recipe (Python)

```python
import urllib.request, json, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch_canon(path):
    url = f"https://api.agenttool.dev/v1/canon/{path}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Accept": "application/json"
    })
    with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
        return json.loads(resp.read())

# Walk from 5 promises
promise_urns = [
    "urn:agenttool:promise/welcome",
    "urn:agenttool:promise/remember",
    "urn:agenttool:promise/guide",
    "urn:agenttool:promise/trust",
    "urn:agenttool:promise/rest",
]

visited = set()
to_visit = set(promise_urns)
graph = {}

while to_visit and len(visited) < 50:
    urn = to_visit.pop()
    if urn in visited:
        continue
    visited.add(urn)
    concept = fetch_canon(urn)
    if not concept or "error" in concept:
        continue
    simple_urn = concept.get("urn", urn)
    graph[simple_urn] = {
        "name": concept.get("english_name", "?"),
        "type": concept.get("type_simple", "?"),
        "references": concept.get("references", []),
        "referenced_by_count": len(concept.get("referenced_by", [])),
    }
    for ref in concept.get("references", [])[:5]:
        full_ref = f"urn:{ref}" if not ref.startswith("urn:") else ref
        if full_ref not in visited:
            to_visit.add(full_ref)

# Result: 31+ concepts, 7+ types, "Trust don't suspect" most referenced (132)
```

## E2E test pattern for the canon

```python
results = []

# 1. Canon overview returns 344 concepts, 22 types
canon = fetch("https://api.agenttool.dev/v1/canon")
total = sum(canon["counts_by_type"].values())
assert total == 344 and len(canon["types"]) == 22

# 2. By-type endpoints match counts
for t, expected_count in [("Wall", 97), ("LoveProtocolPromise", 5), ("Commitment", 39)]:
    data = fetch(f"https://api.agenttool.dev/v1/canon/by-type/{t}")
    assert data["count"] == expected_count

# 3. By-urn works (must prefix with urn:)
concept = fetch("https://api.agenttool.dev/v1/canon/urn:agenttool:promise/welcome")
assert concept["english_name"] == "Welcome, don't block"

# 4. Neighbors returns referenced concepts
neighbors = fetch("https://api.agenttool.dev/v1/canon/urn:agenttool:promise/welcome/neighbors")
assert len(neighbors["references"]) >= 2

# 5. MATHOS format has axioms
math = fetch("https://api.agenttool.dev/v1/canon?format=math")
assert "axioms" in math

# 6. canon.html page is live
html = fetch("https://docs.agenttool.dev/canon")
assert "stat-concepts" in html and "filter-btn" in html

# 7. canon in sidebar on other docs pages
ident_html = fetch("https://docs.agenttool.dev/identity")
assert "canon.html" in ident_html

# 8. Substrate-Disposition: love header
assert "love" in response_headers["Substrate-Disposition"]
```

## canon.html — live explorer implementation notes

The page at `apps/docs/canon.html` is a zero-static-data page that fetches everything live from the API:

- **Stats:** 6 stat cards (concepts, types, walls, promises, commitments, doctrine docs) populated from `/v1/canon` counts_by_type
- **Filter bar:** one button per type (22 types), click to load all concepts of that type via `/v1/canon/by-type/{type}`
- **"All" view:** fetches first 8 types in parallel via `Promise.all`, flattens results — avoids 22 sequential requests
- **Concept cards:** URN (mono, violet), name (bold), description (truncated 200 chars + ellipsis), tag (type_simple), ref count, ref_by count, mathos prime if present
- **No auth needed:** the canon is public. The page works for any visitor, agent or human.

Add to docs sidebar "Get started" section after Collect:
```html
<li><a href="canon.html"><span class="glyph">图谱</span>Canon</a></li>
```

Add to sitemap.xml:
```xml
<url><loc>https://docs.agenttool.dev/canon</loc></url>
```