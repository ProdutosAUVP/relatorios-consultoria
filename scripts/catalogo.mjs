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
import { exemplo } from './exemplos.mjs';

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
        campos[nome] = { rotulo: rotuloCampo(nome), pagina: pag.numero, exemplo: exemplo(nome) };
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
    // A classe pode trazer um modificador junto (`imgbox rt-vaga`), então o
    // casamento é pelo nome do bloco dentro do atributo, não pelo atributo todo.
    // A classe pode trazer modificadores e os atributos vêm em qualquer ordem,
    // então o casamento é pelo nome do bloco e pelo `data-img`, não pela forma
    // exata da tag.
    const ri = /<div class="[^"]*\b(chart|imgbox)\b[^"]*"[^>]*\bdata-img="(\d+)"[^>]*>([\s\S]*?)<div class="cd">([\s\S]*?)<\/div>/g;
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
    writeFileSync(join(outCampos, arq.replace(/\.html$/, '.json')),
                  JSON.stringify({ paginas: paginas(html).length, ...est }));
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

  const catalogo = { produtos: PRODUTOS, documentos: [...porDoc.values()] };
  writeFileSync(join(outDir, 'catalogo.json'), JSON.stringify(catalogo, null, 1));

  console.log(`docs/: ${arquivos.length} modelos, ${catalogo.documentos.length} documentos, `
              + `${nc} campos, ${ni} espaços de imagem.`);
  return 0;
}

process.exit(main());
