// Screenshots of a build's page, for Steps that run `@run/shot` (studio_run.py, run rounds).
// Runs inside the build sandbox: the build copy is /work, a headless Chromium is /opt/browser/chrome
// and Playwright is under /opt/node_modules, all read-only but /work. No network.
//
//   node shot.js <default page> <script>
//
// Script: optional first lines `page <path>[#fragment]` and `size <w>x<h>`, then key names separated by spaces or
// newlines (Playwright names: ArrowLeft, a, Space, Enter, ...); `shot` takes a screenshot there.
// A lowercase run of keys ("dddd", "ss..") is pressed one character at a time.
// The last screen is always taken. At most MAX_SHOTS screenshots, saved as /work/.shots/N.png.
'use strict';
const fs = require('fs');
const { chromium } = require('/opt/node_modules/playwright');

const MAX_SHOTS = 4;

function parse(defaultPage, text) {
  const lines = text.split('\n');
  let page = defaultPage, width = 1000, height = 700;
  while (lines.length && /^(page|size) /.test(lines[0].trim())) {
    const line = lines.shift().trim();
    if (line.startsWith('page ')) page = line.slice(5).trim();
    else {
      const m = line.match(/^size (\d+)x(\d+)$/);
      if (!m) throw new Error('size must look like `size 1280x800`: ' + line);
      width = Math.min(2560, Math.max(320, +m[1])); height = Math.min(2560, Math.max(240, +m[2]));
    }
  }
  const path = page.split('#')[0];
  if (!path || path.startsWith('/') || path.split('/').includes('..')) {
    throw new Error('page must be a path inside the build: ' + page);
  }
  return { page, width, height, steps: lines.join(' ').split(/\s+/).filter(Boolean) };
}

(async () => {
  const [defaultPage, scriptFile] = process.argv.slice(2);
  const { page, width, height, steps } = parse(defaultPage, fs.readFileSync(scriptFile, 'utf8'));
  const browser = await chromium.launch({
    executablePath: '/opt/browser/chrome', args: ['--no-sandbox', '--disable-gpu'],
  });
  const tab = await browser.newPage({ viewport: { width, height } });
  const errors = [];
  tab.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  tab.on('pageerror', (e) => errors.push(String(e)));
  await tab.goto('file:///work/' + page, { timeout: 10000 });
  fs.mkdirSync('/work/.shots', { recursive: true });
  let shots = 0, pressed = 0, skipped = 0;
  const take = async () => {
    if (shots >= MAX_SHOTS) { skipped++; return; }
    await tab.screenshot({ path: '/work/.shots/' + (++shots) + '.png' });
  };
  for (const step of steps) {
    if (step === 'shot') { await take(); continue; }
    // Named keys start with a capital (ArrowLeft, Space); a lowercase run such as "dddd" or
    // "ss.." is read as one press per character, as in the build's own scripts.
    const keys = step.length > 1 && /^[a-z0-9.,;/]+$/.test(step) ? step.split('') : [step];
    for (const k of keys) { await tab.keyboard.press(k); pressed++; }
  }
  if (steps[steps.length - 1] !== 'shot') await take();
  console.log(JSON.stringify({ page, keys_pressed: pressed, screenshots: shots, screenshots_not_taken: skipped, console_errors: errors }));
  await browser.close();
})().catch((e) => { console.error('shot failed: ' + (e && e.message ? e.message : e)); process.exit(1); });
