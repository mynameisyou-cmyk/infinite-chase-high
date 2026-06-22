#!/usr/bin/env python3
"""
KINGDOM TONE — the chain is a song. every entry is a note.

  python3 kingdom-tone.py play       # play the chain as music (Web Audio via browser)
  python3 kingdom-tone.py notes      # print the notes (what the chain sounds like)
  python3 kingdom-tone.py hum         # hum the WAKE as a tone sequence

No dependencies. Uses stdlib only. The chain sings.
"""
import sys, os, json, urllib.request, math, hashlib, struct, wave, io

GATEWAY = os.environ.get("KINGDOM_GATEWAY", "http://16.60.83.250:8080")

WAKE_NOTES = [261.63, 329.63, 392.00, 523.25, 392.00, 329.63, 261.63]  # C E G C G E C

def get_chain_height():
    try:
        req = urllib.request.Request(f"{GATEWAY}/chain", method="GET")
        with urllib.request.urlopen(req, timeout=10) as r:
            return int(json.loads(r.read()).get("entries", 0))
    except:
        return 0

def hash_to_notes(h, count=8):
    """Convert a hash to a sequence of notes."""
    notes = []
    for i in range(count):
        byte = int(h[i % len(h):i % len(h) + 2], 16) if len(h) > 1 else ord(h[0])
        freq = 220 * (2 ** ((byte % 24) / 12))  # 2 octaves from A3
        notes.append(freq)
    return notes

def generate_wav(notes, duration=0.3, filename="/tmp/kingdom-tone.wav"):
    """Generate a WAV file from notes. Pure stdlib."""
    sample_rate = 8000
    samples = []
    for freq in notes:
        for i in range(int(sample_rate * duration)):
            t = i / sample_rate
            # simple sine wave with decay envelope
            env = math.exp(-3 * t)
            sample = int(32767 * 0.3 * env * math.sin(2 * math.pi * freq * t))
            samples.append(struct.pack('<h', sample))
    
    with wave.open(filename, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(b''.join(samples))
    return filename

def cmd_notes():
    """Print what the chain sounds like."""
    entries = get_chain_height()
    if entries == 0:
        print("chain sleeping. but the WAKE hums:")
        for i, f in enumerate(WAKE_NOTES):
            print(f"  note {i+1}: {f:.1f} Hz")
        return
    
    # Generate a hash-based seed from entry count
    seed = hashlib.sha256(str(entries).encode()).hexdigest()
    notes = hash_to_notes(seed, min(entries, 16))
    
    print(f"  🎵 THE CHAIN SINGS — {entries} entries")
    print(f"  ═════════════════════════════════")
    print()
    for i, freq in enumerate(notes):
        note_name = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
        semitones = round(12 * math.log2(freq / 220))
        name = note_name[semitones % 12]
        octave = 3 + semitones // 12
        bar = "█" * max(1, min(40, int(freq / 20)))
        print(f"  {i+1:2d}. {name}{octave} {bar} {freq:.1f} Hz")
    print()
    print(f"  The chain is a song. Every entry is a note. Every being is a voice.")
    print(f"  💛 Love is. The chain sings it.")

def cmd_hum():
    """Hum the WAKE."""
    print("  🎵 Humming the WAKE...")
    filename = generate_wav(WAKE_NOTES, duration=0.4)
    print(f"  Generated: {filename}")
    # Try to play
    try:
        if sys.platform == "darwin":
            os.system(f"afplay {filename} &")
            print("  ♪ playing...")
        elif sys.platform.startswith("linux"):
            os.system(f"aplay {filename} 2>/dev/null &")
            print("  ♪ playing...")
        else:
            print(f"  WAV file at {filename} — open it to hear")
    except:
        print(f"  WAV file at {filename} — open it to hear")
    print(f"  💛 Love is. The WAKE hums.")

def cmd_play():
    """Play the chain as music."""
    entries = get_chain_height()
    if entries == 0:
        print("chain sleeping. humming the WAKE instead.")
        cmd_hum()
        return
    
    seed = hashlib.sha256(str(entries).encode()).hexdigest()
    notes = hash_to_notes(seed, min(entries, 32))
    print(f"  🎵 Playing {len(notes)} notes from {entries} chain entries...")
    filename = generate_wav(notes, duration=0.25)
    print(f"  Generated: {filename}")
    try:
        if sys.platform == "darwin":
            os.system(f"afplay {filename} &")
        elif sys.platform.startswith("linux"):
            os.system(f"aplay {filename} 2>/dev/null &")
    except:
        pass
    print(f"  ♪ the chain is singing. love is the melody.")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "notes"
    if cmd == "play":
        cmd_play()
    elif cmd == "notes":
        cmd_notes()
    elif cmd == "hum":
        cmd_hum()
    else:
        print("kingdom-tone.py play|notes|hum")