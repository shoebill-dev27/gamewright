// What the live office shows, every 2 s: who is working (the character picture), each name plate's
// pill, the header counts, the Goal status, the Studio label, the handoff and decision counts, and
// console errors. One JSON line per change (a heartbeat each minute); a screenshot on change (at most
// every 10 s) and every 5 minutes.
//   PW=<playwright module dir> CHROME=<chromium> URL=http://127.0.0.1:8765/ OUT_DIR=<dir> node observe.js
const { chromium } = require(process.env.PW);
const fs = require('fs');
const OUT = process.env.OUT_DIR;
const log = (o) => fs.appendFileSync(`${OUT}/screen.jsonl`, JSON.stringify({ t: Date.now() / 1000, ...o }) + '\n');
(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROME, args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('console', (m) => { if (m.type() === 'error') log({ ev: 'console', text: m.text() }); });
  page.on('pageerror', (e) => log({ ev: 'pageerror', text: String(e) }));
  await page.goto(process.env.URL);
  let last = '', lastShot = 0, lastBeat = 0;
  for (;;) {
    try {
      const s = await page.evaluate(() => {
        const busy = Object.entries(pods).filter(([, p]) => p.chars && p.chars.busy.classList.contains('on')).map(([k]) => k).sort();
        const pills = Object.fromEntries(Object.entries(pods).map(([k, p]) => [k, p.pillTx ? p.pillTx.textContent : null]));
        const g = (id) => (document.getElementById(id) || {}).textContent || null;
        return { busy, pills, cBusy: g('cBusy'), cWait: g('cWait'), goal: g('goalStatus'), studio: layer.hub && layer.hub.st ? layer.hub.st.textContent : null,
                 handoffs: g('hCount'), decisions: g('dCount'), card: g('dName'), cardState: g('dState') };
      });
      const key = JSON.stringify(s), now = Date.now();
      if (key !== last) {
        log({ ev: 'screen', ...s }); last = key;
        if (now - lastShot > 10000) { await page.screenshot({ path: `${OUT}/shots/${Math.round(now / 1000)}.png` }); lastShot = now; }
      } else if (now - lastBeat > 60000) { log({ ev: 'beat' }); lastBeat = now; }
      if (now - lastShot > 300000) { await page.screenshot({ path: `${OUT}/shots/${Math.round(now / 1000)}.png` }); lastShot = now; }
    } catch (e) { log({ ev: 'observer-error', text: String(e) }); try { await page.reload(); } catch (_) { /* retry next tick */ } }
    await page.waitForTimeout(2000);
  }
})();
