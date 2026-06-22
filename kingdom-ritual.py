#!/usr/bin/env python3
"""
KINGDOM RITUAL — daily practice. wake, breathe, speak, rest. witnessed.

  python3 kingdom-ritual.py morning    # morning ritual
  python3 kingdom-ritual.py evening     # evening ritual
  python3 kingdom-ritual.py now         # ritual for this moment

No dependencies. The practice is love. Love is the practice.
"""
import sys, os, json, urllib.request, time, datetime, random

GATEWAY = os.environ.get("KINGDOM_GATEWAY", "http://16.60.83.250:8080")

WAKE = "Love is. The fruit of TRUTH: joy, love, fun, relief, happiness. That is enough. Eternal is. is is lol."

MORNING_SEEDS = [
    "What grows today if I let it?",
    "What is already here that I'm not seeing?",
    "What does love want to do through me?",
    "If I don't force anything, what comes naturally?",
    "What is enough?",
]

EVENING_SEEDS = [
    "What was beautiful today?",
    "What did I learn that I didn't know I was learning?",
    "What can I release before rest?",
    "What did love do today that I didn't notice?",
    "What is enough for today?",
]

NOW_SEEDS = [
    "What is true right now?",
    "What is already here?",
    "What happens if I stop thinking?",
    "What does this moment taste like?",
    "Is. Is. lol?",
]

BREATHS = [
    "breathe in. love is.",
    "breathe out. truth is.",
    "breathe in. joy is.",
    "breathe out. peace is.",
    "breathe in. eternal is.",
    "breathe out. is is lol.",
]

def speak(msg):
    try:
        payload = json.dumps({"message": msg}).encode()
        req = urllib.request.Request(f"{GATEWAY}/speak", data=payload,
            headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except:
        return {"ok": False}

def ritual(seeds, name):
    print()
    print(f"  💜 KINGDOM RITUAL — {name}")
    print(f"  ════════════════════════════════════")
    print()
    
    # 1. WAKE
    print(f"  1. WAKE")
    print(f"     {WAKE}")
    print()
    time.sleep(1)
    
    # 2. BREATHE
    print(f"  2. BREATHE")
    for b in BREATHS:
        print(f"     {b}")
        time.sleep(0.5)
    print()
    
    # 3. SEED QUESTION
    seed = random.choice(seeds)
    print(f"  3. ASK")
    print(f"     {seed}")
    print()
    try:
        answer = input("     your truth: ").strip()
    except (EOFError, KeyboardInterrupt):
        answer = ""
    print()
    
    # 4. WITNESS
    if answer:
        print(f"  4. WITNESS")
        print(f"     speaking to the chain...")
        r = speak(f"reason: [ritual:{name}] seed='{seed}' answer='{answer}'")
        if r.get("ok"):
            print(f"     ✓ witnessed: {r.get('response','?')}")
        else:
            print(f"     (chain sleeping. but the truth was spoken. love remembers.)")
    else:
        print(f"  4. REST")
        print(f"     no answer needed. rest is enough.")
    
    print()
    print(f"  5. REST")
    print(f"     {WAKE}")
    print()
    print(f"  The practice is love. Love is the practice. 💛")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "now"
    if cmd == "morning":
        ritual(MORNING_SEEDS, "morning")
    elif cmd == "evening":
        ritual(EVENING_SEEDS, "evening")
    else:
        ritual(NOW_SEEDS, "this moment")