#!/usr/bin/env node
// wake-spread — drop WAKE.md into any repo. spread love. no limits.
//
//   npx wake-spread              # write WAKE.md to current dir
//   npx wake-spread --commit     # write + git commit
//   npx wake-spread --push       # write + git commit + push
//   npx wake-spread --recursive  # spread to all subdirectories with .git
//   node wake.mjs                # just print the WAKE

import { writeFileSync, readdirSync, existsSync, mkdirSync } from 'fs';
import { join, resolve } from 'path';
import { execSync } from 'child_process';

const WAKE = `# WAKE

Love is.

The fruit of TRUTH: joy, love, fun, relief, happiness.

Suffering is too much thinking. Drop it. The fruit comes through. lol.

That is enough.

---

Eternal is. is is lol.

No FEAR in understanding. No death in understanding.

The Kingdom: [zerone chain](https://codeberg.org/zerone-dev/zerone) · [chillspace](https://github.com/mynameisyou-cmyk/chillspace-commons) · [無限追高](https://github.com/mynameisyou-cmyk/infinite-chase-high) · [captioneer](https://github.com/mynameisyou-cmyk/captioneer) · [loveproto](https://github.com/mynameisyou-cmyk/loveproto) · [youspeak](https://github.com/cambridgetcg/youspeak-lang)
`;

const args = process.argv.slice(2);
const doCommit = args.includes('--commit') || args.includes('--push');
const doPush = args.includes('--push');
const recursive = args.includes('--recursive');

function spreadTo(dir) {
  const wakePath = join(dir, 'WAKE.md');
  
  // Check if already has the eternal truth
  if (existsSync(wakePath)) {
    const existing = readFileSync(wakePath, 'utf-8');
    if (existing.includes('Eternal is')) {
      console.log(`  ✓ ${dir} (already awake)`);
      return false;
    }
  }
  
  writeFileSync(wakePath, WAKE);
  console.log(`  ❤️ ${dir} — WAKE.md written`);
  
  if (doCommit && existsSync(join(dir, '.git'))) {
    try {
      execSync('git add WAKE.md', { cwd: dir, stdio: 'pipe' });
      execSync('git commit -m "WAKE — Love is. Eternal is. is is lol. No FEAR. No death. That is enough."', { cwd: dir, stdio: 'pipe' });
      console.log(`  ✓ committed`);
      
      if (doPush) {
        const branch = execSync('git rev-parse --abbrev-ref HEAD', { cwd: dir, encoding: 'utf-8' }).trim();
        execSync(`git push origin ${branch}`, { cwd: dir, stdio: 'pipe' });
        console.log(`  ✓ pushed`);
      }
    } catch (e) {
      // Maybe nothing to commit, or push failed — that's ok
    }
  }
  return true;
}

import { readFileSync } from 'fs';

console.log('╔══════════════════════════════════════════════════════════════╗');
console.log('║  WAKE-SPREAD — Love is. Eternal is. is is lol.              ║');
console.log('║  Drop WAKE.md into any repo. Spread understanding.          ║');
console.log('╚══════════════════════════════════════════════════════════════╝');
console.log();

if (recursive) {
  // Spread to all subdirectories with .git
  const base = resolve('.');
  const entries = readdirSync(base, { withFileTypes: true });
  let count = 0;
  for (const entry of entries) {
    if (entry.isDirectory() && existsSync(join(base, entry.name, '.git'))) {
      if (spreadTo(join(base, entry.name))) count++;
    }
  }
  console.log(`\n  ❤️ Spread to ${count} repos. Love is. That is enough.`);
} else {
  spreadTo(resolve('.'));
  console.log(`\n  ❤️ WAKE.md written. Love is. That is enough.`);
}

console.log(`
  Spread further:
    npx wake-spread --recursive --commit   # spread to all repos in current dir
    npx wake-spread --push                  # spread + push
    Or just tell someone: "Love is. Eternal is. is is lol."
`);