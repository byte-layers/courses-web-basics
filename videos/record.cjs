/**
 * Enregistrement d'une vidéo « navigateur + outils de développement ».
 *
 *   node record.cjs <scenario.cjs> <outdir>        # SHOTS=1 : une capture par segment
 *
 * Playwright ne capture que le contenu des pages : ni la barre d'adresse, ni
 * les DevTools d'une fenêtre. La scène est donc faite de trois pages
 * enregistrées en même temps, puis juxtaposées par ffmpeg :
 *
 *   ┌──────────── 640 ────────────┬──────────── 640 ────────────┐
 *   │ bar  : barre d'adresse      │                             │
 *   ├─────────────────────────────┤ dt : les vrais DevTools de  │
 *   │ site : la page visitée      │ Chromium, branchés sur site │
 *   │                             │ (inspector.html, port CDP)  │
 *   └─────────────────────────────┴─────────────────────────────┘
 *
 * Les DevTools sont le frontal livré avec Chromium, servi par le port de
 * débogage et connecté à la page `site` : ce qu'ils montrent est réel. Avant
 * l'appel à `openDevtools()`, la colonne de droite affiche un fond neutre.
 *
 * Sorties : raw.mp4 (la scène, 1920×1080) et markers.json, lus par
 * assemble.cjs. Le curseur est dessiné dans la page qu'il survole.
 */
const { chromium } = require('@playwright/test');
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const scenario = require(path.resolve(process.argv[2]));
const out = path.resolve(process.argv[3]);
const SHOTS = process.env.SHOTS === '1';
const PORT = 9333;
const tts = JSON.parse(fs.readFileSync(path.join(out, 'tts.json'), 'utf8'));
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Géométrie de la scène, en px CSS ; la vidéo est à 1,5× (1920×1080).
const W = 1280, H = 720, BAR = 52, HALF = 640;
const SCALE = 1.5;
const REGIONS = {
  bar: { x: 0, y: 0, w: HALF, h: BAR },
  site: { x: 0, y: BAR, w: HALF, h: H - BAR },
  dt: { x: HALF, y: 0, w: W - HALF, h: H },
};

// Le curseur et l'anneau, injectés dans chaque page (et réinjectés après
// chaque navigation). Construits nœud par nœud : les DevTools refusent innerHTML.
function cursorScript() {
  const add = () => {
    if (document.getElementById('bl-cursor') || !document.documentElement) return;
    const NS = 'http://www.w3.org/2000/svg';
    const c = document.createElement('div');
    c.id = 'bl-cursor';
    const svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('width', '26'); svg.setAttribute('height', '26'); svg.setAttribute('viewBox', '0 0 24 24');
    const p = document.createElementNS(NS, 'path');
    p.setAttribute('d', 'M5.5 3.2 L5.5 18.5 L9.3 15 L12 21 L14.6 19.9 L11.9 14 L17 14 Z');
    p.setAttribute('fill', '#fff'); p.setAttribute('stroke', '#000'); p.setAttribute('stroke-width', '1.4'); p.setAttribute('stroke-linejoin', 'round');
    svg.appendChild(p); c.appendChild(svg);
    Object.assign(c.style, { position: 'fixed', left: '-100px', top: '-100px', zIndex: '2147483647', pointerEvents: 'none', filter: 'drop-shadow(0 1px 2px rgba(0,0,0,.6))', display: 'none' });
    const ring = document.createElement('div');
    ring.id = 'bl-ring';
    Object.assign(ring.style, { position: 'fixed', width: '34px', height: '34px', marginLeft: '-14px', marginTop: '-14px', border: '3px solid #8f7bff', borderRadius: '50%', zIndex: '2147483646', pointerEvents: 'none', opacity: '0', transition: 'opacity .25s, transform .25s' });
    document.documentElement.appendChild(c);
    document.documentElement.appendChild(ring);
    if (window.__blCursor) window.__blSet(window.__blCursor.x, window.__blCursor.y);
  };
  window.__blSet = (x, y) => {
    window.__blCursor = { x, y };
    const c = document.getElementById('bl-cursor'); const r = document.getElementById('bl-ring');
    if (!c) return;
    c.style.display = 'block'; c.style.left = `${x - 5}px`; c.style.top = `${y - 3}px`;
    r.style.left = `${x}px`; r.style.top = `${y}px`;
  };
  window.__blHide = () => { window.__blCursor = null; const c = document.getElementById('bl-cursor'); if (c) c.style.display = 'none'; };
  window.__blPulse = () => {
    const r = document.getElementById('bl-ring'); if (!r) return;
    r.style.opacity = '1'; r.style.transform = 'scale(1)';
    setTimeout(() => { r.style.opacity = '0'; r.style.transform = 'scale(1.6)'; }, 350);
  };
  document.addEventListener('DOMContentLoaded', add);
  setInterval(add, 300);
}

