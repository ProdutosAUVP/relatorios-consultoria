/* Ferramenta de preenchimento dos modelos AUVP Capital.
 *
 * Sem build e sem dependência: o navegador baixa `catalogo.json` (o índice),
 * `campos/<modelo>.json` (os campos daquela variante) e o próprio modelo HTML.
 * O documento exportado é o mesmo modelo do repositório, com os valores no
 * lugar dos campos — o que sai daqui é o que sai do gerador em Python.
 */
'use strict';

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

const TELAS = ['produto', 'documento', 'variante', 'preencher', 'exportar'];
const ARMAZEM = 'auvp-modelos-v1';

const estado = {
  catalogo: null,
  produto: null,
  documento: null,
  variante: null,
  estrutura: null,   // campos, grupos e imagens da variante escolhida
  modelo: null,      // Document do modelo, já parseado
  valores: {},       // campo -> texto
  imagens: {},       // espaço de imagem -> data URL
  fora: new Set(),   // páginas tiradas do documento
  pagina: 1,
  tela: 'produto',
};

/* ---------------------------------------------------------------- utilidades */

const escapa = (s) => String(s).replace(/[&<>"]/g,
  (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

function nomeArquivo(ext) {
  return `${estado.documento.chave}-${estado.variante.sufixo}-${new Date().toISOString().slice(0, 7)}.${ext}`;
}

function baixar(conteudo, nome, tipo) {
  const url = URL.createObjectURL(new Blob([conteudo], { type: tipo }));
  const a = Object.assign(document.createElement('a'), { href: url, download: nome });
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

/* ------------------------------------------------------------- persistência */

/* O que foi digitado não pode se perder num F5, e o navegador oferece dois
 * lugares com garantias diferentes. O texto vai para o localStorage, que é
 * síncrono e sobrevive a qualquer coisa; as imagens vão para o IndexedDB,
 * porque um data URL de foto passa de 1 MB e estouraria a cota de 5 MB do
 * localStorage no primeiro documento com três gráficos. Guardar tudo junto
 * faria o texto se perder junto com as imagens quando a cota acabasse. */

const chaveArmazem = () => `${ARMAZEM}:${estado.documento.chave}:${estado.variante.sufixo}`;

let bd = null;

function abrirBanco() {
  if (bd) return bd;
  bd = new Promise((ok, falha) => {
    const req = indexedDB.open(ARMAZEM, 1);
    req.onupgradeneeded = () => req.result.createObjectStore('imagens');
    req.onsuccess = () => ok(req.result);
    req.onerror = () => falha(req.error);
  }).catch(() => null);   // navegador sem IndexedDB: segue sem guardar imagem
  return bd;
}

async function comLoja(modo, fn) {
  const db = await abrirBanco();
  if (!db) return null;
  return new Promise((ok) => {
    const tx = db.transaction('imagens', modo);
    const req = fn(tx.objectStore('imagens'));
    tx.oncomplete = () => ok(req ? req.result : null);
    tx.onerror = () => ok(null);
  });
}

let aviso = null;

function anunciarSalvo(texto = 'Salvo neste navegador') {
  const el = $('#salvo');
  if (!el) return;
  el.textContent = texto;
  el.hidden = false;
  clearTimeout(aviso);
  aviso = setTimeout(() => { el.hidden = true; }, 2500);
}

function salvar() {
  try {
    localStorage.setItem(chaveArmazem(), JSON.stringify({
      valores: estado.valores, fora: [...estado.fora],
    }));
    anunciarSalvo();
  } catch (e) {
    anunciarSalvo('Este navegador não está guardando o rascunho');
  }
}

function salvarImagens() {
  comLoja('readwrite', (loja) => loja.put(estado.imagens, chaveArmazem()))
    .then(() => anunciarSalvo());
}

async function carregar() {
  try {
    const d = JSON.parse(localStorage.getItem(chaveArmazem()) || 'null');
    estado.valores = (d && d.valores) || {};
    estado.fora = new Set((d && d.fora) || []);
    // Rascunho salvo antes de as imagens irem para o IndexedDB.
    if (d && d.imagens) estado.imagens = d.imagens;
  } catch (e) { /* rascunho corrompido: começa vazio */ }
  const imgs = await comLoja('readonly', (loja) => loja.get(chaveArmazem()));
  if (imgs) estado.imagens = imgs;
}

/* ------------------------------------------------------------------ navegação */

function podeIr(tela) {
  if (tela === 'produto') return true;
  if (tela === 'documento') return !!estado.produto;
  if (tela === 'variante') return !!estado.documento;
  return !!estado.variante && !!estado.modelo;
}

function mostrar(tela) {
  estado.tela = tela;
  $('#carregando').hidden = true;
  TELAS.forEach((t) => { $(`#tela-${t}`).hidden = t !== tela; });
  const i = TELAS.indexOf(tela);
  $$('.passo').forEach((b, j) => {
    b.setAttribute('aria-current', String(j === i));
    b.classList.toggle('feito', j < i);
    b.disabled = !podeIr(TELAS[j]);
  });
  if (tela === 'preencher') requestAnimationFrame(ajustarQuadro);
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

/* ------------------------------------------------------------ tela 1: produto */

const AMOSTRAS = {
  consultoria: ['#023620', '#EFBF4F'],
  'alta-renda': ['#010F08', '#EFBF4F'],
  private: ['#666666', '#8C939A'],
  assessoria: ['#005F45', '#EFBF4F'],
};

/** As variantes de um documento que pertencem a este produto.
 *  Quando a variante é um segmento, o produto é ela mesma; quando não é, é um
 *  plano ou um consultor, e os dois são da consultoria. */
function produtoDaVariante(sufixo) {
  // O `-sem-data` é a mesma variante sem a data no cabeçalho, e não muda de
  // produto: `alta-renda-sem-data` continua sendo Alta Renda.
  const base = sufixo.replace(/-sem-data$/, '');
  return estado.catalogo.produtos.some((p) => p.chave === base) ? base : 'consultoria';
}

const variantesDoProduto = (doc, produto) =>
  doc.variantes.filter((v) => produtoDaVariante(v.sufixo) === produto);

const documentosDoProduto = (p) =>
  estado.catalogo.documentos.filter((d) => variantesDoProduto(d, p).length);

function telaProduto() {
  $('#grade-produtos').innerHTML = estado.catalogo.produtos.map((p) => {
    const [c1, c2] = AMOSTRAS[p.chave] || ['#023620', '#EFBF4F'];
    const n = documentosDoProduto(p.chave).length;
    return `<button type="button" class="cartao" data-produto="${escapa(p.chave)}">
      <span class="amostra"><i style="background:${c1}"></i><i style="background:${c2}"></i></span>
      <span class="nome">${escapa(p.nome)}</span>
      <span class="desc">${escapa(p.descricao)}</span>
      <span class="meta">${n} documento${n === 1 ? '' : 's'}</span>
    </button>`;
  }).join('');
}

/* ---------------------------------------------------------- tela 2: documento */

function telaDocumento() {
  const p = estado.catalogo.produtos.find((x) => x.chave === estado.produto);
  $('#sub-documento').textContent = `Documentos disponíveis para ${p.nome}.`;
  $('#grade-documentos').innerHTML = documentosDoProduto(estado.produto).map((d) => {
    const v = variantesDoProduto(d, estado.produto)[0];
    const n = variantesDoProduto(d, estado.produto).length;
    return `<button type="button" class="cartao" data-documento="${escapa(d.chave)}">
      <span class="nome">${escapa(d.nome)}</span>
      <span class="desc">${escapa(d.descricao)}</span>
      <span class="meta">${v.paginas} ${d.formato === 'slide' ? 'slides' : 'páginas'}
        · ${v.campos} campos${v.imagens ? ` · ${v.imagens} imagens` : ''}${n > 1 ? ` · ${n} versões` : ''}</span>
    </button>`;
  }).join('');
}

/* ----------------------------------------------------------- tela 3: variante */

function telaVariante() {
  const vs = variantesDoProduto(estado.documento, estado.produto);
  $('#sub-variante').textContent = `${estado.documento.nome} — escolha de quem é este documento.`;
  $('#grade-variantes').innerHTML = vs.map((v) => `
    <button type="button" class="cartao" data-variante="${escapa(v.sufixo)}">
      <span class="nome">${escapa(v.rotulo)}</span>
      <span class="meta">${v.paginas} páginas · ${v.campos} campos</span>
    </button>`).join('');
}

async function escolherVariante(v) {
  estado.variante = v;
  TELAS.forEach((t) => { $(`#tela-${t}`).hidden = true; });
  $('#carregando').hidden = false;
  $('#carregando').textContent = 'Carregando o modelo…';
  try {
    const [estrutura, texto] = await Promise.all([
      fetch(`campos/${v.arquivo.replace(/\.html$/, '.json')}`).then((r) => r.json()),
      fetch(`modelos/${v.arquivo}`).then((r) => r.text()),
    ]);
    estado.estrutura = estrutura;
    estado.modelo = new DOMParser().parseFromString(texto, 'text/html');
    estado.valores = {};
    estado.imagens = {};
    estado.fora = new Set();
    estado.pagina = 1;
    await carregar();
    telaPreencher();
    mostrar('preencher');
  } catch (e) {
    $('#carregando').textContent = 'Não foi possível carregar o modelo.';
    setTimeout(() => mostrar('documento'), 1500);
  }
}

/* ------------------------------------------------------------------- páginas */

/* O documento sai com as páginas que o usuário deixar marcadas. A escolha vive
 * no rascunho junto com os valores, e vale para a prévia, para o PDF e para o
 * HTML — tirar uma página não é um recorte do arquivo exportado, é o documento
 * ter outro tamanho. */

const dentro = (n) => !estado.fora.has(n);
const incluidas = () => (estado.estrutura.indice || []).filter((p) => dentro(p.numero));

function alternarPagina(n) {
  if (estado.fora.has(n)) estado.fora.delete(n);
  else estado.fora.add(n);
  // Nunca todas fora: um documento sem página nenhuma não é exportável.
  if (!incluidas().length) estado.fora.delete(n);
  salvar();
  telaPreencher();
}

function listaDePaginas() {
  const idx = estado.estrutura.indice || [];
  if (idx.length < 2) return '';
  const n = incluidas().length;
  return `<details class="secao paginas"${n < idx.length ? ' open' : ''}>
    <summary>
      <span class="pg">${String(idx.length).padStart(2, '0')}</span>
      <span>Páginas do documento</span>
      <span class="contagem${n === idx.length ? ' pronto' : ''}">${n}/${idx.length}</span>
    </summary>
    <div class="campos">
      <p class="dica" style="margin:0 0 2mm">Desmarque o que não deve entrar neste documento.</p>
      ${idx.map((p) => `<label class="pg-item">
        <input type="checkbox" data-pagina="${p.numero}"${dentro(p.numero) ? ' checked' : ''}>
        <span class="n">${String(p.numero).padStart(2, '0')}</span>
        <span>${escapa(p.secao)}</span>
      </label>`).join('')}
    </div>
  </details>`;
}

/* ---------------------------------------------------------- tela 4: preencher */

/** Texto corrido ganha textarea; o resto, uma linha. O critério é o sufixo do
 *  nome, que no gerador já distingue os dois casos. */
const multilinha = (n) => /(texto|analise|comentario|resumo|nota|observacao|descricao|leitura|contexto|justificativa|recomendacao|conclusao|mensagem|sintese)$/.test(n);

function telaPreencher() {
  $('#titulo-preencher').textContent = `${estado.documento.nome} — ${estado.variante.rotulo}`;
  const { grupos, campos, imagens } = estado.estrutura;

  const porPagina = new Map();
  for (const g of grupos) porPagina.set(g.pagina, { ...g, imagens: [] });
  for (const im of imagens) {
    if (!porPagina.has(im.pagina)) {
      porPagina.set(im.pagina, { pagina: im.pagina, secao: im.secao, campos: [], imagens: [] });
    }
    porPagina.get(im.pagina).imagens.push(im);
  }
  const secoes = [...porPagina.values()].sort((a, b) => a.pagina - b.pagina);

  $('#formulario').innerHTML = listaDePaginas() + (secoes.length ? secoes.map((s, i) => `
    <details class="secao${dentro(s.pagina) ? '' : ' fora'}" data-pagina="${s.pagina}"${i === 0 && dentro(s.pagina) ? ' open' : ''}>
      <summary>
        <span class="pg">${String(s.pagina).padStart(2, '0')}</span>
        <span>${escapa(s.secao)}</span>
        <span class="contagem" data-contagem="${s.pagina}"></span>
      </summary>
      <div class="campos">
        ${s.imagens.map(campoImagem).join('')}
        ${s.campos.map((n) => campoTexto(n, campos[n])).join('')}
      </div>
    </details>`).join('')
    : '<p class="solto">Este modelo não tem campos preenchíveis.</p>');

  atualizarContagens();
  renderizar();
}

function campoTexto(nome, meta) {
  const v = escapa(estado.valores[nome] || '');
  const cheio = (estado.valores[nome] || '').trim() ? ' data-preenchido="1"' : '';
  const dica = meta.dica ? `<p class="dica">${escapa(meta.dica)}</p>` : '';
  // O exemplo é `placeholder`: mostra o formato esperado, some ao digitar e
  // nunca entra no documento.
  const ex = meta.exemplo ? ` placeholder="${escapa(meta.exemplo)}"` : '';
  const entrada = multilinha(nome)
    ? `<textarea id="c-${nome}" rows="3" data-campo="${nome}"${ex}${cheio}>${v}</textarea>`
    : `<input id="c-${nome}" type="text" data-campo="${nome}" value="${v}"${ex}${cheio}>`;
  return `<div class="campo" data-nome="${nome}">
    <label for="c-${nome}">${escapa(meta.rotulo)}</label>${entrada}${dica}</div>`;
}

function campoImagem(im) {
  const dado = estado.imagens[im.id];
  return `<div class="imagem${dado ? ' cheia' : ''}" data-imagem="${escapa(im.id)}">
    <span class="miniatura"${dado ? ` style="background-image:url('${dado}')"` : ''}>${dado ? '' : escapa(im.tipo)}</span>
    <div>
      <div class="nome">${escapa(im.rotulo)}</div>
      <div class="desc">${escapa(im.descricao)}</div>
      <div class="acoes">
        <label class="btn neutro pequeno">${dado ? 'Trocar' : 'Enviar imagem'}
          <input type="file" accept="image/*" data-arquivo="${escapa(im.id)}"></label>
        ${dado ? `<button type="button" class="btn neutro pequeno" data-tirar="${escapa(im.id)}">Remover</button>` : ''}
      </div>
    </div>
  </div>`;
}

function atualizarContagens() {
  const { grupos, imagens } = estado.estrutura;
  const conta = new Map();
  for (const g of grupos) {
    conta.set(g.pagina, {
      total: g.campos.length,
      feitos: g.campos.filter((n) => (estado.valores[n] || '').trim()).length,
    });
  }
  for (const im of imagens) {
    if (!conta.has(im.pagina)) conta.set(im.pagina, { total: 0, feitos: 0 });
    const c = conta.get(im.pagina);
    c.total += 1;
    if (estado.imagens[im.id]) c.feitos += 1;
  }
  for (const [pag, c] of conta) {
    const el = $(`[data-contagem="${pag}"]`);
    if (!el) continue;
    el.textContent = `${c.feitos}/${c.total}`;
    el.classList.toggle('pronto', c.feitos === c.total);
  }
}

/* ------------------------------------------------------------------- montagem */

/** O modelo com os valores no lugar.
 *  `modo` é 'previa' (realce do que já foi preenchido), 'exportar' (documento
 *  limpo) ou 'imprimir' (limpo, e chama a impressão sozinho ao abrir).
 *  Campo em branco continua como `{{campo}}` destacado, para o documento
 *  exportado dizer o que ainda falta. */
function montar(modo) {
  const doc = estado.modelo.cloneNode(true);

  // As páginas desmarcadas saem, e as que ficam são renumeradas: o rodapé tem
  // de contar o documento que existe, não o que existia antes do corte.
  const paginas = [...doc.querySelectorAll('.page, .slide')];
  paginas.forEach((p, i) => { if (!dentro(i + 1)) p.remove(); });
  [...doc.querySelectorAll('.page, .slide')].forEach((p, i) => {
    const no = p.querySelector('.pg-foot .no');
    if (no) no.textContent = String(i + 1).padStart(2, '0');
  });

  for (const span of doc.querySelectorAll('span.ph')) {
    const m = span.textContent.match(/^\{\{([a-z0-9_]+)\}\}$/);
    if (!m) continue;
    const v = estado.valores[m[1]];
    if (!v || !v.trim()) continue;
    span.textContent = v;
    span.classList.add('feito');
  }

  for (const [id, dado] of Object.entries(estado.imagens)) {
    const bloco = doc.querySelector(`[data-img="${CSS.escape(String(id))}"]`);
    if (!bloco) continue;
    // A imagem herda o encaixe do bloco que substitui — o estilo e os
    // modificadores de classe —, então o retângulo que era moldura de gráfico
    // ou de retrato continua ocupando exatamente o mesmo espaço, com a mesma
    // proporção e o mesmo canto arredondado.
    const cheia = doc.createElement('div');
    cheia.className = ['imgcheia', ...bloco.classList]
      .filter((c) => c !== 'chart' && c !== 'imgbox').join(' ');
    cheia.setAttribute('style', bloco.getAttribute('style') || '');
    const img = doc.createElement('img');
    img.src = dado;
    img.alt = '';
    cheia.appendChild(img);
    bloco.replaceWith(cheia);
  }

  const estilo = doc.createElement('style');
  estilo.textContent = '.imgcheia{overflow:hidden;display:flex}'
    + '.imgcheia img{width:100%;height:100%;object-fit:cover;display:block}'
    + (modo === 'previa'
      ? '.ph.feito{background:hsl(155 93% 11% / .10);color:inherit}'
      : '.ph.feito{background:none;color:inherit;padding:0;font-weight:inherit}');
  doc.head.appendChild(estilo);

  if (modo === 'imprimir') {
    const s = doc.createElement('script');
    s.textContent = 'addEventListener("load",()=>setTimeout(()=>print(),300))';
    doc.body.appendChild(s);
  }
  return '<!doctype html>\n' + doc.documentElement.outerHTML;
}

function renderizar() {
  const doc = $('#quadro').contentDocument;
  doc.open();
  doc.write(montar('previa'));
  doc.close();
  setTimeout(ajustarQuadro, 50);
}

/** O modelo tem largura fixa em mm; a prévia mostra uma página por vez,
 *  escalada para caber na coluna. */
function ajustarQuadro() {
  const quadro = $('#quadro');
  const moldura = $('#moldura');
  const doc = quadro.contentDocument;
  const paginas = doc ? doc.querySelectorAll('.page, .slide') : [];
  if (!paginas.length) return;

  estado.pagina = Math.min(Math.max(1, estado.pagina), paginas.length);
  $('#pag-atual').textContent = `${estado.pagina} / ${paginas.length}`;
  paginas.forEach((p, i) => { p.style.display = i === estado.pagina - 1 ? '' : 'none'; });

  const alvo = paginas[estado.pagina - 1];
  const l = alvo.offsetWidth || 1;
  const a = alvo.offsetHeight || 1;
  // Cabe na largura da coluna e na altura da janela: a página inteira à vista
  // vale mais do que ver o topo em tamanho real.
  const palco = $('.palco');
  const alturaLivre = Math.max(240, window.innerHeight - palco.getBoundingClientRect().top - 60);
  const escala = Math.min(1, (palco.clientWidth - 40) / l, alturaLivre / a);
  quadro.style.width = `${l}px`;
  quadro.style.height = `${a}px`;
  quadro.style.transform = `scale(${escala})`;
  moldura.style.width = `${l * escala}px`;
  moldura.style.height = `${a * escala}px`;
}

/** A prévia mostra só as páginas incluídas, então a seção do formulário — que
 *  conhece o número original — aponta para a posição que a página tem agora. */
function irPara(original) {
  const i = (estado.estrutura.indice || []).filter((p) => dentro(p.numero))
    .findIndex((p) => p.numero === original);
  estado.pagina = i >= 0 ? i + 1 : original;
  ajustarQuadro();
}

/* ----------------------------------------------------------- tela 5: exportar */

function telaExportar() {
  const { campos, imagens } = estado.estrutura;
  const nomes = Object.keys(campos);
  const feitos = nomes.filter((n) => (estado.valores[n] || '').trim()).length;
  const imgFeitas = imagens.filter((i) => estado.imagens[i.id]).length;
  const faltam = nomes.length - feitos;

  $('#sub-exportar').textContent = `${estado.documento.nome} — ${estado.variante.rotulo}.`;
  $('#resumo').innerHTML = `
    <div><div class="r">Documento</div><div class="v">${escapa(estado.documento.nome)}</div></div>
    <div><div class="r">Versão</div><div class="v">${escapa(estado.variante.rotulo)}</div></div>
    <div><div class="r">Páginas</div>
      <div class="v${estado.fora.size ? ' alerta' : ''}">${incluidas().length || estado.estrutura.paginas}${
        estado.fora.size ? ` de ${estado.estrutura.paginas}` : ''}</div></div>
    <div><div class="r">Campos preenchidos</div>
      <div class="v${faltam ? ' alerta' : ''}">${feitos} de ${nomes.length}</div></div>
    ${imagens.length ? `<div><div class="r">Imagens</div>
      <div class="v${imgFeitas < imagens.length ? ' alerta' : ''}">${imgFeitas} de ${imagens.length}</div></div>` : ''}`;

  $('#pendencias').innerHTML = faltam
    ? `<div class="aviso"><strong>${faltam} campo${faltam === 1 ? '' : 's'} em branco.</strong>
       No arquivo exportado ${faltam === 1 ? 'ele aparece' : 'eles aparecem'} como
       <code>{{campo}}</code>, destacado, para não passar despercebido.</div>`
    : '';
}

function exportarPdf() {
  const janela = window.open('', '_blank');
  if (!janela) {
    alert('O navegador bloqueou a janela. Libere as janelas pop-up para este site e tente de novo.');
    return;
  }
  janela.document.open();
  janela.document.write(montar('imprimir'));
  janela.document.close();
}

/* ------------------------------------------------------------------- rascunho */

function carregarDados(arquivo) {
  const leitor = new FileReader();
  leitor.onload = () => {
    let d;
    try { d = JSON.parse(leitor.result); } catch (e) { alert('Arquivo inválido.'); return; }
    if (d.documento !== estado.documento.chave
        && !confirm(`Este rascunho é de "${d.documento}". Carregar mesmo assim?`)) return;
    estado.valores = d.valores || {};
    estado.imagens = d.imagens || {};
    salvar();
    salvarImagens();
    telaPreencher();
    mostrar('preencher');
  };
  leitor.readAsText(arquivo);
}

/* ------------------------------------------------------------------- ligações */

let temporizador = null;

function ligar() {
  $('#grade-produtos').onclick = (e) => {
    const b = e.target.closest('[data-produto]');
    if (!b) return;
    estado.produto = b.dataset.produto;
    estado.documento = estado.variante = null;
    telaDocumento();
    mostrar('documento');
  };

  $('#grade-documentos').onclick = (e) => {
    const b = e.target.closest('[data-documento]');
    if (!b) return;
    estado.documento = estado.catalogo.documentos.find((d) => d.chave === b.dataset.documento);
    const vs = variantesDoProduto(estado.documento, estado.produto);
    if (vs.length === 1) { escolherVariante(vs[0]); return; }
    telaVariante();
    mostrar('variante');
  };

  $('#grade-variantes').onclick = (e) => {
    const b = e.target.closest('[data-variante]');
    if (!b) return;
    escolherVariante(variantesDoProduto(estado.documento, estado.produto)
      .find((v) => v.sufixo === b.dataset.variante));
  };

  const form = $('#formulario');

  form.addEventListener('input', (e) => {
    const nome = e.target.dataset.campo;
    if (!nome) return;
    estado.valores[nome] = e.target.value;
    e.target.dataset.preenchido = e.target.value.trim() ? '1' : '';
    clearTimeout(temporizador);
    temporizador = setTimeout(() => { salvar(); atualizarContagens(); renderizar(); }, 250);
  });

  form.addEventListener('change', (e) => {
    const id = e.target.dataset.arquivo;
    if (!id || !e.target.files[0]) return;
    const leitor = new FileReader();
    leitor.onload = () => { estado.imagens[id] = leitor.result; salvarImagens(); telaPreencher(); };
    leitor.readAsDataURL(e.target.files[0]);
  });

  form.addEventListener('change', (e) => {
    if (e.target.dataset.pagina) alternarPagina(Number(e.target.dataset.pagina));
  });

  form.addEventListener('click', (e) => {
    const id = e.target.dataset.tirar;
    if (!id) return;
    delete estado.imagens[id];
    salvarImagens();
    telaPreencher();
  });

  // Abrir uma seção leva a prévia para a página correspondente. A lista de
  // páginas é a exceção: ela não é de uma página, é de todas.
  form.addEventListener('toggle', (e) => {
    const n = Number(e.target.dataset.pagina);
    if (e.target.tagName === 'DETAILS' && e.target.open && n) irPara(n);
  }, true);

  $('#abrir-tudo').onclick = () => $$('.secao', form).forEach((d) => { d.open = true; });
  $('#fechar-tudo').onclick = () => $$('.secao', form).forEach((d) => { d.open = false; });

  $('#busca').oninput = (e) => {
    const q = e.target.value.trim().toLowerCase();
    $$('.secao', form).forEach((sec) => {
      let achou = 0;
      $$('.campo, .imagem', sec).forEach((c) => {
        const bate = !q || (c.textContent + ' ' + (c.dataset.nome || '')).toLowerCase().includes(q);
        c.hidden = !bate;
        if (bate) achou++;
      });
      sec.hidden = !!q && !achou;
      if (q && achou) sec.open = true;
    });
  };

  $$('[data-ir]').forEach((b) => {
    b.onclick = () => {
      const t = b.dataset.ir;
      if (!podeIr(t)) return;
      if (t === 'produto') telaProduto();
      if (t === 'documento') telaDocumento();
      if (t === 'variante') telaVariante();
      if (t === 'exportar') telaExportar();
      mostrar(t);
    };
  });
  $$('[data-voltar]').forEach((b) => { b.onclick = () => mostrar(b.dataset.voltar); });

  $('#pag-anterior').onclick = () => irPara(estado.pagina - 1);
  $('#pag-proxima').onclick = () => irPara(estado.pagina + 1);
  $('#exportar-html').onclick = () =>
    baixar(montar('exportar'), nomeArquivo('html'), 'text/html;charset=utf-8');
  $('#exportar-pdf').onclick = exportarPdf;
  $('#baixar-dados').onclick = () => baixar(JSON.stringify({
    documento: estado.documento.chave, variante: estado.variante.sufixo,
    valores: estado.valores, imagens: estado.imagens,
  }, null, 1), nomeArquivo('json'), 'application/json');
  $('#carregar-dados').onclick = () => $('#arquivo-dados').click();
  $('#arquivo-dados').onchange = (e) => e.target.files[0] && carregarDados(e.target.files[0]);

  $('#recomecar').onclick = () => {
    if (!confirm('Voltar ao início? O que você preencheu continua salvo neste navegador.')) return;
    estado.produto = estado.documento = estado.variante = estado.modelo = null;
    telaProduto();
    mostrar('produto');
  };

  let redimensiona = null;
  window.addEventListener('resize', () => {
    clearTimeout(redimensiona);
    redimensiona = setTimeout(() => { if (estado.tela === 'preencher') ajustarQuadro(); }, 120);
  });
}

/* ---------------------------------------------------------------------- início */

(async function iniciar() {
  try {
    estado.catalogo = await fetch('catalogo.json').then((r) => r.json());
  } catch (e) {
    $('#carregando').textContent = 'Não foi possível carregar o catálogo de modelos.';
    return;
  }
  ligar();
  telaProduto();
  mostrar('produto');
}());
