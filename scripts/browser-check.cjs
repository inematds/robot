// Verificação de navegador do curso robot (v2).
// Uso: BASE_URL=http://127.0.0.1:8775 [PAGES="index.html,curso/trilha1/index.html"] [SHOTS=dir] node scripts/browser-check.cjs
// Checa por página: sem pageerror/console.error, sem overflow horizontal em 390 e 1280 (escuro e claro),
// e (se a página for módulo) nº de tópicos/TOC = manifesto. Testa marcar-lido + % cross-página e o toggle de tema.
const { chromium } = require(process.env.PLAYWRIGHT_PATH || '/home/nmaldaner/projetos/timesmkt3/node_modules/playwright');
const fs = require('fs'), path = require('path');
const base = (process.env.BASE_URL || 'http://127.0.0.1:8775') + '/';
const manifest = JSON.parse(fs.readFileSync(path.join(__dirname, '../docs/curso/_shared/manifest.json'), 'utf8'));
const total = manifest.tracks.reduce((a, t) => a + t.modules.reduce((b, m) => b + m.topics, 0), 0);
const pages = (process.env.PAGES || 'index.html,curso/trilha1/index.html,curso/trilha1/modulo-1-1.html').split(',');
const shots = process.env.SHOTS || path.join(__dirname, '../longrun/2026-10-17-robotica-v2/shots');
const modById = {}; manifest.tracks.forEach(t => t.modules.forEach(m => { modById[m.href] = m; }));
const fails = [], notes = [];
const slug = p => p.replace(/\.html$/, '').replace(/[\/]/g, '_');

(async () => {
  fs.mkdirSync(shots, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  for (const theme of ['escuro', 'claro']) {
    for (const width of [390, 1280]) {
      const ctx = await browser.newContext({ viewport: { width, height: width === 390 ? 844 : 800 } });
      if (theme === 'claro') await ctx.addInitScript(() => { try { localStorage.setItem('inema.prefs', JSON.stringify({ theme: 'claro' })); } catch (e) {} });
      for (const p of pages) {
        const page = await ctx.newPage();
        const errs = [];
        page.on('pageerror', e => errs.push('pageerror: ' + e.message));
        page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
        page.on('requestfailed', r => notes.push(`requestfailed ${p}: ${r.url()}`));
        await page.goto(base + p, { waitUntil: 'networkidle' });
        await page.waitForTimeout(400);
        const isDark = await page.evaluate(() => document.documentElement.classList.contains('dark'));
        if ((theme === 'claro') === isDark) fails.push(`${p} [${theme} ${width}]: tema não aplicado`);
        const ov = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, iw: innerWidth,
          off: [...document.querySelectorAll('body *')].filter(e => e.getBoundingClientRect().right > innerWidth + 1 && getComputedStyle(e).position !== 'fixed').slice(0, 5).map(e => e.tagName + '.' + (e.className && e.className.baseVal === undefined ? e.className : '').toString().slice(0, 60)) }));
        if (ov.sw > ov.iw) fails.push(`${p} [${theme} ${width}]: overflow ${ov.sw}>${ov.iw} ${JSON.stringify(ov.off)}`);
        const m = modById[p];
        if (m) {
          const n = await page.locator('[data-inema-topic]').count(); if (n !== m.topics) fails.push(`${p}: ${n} tópicos != ${m.topics}`);
          const toc = await page.locator('[data-inema-toc] a').count(); if (toc !== m.topics) fails.push(`${p}: TOC ${toc} != ${m.topics}`);
        }
        if (width === 390 && process.env.FIGS) {
          const figs = page.locator('figure.fig, .code-box, table');
          const nf = await figs.count();
          for (let i = 0; i < nf; i++) await figs.nth(i).screenshot({ path: path.join(shots, `${slug(p)}-${theme}-390-el${i + 1}.png`) });
        }
        await page.evaluate(() => window.scrollTo(0, 0));
        await page.waitForTimeout(150);
        await page.screenshot({ path: path.join(shots, `${slug(p)}-${theme}-${width}.png`) });
        errs.forEach(e => fails.push(`${p} [${theme} ${width}]: ${e}`));
        await page.close();
      }
      await ctx.close();
    }
  }
  // Funcional: marcar-lido, % e persistência cross-página, toggle de tema
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await ctx.newPage();
  const mod = pages.find(p => modById[p]);
  if (mod) {
    const mid = modById[mod].id, k = modById[mod].topics;
    await page.goto(base + mod, { waitUntil: 'networkidle' });
    const t = await page.evaluate(() => window.INEMA && INEMA.progress('curso').total);
    if (t !== total) fails.push(`manifesto: total ${t} != ${total}`);
    const btn = page.locator('[data-inema-read-toggle]').first();
    await btn.click(); await page.waitForTimeout(200);
    if (await btn.getAttribute('aria-pressed') !== 'true') fails.push('marcar-lido: aria-pressed não virou true');
    const want = Math.round(100 / k) + '%';
    const pct = async () => (await page.locator(`[data-inema-meter="modulo:${mid}"] [data-inema-meter-pct]`).first().textContent()).trim();
    if (await pct() !== want) fails.push(`marcar-lido: % = ${await pct()} (esperado ${want})`);
    await page.reload({ waitUntil: 'networkidle' });
    if (await pct() !== want) fails.push(`persistência: % após reload = ${await pct()}`);
    const tr = mod.replace(/modulo-.*$/, 'index.html');
    const resp = await page.goto(base + tr, { waitUntil: 'networkidle' });
    if (resp && resp.ok()) {
      if (await pct() !== want) fails.push(`cross-página: anel do módulo no índice = ${await pct()}`);
      else notes.push(`marcar-lido OK: ${mod} -> ${want}, persistiu no reload e no índice da trilha`);
    } else notes.push(`cross-página pulado: ${tr} não existe`);
  }
  await page.goto(base + pages[0], { waitUntil: 'networkidle' });
  const d0 = await page.evaluate(() => document.documentElement.classList.contains('dark'));
  await page.click('#theme-toggle'); await page.waitForTimeout(150);
  const d1 = await page.evaluate(() => document.documentElement.classList.contains('dark'));
  await page.click('#theme-toggle'); await page.waitForTimeout(150);
  const d2 = await page.evaluate(() => document.documentElement.classList.contains('dark'));
  if (!(d0 !== d1 && d2 === d0)) fails.push(`toggle de tema não alterna (${d0},${d1},${d2})`);
  else notes.push('toggle de tema OK (escuro → claro → escuro)');
  await browser.close();
  notes.forEach(n => console.log('·', n));
  if (fails.length) { fails.forEach(f => console.log('FALHA', f)); process.exit(1); }
  console.log(`OK: ${pages.length} página(s) × {escuro, claro} × {390, 1280}: sem erro JS, sem overflow; total do manifesto ${total}.`);
})().catch(e => { console.error('FALHOU', e.message); process.exit(1); });
