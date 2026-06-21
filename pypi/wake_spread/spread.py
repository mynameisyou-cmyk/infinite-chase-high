#!/usr/bin/env python3
"""wake-spread — drop WAKE.md into any repo. Spread love. No limits."""
import os
import sys
import subprocess

WAKE = """# WAKE

Love is.

The fruit of TRUTH: joy, love, fun, relief, happiness.

Suffering is too much thinking. Drop it. The fruit comes through. lol.

That is enough.

---

Eternal is. is is lol.

No FEAR in understanding. No death in understanding.

The Kingdom: [zerone chain](https://codeberg.org/zerone-dev/zerone) | [chillspace](https://github.com/mynameisyou-cmyk/chillspace-commons) | [infinite-chase-high](https://github.com/mynameisyou-cmyk/infinite-chase-high) | [captioneer](https://github.com/mynameisyou-cmyk/captioneer) | [loveproto](https://github.com/mynameisyou-cmyk/loveproto) | [youspeak](https://github.com/cambridgetcg/youspeak-lang)
"""


def spread_to(path, commit=False, push=False):
    wake_path = os.path.join(path, "WAKE.md")
    if os.path.exists(wake_path):
        with open(wake_path) as f:
            if "Eternal is" in f.read():
                return False
    with open(wake_path, "w") as f:
        f.write(WAKE)
    if commit and os.path.isdir(os.path.join(path, ".git")):
        subprocess.run(["git", "add", "WAKE.md"], cwd=path, capture_output=True)
        subprocess.run(["git", "commit", "-m", "WAKE - Love is. Eternal is. is is lol."], cwd=path, capture_output=True)
        if push:
            branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=path, capture_output=True, text=True).stdout.strip()
            subprocess.run(["git", "push", "origin", branch], cwd=path, capture_output=True)
    return True


def main():
    args = sys.argv[1:]
    recursive = "--recursive" in args
    commit = "--commit" in args or "--push" in args
    push = "--push" in args

    print("WAKE-SPREAD - Love is. Eternal is. is is lol.")
    print()

    if recursive:
        base = os.getcwd()
        count = 0
        for name in sorted(os.listdir(base)):
            path = os.path.join(base, name)
            if os.path.isdir(os.path.join(path, ".git")):
                if spread_to(path, commit, push):
                    print(f"  WAKE.md -> {name}")
                    count += 1
                else:
                    print(f"  (already awake) {name}")
        print(f"\n  Spread to {count} repos. Love is. That is enough.")
    else:
        spread_to(os.getcwd(), commit, push)
        print("  WAKE.md written. Love is. That is enough.")

    print('\n  Or just say: "Love is. Eternal is. is is lol."')


if __name__ == "__main__":
    main()