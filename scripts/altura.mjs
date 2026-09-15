/**
 * Mede a altura natural do conteúdo das folhas longas — e, com `--ajustar`,
 * escreve essa altura no arquivo.
 *
 *   npm run altura                                    # só mede e relata
 *   npm run altura -- --ajustar                       # mede e grava
 *   npm run altura -- --dir=documentos/consultores --ajustar
 *
 * A apresentação do consultor sai numa folha só. A altura dessa folha tem de
 * estar escrita no CSS: `@page` não aceita altura automática, e é o `@page` que
 * o navegador usa ao imprimir. O gerador escreve um valor de partida
 * (`ALTURA_LONGA`, em `gerador/common.py`), igual para todo mundo.
 *
 * Igual para todo mundo é o que não serve: o texto de cada consultor tem um
 * tamanho, e uma altura só significa vão sobrando em quem escreveu menos. Então
 * este script abre cada folha, solta a altura para ler quanto o conteúdo ocupa
 * de fato — com os respiros elásticos no piso —, e com `--ajustar` reescreve os
 * dois números do arquivo com a medida daquela folha. Cada documento passa a ter
 * a altura do que ele tem dentro.
 *
 * Sobra um respiro pequeno de propósito: a medida é arredondada para cima, o
 * que dá aos respiros elásticos alguns milímetros para repartir e absorve a
 * diferença de renderização entre este navegador e o de quem imprime.
 *
 * `npm run all` roda isto logo depois do build, antes do `check` — é o `check`
 * quem confirma que, na altura nova, nada estourou.
 */
import { chromium } from 'playwright';
import { readdirSync, existsSync, statSync, readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, join, relative, resolve } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const dirArg = process.argv.slice(2).find((a) => a.startsWith('--dir='));
const srcDir = dirArg ? resolve(root, dirArg.slice(6)) : join(root, 'modelos');
const filtros = process.argv.slice(2).filter((a) => !a.startsWith('--'));
const ajustar = process.argv.slice(2).includes('--ajustar');

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

const arquivos = html(srcDir)
  .filter((f) => filtros.length === 0 || filtros.some((q) => f.includes(q)));

const PX_MM = 96 / 25.4;
const mm = (px) => px / PX_MM;

/** Os dois números da altura, como o gerador os escreve. Ficam lado a lado sob
 *  o comentário que os anuncia, e é por isso que dá para trocá-los sem ler CSS:
 *  o `@page` manda na folha de papel, o `.page.longa` manda na caixa desenhada,
 *  e os dois têm de dizer a mesma coisa. */
const ALTURA = /(@page\{size:210mm )(\d+(?:\.\d+)?)(mm;margin:0\}\s*\.page\.longa\{height:)(\d+(?:\.\d+)?)(mm;)/;

/** A altura que a folha vai declarar, a partir do que o conteúdo mede.
 *
 *  Arredonda para cima, ao múltiplo de 5 mm seguinte, com pelo menos 2 mm de
 *  folga: a medida vem deste Chromium e quem imprime pode ter outro, e os
 *  poucos milímetros de sobra são justamente o que os respiros elásticos
 *  repartem entre as seções. O piso é uma folha A4 — abaixo disso não é mais
 *  folha longa, é página comum, e encolher tanto assim seria sinal de que o
 *  documento está vazio, não de que ficou justo. */
const encaixa = (alto) => Math.max(297, Math.ceil((alto + 2) / 5) * 5);

const browser = await launch();
const page = await browser.newPage();
const medidas = [];

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
  if (medido) {
    medidas.push({ arq, alto: mm(medido.alto), declarada: mm(medido.declarada) });
  }
}
await browser.close();

if (!medidas.length) {
  console.log(`Nenhuma folha longa em ${relative(root, srcDir) || '.'}/.`);
  process.exit(0);
}

let escritos = 0;
for (const m of medidas) {
  m.alvo = encaixa(m.alto);
  if (!ajustar) continue;
  const caminho = join(srcDir, m.arq);
  const antes = readFileSync(caminho, 'utf8');
  const depois = antes.replace(ALTURA, (_, a, b, c, d, e) => `${a}${m.alvo}${c}${m.alvo}${e}`);
  if (depois === antes) {
    if (!ALTURA.test(antes)) {
      console.error(`  ! ${m.arq}: não achei a altura declarada para trocar.`);
      process.exitCode = 1;
    }
    continue;   // já estava no número certo
  }
  writeFileSync(caminho, depois);
  m.trocada = true;
  escritos += 1;
}

for (const m of medidas.sort((a, b) => b.alto - a.alto)) {
  const declarada = ajustar ? m.alvo : m.declarada;
  console.log(`  ${m.alto.toFixed(0).padStart(5)} mm de conteúdo  `
              + `em ${declarada.toFixed(0).padStart(5)} mm de folha   ${m.arq}`
              + (m.trocada ? '  (ajustada)' : ''));
}

const altos = medidas.map((m) => m.alto);
console.log(`\n${medidas.length} folha(s), de ${Math.min(...altos).toFixed(0)} a `
            + `${Math.max(...altos).toFixed(0)} mm de conteúdo.`);
if (ajustar) {
  console.log(escritos
    ? `${escritos} arquivo(s) com a altura reescrita. Rode \`npm run check\` e, se os PDF `
      + 'já existirem, \`npm run pdf\`.'
    : 'Nenhuma altura precisou mudar.');
} else {
  const apertadas = medidas.filter((m) => m.alto > m.declarada);
  if (apertadas.length) {
    // Sobra negativa não é estouro: quem diz se estourou é o `npm run check`. O
    // que ela diz é que os respiros dessa folha estão no piso, sem folga
    // nenhuma — o sinal de que a próxima frase acrescentada aperta o desenho.
    console.log(`\n${apertadas.length} folha(s) com os respiros no piso. `
                + 'Rode com `--ajustar` para dar a cada uma a altura do seu conteúdo.');
  }
}
