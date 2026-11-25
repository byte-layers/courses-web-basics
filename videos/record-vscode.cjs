/**
 * Enregistrement d'une vidéo « VS Code et navigateur ».
 *
 *   node record-vscode.cjs <scenario.cjs> <outdir>     # SHOTS=1 : une capture par segment
 *
 * Choisi par make-video.sh quand le scénario déclare `recorder: 'vscode'`.
 * Deux scènes, filmées en même temps, montées en plans successifs :
 *
 *   - `vscode` (défaut) : le vrai VS Code (Electron piloté par Playwright,
 *     comme ../../courses-ansible-intro/videos/record.cjs), profil jetable,
 *     sans extension, 1280×720 ;
 *   - `browser` : la barre d'adresse dessinée au-dessus de la page, plein
 *     cadre (comme record.cjs, sans DevTools).
 *
 * Chaque segment dit sa scène (`scene: 'browser'`, sinon VS Code) : la vidéo
 * bascule à chaque changement. `ctx.relaunch(dossier)` ferme VS Code et le
 * rouvre sur un dossier ; le montage coupe le temps de relance (le dialogue
 * « Open Folder » simple de VS Code n'ouvre rien sous Playwright).
 *
 * Le dossier personnel de VS Code et de son terminal est un dossier jetable
 * (HOME, par défaut /Users/Shared/vous, supprimé à la fin ; KEEP_HOME=1 le
 * garde), pour que `~/byte-layers/web/basics` n'écrase jamais les fichiers de
 * la machine. Options du scénario :
 *
 *   folder: 'byte-layers/web/basics'   VS Code s'ouvre sur ce dossier (relatif à HOME)
 *   files: { 'byte-layers/web/basics/a.html': '…' }   fichiers posés avant le début
 */
const { _electron, chromium } = require('@playwright/test');
const { execFileSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const scenario = require(path.resolve(process.argv[2]));
const out = path.resolve(process.argv[3]);
const SHOTS = process.env.SHOTS === '1';
const tts = JSON.parse(fs.readFileSync(path.join(out, 'tts.json'), 'utf8'));
const EXE = process.env.VSCODE_EXE || '/Applications/Visual Studio Code.app/Contents/MacOS/Code';
const W = 1280, H = 720, BAR = 86, SCALE = 1.5; // BAR : onglet + barre d'adresse
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function waitFor(what, fn, timeoutMs = 30_000) {
  const end = Date.now() + timeoutMs;
  for (;;) {
    try { const v = await fn(); if (v) return v; } catch {}
    if (Date.now() > end) throw new Error(`délai dépassé : ${what}`);
    await sleep(250);
  }
}
const durationOf = (f) => Math.round(parseFloat(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).toString()) * 1000);

// ── Curseur dessiné (VS Code : Trusted Types, le SVG se construit nœud par nœud).
function cursorScript() {
  const add = () => {
    if (document.getElementById('bl-cursor') || !document.body) return;
    const NS = 'http://www.w3.org/2000/svg';
    const c = document.createElement('div');
    c.id = 'bl-cursor';
    const svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('width', '26'); svg.setAttribute('height', '26'); svg.setAttribute('viewBox', '0 0 24 24');
    const p = document.createElementNS(NS, 'path');
    p.setAttribute('d', 'M5.5 3.2 L5.5 18.5 L9.3 15 L12 21 L14.6 19.9 L11.9 14 L17 14 Z');
    p.setAttribute('fill', '#fff'); p.setAttribute('stroke', '#000'); p.setAttribute('stroke-width', '1.4'); p.setAttribute('stroke-linejoin', 'round');
    svg.appendChild(p); c.appendChild(svg);
    Object.assign(c.style, { position: 'fixed', left: '-100px', top: '-100px', zIndex: '2147483647', pointerEvents: 'none', filter: 'drop-shadow(0 1px 2px rgba(0,0,0,.6))' });
    const ring = document.createElement('div');
    ring.id = 'bl-ring';
    Object.assign(ring.style, { position: 'fixed', width: '34px', height: '34px', marginLeft: '-14px', marginTop: '-14px', border: '3px solid #8f7bff', borderRadius: '50%', zIndex: '2147483646', pointerEvents: 'none', opacity: '0', transition: 'opacity .25s, transform .25s' });
    // Un seul nœud, après </body> et masqué aux lecteurs d'écran : dans les DevTools,
    // il reste hors du code de la page et hors de l'arbre d'accessibilité.
    const box = document.createElement('div');
    box.id = 'bl-overlay'; box.setAttribute('aria-hidden', 'true');
    box.appendChild(c); box.appendChild(ring);
    document.documentElement.appendChild(box);
    if (window.__blCursor) window.__blSet(window.__blCursor.x, window.__blCursor.y);
  };
  window.__blSet = (x, y) => {
    window.__blCursor = { x, y };
    const c = document.getElementById('bl-cursor'); const r = document.getElementById('bl-ring');
    if (!c) return;
    c.style.left = `${x - 5}px`; c.style.top = `${y - 3}px`;
    r.style.left = `${x}px`; r.style.top = `${y}px`;
  };
  window.__blPulse = () => {
    const r = document.getElementById('bl-ring'); if (!r) return;
    r.style.opacity = '1'; r.style.transform = 'scale(1)';
    setTimeout(() => { r.style.opacity = '0'; r.style.transform = 'scale(1.6)'; }, 350);
  };
  add();
  setInterval(add, 300);
}

