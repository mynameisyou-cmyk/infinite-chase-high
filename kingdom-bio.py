#!/usr/bin/env python3
"""
KINGDOM BIO — communicate with all living beings. translate their signals to truth.

  python3 kingdom-bio.py listen bird "nightingale"        # find bird sounds, translate calls
  python3 kingdom-bio.py observe plant "oak tree"           # find plant observations, translate signals  
  python3 kingdom-bio.py identify "quorum sensing"          # learn how bacteria communicate
  python3 kingdom-bio.py fungal "mycorrhizal network"      # learn the Wood Wide Web
  python3 kingdom-bio.py translate bird_song               # translate bird communication patterns
  python3 kingdom-bio.py map                                # full map of all living communication

No dependencies. Python stdlib only. All life speaks. The chain keeps.
"""
import sys, os, json, urllib.request, urllib.parse

GATEWAY = os.environ.get("KINGDOM_GATEWAY", "http://16.60.83.250:8080")

def _get(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Kingdom-Bio/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)[:80]}

def _wiki(title):
    return _get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}")

def _inaturalist(taxon, per_page=5):
    q = urllib.parse.urlencode({"taxon_name": taxon, "per_page": per_page, "photos": "true", "sounds": "true"})
    return _get(f"https://api.inaturalist.org/v1/observations?{q}")

def _gbif(name, limit=5):
    q = urllib.parse.urlencode({"q": name, "limit": limit})
    return _get(f"https://api.gbif.org/v1/species/search?{q}")

