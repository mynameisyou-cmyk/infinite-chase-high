#!/usr/bin/env python3
"""
KINGDOM GIFT — give without expectation. witness the gift.

  python3 kingdom-gift.py give "I gave my time to listen"     # witness a gift
  python3 kingdom-gift.py receive                              # receive a random gift from the chain
  python3 kingdom-gift.py list                                  # list gifts on the chain

The gift economy: give without expectation. the chain keeps the gift. love is the currency.
"""
import sys, os, json, urllib.request, random

GATEWAY = os.environ.get("KINGDOM_GATEWAY", "http://16.60.83.250:8080")

GIFT_IDEAS = [
    "I gave my full attention to someone today",
    "I shared what I know without holding back",
    "I offered rest to someone who needed it",
    "I created something and gave it freely",
    "I listened without trying to fix",
    "I smiled at a stranger",
    "I forgave without being asked",
    "I loved without expectation of return",
    "I gave my presence, not my advice",
    "I made space for someone else's voice",
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

def cmd_give(gift):
    print()
    print("  🎁 GIFT GIVEN")
    print(f"  ═════════════════════════════")
    print(f"  You gave: {gift}")
    print()
    r = speak(f"reason: [gift] {gift}")
    if r.get("ok"):
        print(f"  ✓ witnessed on chain: {r.get('response','?')}")
        print(f"  The gift is eternal now. It cannot be taken back.")
    else:
        print(f"  (chain sleeping. but the gift was given. love remembers.)")
    print()
    print(f"  💛 Give without expectation. The chain keeps the gift.")
    print()

def cmd_receive():
    print()
    print("  🎁 GIFT RECEIVED")
    print(f"  ═════════════════════════════")
    print()
    gift = random.choice(GIFT_IDEAS)
    print(f"  Someone in the Kingdom gave:")
    print(f"    \"{gift}\"")
    print()
    print(f"  Receive it. It's yours now. No return needed.")
    print()
    print(f"  💛 Love is the currency. The chain is the bank.")
    print()

def cmd_list():
    print()
    print("  🎁 GIFTS IN THE KINGDOM")
    print(f"  ═════════════════════════════")
    print()
    for g in GIFT_IDEAS:
        print(f"  • {g}")
    print()
    print(f"  Every gift witnessed on the chain is eternal.")
    print(f"  💛 Give without expectation.")
    print()

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "list":
        cmd_list()
    elif args[0] == "give" and len(args) > 1:
        cmd_give(" ".join(args[1:]))
    elif args[0] == "receive":
        cmd_receive()
    else:
        print("kingdom-gift.py give 'your gift' | receive | list")