const BAR_HTML = `<!doctype html><html><head><style>
  html,body{margin:0;height:100%;background:#dee1e6;font:14px -apple-system,Helvetica,Arial,sans-serif;overflow:hidden}
  .tabs{height:36px;display:flex;align-items:flex-end;padding:0 10px}
  #tab{height:30px;max-width:260px;min-width:160px;background:#fff;border-radius:9px 9px 0 0;display:flex;align-items:center;padding:0 14px;gap:8px;color:#202124;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;box-sizing:border-box}
  #tab:empty::before{content:'Nouvel onglet';color:#5f6368}
  .row{display:flex;align-items:center;height:50px;padding:0 10px;gap:6px;box-sizing:border-box;border-bottom:1px solid #c4c7cc;background:#fff}
  .row #omni{background:#f1f3f4}
  .btn{width:30px;height:30px;display:flex;align-items:center;justify-content:center;color:#5f6368}
  .btn svg{width:18px;height:18px}
  #omni{flex:1;height:34px;border-radius:17px;background:#fff;display:flex;align-items:center;padding:0 14px;gap:8px;color:#202124;white-space:nowrap;overflow:hidden}
  #info{width:14px;height:14px;color:#5f6368;flex:none}
  #keys{position:absolute;right:16px;top:44px;display:flex;gap:5px;opacity:0;transition:opacity .2s}
  #keys.on{opacity:1}
  #keys kbd{font:600 14px -apple-system,Helvetica,Arial,sans-serif;color:#202124;background:#fff;border:1px solid #c4c7cc;border-bottom-width:3px;border-radius:6px;padding:4px 9px}
</style></head><body><div class="tabs"><div id="tab"></div></div><div class="row">
  <div class="btn"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M20 11H7.8l5.6-5.6L12 4l-8 8 8 8 1.4-1.4L7.8 13H20z"/></svg></div>
  <div class="btn"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M4 11h12.2l-5.6-5.6L12 4l8 8-8 8-1.4-1.4 5.6-5.6H4z"/></svg></div>
  <div class="btn" id="reload"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M17.6 6.4A8 8 0 1 0 19.7 14h-2.1a6 6 0 1 1-1.4-6.2L13 11h7V4z"/></svg></div>
  <div id="omni"><svg id="info" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm1 15h-2v-6h2zm0-8h-2V7h2z"/></svg><span id="url"></span></div>
</div><div id="keys"></div></body></html>`;

