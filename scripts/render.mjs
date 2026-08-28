/**
 * Renderiza os modelos HTML de `modelos/` para PDF em `pdf/`.
 *
 *   npm install
 *   npm run pdf                       # todos os modelos
 *   npm run pdf -- relatorio-mensal   # só os que casam com o filtro
 *
 * O tamanho da página vem do @page de cada arquivo (A4 nos relatórios,
 * 16:9 de 338,667 x 190,5 mm nas apresentações), por isso usamos
 * preferCSSPageSize. printBackground é obrigatório: as capas e os
 * cabeçalhos de tabela dependem de fundos coloridos.
 */
import { chromium } from 'playwright';
import { readdirSync, mkdirSync, existsSync, statSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, join, resolve } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const srcDir = join(root, 'modelos');
const outDir = join(root, 'pdf');

// Ambientes com PLAYWRIGHT_BROWSERS_PATH fixo podem ter um build de Chromium
// diferente do esperado por esta versão do Playwright; nesse caso apontamos
// direto para o executável encontrado.
function findChromium() {
  const base = process.env.PLAYWRIGHT_BROWSERS_PATH;
  if (!base || !existsSync(base)) return undefined;
  const dirs = readdirSync(base)
    .filter((d) => d.startsWith('chromium-'))
    .sort()
    .reverse();
  for (const d of dirs) {
    const exe = join(base, d, 'chrome-linux', 'chrome');
    if (existsSync(exe)) return exe;
  }
  return undefined;
}

async function launch() {
  try {
    return await chromium.launch();
  } catch (err) {
    const executablePath = findChromium();
    if (!executablePath) throw err;
    return await chromium.launch({ executablePath });
  }
}

const filters = process.argv.slice(2);
const files = readdirSync(srcDir)
  .filter((f) => f.endsWith('.html'))
  .filter((f) => filters.length === 0 || filters.some((q) => f.includes(q)))
  .sort();

if (files.length === 0) {
  console.error(`Nenhum modelo encontrado em modelos/${filters.length ? ` para: ${filters.join(', ')}` : ''}`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
const browser = await launch();
const page = await browser.newPage();

for (const file of files) {
  await page.goto(pathToFileURL(join(srcDir, file)).href, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const out = join(outDir, file.replace(/\.html$/, '.pdf'));
  await page.pdf({ path: out, printBackground: true, preferCSSPageSize: true });
  const kb = (statSync(out).size / 1024).toFixed(0);
  console.log(`  ${file.padEnd(46)} -> pdf/${file.replace(/\.html$/, '.pdf')} (${kb} kB)`);
}

await browser.close();
console.log(`${files.length} PDF(s) gerado(s) em pdf/`);
