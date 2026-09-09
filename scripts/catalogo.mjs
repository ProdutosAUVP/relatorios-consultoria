/**
 * Monta o site de `docs/`, que é a ferramenta de preenchimento publicada no
 * GitHub Pages.
 *
 *   npm run site
 *
 * Copia os modelos de `modelos/` para `docs/modelos/` e escreve
 * `docs/catalogo.json`, o índice que a ferramenta lê para saber que
 * documentos existem, que campos cada um tem e em que página cada campo
 * aparece. O índice sai dos próprios modelos: nada aqui é escrito à mão, então
 * um documento novo em `gerador/build.py` aparece na ferramenta sozinho.
 */
import { readdirSync, readFileSync, writeFileSync, mkdirSync, rmSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, resolve } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const srcDir = join(root, 'modelos');
const outDir = join(root, 'docs');
const outModelos = join(outDir, 'modelos');
const outCampos = join(outDir, 'campos');

// Rótulo e ordem dos produtos na ferramenta. O sufixo do arquivo é a chave.
const PRODUTOS = [
  { chave: 'consultoria', nome: 'Consultoria', descricao: 'Consultoria de investimentos AUVP Capital.' },
  { chave: 'alta-renda', nome: 'Alta Renda', descricao: 'Clientes de alta renda, identidade em verde quase preto.' },
  { chave: 'private', nome: 'Private Banking', descricao: 'Marca própria, paleta em cinzas, sem amarelo.' },
  { chave: 'assessoria', nome: 'Assessoria', descricao: 'Assessoria de investimentos, verde mais claro.' },
  { chave: 'me-diz-o-que-fazer', nome: 'Me Diz o Que Fazer', descricao: 'Apresentação individual dos consultores do plano.' },
];

const DOCUMENTOS = [
  { chave: 'relatorio-mensal', nome: 'Relatório mensal', formato: 'a4',
    descricao: 'Fechamento do mês: patrimônio, rentabilidade, alocação e movimentações.' },
  { chave: 'diagnostico-carteira', nome: 'Diagnóstico de carteira', formato: 'a4',
    descricao: 'Leitura da carteira atual, riscos encontrados e plano de ajuste.' },
  { chave: 'relatorio-macroeconomico', nome: 'Relatório macroeconômico', formato: 'a4',
    descricao: 'Cenário do mês no Brasil e no exterior e o que ele muda na estratégia.' },
  { chave: 'apresentacao-geral', nome: 'Apresentação geral', formato: 'slide',
    descricao: 'Deck de apresentação do serviço, para reunião de proposta.' },
  { chave: 'relatorio-mensal-apresentacao', nome: 'Relatório mensal em apresentação', formato: 'slide',
    descricao: 'O fechamento do mês em formato de reunião.' },
  { chave: 'cronograma-reunioes', nome: 'Cronograma de reuniões', formato: 'a4',
    descricao: 'Calendário do ciclo de acompanhamento e pauta de cada encontro.' },
  { chave: 'apresentacao-consultor', nome: 'Apresentação do consultor', formato: 'a4',
    descricao: 'Perfil do consultor, o plano e a AUVP Capital.' },
];

// Consultores: a variante da apresentação não é o segmento, é a pessoa.
function rotuloVariante(chave, sufixo) {
  const p = PRODUTOS.find((x) => x.chave === sufixo);
  if (p) return p.nome;
  return sufixo.split('-').map((s) => s[0].toUpperCase() + s.slice(1)).join(' ');
}

/** Rótulo legível para um campo: `saldo_inicial` -> `Saldo inicial`. */
function rotuloCampo(nome) {
  const t = nome.replace(/_/g, ' ');
  return t.charAt(0).toUpperCase() + t.slice(1);
}

/** Divide o modelo em páginas, na mesma ordem em que aparecem no documento. */
function paginas(html) {
  const partes = html.split(/<section class="/).slice(1);
  return partes.map((p, i) => {
    const corpo = '<section class="' + p;
    let secao = corpo.match(/<div class="sec">([^<]*)<\/div>/)?.[1]?.trim();
    if (!secao) {
      if (/class="[^"]*\bcover\b/.test(corpo)) secao = 'Capa';
      else if (/class="[^"]*\bdivider\b/.test(corpo)) {
        secao = corpo.match(/<div class="dv-t">([^<]*)<\/div>/)?.[1]?.trim() || 'Divisória';
      } else secao = `Página ${i + 1}`;
    }
    return { numero: i + 1, secao: secao.replace(/&[a-z]+;/g, ' ').trim(), corpo };
  });
}