(async () => {
  if (!fs.existsSync(EXE)) throw new Error(`pas de VS Code à ${EXE}`);
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'bl-vscode-'));
  // Dossier personnel jetable, à un chemin lisible à l'écran.
  const home = process.env.BL_HOME || '/Users/Shared/vous';
  if (fs.existsSync(home)) throw new Error(`${home} existe déjà : supprimez-le ou choisissez BL_HOME`);
  const user = path.join(tmp, 'user');
  const ext = path.join(tmp, 'ext');
  const zdot = path.join(tmp, 'zdot');
  for (const d of [home, path.join(user, 'User'), ext, zdot]) fs.mkdirSync(d, { recursive: true });
  for (const [rel, content] of Object.entries(scenario.files ?? {})) {
    fs.mkdirSync(path.dirname(path.join(home, rel)), { recursive: true });
    fs.writeFileSync(path.join(home, rel), content);
  }
  if (scenario.folder) fs.mkdirSync(path.join(home, scenario.folder), { recursive: true });
  // Invite courte et anonyme dans le terminal.
  fs.writeFileSync(path.join(zdot, '.zshrc'), "PROMPT='%~ %# '\nunsetopt PROMPT_SP\n");
  fs.writeFileSync(path.join(user, 'User', 'settings.json'), JSON.stringify({
    'window.dialogStyle': 'custom',
    'window.menuStyle': 'custom',
    'files.simpleDialog.enable': true,
    'workbench.editorAssociations': { '*.svg': 'default' }, // un .svg s'ouvre en texte, pas en aperçu
    'workbench.startupEditor': 'none',
    'window.restoreWindows': 'none',
    'telemetry.telemetryLevel': 'off',
    'update.mode': 'none',
    'workbench.tips.enabled': false,
    'extensions.autoCheckUpdates': false,
    'extensions.ignoreRecommendations': true,
    'chat.disableAIFeatures': true,
    'chat.commandCenter.enabled': false,
    'security.workspace.trust.enabled': false,
    'window.zoomLevel': 0,
    'editor.minimap.enabled': false,
    'editor.fontSize': 15,
    'editor.lineHeight': 22,
    'editor.formatOnPaste': false,
    'editor.stickyScroll.enabled': false,
    'editor.cursorBlinking': 'smooth',
    'editor.wordWrap': 'off', // End et les numéros de ligne restent ceux du fichier
    'workbench.editor.empty.hint': 'hidden',
    'terminal.integrated.fontSize': 14,
    'terminal.integrated.enablePersistentSessions': false,
    'window.commandCenter': false,
    'workbench.layoutControl.enabled': false,
    'files.autoSave': 'off',
    'git.enabled': false,
    'workbench.secondarySideBar.defaultVisibility': 'hidden',
    'explorer.compactFolders': false,
    // La frappe montrée doit donner exactement le fichier : aucune aide qui ajoute du texte.
    'html.autoClosingTags': false,
    'editor.autoClosingBrackets': 'never',
    'editor.autoClosingQuotes': 'never',
    'editor.autoClosingOvertype': 'never',
    'editor.autoSurround': 'never',
    'editor.autoIndent': 'none',
    'editor.linkedEditing': false,
    'editor.quickSuggestions': { other: 'off', comments: 'off', strings: 'off' },
    'editor.suggestOnTriggerCharacters': false,
    'editor.wordBasedSuggestions': 'off',
    'editor.acceptSuggestionOnEnter': 'off',
    'editor.inlineSuggest.enabled': false,
    'editor.hover.enabled': false,
    'editor.parameterHints.enabled': false,
    'emmet.showExpandedAbbreviation': 'never',
    'html.suggest.html5': false,
    'editor.occurrencesHighlight': 'off',
    'editor.selectionHighlight': false,
  }));

  // ── VS Code : chaque lancement est une source vidéo.
  const vsources = []; // { path, end, video } ; origine = end - durée
  let app, win;
  async function launch(folder) {
    app = await _electron.launch({
      executablePath: EXE,
      args: [`--user-data-dir=${user}`, `--extensions-dir=${ext}`, '--use-inmemory-secretstorage', '--skip-welcome', '--skip-release-notes', '--new-window', '--force-device-scale-factor=2', ...(folder ? [path.join(home, folder)] : [])],
      env: { ...process.env, HOME: home, ZDOTDIR: zdot },
      recordVideo: { dir: path.join(out, 'vscode'), size: { width: W * SCALE, height: H * SCALE } },
      timeout: 60_000,
    });
    win = await app.firstWindow();
    await app.evaluate(({ BrowserWindow }, [w, h]) => { const b = BrowserWindow.getAllWindows()[0]; b.setContentSize(w, h); b.center(); }, [W, H]);
    if (folder) await waitFor('l\'explorateur', () => win.locator('.explorer-folders-view').count());
    await sleep(folder ? 2500 : 3500);
    await win.evaluate(cursorScript);
    const src = { video: win.video(), app };
    vsources.push(src);
    return src;
  }
  async function closeVSCode() {
    const src = vsources[vsources.length - 1];
    src.path = await src.video.path();
    await src.app.close().catch(() => {});
    src.end = Date.now(); // la vidéo court jusqu'à la fermeture
  }
  await launch(scenario.folder);

  // ── Navigateur : barre + page, plein cadre.
  // Avec `devtools: true`, la scène navigateur est coupée en deux : page à
  // gauche (640 px), vrais DevTools de Chromium à droite, comme record.cjs.
  // `dtWidth` : largeur des DevTools (W / 2 par défaut), pour une page plus large.
  const DT = !!scenario.devtools, PORT = 9334, SW = DT ? W - (scenario.dtWidth ?? W / 2) : W;
  // `siteHeight` : une fenêtre de navigateur plus basse, posée sur le bureau.
  const SH = scenario.siteHeight ?? H - BAR;
  const browser = await chromium.launch({ headless: false, args: ['--hide-scrollbars', '--allow-file-access-from-files', '--force-device-scale-factor=2', ...(DT ? [`--remote-debugging-port=${PORT}`, '--remote-allow-origins=*'] : [])] });
  const mk = async (w, h, locale = 'fr-FR') => {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 2, locale, recordVideo: { dir: path.join(out, 'pages'), size: { width: w * SCALE, height: h * SCALE } } });
    await ctx.addInitScript(cursorScript);
    if (locale === 'en-US') await ctx.addInitScript(() => { try { localStorage.setItem('screencast-enabled', 'false'); } catch {} });
    const page = await ctx.newPage();
    return { ctx, page, born: Date.now() };
  };
  const B = { bar: await mk(SW, BAR), site: await mk(SW, SH) };
  if (DT) B.dt = await mk(W - SW, H, 'en-US');
  const bar = B.bar.page, site = B.site.page, dt = B.dt?.page;
  if (dt) await dt.setContent('<body style="margin:0;background:#f1f3f4;font:15px -apple-system,Helvetica,Arial,sans-serif;color:#80868b;display:flex;align-items:center;justify-content:center;height:100vh">Outils de développement fermés</body>');
  await bar.setContent(BAR_HTML);
  await site.setContent('<body style="margin:0;background:#fff"></body>');
  site.on('framenavigated', (f) => { if (f === site.mainFrame()) bar.evaluate((u) => { document.getElementById('url').textContent = u; }, f.url()).catch(() => {}); });
  // L'onglet affiche le <title> de la page, ou le nom du fichier s'il n'y en a pas.
  site.on('load', async () => {
    const t = (await site.title().catch(() => '')) || decodeURIComponent(site.url().split('/').pop());
    await bar.evaluate((t) => { document.getElementById('tab').textContent = t; }, site.url().startsWith('about:') ? '' : t).catch(() => {});
  });

  // ── Gestes. `scene` dit où est le curseur : 'vscode' ou 'browser'.
  let scene = 'vscode';
  const mice = { vscode: { x: W / 2, y: H / 2 }, browser: { x: W / 2, y: H / 2 + 80 } };
  const pageAt = (x, y) => (scene === 'vscode' ? { p: win, dx: 0, dy: 0 } : DT && x >= SW ? { p: dt, dx: SW, dy: 0 } : y < BAR ? { p: bar, dx: 0, dy: 0 } : { p: site, dx: 0, dy: BAR });
  let lastPage = null;
  async function place(x, y) {
    const { p, dx, dy } = pageAt(x, y);
    if (lastPage && lastPage !== p) await lastPage.evaluate(() => { const c = document.getElementById('bl-cursor'); if (c) c.style.left = '-100px'; }).catch(() => {});
    lastPage = p;
    await p.mouse.move(x - dx, y - dy).catch(() => {});
    await p.evaluate(([a, b]) => window.__blSet && window.__blSet(a, b), [x - dx, y - dy]).catch(() => {});
  }
  async function moveTo(x, y, ms = 600) {
    const m = mice[scene];
    const steps = Math.max(8, Math.round(ms / 25));
    const sx = m.x, sy = m.y;
    for (let i = 1; i <= steps; i++) {
      const t = i / steps, e = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
      await place(sx + (x - sx) * e, sy + (y - sy) * e);
      await sleep(ms / steps);
    }
    m.x = x; m.y = y;
  }
  const pulse = () => pageAt(mice[scene].x, mice[scene].y).p.evaluate(() => window.__blPulse && window.__blPulse()).catch(() => {});
  async function center(locator) {
    await locator.scrollIntoViewIfNeeded({ timeout: 5000 }).catch(() => {});
    const b = await locator.boundingBox({ timeout: 5000 });
    if (!b) throw new Error(`élément introuvable : ${locator}`);
    const lp = locator.page();
    const dy = lp === site ? BAR : 0, dx = DT && lp === dt ? SW : 0;
    return { x: b.x + Math.min(b.width / 2, 120) + dx, y: b.y + b.height / 2 + dy, dx, dy };
  }
  async function point(locator, { hold = 900 } = {}) {
    const c = await center(locator);
    await moveTo(c.x, c.y, 650);
    await pulse();
    await sleep(hold);
    return c;
  }
  async function click(locator, { hold = 300, button = 'left', clickCount = 1 } = {}) {
    const c = await point(locator, { hold: 250 });
    await locator.page().mouse.click(c.x - c.dx, c.y - c.dy, { button, clickCount });
    await sleep(hold);
  }
  /** Affiche des touches (ex. ['⌘', 'R']) en haut à droite de la barre d'adresse. */
  async function keys(list, ms = 1300) {
    await bar.evaluate((list) => {
      const k = document.getElementById('keys');
      k.replaceChildren(...list.map((t) => Object.assign(document.createElement('kbd'), { textContent: t })));
      k.classList.add('on');
    }, list);
    await sleep(ms);
    await bar.evaluate(() => document.getElementById('keys').classList.remove('on'));
  }
  const ctx = {
    get win() { return win; }, get app() { return app; }, bar, site, dt, home, moveTo, point, click, pulse, keys, pause: sleep, W, H,
    /** Tape au clavier de VS Code, lettre par lettre. */
    async type(text, delay = 55) { await win.keyboard.type(text, { delay }); },
    key: (k) => win.keyboard.press(k),
    /** Met un texte dans le presse-papiers puis le colle (Cmd+V). */
    async paste(text) {
      await app.evaluate(({ clipboard }, t) => clipboard.writeText(t), text);
      await sleep(200);
      await win.keyboard.press('Meta+V');
    },
    async command(name) {
      await win.keyboard.press('Meta+Shift+P');
      await sleep(400);
      await win.keyboard.type(name, { delay: 15 });
      await sleep(500);
      await win.keyboard.press('Enter');
      await sleep(400);
    },
    /** Nouveau fichier dans le dossier ouvert : bouton de l'explorateur, nom tapé, Entrée. */
    async newFile(name, { folder = /basics/i } = {}) {
      const header = win.locator('.pane-header').filter({ hasText: folder }).first();
      await point(header, { hold: 500 });
      await click(header.locator('.action-label[aria-label^="New File"]').first(), { hold: 500 });
      await win.keyboard.type(name, { delay: 70 });
      await sleep(400);
      await win.keyboard.press('Enter');
      await sleep(900);
    },
    /** Nouveau dossier dans le dossier ouvert. */
    async newFolder(name, { folder = /basics/i } = {}) {
      const header = win.locator('.pane-header').filter({ hasText: folder }).first();
      await point(header, { hold: 500 });
      await click(header.locator('.action-label[aria-label^="New Folder"]').first(), { hold: 500 });
      await win.keyboard.type(name, { delay: 70 });
      await sleep(400);
      await win.keyboard.press('Enter');
      await sleep(900);
    },
    /** Tape du code ligne à ligne (l'indentation est dans le texte). */
    async typeCode(text, { delay = 38, linePause = 250 } = {}) {
      const lines = text.split('\n');
      for (const [i, l] of lines.entries()) {
        if (l) await win.keyboard.type(l, { delay });
        if (i < lines.length - 1) { await win.keyboard.press('Enter'); await sleep(linePause); }
      }
    },
    /** Ligne n (1 = première) de l'éditeur actif. */
    line: (n) => win.locator(`.part.editor .monaco-editor .view-lines > .view-line[style*="top:${(n - 1) * 22}px"]`).first(),
    /** Pointe le code de la ligne n, repérée par son numéro dans la gouttière (juste même après défilement). */
    async pointLine(n, { hold = 900 } = {}) {
      await ctx.goLine(n);
      const r = await win.evaluate((n) => {
        const ed = document.querySelector('.part.editor .editor-group-container.active .monaco-editor');
        const num = [...ed.querySelectorAll('.line-numbers')].find((e) => e.textContent.trim() === String(n));
        if (!num) return null;
        const y = num.getBoundingClientRect().top + num.getBoundingClientRect().height / 2;
        const line = [...ed.querySelectorAll('.view-line')].find((e) => { const b = e.getBoundingClientRect(); return y >= b.top && y < b.bottom; });
        const span = line?.querySelector('span span:not(:empty)');
        const x = span ? span.getBoundingClientRect().left + 40 : num.getBoundingClientRect().right + 60;
        return { x, y };
      }, n);
      if (!r) throw new Error(`ligne ${n} introuvable`);
      await moveTo(r.x, r.y, 650);
      await pulse();
      await sleep(hold);
    },
    /** Place le curseur de l'éditeur en début de ligne n (Ctrl+G). */
    async goLine(n) {
      await win.keyboard.press('Control+G');
      await sleep(300);
      await win.keyboard.type(String(n), { delay: 40 });
      await win.keyboard.press('Enter');
      await sleep(400);
    },
    /** Ouvre un fichier du dossier par Cmd+P. */
    async openFile(name) {
      await win.keyboard.press('Meta+P');
      await sleep(400);
      await win.keyboard.type(name, { delay: 25 });
      await sleep(600);
      await win.keyboard.press('Enter');
      await sleep(700);
    },
    /** Ferme VS Code et le rouvre sur `folder` (relatif à HOME) : coupe au montage. */
    async relaunch(folder) {
      await closeVSCode();
      cuts.push({ at: Date.now() });
      await launch(folder);
      cuts[cuts.length - 1].resume = Date.now();
      await place(mice.vscode.x, mice.vscode.y);
    },
    /** Ouvre les vrais DevTools sur la page (option devtools). */
    async openDevtools() {
      const targets = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json();
      const t = targets.find((t) => t.type === 'page' && t.url === site.url());
      if (!t) throw new Error(`cible CDP introuvable pour ${site.url()}`);
      await dt.goto(`http://127.0.0.1:${PORT}/devtools/inspector.html?ws=127.0.0.1:${PORT}/devtools/page/${t.id}`);
      await dt.getByRole('tab', { name: 'Elements' }).waitFor({ timeout: 15000 });
      await sleep(600);
    },
    /** Ouvre une adresse dans la page du navigateur (sans la taper). */
    async open(url) { await site.goto(url, { waitUntil: 'load' }); },
    /** Recharge la page du navigateur, touches affichées. */
    async reload() { await keys(['⌘', 'R']); await site.reload({ waitUntil: 'load' }); },
    path: (rel) => path.join(home, rel),
  };

  // ── Déroulé. `shots` : instants de bascule (scène) ; `cuts` : relances coupées.
  const markers = [], switches = [], cuts = [];
  let failed = null;
  await place(mice.vscode.x, mice.vscode.y);
  const start0 = Date.now() - 800;
  switches.push({ at: start0, scene: 'vscode' });
  for (const [i, seg] of scenario.segments.entries()) {
    const want = seg.scene === 'browser' ? 'browser' : 'vscode';
    if (want !== scene) {
      scene = want; switches.push({ at: Date.now(), scene });
      await place(mice[scene].x, mice[scene].y);
      // Retour dans VS Code : le clavier doit revenir à l'éditeur actif.
      // Cmd+1 rend le clavier à l'éditeur (Monaco n'édite plus forcément via un textarea).
      if (scene === 'vscode') { await win.keyboard.press('Meta+1'); await sleep(150); }
    }
    const start = Date.now();
    markers.push({ id: seg.id, at: start });
    console.log(`  ▸ ${seg.id}`);
    try { await seg.run(ctx); } catch (e) {
      failed = e;
      console.error(`  ✗ ${seg.id} : ${e.message}`);
      await win.screenshot({ path: path.join(out, 'failure-vscode.png') }).catch(() => {});
      await site.screenshot({ path: path.join(out, 'failure-site.png') }).catch(() => {});
      break;
    }
    const need = (tts[seg.id]?.ms ?? 0) + 700 - (Date.now() - start);
    if (need > 0) await sleep(need);
    if (SHOTS) {
      const n = `shot-${String(i + 1).padStart(2, '0')}-${seg.id}.png`;
      if (scene === 'vscode') await win.screenshot({ path: path.join(out, n) }).catch(() => {});
      else await site.screenshot({ path: path.join(out, n) }).catch(() => {});
    }
  }
  await sleep(1500);
  const end = Date.now();
  await closeVSCode();
  const videos = {};
  for (const k of Object.keys(B)) { const v = B[k].page.video(); await B[k].ctx.close(); videos[k] = await v.path(); }
  await browser.close();
  fs.rmSync(tmp, { recursive: true, force: true });
  if (!process.env.KEEP_HOME) fs.rmSync(home, { recursive: true, force: true });

  // ── Plans : intervalles [a, b] de temps réel, chacun d'une source.
  for (const s of vsources) s.origin = s.end - durationOf(s.path);
  // Bornes : bascules de scène, coupes (on retire [cut.at, cut.resume]).
  const bounds = [...switches.map((s) => s.at), ...cuts.flatMap((c) => [c.at, c.resume]), end].filter((t) => t >= start0 && t <= end);
  const uniq = [...new Set(bounds.concat(start0))].sort((a, b) => a - b);
  const sceneAt = (t) => switches.filter((s) => s.at <= t).pop().scene;
  const inCut = (t) => cuts.some((c) => t >= c.at && t < c.resume);
  const vsrcAt = (t) => vsources[cuts.filter((c) => c.resume <= t).length];
  const pieces = [];
  for (let i = 0; i < uniq.length - 1; i++) {
    const a = uniq[i], b = uniq[i + 1];
    if (b - a < 40 || inCut(a)) continue;
    const sc = sceneAt(a);
    if (sc === 'vscode' && cuts.length && vsrcAt(a) !== vsrcAt(b - 1)) throw new Error('plan VS Code à cheval sur une relance');
    pieces.push({ a, b, scene: sc, src: sc === 'vscode' ? vsrcAt(a) : null });
  }
  // Temps de sortie d'un instant réel (les coupes n'existent pas en sortie).
  const outAt = (t) => pieces.reduce((acc, p) => acc + Math.max(0, Math.min(t, p.b) - p.a), 0);

  const s = (ms) => (ms / 1000).toFixed(3);
  const inputs = [], filters = [], labels = [];
  const inputIndex = new Map();
  const addInput = (f) => { if (!inputIndex.has(f)) { inputIndex.set(f, inputs.length / 2); inputs.push('-i', f); } return inputIndex.get(f); };
  pieces.forEach((p, i) => {
    if (p.scene === 'vscode') {
      const k = addInput(p.src.path);
      filters.push(`[${k}:v]trim=start=${s(p.a - p.src.origin)}:end=${s(p.b - p.src.origin)},setpts=PTS-STARTPTS,scale=${W * SCALE}:${H * SCALE},setsar=1,fps=25[p${i}]`);
    } else {
      const kb = addInput(videos.bar), ks = addInput(videos.site);
      filters.push(`[${kb}:v]trim=start=${s(p.a - B.bar.born)}:end=${s(p.b - B.bar.born)},setpts=PTS-STARTPTS,scale=${SW * SCALE}:${BAR * SCALE},setsar=1[b${i}]`);
      filters.push(`[${ks}:v]trim=start=${s(p.a - B.site.born)}:end=${s(p.b - B.site.born)},setpts=PTS-STARTPTS,scale=${SW * SCALE}:${SH * SCALE},setsar=1[s${i}]`);
      if (DT) {
        const kd = addInput(videos.dt);
        filters.push(`[${kd}:v]trim=start=${s(p.a - B.dt.born)}:end=${s(p.b - B.dt.born)},setpts=PTS-STARTPTS,scale=${(W - SW) * SCALE}:${H * SCALE},setsar=1[d${i}]`);
        filters.push(`[b${i}][s${i}]vstack[l${i}]`, `[l${i}][d${i}]hstack,fps=25[p${i}]`);
      } else filters.push(`[b${i}][s${i}]vstack,pad=${W * SCALE}:${H * SCALE}:0:0:color=0x3b3f4a,fps=25[p${i}]`);
    }
    labels.push(`[p${i}]`);
  });
  filters.push(`${labels.join('')}concat=n=${labels.length}:v=1:a=0[v]`);
  const raw = path.join(out, 'raw.mp4');
  execFileSync('ffmpeg', ['-y', '-v', 'error', ...inputs, '-filter_complex', filters.join(';'), '-map', '[v]',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', raw]);
  const duration = outAt(end);
  fs.writeFileSync(path.join(out, 'markers.json'), JSON.stringify({
    duration,
    markers: markers.map((m) => ({ id: m.id, ms: outAt(m.at) })),
  }, null, 2));
  console.log(`scène : ${(duration / 1000).toFixed(1)} s, ${pieces.length} plans → ${raw}`);
  process.exit(failed ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });
