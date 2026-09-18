/**
 * Confere se algum conteúdo estoura a caixa da página nos modelos de `modelos/`.
 *
 *   npm run check
 *   npm run check -- relatorio-mensal
 *   npm run check -- --dir=documentos/consultores   # outra pasta, e as dela
 *
 * Roda em media print, que é o modo usado na exportação para PDF. Grafismos são
 * ignorados: eles sangram de propósito e ficam recortados por overflow:hidden.
 */
import { chromium } from 'playwright';
import { readdirSync, existsSync, statSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, join, resolve } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const dirArg = process.argv.slice(2).find((a) => a.startsWith('--dir='));
const srcDir = dirArg ? resolve(root, dirArg.slice(6)) : join(root, 'modelos');

function findChromium() {
  const base = process.env.PLAYWRIGHT_BROWSERS_PATH;
  if (!base || !existsSync(base)) return undefined;
  for (const d of readdirSync(base).filter((x) => x.startsWith('chromium-')).sort().reverse()) {
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

const filters = process.argv.slice(2).filter((a) => !a.startsWith('--'));
/** Os HTML de uma pasta. Em `modelos/` é uma lista rasa; fora dela pode haver
 *  uma pasta por assunto — uma por consultor, nos documentos nominais —, e o
 *  caminho devolvido é relativo à raiz da busca. */
function html(dir, prefixo = '') {
  const achados = [];
  for (const nome of readdirSync(dir).sort()) {
    const cheio = join(dir, nome);
    if (statSync(cheio).isDirectory()) {
      achados.push(...html(cheio, join(prefixo, nome)));
    } else if (nome.endsWith('.html')) {
      achados.push(join(prefixo, nome));
    }
  }
  return achados;
}

const files = html(srcDir)
  .filter((f) => filters.length === 0 || filters.some((q) => f.includes(q)));

const browser = await launch();
const page = await browser.newPage();
let bad = 0;

for (const file of files) {
  await page.goto(pathToFileURL(join(srcDir, file)).href, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.emulateMedia({ media: 'print' });
  const problems = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll('.page,.slide').forEach((p, i) => {
      p.querySelectorAll('.graf').forEach((g) => g.remove());
      const box = p.getBoundingClientRect();
      if (p.scrollHeight - p.clientHeight > 1) out.push({ pg: i + 1, kind: 'altura', v: p.scrollHeight - p.clientHeight });
      if (p.scrollWidth - p.clientWidth > 1) out.push({ pg: i + 1, kind: 'largura', v: p.scrollWidth - p.clientWidth });
      const body = p.querySelector('.pg-body');
      if (body && body.scrollHeight - body.clientHeight > 1)
        out.push({ pg: i + 1, kind: 'conteúdo', v: Math.round(body.scrollHeight - body.clientHeight) });
      p.querySelectorAll('table,.kpis,.cards,.plans,.steps,.tl,.dl').forEach((el) => {
        const r = el.getBoundingClientRect();
        if (r.right > box.right + 1 || r.left < box.left - 1)
          out.push({ pg: i + 1, kind: el.className.split(' ')[0], v: Math.round(r.right - box.right) });
      });

      // Transbordo de coluna, e não de página. Uma tabela larga demais para a
      // coluna da grelha em que está não estoura a página — ela invade a coluna
      // vizinha e fica por baixo do que houver lá. Foi assim que o gráfico de
      // proventos passou a ser desenhado por cima da tabela ao lado dele sem
      // que nada aqui reclamasse.
      p.querySelectorAll('.cols2>*,.cols3>*,.cols2u>*').forEach((cel) => {
        const c = cel.getBoundingClientRect();
        for (const el of cel.querySelectorAll('table,.kpis,.cards,.chart,.imgbox')) {
          const r = el.getBoundingClientRect();
          if (r.right > c.right + 1) {
            out.push({ pg: i + 1, kind: `${el.tagName.toLowerCase()} fora da coluna`,
                       v: Math.round(r.right - c.right) });
            break;
          }
        }
      });
    });
    return out;
  });
  if (problems.length) {
    bad++;
    console.log(`\n${file}`);
    for (const p of problems.slice(0, 12)) console.log(`   pág ${p.pg}  ${p.kind}  +${p.v}px`);
    if (problems.length > 12) console.log(`   ... e mais ${problems.length - 12}`);
  }
}

await browser.close();
console.log(bad ? `\n${bad} de ${files.length} arquivo(s) com estouro de página` : `\n${files.length} modelo(s) sem estouro de página.`);
process.exit(bad ? 1 : 0);
