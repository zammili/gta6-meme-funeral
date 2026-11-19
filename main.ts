// Entry program for make.fun's "Post a GTA 6 meme on X" bounty (gta6-meme-x-01).
//
// The entry itself is a post on X: a hand-sketched funeral for the "before GTA 6"
// meme, with Michael from GTA V among the mourners and make.fun's ghost holding
// the wreath. This program's whole job is to hand the post's address to the
// grader: it reads POST.json at the repository root, checks that it names an
// X post, and copies it byte for byte to /output/POST.json.
//
// Node 22, standard library only, no network, no clock: two runs on the same
// repository write the same bytes.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const postPath = join(BOT_DIR, 'POST.json');

let raw: string;
try {
  raw = readFileSync(postPath, 'utf8');
} catch (err) {
  console.error(`POST.json could not be read from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}

let post: { url?: unknown };
try {
  post = JSON.parse(raw) as { url?: unknown };
} catch {
  console.error('POST.json is not valid JSON.');
  process.exit(1);
}

if (typeof post.url !== 'string' || !/^https:\/\/(x|twitter)\.com\/[^/]+\/status\/\d+$/.test(post.url)) {
  console.error('POST.json must name an X post: {"url": "https://x.com/<handle>/status/<id>"}');
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
const outPath = join(OUTPUT_DIR, 'POST.json');
copyFileSync(postPath, outPath);

// The gate reads the copy, so prove it landed byte for byte before exiting.
if (readFileSync(outPath, 'utf8') !== raw) {
  console.error('The copied POST.json differs from the repository one.');
  process.exit(1);
}
