// Screenshots of a build's page, for Steps that run `@run/shot` (studio_run.py, run rounds).
// Runs inside the build sandbox: the build copy is /work, a headless Chromium is /opt/browser/chrome
// and Playwright is under /opt/node_modules, all read-only but /work. No network.
//
//   node shot.js <default page> <script>
//
// Script: an optional first line `page <path>[#fragment]`, then key names separated by spaces or
// newlines (Playwright names: ArrowLeft, a, Space, Enter, ...); `shot` takes a screenshot there.
// The last screen is always taken. At most MAX_SHOTS screenshots, saved as /work/.shots/N.png.
'use strict';
const fs = require('fs');
const { chromium } = require('/opt/node_modules/playwright');

const MAX_SHOTS = 4;

function parse(defaultPage, text) {
  const lines = text.split('\n');
  let page = defaultPage;
  const first = (lines[0] || '').trim();
  if (first.startsWith('page ')) { page = first.slice(5).trim(); lines.shift(); }
  const path = page.split('#')[0];
  if (!path || path.startsWith('/') || path.split('/').includes('..')) {
    throw new Error('page must be a path inside the build: ' + page);
  }
  return { page, steps: lines.join(' ').split(/\s+/).filter(Boolean) };
}

(async () => {
  const [defaultPage, scriptFile] = process.argv.slice(2);
  const { page, steps } = parse(defaultPage, fs.readFileSync(scriptFile, 'utf8'));
  const browser = await chromium.launch({
    executablePath: '/opt/browser/chrome', args: ['--no-sandbox', '--disable-gpu'],
  });
  const tab = await browser.newPage({ viewport: { width: 1000, height: 700 } });
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
    if (step === 'shot') await take();
    else { await tab.keyboard.press(step); pressed++; }
  }
  if (steps[steps.length - 1] !== 'shot') await take();
  console.log(JSON.stringify({ page, keys_pressed: pressed, screenshots: shots, screenshots_not_taken: skipped, console_errors: errors }));
  await browser.close();
})().catch((e) => { console.error('shot failed: ' + (e && e.message ? e.message : e)); process.exit(1); });