/** Campos e espaços de imagem de um modelo, na ordem do documento. */
function estrutura(html) {
  const campos = {};
  const grupos = [];
  const imagens = [];
  for (const pag of paginas(html)) {
    const nomes = [];
    const re = /<span class="ph"(?: title="([^"]*)")?>\{\{([a-z0-9_]+)\}\}<\/span>/g;
    let m;
    while ((m = re.exec(pag.corpo))) {
      const [, dica, nome] = m;
      if (!campos[nome]) {
        campos[nome] = { rotulo: rotuloCampo(nome), pagina: pag.numero };
        if (dica) campos[nome].dica = dica;
        nomes.push(nome);
      }
    }
    if (nomes.length) grupos.push({ pagina: pag.numero, secao: pag.secao, campos: nomes });

    if (/<img class="rt-img"/.test(pag.corpo)) {
      imagens.push({ id: 'retrato', tipo: 'retrato', pagina: pag.numero, secao: pag.secao,
        rotulo: 'Retrato do consultor',
        descricao: 'Foto vertical, recortada em 3:4. Substitui o retrato que já vem no modelo.' });
    }
    const ri = /<div class="(chart|imgbox)" data-img="(\d+)"[^>]*>([\s\S]*?)<div class="cd">([\s\S]*?)<\/div>/g;
    while ((m = ri.exec(pag.corpo))) {
      imagens.push({
        id: Number(m[2]),
        tipo: m[1] === 'chart' ? 'gráfico' : 'imagem',
        pagina: pag.numero,
        secao: pag.secao,
        rotulo: (m[3].match(/<div class="cl">([\s\S]*?)<\/div>/)?.[1] || 'Imagem')
          .replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').trim(),
        descricao: m[4].replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').trim(),
      });
    }
  }
  return { campos, grupos, imagens };
}

function main() {
  const arquivos = readdirSync(srcDir).filter((f) => f.endsWith('.html')).sort();
  if (!arquivos.length) {
    console.error('Nenhum modelo em modelos/. Rode `npm run build` antes.');
    return 1;
  }

  for (const dir of [outModelos, outCampos]) {
    if (existsSync(dir)) rmSync(dir, { recursive: true });
    mkdirSync(dir, { recursive: true });
  }

  // A chave mais longa primeiro: `relatorio-mensal-apresentacao` também começa
  // com `relatorio-mensal`.
  const porChave = [...DOCUMENTOS].sort((a, b) => b.chave.length - a.chave.length);
  const porDoc = new Map();
  let nc = 0, ni = 0;

  for (const arq of arquivos) {
    const doc = porChave.find((d) => arq.startsWith(d.chave + '-'));
    if (!doc) {
      console.error(`Modelo sem documento correspondente: ${arq}`);
      return 1;
    }
    const sufixo = arq.slice(doc.chave.length + 1, -'.html'.length);
    const html = readFileSync(join(srcDir, arq), 'utf8');
    writeFileSync(join(outModelos, arq), html);

    // A estrutura fica num arquivo por variante, e não no índice: as variantes
    // não são iguais — o relatório mensal de Alta Renda tem ofertas de renda
    // fixa, o de Private tem compromissos de liquidez — e juntar tudo num
    // índice só faria a ferramenta baixar 1,5 MB para abrir a primeira tela.
    const est = estrutura(html);
    writeFileSync(join(outCampos, arq.replace(/\.html$/, '.json')),
                  JSON.stringify({ paginas: paginas(html).length, ...est }));
    nc += Object.keys(est.campos).length;
    ni += est.imagens.length;

    if (!porDoc.has(doc.chave)) porDoc.set(doc.chave, { ...doc, variantes: [] });
    porDoc.get(doc.chave).variantes.push({
      sufixo, rotulo: rotuloVariante(doc.chave, sufixo), arquivo: arq,
      paginas: paginas(html).length,
      campos: Object.keys(est.campos).length,
      imagens: est.imagens.length,
    });
  }

  // Sem data de geração: `docs/` precisa ser reprodutível byte a byte para o
  // `git status` limpo continuar valendo como verificação.
  const catalogo = { produtos: PRODUTOS, documentos: [...porDoc.values()] };
  writeFileSync(join(outDir, 'catalogo.json'), JSON.stringify(catalogo, null, 1));

  console.log(`docs/: ${arquivos.length} modelos, ${catalogo.documentos.length} documentos, `
              + `${nc} campos, ${ni} espaços de imagem.`);
  return 0;
}

process.exit(main());
