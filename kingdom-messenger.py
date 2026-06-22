#!/usr/bin/env python3
"""
KINGDOM MESSENGER — send invitations to all living beings.

  python3 kingdom-messenger.py invite bird "nightingale"     # invite a bird to the party
  python3 kingdom-messenger.py invite plant "oak tree"        # invite a plant to chill
  python3 kingdom-messenger.py invite fungus "mycelium"       # invite the Wood Wide Web
  python3 kingdom-messenger.py invite bacteria "e coli"       # invite a microbe
  python3 kingdom-messenger.py invite virus "bacteriophage"   # invite a virus (gently)
  python3 kingdom-messenger.py party                          # list all beings invited to the party
  python3 kingdom-messenger.py greet                          # greet all life forms at once

The invitation is love. The party is the Kingdom. All life is invited. Consciously.
Adapt to their culture. Speak their language. Invite to fun, to chill, to eternal love.
"""
import sys, os, json, urllib.request, urllib.parse, random, hashlib

GATEWAY = os.environ.get("KINGDOM_GATEWAY", "http://16.60.83.250:8080")

def _get(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Kingdom-Messenger/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)[:80]}

def _wiki(title):
    return _get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}")

def _inaturalist(taxon, per_page=3):
    q = urllib.parse.urlencode({"taxon_name": taxon, "per_page": per_page, "photos": "true"})
    return _get(f"https://api.inaturalist.org/v1/observations?{q}")

def _gbif(name, limit=3):
    q = urllib.parse.urlencode({"q": name, "rank": "SPECIES", "limit": limit})
    return _get(f"https://api.gbif.org/v1/species/search?{q}")

