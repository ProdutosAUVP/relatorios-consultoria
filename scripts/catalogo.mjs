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

import { PRODUTOS, classifica, rotuloVariante, ordemVariante } from './documentos.mjs';
import { exemplo, nomeado } from './exemplos.mjs';
import { tipoDoCampo, exemploDoTipo, exemploDoCabecalho, OPCOES } from './tipos.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const srcDir = join(root, 'modelos');
const outDir = join(root, 'docs');
const outModelos = join(outDir, 'modelos');
const outCampos = join(outDir, 'campos');

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
    // `data-sec` nomeia a página quando ela não tem cabeçalho corrido.
    let secao = corpo.match(/^<section [^>]*data-sec="([^"]*)"/)?.[1]?.trim()
      || corpo.match(/<div class="sec">([^<]*)<\/div>/)?.[1]?.trim();
    if (!secao) {
      if (/class="[^"]*\bcover\b/.test(corpo)) secao = 'Capa';
      else if (/class="[^"]*\bdivider\b/.test(corpo)) {
        secao = corpo.match(/<div class="dv-t">([^<]*)<\/div>/)?.[1]?.trim() || 'Divisória';
      } else secao = `Página ${i + 1}`;
    }
    return { numero: i + 1, secao: secao.replace(/&[a-z]+;/g, ' ').trim(), corpo };
  });
}

/** Em que coluna de tabela cada campo está: o cabeçalho dela e se a célula é
 *  numérica. É o que diz o tipo do campo com mais segurança do que o nome —
 *  `alvo_rf_pos` é percentual porque a coluna se chama Meta. */
function colunas(html) {
  const limpa = (x) => x.replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').trim();
  const onde = {};
  for (const tb of html.matchAll(/<table class="tb[^"]*">([\s\S]*?)<\/table>/g)) {
    const cabs = [...tb[1].matchAll(/<th[^>]*>([\s\S]*?)<\/th>/g)].map((m) => limpa(m[1]));
    for (const tr of tb[1].matchAll(/<tr>([\s\S]*?)<\/tr>/g)) {
      const tds = [...tr[1].matchAll(/<td([^>]*)>([\s\S]*?)<\/td>/g)];
      if (tds.length !== cabs.length) continue;
      tds.forEach((td, i) => {
        for (const c of td[2].matchAll(/data-campo="([a-z0-9_]+)"/g)) {
          if (!onde[c[1]]) onde[c[1]] = { cabecalho: cabs[i], num: /\bnum\b/.test(td[1]) };
        }
      });
    }
  }
  return onde;
}

/** As tabelas de uma página, célula a célula: o que a ferramenta precisa para
 *  oferecer a tabela como grade — uma linha por linha, os campos nas colunas
 *  certas, o rótulo da linha onde o modelo tem texto fixo — em vez de uma
 *  lista de quarenta campos soltos chamados `mov_1_data`, `mov_1_tipo`... */
function tabelasDe(corpo, numero) {
  const ENT = { nbsp: ' ', mdash: '—', ndash: '–', amp: '&', middot: '·', lt: '<', gt: '>' };
  const limpa = (x) => x.replace(/<[^>]+>/g, '')
    .replace(/&([a-z]+);/g, (m, e) => ENT[e] ?? m).trim();
  const celula = (td) => {
    const campo = td.match(/data-campo="([a-z0-9_]+)"/)?.[1];
    return campo ? { c: campo } : { t: limpa(td) };
  };
  const linhasDe = (bloco) => [...bloco.matchAll(/<tr>([\s\S]*?)<\/tr>/g)]
    .map((tr) => [...tr[1].matchAll(/<td[^>]*>([\s\S]*?)<\/td>/g)].map((m) => celula(m[1])))
    .filter((l) => l.length);
  const out = [];
  for (const tb of corpo.matchAll(/<table class="tb[^"]*">([\s\S]*?)<\/table>/g)) {
    const cabecalhos = [...tb[1].matchAll(/<th[^>]*>([\s\S]*?)<\/th>/g)].map((m) => limpa(m[1]));
    const pe = tb[1].match(/<tfoot>([\s\S]*?)<\/tfoot>/)?.[1] || '';
    const linhas = linhasDe(tb[1].replace(/<tfoot>[\s\S]*?<\/tfoot>/, ''));
    const rodape = pe ? linhasDe(pe) : [];
    const todas = [...linhas, ...rodape];
    if (!todas.length || todas.some((l) => l.length !== cabecalhos.length)) continue;
    if (!todas.some((l) => l.some((c) => c.c))) continue;
    // O título é o último <h2> antes da tabela — "Operações executadas",
    // "Por instituição custodiante" — ou o da página quando não há um.
    const antes = corpo.slice(0, tb.index);
    const h2 = [...antes.matchAll(/<h2[^>]*>([\s\S]*?)<\/h2>/g)].pop()?.[1]
      || antes.match(/<h1[^>]*>([\s\S]*?)<\/h1>/)?.[1] || '';
    out.push({ pagina: numero, titulo: limpa(h2), cabecalhos, linhas, rodape });
  }
  return out;
}

