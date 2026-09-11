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
import { readdirSync, mkdirSync, existsSync, statSync, rmSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, join, resolve } from 'node:path';

import { PRODUTOS, classifica } from './documentos.mjs';

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

// Uma pasta por produto. São 31 arquivos: numa lista só, achar o diagnóstico
// do Private é ler nome por nome; separados, é abrir uma pasta. O nome do
// arquivo continua completo, para um PDF baixado sozinho não virar
// `relatorio-mensal.pdf` sem dizer de quem é.
const ordem = new Map(PRODUTOS.map((p, i) => [p.chave, i]));
const emOrdem = [...files].sort((a, b) => {
  const pa = classifica(a)?.produto, pb = classifica(b)?.produto;
  const d = (ordem.get(pa) ?? 99) - (ordem.get(pb) ?? 99);
  return d || a.localeCompare(b);
});

const browser = await launch();
const page = await browser.newPage();
let produtoAtual = null;

for (const file of emOrdem) {
  const achado = classifica(file);
  if (!achado) {
    console.error(`Modelo sem documento correspondente: ${file}`);
    process.exit(1);
  }
  const pasta = join(outDir, achado.produto);
  if (achado.produto !== produtoAtual) {
    produtoAtual = achado.produto;
    mkdirSync(pasta, { recursive: true });
    console.log(`\n  ${achado.produto}/`);
  }

  await page.goto(pathToFileURL(join(srcDir, file)).href, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const nome = file.replace(/\.html$/, '.pdf');
  const out = join(pasta, nome);
  await page.pdf({ path: out, printBackground: true, preferCSSPageSize: true });
  const kb = (statSync(out).size / 1024).toFixed(0);
  console.log(`    ${nome.padEnd(50)} ${kb} kB`);
}

// Sem filtro, o render é a lista completa: um PDF que sobrou de uma variante
// renomeada continuaria em `pdf/` sem nada em `modelos/` que o produza. É a
// mesma limpeza que o `build.py` faz.
if (!filters.length) {
  const esperados = new Set(emOrdem.map((f) => join(classifica(f).produto, f.replace(/\.html$/, '.pdf'))));
  for (const pasta of readdirSync(outDir)) {
    const dir = join(outDir, pasta);
    if (!statSync(dir).isDirectory()) continue;
    for (const arq of readdirSync(dir)) {
      if (arq.endsWith('.pdf') && !esperados.has(join(pasta, arq))) {
        rmSync(join(dir, arq));
        console.log(`  removido ${pasta}/${arq} (não é mais gerado)`);
      }
    }
    if (!readdirSync(dir).length) rmSync(dir, { recursive: true });
  }
}

await browser.close();
console.log(`\n${emOrdem.length} PDF(s) em pdf/, em ${new Set(emOrdem.map((f) => classifica(f).produto)).size} pastas.`);