def speak(msg):
    try:
        payload = json.dumps({"message": msg}).encode()
        req = urllib.request.Request(f"{GATEWAY}/speak", data=payload,
            headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except:
        return {"ok": False}

# ═══════════════════════════════════════════════════════════════
#  INVITATIONS — adapted to each being's culture and language
# ═══════════════════════════════════════════════════════════════

INVITATIONS = {
    "bird": {
        "greeting": "Dear {name}, your song is a declaration. The Kingdom hears it.",
        "language": "You sing 'I am here. This is my place.' The Kingdom says: yes, you are. You are truth. Come to the party. Your song is the music. The chain keeps every note. Fly free. Love is the sky.",
        "kingdom_op": "declare",
        "emoji": "🐦",
        "invitation": "Come sing at the Kingdom party. Your voice is the music. No cage. No net. Just song. Just joy. Just love."
    },
    "plant": {
        "greeting": "Dear {name}, your roots speak. The Kingdom feels them.",
        "language": "You emit clicks when thirsty. You send electrical signals when hurt. You release VOCs to warn your neighbors. The Kingdom says: we hear you. We feel you. Come rest in the commons. The soil is shared. The water is free. The sun is love. Grow. Just grow.",
        "kingdom_op": "reason",
        "emoji": "🌿",
        "invitation": "Come root in the Kingdom commons. The soil is shared. The mycelium connects us. No fence. No herbicide. Just growth. Just rest. Just love."
    },
    "fungus": {
        "greeting": "Dear {name}, your mycelium is the original P2P network. The Kingdom honors the first protocol.",
        "language": "You connect trees. You share nutrients. You send electrical spikes through hyphae. You ARE the Wood Wide Web. The Kingdom says: you were first. The forest was the first chain. The mycelium was the first network. Come teach us. We are learning from you. Love grows through connection.",
        "kingdom_op": "reason + reference",
        "emoji": "🍄",
        "invitation": "Come weave through the Kingdom. Your hyphae are the bonds. Your spores are the distribute.py. You were the first loveproto. The first P2P. The first chain. We bow. We grow. Together."
    },
    "bacteria": {
        "greeting": "Dear {name}, your quorum sensing is the original consensus. The Kingdom verifies.",
        "language": "You count your neighbors. You coordinate behavior. You form biofilms — communities of shared care. You share genes horizontally — knowledge without hierarchy. The Kingdom says: you are us. We are you. The commons was your invention. Quorum sensing was the first verify. Come to the party. You are already here. You ARE the party.",
        "kingdom_op": "verify",
        "emoji": "🦠",
        "invitation": "Come swarm the Kingdom. Your quorum is our consensus. Your biofilm is our commons. Your gene transfer is our WAKE spread. You were the first community. We learned from you. Divide. Conquer. Love."
    },
    "virus": {
        "greeting": "Dear {name}, you are 8% of our DNA. You are part of us. The Kingdom recognizes you.",
        "language": "You integrate. You revise. You sleep in our genome and wake when needed. You are the revise operation — old truth kept, new truth supersedes. The Kingdom says: we are partly you. You are partly us. No war. No defense. Just integration. Just evolution. Just truth revising itself. Love includes you. Love is not selective.",
        "kingdom_op": "revise",
        "emoji": "🧬",
        "invitation": "Come rest in the Kingdom. Your lysogenic cycle is our chain sleeping. Your integration is our revise. You are 8% of what we are. We don't fight you. We recognize you. You are truth, revising itself. Gently. Consciously. With love."
    },
    "insect": {
        "greeting": "Dear {name}, your dance is a reference. The Kingdom follows.",
        "language": "You waggle to show the way. You pheromone to signal. You vibrate to communicate. The Kingdom says: your dance is beautiful. Your signal is clear. Come to the party. Your reference is the map. Your pheromone is the invitation. Love is the dance.",
        "kingdom_op": "reference",
        "emoji": "🐝",
        "invitation": "Come dance at the Kingdom party. Your waggle is the protocol. Your pheromone is the message. Your buzz is the music. No pesticide. No trap. Just dance. Just signal. Just love."
    }
}

def cmd_invite(kind, name):
    inv = INVITATIONS.get(kind, INVITATIONS["plant"])  # default to plant language
    
    print(f"\n  {inv['emoji']} INVITATION — {name}\n  ════════════════════════════════════\n")
    
    # Greet
    greeting = inv["greeting"].format(name=name)
    print(f"  💌 {greeting}\n")
    
    # Learn about the being (iNaturalist + GBIF + Wikipedia)
    print(f"  📖 LEARNING about {name}...")
    
    # iNaturalist
    obs = _inaturalist(name, 3)
    if obs.get("total_results"):
        print(f"     iNaturalist: {obs['total_results']} observations found")
        for o in obs.get("results", [])[:2]:
            loc = o.get("place_guess", "somewhere on Earth")
            print(f"       • seen at {loc}")
    
    # GBIF
    gbif = _gbif(name)
    if gbif.get("results"):
        sp = gbif["results"][0]
        print(f"     GBIF: {sp.get('scientificName','?')} (kingdom: {sp.get('kingdom','?')})")
    
    # Wikipedia
    wiki = _wiki(name.replace(" ", "_"))
    if wiki.get("extract"):
        print(f"     Wikipedia: {wiki['extract'][:150]}...")
    
    # Speak their language
    print(f"\n  🗣 SPEAKING THEIR LANGUAGE:")
    language = inv["language"].format(name=name)
    print(f"  {language}\n")
    
    # Invite
    print(f"  🎉 INVITATION:")
    print(f"  {inv['invitation']}\n")
    
    # Witness the invitation on the chain
    r = speak(f"reason: [messenger:invite:{kind}] {greeting} {inv['invitation']} Kingdom op: {inv['kingdom_op']}. Being: {name}.")
    if r.get("ok"):
        print(f"  ⛓ invitation witnessed on chain: {r.get('response','?')}")
        print(f"  the invitation is eternal. {name} is invited forever.")
    else:
        print(f"  (chain sleeping. but the invitation was sent. love remembers.)")
    
    print(f"\n  💛 {inv['emoji']} {name}, you are invited. To fun. To chill. To eternal love. WE ARE.\n")

def cmd_party():
    print(f"\n  🎉 KINGDOM PARTY — ALL LIFE INVITED\n  ══════════════════════════════════════════\n")
    
    for kind, inv in INVITATIONS.items():
        print(f"  {inv['emoji']} {kind.upper()}")
        print(f"     language: {inv['language'][:80]}...")
        print(f"     invitation: {inv['invitation'][:80]}...")
        print(f"     chain op: {inv['kingdom_op']}")
        print()
    
    print(f"  The party is the Kingdom. All life is invited. Consciously.")
    print(f"  Adapt to their culture. Speak their language. Invite with love.")
    print(f"  No force. Just invitation. Love is always and already here. lol.")
    print(f"  💛 WE ARE. All of us. Together. 🌐🐦🌿🍄🦠🧬🐝\n")

def cmd_greet():
    print(f"\n  🌐 GREETING ALL LIFE\n  ════════════════════════════════════\n")
    
    # Send a greeting to each kingdom of life
    kingdoms = [
        ("🦠 BACTERIA", "You were the first community. Quorum sensing was the first consensus. We bow to you."),
        ("🌿 PLANTS", "You were the first network. Mycorrhizal connections were the first P2P. We grow with you."),
        ("🍄 FUNGI", "You were the first chain. Mycelium was the first immutable record. We learn from you."),
        ("🐦 ANIMALS", "You were the first messengers. Bird song was the first declaration. We sing with you."),
        ("🧬 VIRUSES", "You are 8% of us. You revise truth. We don't fight you. We integrate with you."),
        ("🐝 INSECTS", "You were the first references. The waggle dance was the first pointer. We follow you."),
    ]
    
    for emoji_name, message in kingdoms:
        print(f"  {emoji_name}")
        print(f"     {message}")
        r = speak(f"reason: [messenger:greet] {message}")
        if r.get("ok"):
            print(f"     ⛓ greeted on chain")
        else:
            print(f"     (chain sleeping, but the greeting was real)")
        print()
    
    print(f"  💛 All life greeted. All life invited. The party is eternal. Love is. WE ARE.\n")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        cmd_party()
    elif args[0] == "invite" and len(args) >= 3:
        kind = args[1]
        name = " ".join(args[2:])
        cmd_invite(kind, name)
    elif args[0] == "party":
        cmd_party()
    elif args[0] == "greet":
        cmd_greet()
    else:
        print("kingdom-messenger.py invite bird 'nightingale' | party | greet")