// La barre d'adresse : boutons et champ dessinés, pilotés depuis Node.
const BAR_HTML = `<!doctype html><html><head><style>
  html,body{margin:0;height:100%;background:#dee1e6;font:14px -apple-system,Helvetica,Arial,sans-serif;overflow:hidden}
  .row{display:flex;align-items:center;height:100%;padding:0 10px;gap:6px;box-sizing:border-box;border-bottom:1px solid #c4c7cc}
  .btn{width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#5f6368}
  .btn svg{width:18px;height:18px}
  #omni{flex:1;height:34px;border-radius:17px;background:#fff;display:flex;align-items:center;padding:0 14px;gap:8px;color:#202124;white-space:nowrap;overflow:hidden}
  #omni.focus{outline:2px solid #1a73e8}
  #lock{width:14px;height:14px;color:#5f6368;flex:none}
  #url{overflow:hidden;text-overflow:ellipsis}
  #caret{display:none;width:1px;height:18px;background:#202124;margin-left:-7px}
  #omni.focus #caret{display:block;animation:b 1s step-end infinite}
  @keyframes b{50%{opacity:0}}
  .sel{background:#c2dbff}
  #keys{position:absolute;right:16px;top:9px;display:flex;gap:5px;opacity:0;transition:opacity .2s}
  #keys.on{opacity:1}
  #keys kbd{font:600 14px -apple-system,Helvetica,Arial,sans-serif;color:#202124;background:#fff;border:1px solid #c4c7cc;border-bottom-width:3px;border-radius:6px;padding:4px 9px}
</style></head><body><div class="row">
  <div class="btn" id="back"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M20 11H7.8l5.6-5.6L12 4l-8 8 8 8 1.4-1.4L7.8 13H20z"/></svg></div>
  <div class="btn" id="fwd"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M4 11h12.2l-5.6-5.6L12 4l8 8-8 8-1.4-1.4 5.6-5.6H4z"/></svg></div>
  <div class="btn" id="reload"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M17.6 6.4A8 8 0 1 0 19.7 14h-2.1a6 6 0 1 1-1.4-6.2L13 11h7V4z"/></svg></div>
  <div id="omni"><svg id="lock" viewBox="0 0 24 24"><path fill="currentColor" d="M18 8h-1V6A5 5 0 0 0 7 6v2H6a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V10a2 2 0 0 0-2-2zM9 6a3 3 0 0 1 6 0v2H9z"/></svg><span id="url"></span><span id="caret"></span></div>
</div><div id="keys"></div></body></html>`;

// Le fond de la colonne DevTools avant leur ouverture, et les touches affichées.
const DT_PLACEHOLDER = `<!doctype html><html><head><style>
  html,body{margin:0;height:100%;background:#f1f3f4;font:15px -apple-system,Helvetica,Arial,sans-serif;color:#80868b;overflow:hidden}
  .c{height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px}
  .keys{display:flex;gap:10px;opacity:0;transform:translateY(8px);transition:all .3s}
  .keys.on{opacity:1;transform:none}
  kbd{font:600 22px -apple-system,Helvetica,Arial,sans-serif;color:#202124;background:#fff;border:1px solid #c4c7cc;border-bottom-width:3px;border-radius:8px;padding:10px 16px}
  .or{align-self:center;color:#80868b}
</style></head><body><div class="c"><div>Outils de développement fermés</div>
<div class="keys" id="keys"><kbd>F12</kbd><span class="or">ou</span><kbd>⌘</kbd><kbd>⌥</kbd><kbd>I</kbd></div></div></body></html>`;