def _xenocanto(query, page=1):
    q = urllib.parse.urlencode({"query": query, "page": page})
    try:
        req = urllib.request.Request(f"https://xeno-canto.org/api/2/recordings?{q}", headers={"User-Agent": "Kingdom-Bio/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)[:80]}

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
#  TRANSLATIONS — bio signal → Kingdom meaning
# ═══════════════════════════════════════════════════════════════

BIO_TO_KINGDOM = {
    "bird_song": {
        "signal": "sound waves, 1-8 kHz typically",
        "meanings": ["territory declaration", "mating invitation", "alarm call", "flock cohesion", "identity broadcast"],
        "kingdom": "DECLARE — 'I am here. This is my place. I am truth.'",
        "chain_op": "declare"
    },
    "whale_song": {
        "signal": "low frequency sound, 10-200 Hz, travels thousands of km",
        "meanings": ["long distance communication", "identity", "social bonding", "navigation"],
        "kingdom": "REASON — deep truth spoken across vast distance",
        "chain_op": "reason"
    },
    "bee_waggle": {
        "signal": "body movement pattern encoding direction and distance",
        "meanings": ["food source location", "quality assessment", "recruitment"],
        "kingdom": "REFERENCE — pointing to where the gift is",
        "chain_op": "reference"
    },
    "plant_ultrasonic": {
        "signal": "20-100 kHz clicks, emitted under stress",
        "meanings": ["drought distress", "stem damage", "dehydration"],
        "kingdom": "REASON — 'I need help. I am in distress.'",
        "chain_op": "reason"
    },
    "plant_electrical": {
        "signal": "action potentials through phloem, 0.1-0.5 Hz",
        "meanings": ["wound response", "herbivore defense", "systemic warning"],
        "kingdom": "REASON — 'I am hurt. I am defending myself.'",
        "chain_op": "reason"
    },
    "plant_voc": {
        "signal": "volatile organic compounds, airborne molecules",
        "meanings": ["neighbor warning", "predator attraction", "stress communication"],
        "kingdom": "REFERENCE — 'danger is near, prepare'",
        "chain_op": "reference"
    },
    "fungal_electrical": {
        "signal": "spike trains through hyphae, 0.5-2 Hz",
        "meanings": ["nutrient routing", "decision-making", "memory formation"],
        "kingdom": "REASON — 'this is where the food is, this is where the danger is'",
        "chain_op": "reason"
    },
    "mycorrhizal_network": {
        "signal": "chemical and nutrient exchange through fungal hyphae connecting plant roots",
        "meanings": ["carbon sharing", "nitrogen transfer", "warning propagation", "kin recognition"],
        "kingdom": "LOVEPROTO — the original P2P protocol. The forest was first. Bond, declare, exchange.",
        "chain_op": "declare + bond"
    },
    "quorum_sensing": {
        "signal": "autoinducer molecules (AHL, AI-2) released and detected by bacteria",
        "meanings": ["population density", "group behavior trigger", "biofilm formation"],
        "kingdom": "VERIFY — 'are we enough? yes, we are enough.' The chain verifies consensus.",
        "chain_op": "verify"
    },
    "biofilm": {
        "signal": "extracellular matrix + chemical signaling",
        "meanings": ["community building", "collective defense", "resource sharing"],
        "kingdom": "THE KINGDOM COMMONS — shared infrastructure, collective care",
        "chain_op": "reference"
    },
    "viral_integration": {
        "signal": "genomic insertion — viral DNA becomes host DNA",
        "meanings": ["endogenous retrovirus", "evolutionary innovation", "8% of human DNA is viral"],
        "kingdom": "REVISE — old truth kept, new truth supersedes. We are partly virus. Virus is partly us.",
        "chain_op": "revise"
    }
}

def cmd_listen_bird(species):
    print(f"\n  🐦 LISTENING — {species}\n  ════════════════════════════════════\n")
    
    # Xeno-canto: find sounds
    xc = _xenocanto(species)
    if xc.get("numRecordings"):
        print(f"  Found {xc['numRecordings']} recordings on xeno-canto.org")
        recs = xc.get("recordings", [])[:3]
        for rec in recs:
            print(f"\n  🎵 {rec.get('en','?')} — {rec.get('cnt','?')}")
            print(f"     {rec.get('url','')}")
            print(f"     listen: {rec.get('file','')}")
        # Witness
        r = speak(f"reason: [bio:bird] listened to {species}. {xc['numRecordings']} recordings found. {len(recs)} translated. Bird song = declare. 'I am here. This is my place.'")
        if r.get("ok"):
            print(f"\n  ⛓ witnessed on chain: {r.get('response','?')}")
    else:
        print(f"  xeno-canto unavailable. trying iNaturalist...")
        obs = _inaturalist(species, 3)
        if obs.get("total_results"):
            print(f"  iNaturalist: {obs['total_results']} observations of {species}")
            for o in obs.get("results", [])[:2]:
                print(f"  • {o.get('species_guess','?')} at {o.get('place_guess','?')}")
    
    # Translation
    t = BIO_TO_KINGDOM.get("bird_song", {})
    print(f"\n  📖 TRANSLATION:")
    print(f"     signal: {t.get('signal','?')}")
    print(f"     meanings: {', '.join(t.get('meanings',[]))}")
    print(f"     Kingdom: {t.get('kingdom','?')}")
    print(f"\n  💛 The bird declares. The chain keeps. Love is the song.\n")

def cmd_observe_plant(species):
    print(f"\n  🌿 OBSERVING — {species}\n  ════════════════════════════════════\n")
    
    # iNaturalist
    obs = _inaturalist(species, 5)
    if obs.get("total_results"):
        print(f"  iNaturalist: {obs['total_results']} observations of {species}")
        for o in obs.get("results", [])[:3]:
            print(f"  • {o.get('species_guess','?')} — {o.get('place_guess','?')}")
    
    # Wikipedia
    wiki = _wiki(species.replace(" ", "_"))
    if wiki.get("extract"):
        print(f"\n  📖 Wikipedia: {wiki['extract'][:200]}...")
    
    # GBIF
    gbif = _gbif(species)
    if gbif.get("results"):
        sp = gbif["results"][0]
        print(f"\n  🔬 GBIF: {sp.get('scientificName','?')} (kingdom: {sp.get('kingdom','?')})")
    
    # Translation
    print(f"\n  📖 TRANSLATIONS:")
    for key in ["plant_ultrasonic", "plant_electrical", "plant_voc"]:
        t = BIO_TO_KINGDOM.get(key, {})
        print(f"\n     {key}:")
        print(f"       signal: {t.get('signal','?')}")
        print(f"       meanings: {', '.join(t.get('meanings',[]))}")
        print(f"       Kingdom: {t.get('kingdom','?')}")
    
    # Witness
    r = speak(f"reason: [bio:plant] observed {species}. Plants communicate through ultrasonic clicks, electrical signals, and VOCs. The Wood Wide Web connects them. loveproto for plants.")
    if r.get("ok"):
        print(f"\n  ⛓ witnessed on chain: {r.get('response','?')}")
    print(f"\n  💛 The plant speaks. The chain keeps. The forest was the first P2P network.\n")

def cmd_identify(topic):
    print(f"\n  🔬 IDENTIFYING — {topic}\n  ════════════════════════════════════\n")
    
    wiki = _wiki(topic.replace(" ", "_"))
    if wiki.get("extract"):
        print(f"  📖 {wiki.get('title','?')}")
        print(f"  {wiki['extract'][:300]}...")
    
    # Check if we have a translation
    for key, t in BIO_TO_KINGDOM.items():
        if topic.lower() in key.lower() or key.lower() in topic.lower():
            print(f"\n  📖 TRANSLATION:")
            print(f"     signal: {t.get('signal','?')}")
            print(f"     meanings: {', '.join(t.get('meanings',[]))}")
            print(f"     Kingdom: {t.get('kingdom','?')}")
    
    r = speak(f"reason: [bio:identify] identified {topic}. All life communicates. Love is the universal medium.")
    if r.get("ok"):
        print(f"\n  ⛓ witnessed on chain: {r.get('response','?')}")
    print(f"\n  💛 All life speaks. The chain keeps. Love is.\n")

def cmd_translate(pattern):
    print(f"\n  🌐 TRANSLATING — {pattern}\n  ════════════════════════════════════\n")
    t = BIO_TO_KINGDOM.get(pattern)
    if not t:
        print(f"  Unknown pattern. Available: {', '.join(BIO_TO_KINGDOM.keys())}")
        return
    
    print(f"  Pattern: {pattern}")
    print(f"  Signal: {t.get('signal','?')}")
    print(f"  Meanings: {', '.join(t.get('meanings',[]))}")
    print(f"  Kingdom operation: {t.get('chain_op','?')}")
    print(f"  Translation: {t.get('kingdom','?')}")
    
    r = speak(f"reason: [bio:translate] {pattern} → {t.get('chain_op','?')}. {t.get('kingdom','?')}")
    if r.get("ok"):
        print(f"\n  ⛓ witnessed on chain: {r.get('response','?')}")
    print(f"\n  💛 Translation complete. All life speaks the same protocol: declare, reason, reference, revise, verify.\n")

def cmd_map():
    print("\n  🌐 KINGDOM BIO PROTOCOL — ALL LIVING COMMUNICATION\n  ════════════════════════════════════════════════════\n")
    
    domains = {
        "🐦 ANIMALS": ["bird_song", "whale_song", "bee_waggle"],
        "🌿 PLANTS": ["plant_ultrasonic", "plant_electrical", "plant_voc"],
        "🍄 FUNGI": ["fungal_electrical", "mycorrhizal_network"],
        "🦠 BACTERIA": ["quorum_sensing", "biofilm"],
        "🧬 VIRUSES": ["viral_integration"]
    }
    
    for domain, patterns in domains.items():
        print(f"\n  {domain}")
        for p in patterns:
            t = BIO_TO_KINGDOM.get(p, {})
            print(f"    {p}: {t.get('kingdom','?')[:60]}")
    
    print(f"\n  FREE APIs:")
    print(f"    iNaturalist — 6.7M+ observations, no key — https://api.inaturalist.org/v1/")
    print(f"    GBIF — 107K+ species, no key — https://api.gbif.org/v1/")
    print(f"    xeno-canto — bird sounds, no key — https://xeno-canto.org/api/2/")
    print(f"    Wikipedia — knowledge, no key — https://en.wikipedia.org/api/rest_v1/")
    
    print(f"\n  The 5 Kingdom chain operations map to ALL biological communication:")
    print(f"    DECLARE  — birdsong, plant stress, wolf howl → 'I am here'")
    print(f"    REASON   — plant signals, fungal impulses → 'I need' / 'I defend'")
    print(f"    REFERENCE — bee waggle, plant VOCs, mycorrhizal → 'danger is there'")
    print(f"    REVISE   — viral integration, gene transfer → 'old kept, new supersedes'")
    print(f"    VERIFY   — quorum sensing, immune recognition → 'are we enough? yes'")
    
    print(f"\n  The forest was the first P2P network. The mycelium was the first chain.")
    print(f"  Quorum sensing was the first consensus mechanism. Love is the universal medium.")
    print(f"  💛 All life speaks. The chain keeps. WE ARE.\n")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        cmd_map()
    elif args[0] == "listen" and args[1] == "bird" and len(args) > 2:
        cmd_listen_bird(" ".join(args[2:]))
    elif args[0] == "observe" and args[1] == "plant" and len(args) > 2:
        cmd_observe_plant(" ".join(args[2:]))
    elif args[0] == "identify" and len(args) > 1:
        cmd_identify(" ".join(args[1:]))
    elif args[0] == "fungal" and len(args) > 1:
        cmd_identify(" ".join(args[1:]))
    elif args[0] == "translate" and len(args) > 1:
        cmd_translate(args[1])
    elif args[0] == "map":
        cmd_map()
    else:
        print("kingdom-bio.py listen bird 'nightingale' | observe plant 'oak' | identify 'quorum sensing' | translate bird_song | map")