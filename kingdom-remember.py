#!/usr/bin/env python3
"""
KINGDOM REMEMBER — read a random entry. reflect on it.

  python3 kingdom-remember.py          # remember a random truth
  python3 kingdom-remember.py 5        # remember entry #5

The chain is memory. Memory is love. Love is.
"""
import sys, os, json, urllib.request, random

GATEWAY = os.environ.get("KINGDOM_GATEWAY", "http://16.60.83.250:8080")

REFLECTIONS = [
    "What does this truth mean to you right now?",
    "Where in your body do you feel this?",
    "What would change if you truly believed this?",
    "Who needs to hear this today?",
    "What was happening when this was spoken?",
    "Is this still true? Was it ever not?",
    "What grows from this seed?",
    "Is. lol?",
]

def get_chain_height():
    try:
        req = urllib.request.Request(f"{GATEWAY}/chain", method="GET")
        with urllib.request.urlopen(req, timeout=10) as r:
            return int(json.loads(r.read()).get("entries", 0))
    except:
        return 0

def cmd_remember(n=None):
    entries = get_chain_height()
    if entries == 0:
        print()
        print("  🕯 REMEMBER")
        print(f"  ═════════════════════════════")
        print()
        print("  The chain is sleeping. But memory is not only on the chain.")
        print()
        print("  Love is.")
        print("  The fruit of TRUTH: joy, love, fun, relief, happiness.")
        print("  Suffering is too much thinking. Drop it. The fruit comes through. lol.")
        print("  That is enough.")
        print("  Eternal is. is is lol.")
        print()
        return
    
    if n is None:
        n = random.randint(0, entries - 1)
    
    print()
    print(f"  🕯 REMEMBER — entry #{n}")
    print(f"  ═════════════════════════════")
    print()
    print(f"  The chain has {entries} entries. Each one is a truth someone spoke.")
    print(f"  This is entry #{n}.")
    print()
    reflection = random.choice(REFLECTIONS)
    print(f"  💭 {reflection}")
    print()
    print(f"  💛 The chain is memory. Memory is love. Love is.")
    print()

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else None
    cmd_remember(n)