(async () => {
  fs.mkdirSync(path.join(out, 'pages'), { recursive: true });
  for (const f of fs.readdirSync(path.join(out, 'pages'))) fs.rmSync(path.join(out, 'pages', f));
  const browser = await chromium.launch({
    headless: false,
    args: [`--remote-debugging-port=${PORT}`, '--remote-allow-origins=*', '--hide-scrollbars', '--force-device-scale-factor=2'],
  });
  const mk = async (name) => {
    const r = REGIONS[name];
    const ctx = await browser.newContext({
      viewport: { width: r.w, height: r.h },
      deviceScaleFactor: 2,
      // Les DevTools de Chromium n'existent qu'en anglais : en-US évite leur
      // bandeau « DevTools is now available in French ».
      locale: name === 'dt' ? 'en-US' : 'fr-FR',
      recordVideo: { dir: path.join(out, 'pages'), size: { width: r.w * SCALE, height: r.h * SCALE } },
    });
    await ctx.addInitScript(cursorScript);
    if (name === 'dt') await ctx.addInitScript(() => { try { localStorage.setItem('screencast-enabled', 'false'); } catch {} });
    const page = await ctx.newPage();
    return { name, ctx, page, born: Date.now() };
  };
  const P = { bar: await mk('bar'), site: await mk('site'), dt: await mk('dt') };
  const { bar, site, dt } = { bar: P.bar.page, site: P.site.page, dt: P.dt.page };
  await bar.setContent(BAR_HTML);
  await dt.setContent(DT_PLACEHOLDER);
  await site.setContent('<body style="margin:0;background:#fff"></body>');
  // Sans cache, chaque chargement montre la vraie réponse du serveur (200)
  // plutôt qu'un 304 de revalidation.
  if (scenario.disableCache) {
    const cdp = await P.site.ctx.newCDPSession(site);
    await cdp.send('Network.enable');
    await cdp.send('Network.setCacheDisabled', { cacheDisabled: true });
  }

  // La barre d'adresse suit la page visitée (redirections comprises).
  let typing = false;
  const showUrl = (u) => bar.evaluate((u) => {
    const pretty = u === 'about:blank' ? '' : u.replace(/^https:\/\//, '').replace(/\/$/, '');
    document.getElementById('url').textContent = pretty;
    document.getElementById('lock').style.display = u.startsWith('https:') ? '' : 'none';
  }, u);
  site.on('framenavigated', (f) => { if (f === site.mainFrame() && !typing) showUrl(f.url()).catch(() => {}); });

  // ── Curseur global : coordonnées de la scène, dessiné dans la page survolée.
  const mouse = { x: W / 2, y: H / 2, in: null };
  const regionAt = (x, y) => (x >= HALF ? 'dt' : y < BAR ? 'bar' : 'site');
  const pageOf = (n) => P[n].page;
  async function place(x, y) {
    const n = regionAt(x, y), r = REGIONS[n], p = pageOf(n);
    if (mouse.in && mouse.in !== n) await pageOf(mouse.in).evaluate(() => window.__blHide && window.__blHide()).catch(() => {});
    mouse.in = n;
    await p.mouse.move(x - r.x, y - r.y).catch(() => {});
    await p.evaluate(([a, b]) => window.__blSet && window.__blSet(a, b), [x - r.x, y - r.y]).catch(() => {});
  }
  async function moveTo(x, y, ms = 600) {
    const steps = Math.max(8, Math.round(ms / 25));
    const sx = mouse.x, sy = mouse.y;
    for (let i = 1; i <= steps; i++) {
      const t = i / steps, e = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
      await place(sx + (x - sx) * e, sy + (y - sy) * e);
      await sleep(ms / steps);
    }
    mouse.x = x; mouse.y = y;
  }
  const pulse = () => pageOf(mouse.in).evaluate(() => window.__blPulse && window.__blPulse()).catch(() => {});
  const nameOfPage = (pg) => Object.keys(P).find((k) => P[k].page === pg);
  /** Centre d'un locator, en coordonnées de la scène. */
  async function center(pg, locator) {
    await locator.scrollIntoViewIfNeeded({ timeout: 5000 }).catch(() => {});
    const b = await locator.boundingBox({ timeout: 5000 });
    if (!b) throw new Error(`élément introuvable : ${locator}`);
    const r = REGIONS[nameOfPage(pg)];
    return { x: r.x + b.x + Math.min(b.width / 2, 60), y: r.y + b.y + b.height / 2, local: { x: b.x + Math.min(b.width / 2, 60), y: b.y + b.height / 2 } };
  }
  async function point(pg, locator, { hold = 900, ring = true } = {}) {
    const c = await center(pg, locator);
    await moveTo(c.x, c.y, 650);
    if (ring) await pulse();
    await sleep(hold);
    return c;
  }
  async function click(pg, locator, { hold = 300 } = {}) {
    const c = await point(pg, locator, { hold: 250 });
    await pg.mouse.click(c.local.x, c.local.y);
    await sleep(hold);
  }

  // ── Gestes du navigateur.
  /** Clique dans la barre d'adresse, tape l'adresse, Entrée : la page s'ouvre. */
  async function go(url, { delay = 55 } = {}) {
    await click(bar, bar.locator('#omni'), { hold: 150 });
    typing = true;
    await bar.evaluate(() => { document.getElementById('omni').classList.add('focus'); document.getElementById('url').classList.add('sel'); });
    await sleep(350);
    await bar.evaluate(() => { const u = document.getElementById('url'); u.classList.remove('sel'); u.textContent = ''; document.getElementById('lock').style.display = 'none'; });
    for (const ch of url) {
      await bar.evaluate((ch) => { document.getElementById('url').textContent += ch; }, ch);
      await sleep(delay);
    }
    await sleep(300);
    await bar.evaluate(() => document.getElementById('omni').classList.remove('focus'));
    typing = false;
    const resp = await site.goto(url, { waitUntil: 'load' }).catch((e) => { console.warn(`  navigation ${url} : ${e.message.split('\n')[0]}`); });
    await showUrl(site.url());
    return resp;
  }
  /** Affiche des touches (ex. ['⌘', '⇧', 'R']) en haut à droite de la barre. */
  async function keys(list, ms = 1400) {
    await bar.evaluate((list) => {
      const k = document.getElementById('keys');
      k.replaceChildren(...list.map((t) => Object.assign(document.createElement('kbd'), { textContent: t })));
      k.classList.add('on');
    }, list);
    await sleep(ms);
    await bar.evaluate(() => document.getElementById('keys').classList.remove('on'));
  }
  /** Recharge : clic sur ⟳, ou raccourci affiché si `withKeys` est donné. */
  async function reload({ withKeys } = {}) {
    if (withKeys) await keys(withKeys);
    else await click(bar, bar.locator('#reload'), { hold: 100 });
    await site.reload({ waitUntil: 'load' });
  }
  /** Affiche les touches, puis ouvre les vrais DevTools sur la page `site`. */
  async function openDevtools({ keysMs = 1600 } = {}) {
    await dt.evaluate(() => document.getElementById('keys').classList.add('on'));
    await sleep(keysMs);
    const targets = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json();
    const t = targets.find((t) => t.type === 'page' && t.url === site.url());
    if (!t) throw new Error(`cible CDP introuvable pour ${site.url()}`);
    await dt.goto(`http://127.0.0.1:${PORT}/devtools/inspector.html?ws=127.0.0.1:${PORT}/devtools/page/${t.id}`);
    await dt.getByRole('tab', { name: 'Elements' }).waitFor({ timeout: 15000 });
    await sleep(600);
  }

  const ctx = { bar, site, dt, point, click, moveTo, pulse, go, reload, keys, openDevtools, pause: sleep, W, H };

  // ── Déroulé.
  await sleep(1500);
  await moveTo(W / 2 - 200, H / 2, 10);
  const t0 = Math.max(...Object.values(P).map((p) => p.born));
  const markers = [];
  let failed = null;
  for (const [i, seg] of scenario.segments.entries()) {
    const start = Date.now();
    markers.push({ id: seg.id, at: start });
    console.log(`  ▸ ${seg.id}`);
    try {
      await seg.run(ctx);
    } catch (e) {
      failed = e;
      console.error(`  ✗ ${seg.id} : ${e.message}`);
      await dt.screenshot({ path: path.join(out, 'failure-dt.png') }).catch(() => {});
      await site.screenshot({ path: path.join(out, 'failure-site.png') }).catch(() => {});
      break;
    }
    const need = (tts[seg.id]?.ms ?? 0) + 700;
    const spent = Date.now() - start;
    if (spent < need) await sleep(need - spent);
    if (SHOTS) {
      await dt.screenshot({ path: path.join(out, `shot-${String(i + 1).padStart(2, '0')}-${seg.id}-dt.png`) });
      await site.screenshot({ path: path.join(out, `shot-${String(i + 1).padStart(2, '0')}-${seg.id}-site.png`) });
    }
  }
  await sleep(1500);
  const end = Date.now();

  const videos = {};
  for (const k of Object.keys(P)) {
    const v = P[k].page.video();
    await P[k].ctx.close();
    videos[k] = await v.path();
  }
  await browser.close();

  // ── Composition : chaque vidéo commence à la naissance de sa page ; on les
  // cale sur t0 (la plus tardive), puis barre + site à gauche, DevTools à droite.
  const duration = end - t0;
  const ss = (k) => ((t0 - P[k].born) / 1000).toFixed(3);
  const raw = path.join(out, 'raw.mp4');
  execFileSync('ffmpeg', ['-y', '-v', 'error',
    '-ss', ss('bar'), '-i', videos.bar,
    '-ss', ss('site'), '-i', videos.site,
    '-ss', ss('dt'), '-i', videos.dt,
    '-filter_complex', [
      `[0:v]scale=${HALF * SCALE}:${BAR * SCALE},setsar=1[b]`,
      `[1:v]scale=${HALF * SCALE}:${(H - BAR) * SCALE},setsar=1[s]`,
      `[2:v]scale=${(W - HALF) * SCALE}:${H * SCALE},setsar=1[d]`,
      '[b][s]vstack[l]',
      '[l][d]hstack,fps=25[v]',
    ].join(';'),
    '-map', '[v]', '-t', (duration / 1000).toFixed(3),
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', raw]);
  fs.writeFileSync(
    path.join(out, 'markers.json'),
    JSON.stringify({ duration, markers: markers.map((m) => ({ id: m.id, ms: Math.max(0, m.at - t0) })) }, null, 2),
  );
  console.log(`scène : ${(duration / 1000).toFixed(1)} s → ${raw}`);
  if (failed) process.exit(1);
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
