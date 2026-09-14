/**
 * Mede a altura natural do conteúdo das folhas longas.
 *
 *   npm run altura
 *   npm run altura -- --dir=documentos/consultores
 *
 * A apresentação do consultor sai numa folha só, e a altura dessa folha é fixa:
 * `@page` não aceita altura automática, e é o `@page` que a ferramenta usa ao
 * imprimir pelo navegador. A altura vive em `ALTURA_LONGA`, em
 * `gerador/common.py`.
 *
 * Este script mede quanto o conteúdo de cada folha ocupa de fato, com os
 * respiros elásticos no piso. Serve para escolher o número: ele tem de ser
 * maior que a maior das medidas — senão estoura, e o `npm run check` acusa — e
 * não muito maior que ela, senão sobra vão. A diferença entre a maior e a menor
 * é o que os respiros repartem.
 *
 * Não faz parte do `npm run all`: a altura só muda quando o conteúdo do
 * documento muda, e aí se roda isto e se acerta a constante à mão.
 */
import { chromium } from 'playwright';
import { readdirSync, existsSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, join, relative, resolve } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const dirArg = process.argv.slice(2).find((a) => a.startsWith('--dir='));
const srcDir = dirArg ? resolve(root, dirArg.slice(6)) : join(root, 'modelos');
const filtros = process.argv.slice(2).filter((a) => !a.startsWith('--'));

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

const arquivos = readdirSync(srcDir)
  .filter((f) => f.endsWith('.html'))
  .filter((f) => filtros.length === 0 || filtros.some((q) => f.includes(q)))
  .sort();

const browser = await launch();
const page = await browser.newPage();
const medidas = [];
const PX_MM = 96 / 25.4;

for (const arq of arquivos) {
  await page.goto(pathToFileURL(join(srcDir, arq)).href, { waitUntil: 'load' });
  await page.emulateMedia({ media: 'print' });
  await page.evaluate(() => document.fonts.ready);
  const medido = await page.evaluate(() => {
    const s = document.querySelector('.page.longa');
    if (!s) return null;
    // Com a altura fixa o conteúdo já está esticado pelos respiros; solta a
    // altura para ler o que ele ocupa com os respiros no piso.
    const antes = s.style.height;
    s.style.height = 'auto';
    const alto = s.getBoundingClientRect().height;
    const declarada = (s.style.height = antes, s.getBoundingClientRect().height);
    return { alto, declarada };
  });
  if (medido) medidas.push({ arq, ...medido });
}
await browser.close();

if (!medidas.length) {
  console.log(`Nenhuma folha longa em ${relative(root, srcDir) || '.'}/.`);
  process.exit(0);
}

const mm = (px) => px / PX_MM;
const declarada = mm(medidas[0].declarada);
for (const m of medidas.sort((a, b) => b.alto - a.alto)) {
  const sobra = declarada - mm(m.alto);
  console.log(`  ${mm(m.alto).toFixed(0).padStart(5)} mm  `
              + `(sobra ${sobra.toFixed(0).padStart(4)} mm)   ${m.arq}`);
}
const altos = medidas.map((m) => mm(m.alto));
console.log(`\n${medidas.length} folha(s). Conteúdo de ${Math.min(...altos).toFixed(0)} `
            + `a ${Math.max(...altos).toFixed(0)} mm; página declarada em ${declarada.toFixed(0)} mm.`);
if (Math.max(...altos) > declarada) {
  // Sobra negativa não é estouro: quem diz se estourou é o `npm run check`. O
  // que ela diz é que os respiros dessa folha estão no piso, sem folga nenhuma
  // — o sinal de que a próxima frase acrescentada vai apertar o desenho.
  console.log('\nA maior folha já usa os respiros no piso. Convém subir ALTURA_LONGA.');
}