/** Campos e espaços de imagem de um modelo, na ordem do documento. */
function estrutura(html) {
  const campos = {};
  const grupos = [];
  const imagens = [];
  const tabelas = [];
  const emTabela = colunas(html);
  for (const pag of paginas(html)) {
    const nomes = [];
    tabelas.push(...tabelasDe(pag.corpo, pag.numero));
    // Os atributos vêm em número e ordem variáveis — `title` quando há dica,
    // `data-link` quando o campo é endereço de alguma coisa —, então o
    // casamento é pelo bloco e a dica sai de dentro dele.
    // O nome sai do `data-campo`, e não das chaves: o campo que já vem
    // preenchido não tem chaves — o que está escrito ali é o texto padrão, e é
    // ele que a ferramenta oferece para editar.
    const re = /<span class="ph( pronto)?" data-campo="([a-z0-9_]+)"([^>]*)>([\s\S]*?)<\/span>/g;
    let m;
    while ((m = re.exec(pag.corpo))) {
      const [, pronto, nome, attrs, conteudo] = m;
      const dica = attrs.match(/ title="([^"]*)"/)?.[1];
      if (!campos[nome]) {
        const col = emTabela[nome];
        const t = tipoDoCampo(nome, col?.cabecalho, col?.num);
        // O exemplo pelo tipo só entra onde o pelo nome é chute: o que está
        // escrito à mão em `exemplos.mjs` continua valendo.
        const ex = (!nomeado(nome) && (exemploDoTipo(t.tipo) || (t.opcoes && OPCOES[t.opcoes][0])
          || (col && exemploDoCabecalho(col.cabecalho)))) || exemplo(nome);
        campos[nome] = { rotulo: rotuloCampo(nome), pagina: pag.numero, exemplo: ex, ...t };
        if (t.tipo === 'texto') delete campos[nome].tipo;
        if (dica) campos[nome].dica = dica;
        if (pronto) campos[nome].padrao = conteudo.replace(/&nbsp;/g, ' ').trim();
        nomes.push(nome);
      }
    }
    if (nomes.length) grupos.push({ pagina: pag.numero, secao: pag.secao, campos: nomes });

    if (/<img class="rt-img"/.test(pag.corpo)) {
      imagens.push({ id: 'retrato', tipo: 'retrato', pagina: pag.numero, secao: pag.secao,
        rotulo: 'Retrato do consultor',
        descricao: 'Foto vertical, recortada em 3:4. Substitui o retrato que já vem no modelo.' });
    }
    // A classe pode trazer um modificador junto (`imgbox rt-vaga`), então o
    // casamento é pelo nome do bloco dentro do atributo, não pelo atributo todo.
    // A classe pode trazer modificadores e os atributos vêm em qualquer ordem,
    // então o casamento é pelo nome do bloco e pelo `data-img`, não pela forma
    // exata da tag.
    const ri = /<div class="[^"]*\b(chart|imgbox)\b[^"]*"([^>]*)\bdata-img="(\d+)"([^>]*)>([\s\S]*?)<div class="cd">([\s\S]*?)<\/div>/g;
    while ((m = ri.exec(pag.corpo))) {
      // O bloco de gráfico anuncia o formato e os rótulos sugeridos. É o que
      // permite à ferramenta oferecer a tabelinha certa — quantas linhas, com
      // que nome, e se pede um valor ou dois — em vez de um campo de imagem.
      const attrs = m[2] + m[4];
      const limpa = (x) => x.replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').trim();
      const serie = attrs.match(/data-series="([^"]*)"/)?.[1];
      const pts = attrs.match(/data-pontos="([^"]*)"/)?.[1];
      imagens.push({
        id: Number(m[3]),
        tipo: m[1] === 'chart' ? 'gráfico' : 'imagem',
        grafico: attrs.match(/data-grafico="([^"]*)"/)?.[1] || null,
        series: serie ? serie.split('|') : null,
        eixo: attrs.match(/data-eixo="([^"]*)"/)?.[1] || null,
        pontos: pts ? pts.split('|') : null,
        pagina: pag.numero,
        secao: pag.secao,
        rotulo: limpa(m[5].match(/<div class="cl">([\s\S]*?)<\/div>/)?.[1] || 'Imagem'),
        descricao: limpa(m[6]),
      });
    }
  }
  return { campos, grupos, imagens, tabelas };
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

  const porDoc = new Map();
  let nc = 0, ni = 0;

  for (const arq of arquivos) {
    const achado = classifica(arq);
    if (!achado) {
      console.error(`Modelo sem documento correspondente: ${arq}`);
      return 1;
    }
    const { doc, sufixo } = achado;
    const html = readFileSync(join(srcDir, arq), 'utf8');
    writeFileSync(join(outModelos, arq), html);

    // A estrutura fica num arquivo por variante, e não no índice: as variantes
    // não são iguais — o relatório mensal de Alta Renda tem ofertas de renda
    // fixa, o de Private tem compromissos de liquidez — e juntar tudo num
    // índice só faria a ferramenta baixar 1,5 MB para abrir a primeira tela.
    const est = estrutura(html);
    // A lista de páginas, e não só a contagem: é ela que a ferramenta usa para
    // deixar escolher quais entram no documento exportado, inclusive as que não
    // têm campo nenhum — capa, divisória, fecho.
    const pags = paginas(html).map((p) => ({ numero: p.numero, secao: p.secao }));
    writeFileSync(join(outCampos, arq.replace(/\.html$/, '.json')),
                  JSON.stringify({ paginas: pags.length, indice: pags, ...est }));
    nc += Object.keys(est.campos).length;
    ni += est.imagens.length;

    if (!porDoc.has(doc.chave)) porDoc.set(doc.chave, { ...doc, variantes: [] });
    porDoc.get(doc.chave).variantes.push({
      sufixo, rotulo: rotuloVariante(sufixo, html), arquivo: arq,
      paginas: paginas(html).length,
      campos: Object.keys(est.campos).length,
      imagens: est.imagens.length,
    });
  }

  // Sem data de geração: `docs/` precisa ser reprodutível byte a byte para o
  // `git status` limpo continuar valendo como verificação.
  const rotuloBase = (v) => v.rotulo.replace(/, sem data$/, '');
  for (const d of porDoc.values()) {
    d.variantes.sort((a, b) => {
      const [ga, pa, da] = ordemVariante(a.sufixo);
      const [gb, pb, db] = ordemVariante(b.sufixo);
      // A gêmea sem data vem logo depois da sua, e não em outro ponto da lista.
      return ga - gb || pa - pb
        || rotuloBase(a).localeCompare(rotuloBase(b), 'pt-BR') || da - db;
    });
  }

  const catalogo = { produtos: PRODUTOS, documentos: [...porDoc.values()], opcoes: OPCOES };
  writeFileSync(join(outDir, 'catalogo.json'), JSON.stringify(catalogo, null, 1));

  console.log(`docs/: ${arquivos.length} modelos, ${catalogo.documentos.length} documentos, `
              + `${nc} campos, ${ni} espaços de imagem.`);
  return 0;
}

process.exit(main());
