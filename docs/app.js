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
  graficos: {},      // espaço de gráfico -> [{r: rótulo, v: valor, m: meta}]
  paginas: [],       // páginas montadas por quem preenche: [{id, depois, secao, blocos}]
  proximoBloco: 1,   // numera as instâncias de bloco, para os campos não colidirem
  fora: new Set(),   // páginas tiradas do documento
  estouro: [],       // páginas cujo conteúdo não coube: [{no, secao, sobra}]
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

/* A memória deste computador: o que não muda de um documento para outro. Quem
 * emite vai preencher o próprio nome, o registro, o CNPJ da casa, o disclaimer
 * do compliance e — na apresentação do consultor — a própria biografia em todo
 * documento que abrir. Guardar isso uma vez e oferecer nos próximos poupa a
 * maior parte do trabalho.
 *
 * O que é do cliente ou do período fica de fora, e essa é a parte que importa:
 * se `nome_cliente` fosse lembrado, o relatório do cliente seguinte abriria com
 * o nome do anterior, e alguém exportaria sem reparar. Por isso a lista é de
 * inclusão, e não de exclusão — campo novo não entra na memória por descuido. */
const MEMORIA = `${ARMAZEM}:memoria`;

const LEMBRAR = [
  // quem emite o documento
  /^nome_responsavel$/, /^registro_cvm_ou_ancord$/, /^papel_consultor$/,
  // a pessoa, na apresentação do consultor: escrita uma vez, usada sempre
  /^(nome|frase)_consultor$/,
  /^(formacao|especializacao|certificacao|qualificacoes|proposito|trajetoria|fora_do_escritorio|interesse)_\d+$/,
  /^marco_\d+_(quando|texto)$/,
  // contato e identificação da casa
  /^(email|whatsapp|telefone)_(contato|consultor)$/, /^instagram_consultor$/,
  /^(site|razao_social|cnpj|canal_ouvidoria|canal_atendimento|link_agendamento)$/,
  /^canal_(email|whats|tel|portal)_(endereco|horario|para)$/,
  /^time_\w+_(nome|papel|contato)$/,
  // texto que o compliance aprova uma vez e vale para o segmento inteiro
  /^(disclaimer_regulatorio|notas_de_rodape|texto_ouvidoria|nota_taxas)$/,
];

const lembrado = (campo) => LEMBRAR.some((re) => re.test(campo));

function lembrar() {
  try {
    const m = JSON.parse(localStorage.getItem(MEMORIA) || '{}');
    for (const [campo, valor] of Object.entries(estado.valores)) {
      if (lembrado(campo) && valor && valor.trim()) m[campo] = valor;
    }
    localStorage.setItem(MEMORIA, JSON.stringify(m));
  } catch (e) { /* sem espaço ou sem localStorage: o documento atual não perde nada */ }
}

function recordar() {
  try {
    return JSON.parse(localStorage.getItem(MEMORIA) || '{}');
  } catch (e) { return {}; }
}

function esquecer() {
  try { localStorage.removeItem(MEMORIA); } catch (e) { /* nada a esquecer */ }
}

/* A data de hoje, onde ela é a resposta certa na maioria das vezes.
 *
 * A tabela é explícita porque `_mes` e `_ano` no fim do nome quase nunca são
 * data: `rent_mes` é rentabilidade e `mk_spx_ano` é variação no ano. Um padrão
 * pelo sufixo preencheria percentual com data. Fica de fora também a data do
 * que ainda vai acontecer — hoje não é palpite para a próxima reunião — e a de
 * cada linha de tabela, que é de um evento e não do documento. */
const MESES = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
               'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];

const HOJE = {
  data_apresentacao: 'mes', data_carta: 'mes', mes_referencia: 'mes',
  mes_seguinte: 'mes+1',
  data_posicao: 'dia', data_corte: 'dia', data_ptax: 'dia',
  data_diagnostico: 'dia', data_emissao: 'dia', data_fechamento: 'dia',
  data_primeira_reuniao: 'dia',
  data_inicio_periodo: 'primeiro', data_fim_periodo: 'ultimo',
  ano_vigencia: 'ano', ano_corrente: 'ano', ano_seguinte: 'ano+1',
};

function dataDeHoje(forma, hoje = new Date()) {
  const dd = (d) => `${String(d.getDate()).padStart(2, '0')}/`
    + `${String(d.getMonth() + 1).padStart(2, '0')}/${d.getFullYear()}`;
  switch (forma) {
    case 'dia': return dd(hoje);
    case 'mes': return `${MESES[hoje.getMonth()]} de ${hoje.getFullYear()}`;
    case 'mes+1': {
      const m = new Date(hoje.getFullYear(), hoje.getMonth() + 1, 1);
      return `${MESES[m.getMonth()]} de ${m.getFullYear()}`;
    }
    case 'ano': return String(hoje.getFullYear());
    case 'ano+1': return String(hoje.getFullYear() + 1);
    case 'primeiro': return dd(new Date(hoje.getFullYear(), hoje.getMonth(), 1));
    case 'ultimo': return dd(new Date(hoje.getFullYear(), hoje.getMonth() + 1, 0));
    default: return '';
  }
}

/* O que o documento já sabe antes de alguém digitar: a memória deste
 * computador e a data de hoje. Só entra em campo vazio — rascunho salvo nunca
 * é sobrescrito, e a data de ontem continua sendo a de ontem se alguém a
 * escreveu. Só entra também em campo que este documento tem. */
function sugerir() {
  const memoria = recordar();
  let n = 0;
  for (const [campo, meta] of Object.entries(estado.estrutura.campos)) {
    // Um campo esvaziado de propósito guarda a string vazia, e `undefined` só
    // acontece na primeira abertura: é a diferença entre "ainda não preenchi"
    // e "apaguei porque não se aplica". O padrão só entra no primeiro caso.
    if (estado.valores[campo] !== undefined) continue;
    const v = memoria[campo] || (HOJE[campo] && dataDeHoje(HOJE[campo])) || meta.padrao;
    if (!v) continue;
    estado.valores[campo] = v;
    n += 1;
  }
  // As tabelinhas de gráfico também abrem preenchidas, com os rótulos que o
  // modelo sugere: os doze meses, as faixas de liquidez, as classes de ativo.
  // Precisam entrar no estado, e não só na tela — quem digitasse os valores sem
  // tocar nos rótulos veria o gráfico sair sem eixo horizontal.
  for (const im of estado.estrutura.imagens) {
    if (!im.grafico || estado.graficos[im.id] !== undefined) continue;
    estado.graficos[im.id] = linhasDe(im);
  }
  return n;
}

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
    // Os dados de gráfico vão no localStorage junto com o texto: são dezenas
    // de números, não megabytes de foto, e perder a tabela de um gráfico é tão
    // ruim quanto perder um parágrafo.
    localStorage.setItem(chaveArmazem(), JSON.stringify({
      valores: estado.valores, graficos: estado.graficos, fora: [...estado.fora],
      paginas: estado.paginas, proximoBloco: estado.proximoBloco,
    }));
    lembrar();
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
    estado.graficos = (d && d.graficos) || {};
    estado.paginas = (d && d.paginas) || [];
    estado.proximoBloco = (d && d.proximoBloco) || 1;
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
    estado.graficos = {};
    estado.paginas = [];
    estado.proximoBloco = 1;
    estado.fora = new Set();
    estado.pagina = 1;
    if (v.doc ? v.doc.blocos : estado.documento.blocos) await carregarBlocos();
    await carregar();
    // Depois do rascunho, nunca antes: o que já foi digitado manda.
    const sugeridos = sugerir();
    if (sugeridos) salvar();
    telaPreencher();
    if (sugeridos) {
      anunciarSalvo(`${sugeridos} campo${sugeridos > 1 ? 's' : ''} `
        + 'preenchido com o que este navegador já sabia');
    }
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

/* ------------------------------------------------- páginas montadas na mão

   O diagnóstico e o macroeconômico não cabem num molde fixo: o diagnóstico muda
   de forma conforme a carteira que se lê, e o macro precisa abrir espaço quando
   o mês traz um evento que ninguém previu. Para esses dois, a ferramenta deixa
   montar páginas novas a partir de blocos prontos.

   Não é um editor livre. Cada bloco já vem diagramado em `gerador/blocos.py`,
   no mesmo desenho do resto, e o que se escolhe é qual bloco e o que escrever
   dentro dele — é o que evita que a página nova pareça de outro documento.

   A casca da página não vem de lugar nenhum: clona-se uma página do modelo
   aberto e esvazia-se o corpo. Assim o cabeçalho, a logo, a data e o rodapé são
   exatamente os daquele documento e daquele segmento. */

let BIBLIOTECA = null;

async function carregarBlocos() {
  if (BIBLIOTECA) return BIBLIOTECA;
  try {
    BIBLIOTECA = await fetch('blocos.json').then((r) => r.json());
  } catch (e) {
    BIBLIOTECA = { marca: '@I@', blocos: [] };
  }
  return BIBLIOTECA;
}

const blocoDe = (chave) => (BIBLIOTECA?.blocos || []).find((b) => b.chave === chave);

/** O HTML de uma instância de bloco, com o número trocado onde for preciso. */
function blocoHtml(inst) {
  const b = blocoDe(inst.chave);
  if (!b) return '';
  return b.html.split(BIBLIOTECA.marca).join(String(inst.id));
}

/** Os campos de uma instância, já com o número no nome. */
function blocoCampos(inst) {
  const b = blocoDe(inst.chave);
  if (!b) return {};
  const fora = {};
  for (const [nome, meta] of Object.entries(b.campos)) {
    fora[nome.split(BIBLIOTECA.marca).join(String(inst.id))] = meta;
  }
  return fora;
}

/** O formulário de uma instância: os campos na ordem do bloco, com a tabela
 *  do bloco como grade, e a tabelinha de gráfico ou o envio de imagem quando
 *  o bloco os tem. */
function camposDoBloco(inst) {
  const b = blocoDe(inst.chave);
  if (!b) return '';
  const num = (x) => x.split(BIBLIOTECA.marca).join(String(inst.id));
  const campos = blocoCampos(inst);
  const celula = (c) => (c.c ? { c: num(c.c) } : c);
  const tabelas = (b.tabelas || []).map((t) => ({
    ...t, linhas: t.linhas.map((l) => l.map(celula)), rodape: t.rodape.map((l) => l.map(celula)),
  }));
  let fora = camposEmOrdem(Object.keys(campos), campos, tabelas);
  if (b.imagem && b.imagem.tipo === 'gráfico') {
    fora += campoGrafico({ ...b.imagem, id: num(b.imagem.id), rotulo: 'Dados do gráfico', descricao: '' });
  } else if (b.imagem) {
    fora += campoImagemSimples(num(b.imagem.id));
  }
  return fora;
}

const podeBlocos = () => !!(estado.documento && estado.documento.blocos && BIBLIOTECA);

function novaPagina() {
  const idx = estado.estrutura.indice || [];
  estado.paginas.push({
    id: 'p' + estado.proximoBloco++,
    // Entra no fim por padrão, mas antes da última: a última costuma ser a de
    // avisos, e nada deve ficar depois dela.
    depois: Math.max(1, idx.length - 1),
    secao: '',
    blocos: [],
  });
  estado.verMontada = estado.paginas[estado.paginas.length - 1].id;
  salvar();
  telaPreencher();
}

/* O construtor de páginas.
 *
 *  Uma página montada é uma caixa; dentro dela, os blocos empilhados na ordem
 *  em que saem no papel, e embaixo a paleta com todos os blocos à vista — não
 *  numa lista suspensa que esconde o que existe. Clicar num bloco da paleta
 *  o acrescenta ao fim; a alça arrasta para reordenar, e as setas fazem o
 *  mesmo sem mouse. Cada bloco fecha e abre, e fechado mostra o começo do que
 *  tem dentro, para uma página com oito blocos continuar navegável. */
const GRUPOS_DE_BLOCOS = [
  ['Texto', ['titulo', 'subtitulo', 'paragrafo', 'texto', 'texto2', 'topicos', 'destaque', 'abertura']],
  ['Dados', ['kpis', 'tabela', 'tabela6', 'marcos']],
  ['Gráficos', ['grafico_donut', 'grafico_anel', 'grafico_bars', 'grafico_bars2', 'grafico_line', 'grafico_line2']],
  ['Imagem', ['imagem']],
];

// Ícones de 16 px, traço só, para a paleta ler de relance.
const ICONES = {
  titulo: '<path d="M3 3v10M11 3v10M3 8h8"/>',
  subtitulo: '<path d="M3 5v8M9 5v8M3 9h6M13 11v2"/>',
  paragrafo: '<path d="M2 4h12M2 7h12M2 10h8"/>',
  texto: '<path d="M2 3h7M2 7h12M2 10h12M2 13h8"/>',
  texto2: '<path d="M2 4h5M2 7h5M2 10h5M9 4h5M9 7h5M9 10h5"/>',
  topicos: '<path d="M6 4h8M6 8h8M6 12h8"/><circle cx="3" cy="4" r="1"/><circle cx="3" cy="8" r="1"/><circle cx="3" cy="12" r="1"/>',
  destaque: '<path d="M3 3v10M6 5h7M6 8h7M6 11h5"/>',
  abertura: '<path d="M2 3h5M2 7h12M2 11h9"/>',
  kpis: '<path d="M2 12V6M6 12V3M10 12V8M14 12V5"/>',
  tabela: '<path d="M2 3h12v10H2zM2 7h12M2 10h12M7 3v10"/>',
  tabela6: '<path d="M2 3h12v10H2zM2 6h12M2 9h12M5 3v10M8 3v10M11 3v10"/>',
  marcos: '<path d="M2 8h12"/><circle cx="4" cy="8" r="1.5"/><circle cx="8" cy="8" r="1.5"/><circle cx="12" cy="8" r="1.5"/>',
  grafico_donut: '<circle cx="8" cy="8" r="5.5"/><circle cx="8" cy="8" r="2"/><path d="M8 2.5v3.5"/>',
  grafico_anel: '<circle cx="8" cy="8" r="6"/><circle cx="8" cy="8" r="3.5"/><circle cx="8" cy="8" r="1.2"/>',
  grafico_bars: '<path d="M3 13V7M7 13V4M11 13V9M2 13h12"/>',
  grafico_bars2: '<path d="M2.5 13V8M5 13V5M8.5 13V9M11 13V6M2 13h12"/>',
  grafico_line: '<path d="M2 12l4-5 3 3 5-6"/>',
  grafico_line2: '<path d="M2 12l4-5 3 3 5-6M2 8l4 3 3-4 5 4"/>',
  imagem: '<path d="M2 3h12v10H2zM2 11l4-4 3 3 2-2 3 3"/><circle cx="11" cy="6" r="1"/>',
};
const icone = (chave) => `<svg class="ico" viewBox="0 0 16 16" fill="none" stroke="currentColor"
  stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">${ICONES[chave] || ICONES.paragrafo}</svg>`;

/** A paleta de blocos de uma página: todos à vista, por grupo. */
function paletaDeBlocos(pagId, primeira) {
  const blocos = BIBLIOTECA.blocos || [];
  // O grupo já diz "Gráficos": a ficha diz só qual.
  const curto = (n) => n.replace(/^Gráfico de (\w)/, (m, c) => c.toUpperCase());
  const chip = (b) => `<button type="button" class="chip" data-bl-add="${pagId}" data-chave="${b.chave}"
      title="${escapa(b.descricao)}">${icone(b.chave)}<span>${escapa(curto(b.nome))}</span></button>`;
  const vistos = new Set();
  const grupos = GRUPOS_DE_BLOCOS.map(([nome, chaves]) => {
    const itens = chaves.map((c) => blocos.find((b) => b.chave === c)).filter(Boolean);
    itens.forEach((b) => vistos.add(b.chave));
    return [nome, itens];
  });
  const resto = blocos.filter((b) => !vistos.has(b.chave));
  if (resto.length) grupos.push(['Outros', resto]);
  return `<div class="paleta">
    <div class="paleta-titulo">${primeira ? 'Escolha o primeiro bloco da página' : 'Acrescentar bloco no fim da página'}</div>
    ${grupos.filter(([, itens]) => itens.length).map(([nome, itens]) => `<div class="grupo">
      <span class="rotulo">${nome}</span>
      <span class="chips">${itens.map(chip).join('')}</span>
    </div>`).join('')}
  </div>`;
}

/** O começo do que o bloco tem dentro, para o bloco fechado. */
function resumoDoBloco(inst) {
  const nomes = Object.keys(blocoCampos(inst));
  const texto = nomes.map((n) => (estado.valores[n] || '').trim()).find(Boolean);
  if (texto) return texto.length > 48 ? texto.slice(0, 47) + '…' : texto;
  const b = blocoDe(inst.chave);
  if (b?.imagem?.tipo === 'gráfico') {
    const linhas = estado.graficos[b.imagem.id.split(BIBLIOTECA.marca).join(String(inst.id))];
    if (linhas && window.Graficos.temDados(linhas)) return 'com dados';
  }
  if (b?.imagem && estado.imagens['bl' + inst.id]) return 'com imagem';
  return 'em branco';
}

function editorDePaginas() {
  if (!podeBlocos()) return '';
  const idx = estado.estrutura.indice || [];
  const opcoes = (sel) => idx.map((p) =>
    `<option value="${p.numero}"${p.numero === sel ? ' selected' : ''}>`
    + `depois da ${String(p.numero).padStart(2, '0')} — ${escapa(p.secao)}</option>`).join('');
  const fechados = estado.fechados || new Set();

  const bloco = (bl, i, n) => `<details class="bloco" data-bloco="${bl.id}"${fechados.has(bl.id) ? '' : ' open'}>
    <summary>
      <span class="alca" draggable="true" data-arrasta="${bl.id}" title="Arraste para mudar a ordem">⋮⋮</span>
      <span class="nome">${icone(bl.chave)}<strong>${escapa(blocoDe(bl.chave)?.nome || bl.chave)}</strong></span>
      <span class="previa">${escapa(resumoDoBloco(bl))}</span>
      <span class="acoes">
        <button type="button" class="btn neutro pequeno" data-bl-sobe="${bl.id}"${i === 0 ? ' disabled' : ''} title="Subir">↑</button>
        <button type="button" class="btn neutro pequeno" data-bl-desce="${bl.id}"${i === n - 1 ? ' disabled' : ''} title="Descer">↓</button>
        <button type="button" class="btn neutro pequeno" data-bl-fora="${bl.id}" title="Remover bloco">×</button>
      </span>
    </summary>
    <div class="campos">${camposDoBloco(bl)}</div>
  </details>`;

  const pagina = (pg, k) => `<div class="pag-nova" data-pag="${pg.id}">
    <div class="cabeca">
      <span class="etiqueta">Página nova ${k + 1}</span>
      <button type="button" class="btn neutro pequeno" data-pag-fora="${pg.id}" title="Remover esta página">Remover página</button>
    </div>
    <div class="onde">
      <label>Nome no cabeçalho
        <input type="text" class="secao-nome" data-pag-secao="${pg.id}" placeholder="Ex.: Análise setorial" value="${escapa(pg.secao)}"></label>
      <label>Posição no documento
        <select data-pag-onde="${pg.id}">${opcoes(pg.depois)}</select></label>
    </div>
    ${pg.blocos.length ? `<div class="blocos">${pg.blocos.map((bl, i) => bloco(bl, i, pg.blocos.length)).join('')}</div>` : ''}
    ${paletaDeBlocos(pg.id, !pg.blocos.length)}
  </div>`;

  return `<details class="secao montagem"${estado.paginas.length ? ' open' : ''}>
    <summary>
      <span class="pg">+</span>
      <span>Páginas que você monta</span>
      <span class="contagem">${estado.paginas.length}</span>
    </summary>
    <div class="campos">
      ${estado.paginas.length ? '' : `<p class="dica" style="margin:0 0 3mm">Este documento aceita páginas novas,
        montadas com blocos prontos no desenho da casa: título, texto, tabela, gráficos, imagem.
        Use quando o mês ou a carteira pedirem um assunto que não cabe nas páginas que já existem.</p>`}
      ${estado.paginas.map(pagina).join('')}
      <button type="button" class="btn neutro" id="nova-pagina">${estado.paginas.length ? 'Mais uma página' : 'Nova página'}</button>
    </div>
  </details>`;
}

function campoImagemSimples(id) {
  const dado = estado.imagens[id];
  return `<div class="imagem${dado ? ' cheia' : ''}">
    <span class="miniatura"${dado ? ` style="background-image:url('${dado}')"` : ''}>${dado ? '' : 'imagem'}</span>
    <div>
      <div class="nome">Imagem do bloco</div>
      <div class="acoes">
        <label class="btn neutro pequeno">${dado ? 'Trocar' : 'Enviar imagem'}
          <input type="file" accept="image/*" data-arquivo="${escapa(id)}"></label>
        ${dado ? `<button type="button" class="btn neutro pequeno" data-tirar="${escapa(id)}">Remover</button>` : ''}
      </div>
    </div>
  </div>`;
}

/** A chave que põe uma página no documento ou tira dela. Diz o estado por
 *  extenso — "Entra" / "Fora" — e não só pela cor. */
function chaveDePagina(n) {
  const entra = dentro(n);
  return `<span class="chave${entra ? ' ligada' : ''}" data-pagina="${n}" role="switch" tabindex="0"
    aria-checked="${entra}" aria-label="${entra ? 'Página no documento' : 'Página fora do documento'}"
    title="${entra ? 'Tirar esta página do documento' : 'Pôr esta página no documento'}">
    <span class="trilho"><span class="botao"></span></span></span>`;
}

/** A linha que abre o formulário: quantas páginas entram, e o cabeçalho da
 *  coluna de chaves à direita. A chave de cada página fica numa coluna só,
 *  ao lado da seção dela — um lugar, um controle. */
function cabecaDasPaginas() {
  const idx = estado.estrutura.indice || [];
  if (idx.length < 2) return '';
  const n = incluidas().length;
  const todas = n === idx.length;
  return `<div class="linha-secao cabeca-paginas">
    <div class="estado-paginas${todas ? '' : ' parcial'}">${n} de ${idx.length} páginas entram no documento${todas ? ''
      : ` <button type="button" class="ligar-todas" id="todas-paginas">Incluir todas</button>`}</div>
    <div class="rotulo-coluna" title="Ligada, a página entra no arquivo exportado; desligada, fica de fora e o resto é renumerado">Entra</div>
  </div>`;
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

  $('#formulario').innerHTML = listasDeOpcoes() + cabecaDasPaginas() + editorDePaginas() + (secoes.length ? secoes.map((s, i) => `
    <div class="linha-secao${dentro(s.pagina) ? '' : ' fora'}">
    <details class="secao${dentro(s.pagina) ? '' : ' fora'}" data-pagina="${s.pagina}"${i === 0 && dentro(s.pagina) ? ' open' : ''}>
      <summary>
        <span class="pg">${String(s.pagina).padStart(2, '0')}</span>
        <span class="titulo-secao">${escapa(s.secao)}</span>
        <span class="contagem" data-contagem="${s.pagina}"></span>
      </summary>
      <div class="campos">
        ${s.imagens.map(campoImagem).join('')}
        ${camposDaPagina(s.campos, campos, s.pagina)}
      </div>
    </details>
    ${chaveDePagina(s.pagina)}
    </div>`).join('')
    : '<p class="solto">Este modelo não tem campos preenchíveis.</p>');

  atualizarContagens();
  renderizar();
}

/* O campo pelo tipo.
 *
 *  O catálogo diz o que cada campo recebe — dinheiro, percentual, data, uma
 *  escolha entre poucas —, e o campo se apresenta de acordo: teclado numérico
 *  onde vai número, calendário onde vai data, lista onde há opções. O que sai
 *  para o documento continua sendo texto, no formato que o modelo espera; o
 *  tipo só encurta o caminho até ele. */
const ENTRADA = {
  dinheiro: ' inputmode="decimal" data-formato="dinheiro"',
  percentual: ' inputmode="decimal" data-formato="percentual"',
  pp: ' inputmode="decimal" data-formato="pp"',
  numero: ' inputmode="decimal" data-formato="numero"',
  ano: ' type="number" inputmode="numeric" min="1990" max="2100" step="1"',
  email: ' type="email" autocomplete="off"',
  telefone: ' type="tel" inputmode="tel"',
  data: ' inputmode="numeric"',
};

const tipoDe = (nome, meta) => meta.tipo || (multilinha(nome) ? 'longo' : 'texto');

/** A entrada de um campo — só o controle, sem rótulo. `grade` é a versão
 *  compacta para célula de tabela: o texto corrido vira uma linha que cresce
 *  conforme se escreve, porque três linhas fixas por célula não cabem. */
function entradaDe(nome, meta, grade = false) {
  const v = escapa(estado.valores[nome] || '');
  const cheio = (estado.valores[nome] || '').trim() ? ' data-preenchido="1"' : '';
  // O exemplo é `placeholder`: mostra o formato esperado, some ao digitar e
  // nunca entra no documento.
  const ex = meta.exemplo ? ` placeholder="${escapa(meta.exemplo)}"` : '';
  const tipo = tipoDe(nome, meta);
  let entrada;
  if (tipo === 'longo') {
    entrada = `<textarea id="c-${nome}" rows="${grade ? 1 : 3}" data-campo="${nome}"${ex}${cheio}>${v}</textarea>`;
  } else {
    const extra = (ENTRADA[tipo] || '') + (tipo === 'opcoes' ? ` list="op-${meta.opcoes}"` : '');
    const type = /type="/.test(extra) ? '' : ' type="text"';
    entrada = `<input id="c-${nome}"${type} data-campo="${nome}" value="${v}"${ex}${cheio}${extra}>`;
    // Data e mês ganham o calendário do navegador ao lado. O campo continua
    // sendo de texto — "2º semestre" ainda cabe ali —, e o calendário só
    // escreve nele, no formato que o documento usa.
    if (tipo === 'data' || tipo === 'mes') {
      entrada = `<div class="com-seletor">${entrada}
        <button type="button" class="seletor" data-seletor="${nome}" title="Escolher no calendário">📅</button>
        <input type="${tipo === 'mes' ? 'month' : 'date'}" class="oculto" data-seletor-de="${nome}" tabindex="-1" aria-hidden="true"></div>`;
    }
  }
  return entrada;
}

function campoTexto(nome, meta) {
  const dica = meta.dica ? `<p class="dica">${escapa(meta.dica)}</p>` : '';
  return `<div class="campo" data-nome="${nome}">
    <label for="c-${nome}">${escapa(meta.rotulo)}</label>${entradaDe(nome, meta)}${dica}</div>`;
}

/** Uma tabela do modelo como grade de preenchimento.
 *
 *  O modelo tem a tabela pronta; o que falta são os números. Oferecer os
 *  campos dela um a um, em lista — `Mov 1 data`, `Mov 1 tipo`, `Mov 1 ativo`,
 *  quarenta vezes — obrigava a reconstruir de cabeça a tabela que está logo
 *  ali na prévia. Aqui ela aparece com a mesma forma: cabeçalho, uma linha
 *  por linha, o rótulo fixo onde o modelo o tem, e o campo na coluna certa.
 *
 *  A linha de total ganha um botão de soma por coluna numérica. É pedido, não
 *  automático: nem toda coluna se soma — rentabilidade não —, e quem preenche
 *  sabe qual é qual. */
function campoTabela(tab, campos) {
  const cab = (t) => t.replace(/\{\{([a-z0-9_]+)\}\}/g, (_, n) => estado.valores[n] || n);
  const celula = (c, i, rodape) => {
    if (!c.c) return `<td class="rotulo">${escapa(c.t)}</td>`;
    const meta = campos[c.c] || { rotulo: c.c };
    const tipo = tipoDe(c.c, meta);
    const soma = rodape && /^(dinheiro|percentual|pp|numero)$/.test(tipo)
      ? `<button type="button" class="soma" data-soma="${c.c}" data-coluna="${i}" title="Somar a coluna">Σ</button>` : '';
    const entrada = entradaDe(c.c, meta, true);
    return `<td class="t-${tipo}">${soma ? `<span class="com-soma">${entrada}${soma}</span>` : entrada}</td>`;
  };
  const linha = (l, rodape) => `<tr>${l.map((c, i) => celula(c, i, rodape)).join('')}</tr>`;
  const nomes = [...tab.linhas, ...tab.rodape].flat().filter((c) => c.c).map((c) => c.c);
  return `<div class="tabela" data-nome="${nomes.join(' ')}">
    <div class="nome">${escapa(tab.titulo || 'Tabela')}</div>
    <div class="rolagem"><table class="dados">
      <thead><tr>${tab.cabecalhos.map((h) => `<th>${escapa(cab(h))}</th>`).join('')}</tr></thead>
      <tbody>${tab.linhas.map((l) => linha(l, false)).join('')}</tbody>
      ${tab.rodape.length ? `<tfoot>${tab.rodape.map((l) => linha(l, true)).join('')}</tfoot>` : ''}
    </table></div></div>`;
}

/** Os campos de uma página, na ordem do documento, com cada tabela entrando
 *  inteira no lugar do seu primeiro campo. */
function camposDaPagina(nomes, campos, pagina) {
  // Só as tabelas desta página. Um campo pode aparecer em duas — o patrimônio
  // total é KPI na página 3 e linha de total na 5 — e a tabela entra onde
  // está, não onde o campo apareceu primeiro.
  const tabelas = (estado.estrutura.tabelas || []).filter((t) => t.pagina === pagina);
  return camposEmOrdem(nomes, campos, tabelas);
}

function camposEmOrdem(nomes, campos, tabelas) {
  const de = new Map();
  for (const t of tabelas) for (const c of [...t.linhas, ...t.rodape].flat()) if (c.c) de.set(c.c, t);
  const feitas = new Set();
  const partes = [];
  for (const n of nomes) {
    const t = de.get(n);
    if (!t) { partes.push(campoTexto(n, campos[n])); continue; }
    if (feitas.has(t)) continue;
    feitas.add(t);
    partes.push(campoTabela(t, campos));
  }
  return partes.join('');
}

/** As listas dos campos de escolha, uma vez por formulário. */
function listasDeOpcoes() {
  return Object.entries(estado.catalogo.opcoes || {}).map(([k, itens]) =>
    `<datalist id="op-${k}">${itens.map((o) => `<option value="${escapa(o)}">`).join('')}</datalist>`).join('');
}

/** Guarda o que foi digitado num campo e agenda salvar e redesenhar. */
function anotar(el, valor) {
  estado.valores[el.dataset.campo] = valor;
  // O mesmo campo pode estar em dois lugares do formulário — o total como KPI
  // e como pé de tabela. O que se escreve num aparece no outro.
  for (const outro of $$(`[data-campo="${CSS.escape(el.dataset.campo)}"]`)) {
    if (outro !== el && outro.value !== valor) outro.value = valor;
    outro.dataset.preenchido = valor.trim() ? '1' : '';
  }
  clearTimeout(temporizador);
  temporizador = setTimeout(() => { salvar(); atualizarContagens(); renderizar(); }, 250);
}

/* ---------------------------------------------------------------- formatos */

/** O número dentro de um texto como `R$ 12.400,00`, `-1,2%` ou `12400`.
 *  Devolve `null` quando o texto tem mais do que número e unidade — "CDI +
 *  2,10%" ou "isento" ficam como estão. */
function numeroDe(texto) {
  const s = texto.trim().replace(/^(R\$|US\$|EUR|€)\s*/i, '').replace(/\s*(%|p\.p\.)$/i, '').trim();
  if (!/^[+-]?\d[\d.,]*$/.test(s)) return null;
  let n = s;
  if (s.includes(',')) n = s.replace(/\./g, '').replace(',', '.');
  else if (/^[+-]?\d{1,3}(\.\d{3})+$/.test(s)) n = s.replace(/\./g, '');   // 1.284.000 é milhar
  const v = Number(n);
  return Number.isFinite(v) ? v : null;
}

/** Quantas casas decimais o texto tem. É o que preserva "12%" e "12,4%" em
 *  vez de forçar tudo a duas casas. */
function casasDe(texto) {
  const m = texto.match(/[.,](\d+)\s*(%|p\.p\.)?$/);
  return m && !/^\d{3}$/.test(m[1]) ? Math.min(m[1].length, 2) : 0;
}

/** O texto no formato do documento. Só mexe no que é número puro. */
function formatar(tipo, texto) {
  const n = numeroDe(texto);
  if (n === null) return texto;
  const sinal = /^\s*\+/.test(texto) && n >= 0 ? '+' : '';
  const fixo = (d) => n.toLocaleString('pt-BR', { minimumFractionDigits: d, maximumFractionDigits: d });
  switch (tipo) {
    case 'dinheiro': {
      const moeda = /^\s*US\$/i.test(texto) ? 'US$' : /^\s*(EUR|€)/i.test(texto) ? 'EUR' : 'R$';
      return `${moeda} ${fixo(2)}`;
    }
    case 'percentual': return `${sinal}${fixo(casasDe(texto))}%`;
    case 'pp': return `${sinal}${fixo(casasDe(texto))} p.p.`;
    case 'numero': return `${sinal}${n.toLocaleString('pt-BR', { maximumFractionDigits: 2 })}`;
    default: return texto;
  }
}

/** `31/08/2026` -> `2026-08-31`, para abrir o calendário no dia certo. */
function isoDe(texto) {
  const m = texto.match(/^\s*(\d{1,2})\/(\d{1,2})\/(\d{4})\s*$/);
  return m ? `${m[3]}-${m[2].padStart(2, '0')}-${m[1].padStart(2, '0')}` : '';
}

/** `Setembro de 2026` -> `2026-09`. */
function mesIsoDe(texto) {
  const m = texto.match(/^\s*([A-Za-zçÇ]+)\s+de\s+(\d{4})\s*$/);
  if (!m) return '';
  const i = MESES.findIndex((x) => x.toLowerCase() === m[1].toLowerCase());
  return i < 0 ? '' : `${m[2]}-${String(i + 1).padStart(2, '0')}`;
}

/** O que o calendário escolheu, no formato do documento. */
function textoDaData(tipo, iso) {
  if (!iso) return '';
  const [a, m, d] = iso.split('-');
  return tipo === 'month' ? `${MESES[Number(m) - 1]} de ${a}` : `${d}/${m}/${a}`;
}

/** Quantas linhas a tabelinha oferece de saída. Os formatos com série nomeada
 *  já vêm com os nomes; os de eixo temporal abrem com doze, que é o ano. */
const LINHAS_GRAFICO = { donut: 6, anel: 6, bars: 12, line: 12 };

/** As colunas de valor da tabelinha: uma por série.
 *
 *  Nem todo gráfico é de uma série só. O juro longo contra o dólar, a carteira
 *  contra o benchmark, a curva de hoje contra a de um ano atrás: são três
 *  gráficos do sistema em que a comparação é o assunto, e desenhá-los com uma
 *  linha só era perder o que eles têm para dizer. */
const colunasDe = (im) => window.Graficos.colunas(im.grafico, im.series, im.eixo);

function linhasDe(im) {
  const guardado = estado.graficos[im.id];
  if (guardado && guardado.length) {
    // Rascunho salvo antes das séries guardava `{r, v, m}`.
    return guardado.map((l) => (Array.isArray(l.v) ? l
      : { r: l.r || '', v: [l.v, l.m].filter((x) => x !== undefined) }));
  }
  const cols = colunasDe(im);
  // Nos de rosca, cada linha é uma fatia, e o nome da fatia vem de `series`.
  // Nos de eixo, cada linha é um ponto do eixo horizontal, e o nome vem de
  // `pontos` — os doze meses, as faixas de liquidez, os vértices da curva.
  // Quem nomeia as colunas, ali, é `series`.
  const fatias = (im.grafico === 'donut' || im.grafico === 'anel') && im.series;
  const rotulos = fatias ? im.series : (im.pontos || []);
  const n = rotulos.length || LINHAS_GRAFICO[im.grafico] || 6;
  return Array.from({ length: n }, (_, i) => ({
    r: rotulos[i] || '',
    v: cols.map(() => ''),
  }));
}

/** O gráfico como tabelinha: uma linha por fatia, rótulo e valor.
 *
 *  É o que substituiu o campo de imagem. Antes o consultor montava a rosca em
 *  outro lugar e subia um PNG; agora ele digita os números e o desenho sai no
 *  documento, em SVG, nas cores do segmento. O envio de imagem continua ali
 *  embaixo para quem tiver um gráfico pronto que não cabe neste formato — e o
 *  dado tem precedência sobre ela. */
function campoGrafico(im) {
  const linhas = linhasDe(im);
  const cols = colunasDe(im);
  const eixoX = (im.grafico === 'line' || im.grafico === 'bars') ? 'Período' : 'Rótulo';
  const dado = estado.imagens[im.id];
  const preenchido = linhas.some((l) => l.v.some((x) => (x || '').trim()));
  return `<div class="grafico${preenchido ? ' cheio' : ''}" data-grafico="${escapa(im.id)}">
    <div class="nome">${escapa(im.rotulo)}</div>
    <div class="desc">${escapa(im.descricao)}</div>
    <table class="dados">
      <thead><tr><th>${eixoX}</th>${cols.map((c) => `<th>${escapa(c)}</th>`).join('')}</tr></thead>
      <tbody>${linhas.map((l, i) => `<tr>
        <td><input type="text" data-gr="${escapa(im.id)}" data-i="${i}" data-c="r" value="${escapa(l.r)}"></td>
        ${cols.map((c, k) => `<td><input type="text" inputmode="decimal" data-gr="${escapa(im.id)}"`
          + ` data-i="${i}" data-c="${k}" value="${escapa(l.v[k] || '')}"></td>`).join('')}
      </tr>`).join('')}</tbody>
    </table>
    <div class="acoes">
      <button type="button" class="btn neutro pequeno" data-mais="${escapa(im.id)}">Mais uma linha</button>
      <label class="btn neutro pequeno">${dado ? 'Trocar imagem' : 'Enviar imagem'}
        <input type="file" accept="image/*" data-arquivo="${escapa(im.id)}"></label>
      ${dado ? `<button type="button" class="btn neutro pequeno" data-tirar="${escapa(im.id)}">Remover imagem</button>` : ''}
    </div>
  </div>`;
}

function campoImagem(im) {
  if (im.grafico) return campoGrafico(im);
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
    if (estado.imagens[im.id]
        || (estado.graficos[im.id] && window.Graficos.temDados(estado.graficos[im.id]))) {
      c.feitos += 1;
    }
  }
  for (const [pag, c] of conta) {
    const el = $(`[data-contagem="${pag}"]`);
    if (!el) continue;
    el.textContent = `${c.feitos}/${c.total}`;
    el.classList.toggle('pronto', c.feitos === c.total);
  }
}

/* ------------------------------------------------------------------- montagem */

/** O que se abre ao clicar num campo de contato.
 *  O tipo vem do modelo, do `data-link` que o gerador põe nos campos que são
 *  endereço de alguma coisa. `auto` deixa o valor decidir, porque a ouvidoria
 *  de uma casa é 0800 e a de outra é um e-mail. Devolve vazio quando não há o
 *  que abrir — e aí o valor fica sendo só texto, como era. */
function endereco(tipo, valor) {
  if (!tipo) return '';
  const digitos = valor.replace(/\D/g, '');
  // Quem digita "(62) 3095-8115" não põe o país, e sem ele o wa.me não abre.
  // Dez ou onze dígitos é telefone brasileiro; daí para cima o país já veio.
  // Número de serviço — 0800, 0300 — não leva país nenhum: ele já é nacional,
  // e "+55 0800…" não completa a ligação.
  const servico = digitos.startsWith('0');
  const e164 = servico || digitos.length >= 12 ? digitos : `55${digitos}`;
  switch (tipo === 'auto' ? adivinha(valor) : tipo) {
    case 'mailto': return `mailto:${valor}`;
    case 'whatsapp': return digitos.length >= 8 ? `https://wa.me/${e164}` : '';
    case 'tel': return digitos.length >= 8 ? `tel:${servico ? e164 : '+' + e164}` : '';
    case 'instagram': return `https://instagram.com/${valor.replace(/^@/, '')}`;
    case 'url':
      if (/^https?:\/\//i.test(valor)) return valor;
      return /^[\w-]+(\.[\w-]+)+/.test(valor) ? `https://${valor}` : '';
    default: return '';
  }
}

/** O tipo de endereço deduzido do próprio valor, para os campos que mudam de
 *  natureza conforme a casa. */
function adivinha(v) {
  if (/^https?:\/\//i.test(v)) return 'url';
  if (/^@/.test(v)) return 'instagram';
  if (/^\S+@\S+\.\S+$/.test(v)) return 'mailto';
  if (/^[\d\s()+.-]{8,}$/.test(v)) return 'tel';
  if (/^[\w-]+(\.[\w-]+)+(\/\S*)?$/.test(v)) return 'url';
  return '';
}

/** O modelo com os valores no lugar.
 *  `modo` é 'previa' (realce do que já foi preenchido), 'exportar' (documento
 *  limpo) ou 'imprimir' (limpo, e chama a impressão sozinho ao abrir).
 *
 *  Na prévia o campo em branco continua sendo `{{campo}}` destacado: a tela é
 *  onde se preenche, e ali a lacuna tem de saltar aos olhos. No arquivo que sai
 *  daqui ele some — o documento vai para o cliente, e `{{nome_cliente}}` escrito
 *  numa apresentação é pior do que a linha vazia. Quem avisa o que ficou
 *  faltando é a tela de exportar, antes de gerar o arquivo. */
function montar(modo) {
  const doc = estado.modelo.cloneNode(true);

  // As páginas desmarcadas saem, e as que ficam são renumeradas: o rodapé tem
  // de contar o documento que existe, não o que existia antes do corte.
  const paginas = [...doc.querySelectorAll('.page, .slide')];
  // As páginas montadas entram antes de tirar as desmarcadas, porque a posição
  // delas é dada pelo número original da página — "depois da 07" quer dizer
  // depois da sétima do modelo, e não da sétima do que sobrou.
  paginas.forEach((p, i) => { p.dataset.original = i + 1; });
  inserirMontadas(doc, paginas, modo);
  paginas.forEach((p, i) => { if (!dentro(i + 1)) p.remove(); });
  renumerar(doc);

  const esvaziados = new Set();
  for (const span of doc.querySelectorAll('span.ph')) {
    const nome = span.dataset.campo;
    if (!nome) continue;
    const v = estado.valores[nome];
    // Na prévia, o campo se edita no lugar: clicar no texto e escrever. O que
    // se escreve ali vai para o mesmo estado que o formulário lê.
    if (modo === 'previa') {
      span.setAttribute('contenteditable', 'true');
      span.setAttribute('spellcheck', 'false');
    }
    if (!v || !v.trim()) {
      // O campo que já vem preenchido não some quando o consultor não mexe
      // nele: o que está escrito ali é o texto padrão, e não uma lacuna.
      if (span.classList.contains('pronto')) continue;
      if (modo !== 'previa') {
        // O item de lista que era só o campo fica sendo um traço solto na
        // margem: some o texto e o marcador continua lá, anunciando uma linha
        // que não existe. O mesmo vale para a pílula de certificação, que sem
        // texto vira uma cápsula vazia. Guarda o pai para conferir depois de
        // tirar todos os campos — antes disso não dá para saber se o que
        // sobrou está vazio.
        // A célula de tabela fica: tirá-la desalinharia a linha. Linha e
        // coluna que ficaram inteiras em branco saem mais abaixo, juntas.
        const item = span.closest('.pill, .tags > span, li, dd, dt, p');
        if (item && !item.closest('td, th')) esvaziados.add(item);
        span.remove();
      }
      continue;
    }
    span.textContent = v;
    span.classList.add('feito');
    // Campo de contato vira link: o Chromium leva a âncora para o PDF, e no
    // HTML exportado ela é um endereço que se clica. Sem isto o e-mail do
    // consultor sai como texto morto num documento que o cliente lê na tela.
    const href = endereco(span.dataset.link, v.trim());
    if (href) {
      const a = doc.createElement('a');
      a.href = href;
      span.replaceWith(a);
      a.appendChild(span);
    }
  }

  // Tabela: a linha do corpo que ficou toda em branco sai, e a coluna cujo
  // cabeçalho e células ficaram em branco também. É o que deixa a tabela de
  // cinco linhas do construtor servir para três, e a de movimentações do
  // mensal servir para um mês com duas operações.
  if (modo !== 'previa') {
    const vazia = (cel) => !cel.textContent.trim() && !cel.querySelector('img, svg');
    for (const tabela of doc.querySelectorAll('table')) {
      const corpo = [...tabela.querySelectorAll('tbody > tr')];
      for (const tr of corpo) {
        if ([...tr.children].every(vazia)) tr.remove();
      }
      const cabecalho = tabela.querySelector('thead > tr');
      if (!cabecalho) continue;
      const linhas = [...tabela.querySelectorAll('tbody > tr, tfoot > tr')];
      for (let i = cabecalho.children.length - 1; i >= 0; i--) {
        const coluna = [cabecalho.children[i], ...linhas.map((tr) => tr.children[i])].filter(Boolean);
        if (!vazia(cabecalho.children[i]) || !coluna.every(vazia)) continue;
        coluna.forEach((cel) => cel.remove());
        tabela.querySelectorAll('colgroup > col')[i]?.remove();
      }
    }
  }

  // A linha que ficou sem nada dentro sai inteira, com o marcador junto. Numa
  // lista de definição sai o par: rótulo sem valor é pior do que a ausência.
  for (const item of esvaziados) {
    if (item.textContent.trim() || item.querySelector('img, svg')) continue;
    if (item.tagName === 'DD' && item.previousElementSibling?.tagName === 'DT') {
      item.previousElementSibling.remove();
    } else if (item.tagName === 'DT' && item.nextElementSibling?.tagName === 'DD') {
      item.nextElementSibling.remove();
    }
    item.remove();
  }

  // O gráfico desenhado tem precedência sobre a imagem enviada: quem digitou os
  // números quis o desenho, e o PNG que estiver guardado no espaço é o de uma
  // tentativa anterior. A moldura vira o SVG e mantém a caixa — a mesma altura
  // mínima, o mesmo lugar na grelha —, só perde o tracejado e o texto de
  // instrução, que eram o pedido de preenchimento.
  for (const [id, linhas] of Object.entries(estado.graficos)) {
    const bloco = doc.querySelector(`[data-grafico][data-img="${CSS.escape(String(id))}"]`);
    if (!bloco || !window.Graficos.temDados(linhas)) continue;
    const series = bloco.dataset.series ? bloco.dataset.series.split('|') : null;
    const html = window.Graficos.desenha(bloco.dataset.grafico, linhas, series);
    if (!html) continue;
    bloco.innerHTML = html;
    bloco.classList.add('feito');
  }

  for (const [id, dado] of Object.entries(estado.imagens)) {
    if (estado.graficos[id] && window.Graficos.temDados(estado.graficos[id])) continue;
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
        // Na prévia a folha longa acompanha o conteúdo sozinha, sem número
        // nenhum: é o navegador que mede. O arquivo exportado não pode contar
        // com isso — `@page` exige altura escrita —, e ali entra a medida de
        // `montarFinal`. As duas dão na mesma folha.
        + '.page.longa{height:auto}'
      : '.ph.feito{background:none;color:inherit;padding:0;font-weight:inherit}');
  doc.head.appendChild(estilo);

  if (modo === 'imprimir') {
    const s = doc.createElement('script');
    s.textContent = 'addEventListener("load",()=>setTimeout(()=>print(),300))';
    doc.body.appendChild(s);
  }
  return '<!doctype html>\n' + doc.documentElement.outerHTML;
}

/** Põe no documento as páginas que o consultor montou.
 *
 *  A casca sai de uma página do próprio modelo: clona-se a primeira que tenha
 *  corpo e cabeçalho, esvazia-se o corpo e põem-se os blocos. Assim o
 *  cabeçalho, a logo, a data e o rodapé são exatamente os daquele documento e
 *  daquele segmento — nada aqui redesenha nada.
 *
 *  Página sem bloco nenhum não entra: é uma página em branco, e ninguém a quis. */
function inserirMontadas(doc, originais, modo = 'previa') {
  if (!estado.paginas.length || !BIBLIOTECA) return;
  const molde = originais.find((p) => p.querySelector('.pg-body') && p.querySelector('.pg-head'));
  if (!molde) return;
  // De trás para a frente: inserir a de trás primeiro não mexe no índice das
  // que ainda faltam.
  // Na prévia a página sem bloco entra também, em branco: quem acabou de
  // clicar em "Nova página" precisa vê-la. No arquivo exportado ela não sai.
  const pedidos = [...estado.paginas].filter((pg) => pg.blocos.length || modo === 'previa')
    .sort((a, b) => b.depois - a.depois);
  for (const pg of pedidos) {
    const nova = molde.cloneNode(true);
    // A marca é o que permite repaginá-la depois. Só as páginas montadas se
    // dividem: as do modelo são desenho fechado, e quebrar uma tabela ao meio
    // para caber deixaria o cabeçalho órfão numa página e os números na outra.
    nova.classList.add('montada');
    nova.dataset.montada = pg.id;
    delete nova.dataset.original;   // é cópia do molde, não a página dele
    const sec = nova.querySelector('.pg-head .sec');
    if (sec) sec.textContent = pg.secao || 'Análise';
    const corpo = nova.querySelector('.pg-body');
    corpo.innerHTML = pg.blocos.length ? pg.blocos.map(blocoHtml).join('\n')
      : '<div style="flex:1 1 auto;display:flex;align-items:center;justify-content:center;'
        + 'border:1px dashed currentColor;opacity:.45;border-radius:2mm;font-size:9pt;text-align:center;padding:8mm">'
        + 'Página em branco.<br>Escolha o primeiro bloco na paleta.</div>';
    const depois = originais[Math.min(pg.depois, originais.length) - 1] || originais[originais.length - 1];
    depois.after(nova);
  }
}

/** Redesenha os gráficos na proporção da caixa que o documento reservou.
 *
 *  `montar()` desenha às cegas: ele trabalha sobre um documento sem layout, e
 *  ali não há como saber que a evolução do patrimônio ocupa a página inteira e
 *  quatro centímetros de altura. O desenho saía sempre na mesma proporção e
 *  encolhia até caber na altura, deixando metade da largura vazia.
 *
 *  Aqui, com o documento diagramado, a caixa se mede — e o gráfico se estica no
 *  eixo em que há espaço. */
function ajustarGraficos(doc) {
  for (const bloco of doc.querySelectorAll('.chart.feito[data-grafico]')) {
    const linhas = estado.graficos[bloco.dataset.img];
    if (!linhas || !window.Graficos.temDados(linhas)) continue;
    const caixa = bloco.getBoundingClientRect();
    if (!caixa.width || !caixa.height) continue;
    const series = bloco.dataset.series ? bloco.dataset.series.split('|') : null;
    // O que sobra para o desenho é a caixa menos a legenda e a nota, que ficam
    // embaixo dele. Descontá-las é o que faz a conta dar o mesmo resultado na
    // segunda passada: sem isso, o desenho encolheria um pouco a cada vez.
    let ocupado = 0;
    for (const abaixo of bloco.querySelectorAll('.legend, .g-nota')) {
      ocupado += abaixo.getBoundingClientRect().height;
    }
    const html = window.Graficos.desenha(bloco.dataset.grafico, linhas, series,
                                         { w: caixa.width, h: Math.max(60, caixa.height - ocupado) });
    if (html) bloco.innerHTML = html;
  }
}

/** Renumera o rodapé na ordem em que as páginas ficaram. */
function renumerar(doc) {
  [...doc.querySelectorAll('.page, .slide')].forEach((pg, i) => {
    const no = pg.querySelector('.pg-foot .no');
    if (no) no.textContent = String(i + 1).padStart(2, '0');
  });
}

/** Quebra em duas a página montada que não coube, e repete até caber.
 *
 *  Precisa de um documento já diagramado: a conta é `scrollHeight` contra
 *  `clientHeight`, e num documento solto na memória não há nem um nem outro.
 *  Por isso ela roda no quadro da prévia e no quadro escondido da exportação, e
 *  não dentro de `montar()`.
 *
 *  O algoritmo é o do compositor: enquanto não couber, tira o último bloco e
 *  passa para a página seguinte. Ler `scrollHeight` a cada passo força o
 *  navegador a recalcular, então a medida acompanha a mudança.
 *
 *  Um bloco sozinho que não cabe não tem como ser dividido — uma tabela de
 *  quinze linhas é uma coisa só. Esse fica, e quem avisa é `conferirEstouro()`.
 *
 *  A guarda de 60 voltas existe para o caso de uma página em que nada couber:
 *  sem ela, o laço passaria o bloco adiante para sempre.
 */
function repaginar(doc) {
  const fila = [...doc.querySelectorAll('.page.montada')];
  let guarda = 0;
  while (fila.length && guarda < 60) {
    guarda += 1;
    const pg = fila.shift();
    const corpo = pg.querySelector('.pg-body');
    if (!corpo || corpo.scrollHeight - corpo.clientHeight <= 1) continue;
    if (corpo.children.length <= 1) continue;

    const nova = pg.cloneNode(true);
    const novoCorpo = nova.querySelector('.pg-body');
    novoCorpo.innerHTML = '';
    // A continuação diz que é continuação: quem lê o documento impresso vê duas
    // páginas com o mesmo título no cabeçalho e precisa saber que é a mesma
    // seção, e não um assunto repetido.
    const sec = nova.querySelector('.pg-head .sec');
    if (sec && !/ · continuação$/.test(sec.textContent)) {
      sec.textContent = `${sec.textContent} · continuação`;
    }
    while (corpo.children.length > 1 && corpo.scrollHeight - corpo.clientHeight > 1) {
      novoCorpo.prepend(corpo.lastElementChild);
    }
    pg.after(nova);
    fila.unshift(nova);   // a continuação também pode não caber
  }
  renumerar(doc);
}

const PX_MM = 96 / 25.4;

/** Faz um trabalho sobre o documento diagramado, e devolve o HTML resultante.
 *
 *  Há coisas que não se sabem sobre um documento solto na memória: quanto uma
 *  página ocupa, se o conteúdo dela coube, onde cortar. Tudo isso pede layout,
 *  e layout pede um documento numa janela. O quadro escondido é essa janela —
 *  fora da tela, sem interferir em nada, descartado ao fim.
 */
async function noQuadro(html, trabalho) {
  const quadro = document.createElement('iframe');
  quadro.setAttribute('aria-hidden', 'true');
  quadro.style.cssText = 'position:fixed;left:-20000px;top:0;width:1200px;height:800px;'
                       + 'border:0;visibility:hidden';
  document.body.appendChild(quadro);
  try {
    const doc = quadro.contentDocument;
    doc.open();
    doc.write(html);
    doc.close();
    // A fonte e as imagens vêm embutidas no próprio arquivo, mas assentar leva
    // um quadro: medir antes disso dá a altura da fonte de reserva, que é outra.
    if (doc.fonts) { try { await doc.fonts.ready; } catch (e) { /* sem a API */ } }
    await new Promise((pronto) => requestAnimationFrame(pronto));
    trabalho(doc);
    return '<!doctype html>\n' + doc.documentElement.outerHTML;
  } finally {
    quadro.remove();
  }
}

/** A altura, em milímetros, que a folha longa precisa para caber o que foi
 *  escrito — ou `null` se o documento não tiver folha longa, que é o caso da
 *  maioria: A4 e slide têm tamanho de papel, e neles é o conteúdo que se ajusta
 *  à página, não o contrário.
 *
 *  A apresentação do consultor é a exceção: uma folha só, de mais de um metro,
 *  cuja altura depende de quanto foi escrito. Solta a altura da folha, lê o que
 *  o conteúdo ocupa e devolve a caixa ao que era. É a mesma conta do
 *  `scripts/altura.mjs`, que acerta os arquivos gerados; aqui ela vale para o
 *  que a pessoa acabou de digitar. */
function alturaDaFolha(doc) {
  const altos = [...doc.querySelectorAll('.page.longa')].map((folha) => {
    const antes = folha.style.height;
    folha.style.height = 'auto';
    const px = folha.getBoundingClientRect().height;
    folha.style.height = antes;
    return px / PX_MM;
  });
  if (!altos.length) return null;
  // Arredonda para cima, ao múltiplo de 5 mm seguinte e com pelo menos 2 mm de
  // folga: os poucos milímetros de sobra são o que os respiros elásticos
  // repartem entre as seções, e absorvem a diferença entre o que este navegador
  // mede e o que o mecanismo de impressão desenha. O piso é o A4. `@page` tem um
  // tamanho só para o arquivo inteiro, então com mais de uma folha vale a maior:
  // sobra vão nas outras, mas nenhuma sai cortada.
  return Math.max(297, Math.ceil((Math.max(...altos) + 2) / 5) * 5);
}

/** O arquivo pronto para sair.
 *
 *  Duas coisas exigem um documento diagramado, e as duas acontecem no mesmo
 *  quadro escondido: repaginar as páginas montadas que não couberam e medir a
 *  altura da folha longa. O quadro trabalha sempre sobre a versão sem o script
 *  de impressão — ele é um documento como outro qualquer, e o script mandaria o
 *  navegador abrir a caixa de imprimir a partir dele. O script entra no fim,
 *  no texto já pronto. */
async function montarFinal(modo) {
  let html = montar(modo === 'imprimir' ? 'exportar' : modo);
  const montadas = html.includes('page montada');
  const longa = html.includes('page longa');
  const graficos = html.includes('chart feito');
  if (montadas || longa || graficos) {
    html = await noQuadro(html, (doc) => {
      if (montadas) repaginar(doc);
      if (graficos) ajustarGraficos(doc);
      if (!longa) return;
      const alto = alturaDaFolha(doc);
      if (!alto) return;
      const estilo = doc.createElement('style');
      estilo.textContent =
        `@page{size:210mm ${alto}mm;margin:0}.page.longa{height:${alto}mm}`;
      doc.head.appendChild(estilo);
    });
  }
  if (modo === 'imprimir') {
    html = html.replace('</body>', () =>
      '<script>addEventListener("load",()=>setTimeout(()=>print(),300))</script></body>');
  }
  return html;
}

/** Em que posição da prévia está a página montada `id` (-1 se não está). */
function indiceDaMontada(id) {
  const doc = $('#quadro').contentDocument;
  if (!doc) return -1;
  return [...doc.querySelectorAll('.page, .slide')].findIndex((p) => p.dataset.montada === id);
}

/* Editar na prévia.
 *
 *  O texto do documento é o próprio campo: clicar nele e escrever grava no
 *  mesmo lugar que o formulário grava, e o formulário acompanha. Enquanto se
 *  escreve a prévia não é redesenhada — redesenhar tiraria o cursor do lugar
 *  —; ela se refaz ao sair do campo, quando o número ganha o formato do
 *  documento e a lacuna que ficou vazia volta a se anunciar. */
const ESTILO_PREVIA = `<style>
.ph[contenteditable]{cursor:text;border-radius:2px;transition:outline-color .12s}
.ph[contenteditable]:hover{outline:1px dashed rgba(2,54,32,.55);outline-offset:1px}
.ph[contenteditable]:focus{outline:2px solid #0F8A51;outline-offset:1px;background:rgba(15,138,81,.08);text-decoration:none}
.slide.dark .ph[contenteditable]:hover,.page.dark .ph[contenteditable]:hover{outline-color:rgba(255,255,255,.6)}
</style>`;

function ligarPrevia(doc) {
  const campoDe = (el) => el.closest?.('.ph[data-campo][contenteditable]');
  doc.addEventListener('focusin', (e) => {
    const span = campoDe(e.target);
    if (!span) return;
    // A lacuna mostra {{campo}} para se anunciar; ao entrar nela, o nome sai
    // para o que se digitar não se misturar com ele.
    if (!span.classList.contains('feito') && !span.classList.contains('pronto')) span.textContent = '';
  });
  doc.addEventListener('input', (e) => {
    const span = campoDe(e.target);
    if (!span) return;
    const nome = span.dataset.campo;
    const valor = span.textContent;
    estado.valores[nome] = valor;
    for (const el of $$(`[data-campo="${CSS.escape(nome)}"]`)) {
      if (el.value !== valor) el.value = valor;
      el.dataset.preenchido = valor.trim() ? '1' : '';
    }
    clearTimeout(temporizador);
    temporizador = setTimeout(() => { salvar(); atualizarContagens(); }, 250);
  });
  doc.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && campoDe(e.target)) { e.preventDefault(); e.target.blur(); }
  });
  doc.addEventListener('focusout', (e) => {
    const span = campoDe(e.target);
    if (!span) return;
    const nome = span.dataset.campo;
    const meta = estado.estrutura.campos[nome];
    const tipo = meta && /^(dinheiro|percentual|pp|numero)$/.test(meta.tipo || '') ? meta.tipo : null;
    const valor = tipo ? formatar(tipo, span.textContent) : span.textContent;
    estado.valores[nome] = valor;
    for (const el of $$(`[data-campo="${CSS.escape(nome)}"]`)) el.value = valor;
    clearTimeout(temporizador);
    salvar();
    atualizarContagens();
    renderizar();
  });
}

function renderizar() {
  const doc = $('#quadro').contentDocument;
  doc.open();
  doc.write(montar('previa').replace('</head>', ESTILO_PREVIA + '</head>'));
  doc.close();
  ligarPrevia(doc);
  // Na mesma ordem da exportação: primeiro reparte as páginas montadas que não
  // couberam, depois confere o que sobrou, e só então ajusta a vista. O ajuste
  // esconde todas as páginas menos a que está à frente, e página escondida não
  // tem altura para medir nem para repaginar.
  setTimeout(() => {
    repaginar(doc);
    ajustarGraficos(doc);
    conferirEstouro();
    // O bloco recém-acrescentado pede a página dele à vista.
    if (estado.verMontada) {
      const i = indiceDaMontada(estado.verMontada);
      if (i >= 0) estado.pagina = i + 1;
      estado.verMontada = null;
    }
    ajustarQuadro();
  }, 50);
}

/** Que páginas não couberam.
 *
 *  A página tem altura fechada e `overflow:hidden`: o que passa dela não
 *  aparece, e não aparece calado. Quem escreveu três parágrafos onde cabia um
 *  exportava o documento com o terceiro cortado sem nenhum sinal — e com o
 *  construtor de páginas isso deixou de ser raro, porque empilhar oito blocos é
 *  um clique cada.
 *
 *  A conta é a mesma do `npm run check`, que valida os modelos no build: o
 *  corpo da página rola mais do que a caixa dele. A diferença é que aqui ela
 *  roda sobre o que a pessoa acabou de escrever. */
function conferirEstouro() {
  const doc = $('#quadro').contentDocument;
  if (!doc) return;
  const antes = JSON.stringify(estado.estouro);
  estado.estouro = [...doc.querySelectorAll('.page, .slide')].map((pg, i) => {
    const corpo = pg.querySelector('.pg-body');
    const sobra = corpo ? Math.round(corpo.scrollHeight - corpo.clientHeight) : 0;
    return { no: i + 1, secao: pg.querySelector('.pg-head .sec')?.textContent || '', sobra };
  }).filter((x) => x.sobra > 1);
  if (JSON.stringify(estado.estouro) !== antes) mostrarEstouro();
}

/** O aviso, onde ele é útil: no alto do formulário e junto da página montada
 *  que causou o problema. */
function mostrarEstouro() {
  const caixa = $('#estouro');
  if (!caixa) return;
  const n = estado.estouro.length;
  caixa.hidden = !n;
  if (n) {
    // As páginas montadas já se repartiram sozinhas antes desta conferência. O
    // que sobra aqui é o que não tem como repartir: uma página do modelo com
    // texto demais, ou um bloco único — uma tabela de quinze linhas — que não
    // cabe inteiro em folha nenhuma.
    caixa.innerHTML = `<strong>${n === 1 ? 'Uma página não coube' : `${n} páginas não couberam`}.</strong>
      O que passa da margem é cortado no arquivo exportado. ${estado.estouro.map((x) =>
        `<span class="pg-estourou">${String(x.no).padStart(2, '0')} ${escapa(x.secao)}</span>`).join(' ')}
      Encurte o texto dessas páginas — ou, se for um bloco só que não cabe, divida-o em dois.`;
  }
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
  const palco = $('.palco');
  const alturaLivre = Math.max(240, window.innerHeight - palco.getBoundingClientRect().top - 60);
  // Cabe na largura da coluna e na altura da janela: a página inteira à vista
  // vale mais do que ver o topo em tamanho real. A exceção é a folha longa da
  // apresentação do consultor, que tem mais de um metro e meio de altura:
  // encolhê-la até caber na janela deixaria o texto com um pixel e meio. Nela a
  // escala sai só da largura, e a prévia rola, como o documento rola na tela de
  // quem recebe.
  const rolar = a / l > 2;
  const escala = rolar
    ? Math.min(1, (palco.clientWidth - 40) / l)
    : Math.min(1, (palco.clientWidth - 40) / l, alturaLivre / a);
  quadro.style.width = `${l}px`;
  quadro.style.height = `${a}px`;
  quadro.style.transform = `scale(${escala})`;
  moldura.style.width = `${l * escala}px`;
  moldura.style.height = `${(rolar ? Math.min(a * escala, alturaLivre) : a * escala)}px`;
  moldura.style.overflowY = rolar ? 'auto' : '';
}

/** A prévia mostra só as páginas incluídas, então a seção do formulário — que
 *  conhece o número original — aponta para a posição que a página tem agora. */
/** Leva a prévia à página `original` do modelo. O índice na prévia não é o
 *  número do modelo: páginas desmarcadas saem e páginas montadas entram no
 *  meio, então a busca é pela marca que `montar()` deixa em cada uma. */
function irPara(original) {
  const doc = $('#quadro').contentDocument;
  const i = doc ? [...doc.querySelectorAll('.page, .slide')]
    .findIndex((p) => Number(p.dataset.original) === original) : -1;
  if (i >= 0) estado.pagina = i + 1;
  ajustarQuadro();
}

/** Leva a prévia à posição `i` (1 a n), como o paginador conta. */
function irIndice(i) {
  estado.pagina = i;
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
       Ao exportar, a ferramenta mostra ${faltam === 1 ? 'qual é' : 'quais são'}. Se você
       exportar assim mesmo, ${faltam === 1 ? 'ele sai' : 'eles saem'} em branco no
       documento — sem <code>{{campo}}</code> no lugar.</div>`
    : '';
}

/** Os campos que ficaram em branco, com rótulo e página, na ordem do documento.
 *  Campo de página desmarcada não entra: ela não vai sair no arquivo, e cobrar
 *  o preenchimento de uma página que foi tirada é ruído. */
function emBranco() {
  const { grupos, campos } = estado.estrutura;
  const achados = [];
  for (const g of [...grupos].sort((a, b) => a.pagina - b.pagina)) {
    if (!dentro(g.pagina)) continue;
    for (const n of g.campos) {
      if ((estado.valores[n] || '').trim()) continue;
      achados.push({ nome: n, rotulo: (campos[n] || {}).rotulo || n, pagina: g.pagina, secao: g.secao });
    }
  }
  // Os campos dos blocos não estão na estrutura do modelo — eles nascem quando
  // o consultor acrescenta o bloco —, e por isso passavam despercebidos pelo
  // aviso: dava para montar uma página inteira em branco e exportar sem que
  // nada avisasse.
  for (const pg of estado.paginas) {
    for (const bl of pg.blocos) {
      for (const [nome, meta] of Object.entries(blocoCampos(bl))) {
        if ((estado.valores[nome] || '').trim()) continue;
        achados.push({ nome, rotulo: meta.rotulo, pagina: pg.depois,
                       secao: (pg.secao || 'Página montada') + ' · '
                              + (blocoDe(bl.chave)?.nome || bl.chave) });
      }
    }
  }
  // Na ordem do documento, e não na de descoberta: com trezentos campos vazios
  // a lista mostra os doze primeiros, e "os doze primeiros" só quer dizer
  // alguma coisa se for pela página.
  achados.sort((a, b) => a.pagina - b.pagina);
  return achados;
}

/** O aviso antes de exportar. Diz quantos campos ficaram em branco e quais são,
 *  porque "faltam 7" sem a lista obriga a caçar os 7 de volta pelo formulário.
 *  Quem confirma leva o documento com as lacunas vazias — é uma escolha
 *  legítima, há campo que não se aplica a todo cliente —, e quem cancela volta
 *  para o formulário com os nomes em mãos. */
const MOSTRA = 12;

function confirmaBrancos() {
  const faltam = emBranco();
  const semImagem = estado.estrutura.imagens.filter((im) => dentro(im.pagina)
    && !estado.imagens[im.id]
    && !(estado.graficos[im.id] && window.Graficos.temDados(estado.graficos[im.id])));
  if (!faltam.length && !semImagem.length) return true;

  const linhas = [];
  if (faltam.length) {
    linhas.push(`${faltam.length} campo${faltam.length === 1 ? '' : 's'} em branco:`, '');
    for (const c of faltam.slice(0, MOSTRA)) {
      linhas.push(`• ${c.rotulo} — pág. ${String(c.pagina).padStart(2, '0')}, ${c.secao}`);
    }
    if (faltam.length > MOSTRA) linhas.push(`• e mais ${faltam.length - MOSTRA}.`);
    linhas.push('');
  }
  if (semImagem.length) {
    linhas.push(`${semImagem.length} imagem${semImagem.length === 1 ? '' : 'ns'} sem arquivo: `
                + `${semImagem.slice(0, MOSTRA).map((im) => im.rotulo).join(', ')}.`,
                'O espaço reservado sai como moldura vazia.', '');
  }
  linhas.push(faltam.length
    ? 'Exportar assim mesmo? No documento essas lacunas saem em branco.'
    : 'Exportar assim mesmo?');
  return confirm(linhas.join('\n'));
}

async function exportarPdf() {
  if (!confirmaBrancos()) return;
  const janela = window.open('', '_blank');
  if (!janela) {
    alert('O navegador bloqueou a janela. Libere as janelas pop-up para este site e tente de novo.');
    return;
  }
  // A folha longa é medida antes de sair, e medir leva um instante: a janela
  // abre já dizendo o que está fazendo, em vez de ficar em branco.
  janela.document.write('<!doctype html><meta charset="utf-8"><title>Preparando…</title>'
    + '<body style="margin:0;font:15px/1.6 system-ui,sans-serif;color:#555;padding:40px">'
    + 'Preparando o documento…');
  const html = await montarFinal('imprimir');
  janela.document.open();
  janela.document.write(html);
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
    estado.graficos = d.graficos || {};
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
    const secao = e.target.dataset.pagSecao;
    if (secao) {
      const pg = estado.paginas.find((p) => p.id === secao);
      if (pg) pg.secao = e.target.value;
      clearTimeout(temporizador);
      temporizador = setTimeout(() => { salvar(); renderizar(); }, 250);
      return;
    }
    const gr = e.target.dataset.gr;
    if (gr) {
      const i = Number(e.target.dataset.i);
      const c = e.target.dataset.c;
      const linhas = estado.graficos[gr] || (estado.graficos[gr] = []);
      while (linhas.length <= i) linhas.push({ r: '', v: [] });
      if (!Array.isArray(linhas[i].v)) linhas[i] = { r: linhas[i].r || '', v: [] };
      if (c === 'r') linhas[i].r = e.target.value;
      else linhas[i].v[Number(c)] = e.target.value;
      clearTimeout(temporizador);
      temporizador = setTimeout(() => { salvar(); atualizarContagens(); renderizar(); }, 250);
      return;
    }
    if (!e.target.dataset.campo) return;
    anotar(e.target, e.target.value);
  });

  // Ao sair do campo, o número ganha o formato do documento: `12400` vira
  // `R$ 12.400,00`, `-1,2` vira `-1,2%`. Enquanto se digita nada muda.
  form.addEventListener('change', (e) => {
    const tipo = e.target.dataset.formato;
    if (!tipo) return;
    const f = formatar(tipo, e.target.value);
    if (f === e.target.value) return;
    e.target.value = f;
    anotar(e.target, f);
  });

  // Arrastar a alça de um bloco para cima ou para baixo de outro da mesma
  // página. As setas continuam fazendo o mesmo para quem não usa mouse.
  let arrastando = null;
  form.addEventListener('dragstart', (e) => {
    const alca = e.target.closest?.('[data-arrasta]');
    if (!alca) return;
    arrastando = Number(alca.dataset.arrasta);
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', String(arrastando));
    alca.closest('.bloco').classList.add('arrastando');
  });
  form.addEventListener('dragover', (e) => {
    const sobre = e.target.closest?.('.bloco');
    if (arrastando === null || !sobre) return;
    const pg = estado.paginas.find((p) => p.blocos.some((b) => b.id === arrastando));
    if (!pg || !pg.blocos.some((b) => b.id === Number(sobre.dataset.bloco))) return;
    e.preventDefault();
    const r = sobre.getBoundingClientRect();
    const antes = e.clientY < r.top + r.height / 2;
    $$('.bloco.antes, .bloco.depois', form).forEach((b) => b.classList.remove('antes', 'depois'));
    sobre.classList.add(antes ? 'antes' : 'depois');
  });
  form.addEventListener('dragleave', (e) => {
    const sobre = e.target.closest?.('.bloco');
    if (sobre && !sobre.contains(e.relatedTarget)) sobre.classList.remove('antes', 'depois');
  });
  form.addEventListener('drop', (e) => {
    const sobre = e.target.closest?.('.bloco');
    if (arrastando === null || !sobre) return;
    e.preventDefault();
    const pg = estado.paginas.find((p) => p.blocos.some((b) => b.id === arrastando));
    const alvo = Number(sobre.dataset.bloco);
    if (!pg || alvo === arrastando) { arrastando = null; telaPreencher(); return; }
    const antes = sobre.classList.contains('antes');
    const [bl] = pg.blocos.splice(pg.blocos.findIndex((b) => b.id === arrastando), 1);
    const j = pg.blocos.findIndex((b) => b.id === alvo);
    pg.blocos.splice(antes ? j : j + 1, 0, bl);
    arrastando = null;
    salvar();
    telaPreencher();
  });
  form.addEventListener('dragend', () => {
    arrastando = null;
    $$('.bloco.arrastando, .bloco.antes, .bloco.depois', form)
      .forEach((b) => b.classList.remove('arrastando', 'antes', 'depois'));
  });

  // A prévia acompanha: escrever num bloco mostra a página montada em que
  // ele está, em vez de deixar a página do modelo que estava à vista.
  form.addEventListener('focusin', (e) => {
    const pg = e.target.closest('.pag-nova');
    if (!pg) return;
    const i = indiceDaMontada(pg.dataset.pag);
    if (i >= 0 && estado.pagina !== i + 1) { estado.pagina = i + 1; ajustarQuadro(); }
  });

  // A soma de uma coluna, na linha de total. Soma o que é número nas linhas
  // do corpo e escreve no formato do campo de total.
  form.addEventListener('click', (e) => {
    const nome = e.target.dataset.soma;
    if (!nome) return;
    const col = Number(e.target.dataset.coluna) + 1;
    const tabela = e.target.closest('table');
    const alvo = form.querySelector(`[data-campo="${CSS.escape(nome)}"]`);
    if (!tabela || !alvo) return;
    let total = 0, n = 0;
    for (const el of tabela.querySelectorAll(`tbody tr > td:nth-child(${col}) [data-campo]`)) {
      const v = numeroDe(el.value);
      if (v !== null) { total += v; n += 1; }
    }
    if (!n) return;
    const tipo = alvo.dataset.formato || 'numero';
    const texto = formatar(tipo, String(total).replace('.', ','));
    alvo.value = texto;
    anotar(alvo, texto);
  });

  // O calendário ao lado do campo de data. Abre no dia que está escrito e, ao
  // escolher, escreve no campo de texto — que é o que o documento lê.
  form.addEventListener('click', (e) => {
    const nome = e.target.dataset.seletor;
    if (!nome) return;
    const texto = form.querySelector(`[data-campo="${CSS.escape(nome)}"]`);
    const sel = form.querySelector(`[data-seletor-de="${CSS.escape(nome)}"]`);
    if (!texto || !sel) return;
    sel.value = sel.type === 'month' ? mesIsoDe(texto.value) : isoDe(texto.value);
    try { sel.showPicker(); } catch (err) { sel.focus(); sel.click(); }
  });
  form.addEventListener('change', (e) => {
    const nome = e.target.dataset.seletorDe;
    if (!nome) return;
    const texto = form.querySelector(`[data-campo="${CSS.escape(nome)}"]`);
    if (!texto) return;
    texto.value = textoDaData(e.target.type, e.target.value);
    anotar(texto, texto.value);
  });

  form.addEventListener('change', (e) => {
    const id = e.target.dataset.arquivo;
    if (!id || !e.target.files[0]) return;
    const leitor = new FileReader();
    leitor.onload = () => { estado.imagens[id] = leitor.result; salvarImagens(); telaPreencher(); };
    leitor.readAsDataURL(e.target.files[0]);
  });

  form.addEventListener('change', (e) => {

    const onde = e.target.dataset.pagOnde;
    if (onde) {
      const pg = estado.paginas.find((p) => p.id === onde);
      if (pg) pg.depois = Number(e.target.value);
      salvar();
      renderizar();
    }
  });

  form.addEventListener('toggle', (e) => {
    const bl = e.target.closest?.('details.bloco');
    if (!bl) return;
    estado.fechados = estado.fechados || new Set();
    if (bl.open) estado.fechados.delete(Number(bl.dataset.bloco));
    else estado.fechados.add(Number(bl.dataset.bloco));
  }, true);

  form.addEventListener('click', (e) => {
    if (e.target.id === 'nova-pagina') { novaPagina(); return; }

    if (e.target.id === 'todas-paginas') { estado.fora = new Set(); salvar(); telaPreencher(); return; }

    const chave = e.target.closest('.chave[data-pagina]');
    if (chave) {
      // Dentro do <summary>, o clique abriria ou fecharia a seção: não é isso.
      e.preventDefault();
      alternarPagina(Number(chave.dataset.pagina));
      return;
    }

    // Botão dentro do <summary> do bloco age sem abrir nem fechar o bloco.
    if (e.target.closest('summary') && e.target.closest('button')) e.preventDefault();

    const add = e.target.closest('[data-bl-add]');
    if (add) {
      const pg = estado.paginas.find((p) => p.id === add.dataset.blAdd);
      if (!pg) return;
      const id = estado.proximoBloco++;
      pg.blocos.push({ id, chave: add.dataset.chave });
      estado.verMontada = pg.id;
      salvar();
      telaPreencher();
      // O foco vai para o primeiro campo do bloco novo: quem clicou quer escrever nele.
      $(`.bloco[data-bloco="${id}"] input, .bloco[data-bloco="${id}"] textarea`)?.focus();
      return;
    }

    const pgFora = e.target.dataset.pagFora;
    if (pgFora) {
      if (!confirm('Remover esta página e tudo o que você escreveu nela?')) return;
      estado.paginas = estado.paginas.filter((p) => p.id !== pgFora);
      salvar();
      telaPreencher();
      return;
    }

    // Subir, descer e remover bloco. O bloco não sabe de que página é, então a
    // busca é pela página que o contém — são poucas, e é o que dispensa guardar
    // o vínculo em dois lugares e mantê-los de acordo.
    const sobe = e.target.dataset.blSobe;
    const desce = e.target.dataset.blDesce;
    const blFora = e.target.dataset.blFora;
    const alvo = sobe || desce || blFora;
    if (alvo) {
      const pg = estado.paginas.find((p) => p.blocos.some((b) => b.id === Number(alvo)));
      if (!pg) return;
      const i = pg.blocos.findIndex((b) => b.id === Number(alvo));
      if (blFora) {
        const cheio = resumoDoBloco(pg.blocos[i]) !== 'em branco';
        if (cheio && !confirm('Remover este bloco e o que você escreveu nele?')) return;
        pg.blocos.splice(i, 1);
      } else {
        const j = sobe ? i - 1 : i + 1;
        [pg.blocos[i], pg.blocos[j]] = [pg.blocos[j], pg.blocos[i]];
      }
      salvar();
      telaPreencher();
      return;
    }

    const mais = e.target.dataset.mais;
    if (mais) {
      const im = estado.estrutura.imagens.find((x) => String(x.id) === mais)
        || { id: mais, grafico: 'line', series: null, eixo: null };
      estado.graficos[mais] = linhasDe(im).concat([{ r: '', v: colunasDe(im).map(() => '') }]);
      salvar();
      telaPreencher();
      return;
    }
    const id = e.target.dataset.tirar;
    if (!id) return;
    delete estado.imagens[id];
    salvarImagens();
    telaPreencher();
  });

  // Abrir uma seção leva a prévia para a página correspondente. A lista de
  // páginas é a exceção: ela não é de uma página, é de todas.
  // Só o clique de quem usa conta: o formulário se redesenha a cada mudança, e
  // a seção que nasce aberta também dispara `toggle` — sem esta trava, mudar a
  // ordem de um bloco levava a prévia de volta à página 1.
  form.addEventListener('click', (e) => {
    const sum = e.target.closest('.secao > summary');
    estado.secaoClicada = sum && !e.target.closest('.chave') ? sum.parentElement : null;
  }, true);
  form.addEventListener('keydown', (e) => {
    const chave = e.target.closest?.('.chave[data-pagina]');
    if (chave && (e.key === ' ' || e.key === 'Enter')) { e.preventDefault(); alternarPagina(Number(chave.dataset.pagina)); }
  });

  form.addEventListener('toggle', (e) => {
    if (e.target !== estado.secaoClicada) return;
    estado.secaoClicada = null;
    const n = Number(e.target.dataset.pagina);
    if (e.target.open && n) irPara(n);
  }, true);

  $('#abrir-tudo').onclick = () => $$('.secao', form).forEach((d) => { d.open = true; });
  $('#fechar-tudo').onclick = () => $$('.secao', form).forEach((d) => { d.open = false; });

  $('#busca').oninput = (e) => {
    const q = e.target.value.trim().toLowerCase();
    $$('.secao', form).forEach((sec) => {
      let achou = 0;
      $$('.campo, .imagem, .tabela', sec).forEach((c) => {
        const bate = !q || (c.textContent + ' ' + (c.dataset.nome || '')).toLowerCase().includes(q);
        c.hidden = !bate;
        if (bate) achou++;
      });
      (sec.closest('.linha-secao') || sec).hidden = !!q && !achou;
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

  $('#pag-anterior').onclick = () => irIndice(estado.pagina - 1);
  $('#pag-proxima').onclick = () => irIndice(estado.pagina + 1);
  $('#exportar-html').onclick = async () => {
    if (!confirmaBrancos()) return;
    baixar(await montarFinal('exportar'), nomeArquivo('html'), 'text/html;charset=utf-8');
  };
  $('#exportar-pdf').onclick = exportarPdf;
  // Quem empresta o computador, ou troca de escritório, precisa de um jeito de
  // limpar o que ficou guardado.
  $('#esquecer').onclick = () => {
    if (!confirm('Apagar o nome, o contato e os textos que este navegador guardou '
                 + 'para preencher documentos futuros?\n\n'
                 + 'O documento aberto não muda.')) return;
    esquecer();
    anunciarSalvo('Este navegador esqueceu os dados guardados');
  };

  $('#baixar-dados').onclick = () => baixar(JSON.stringify({
    documento: estado.documento.chave, variante: estado.variante.sufixo,
    valores: estado.valores, graficos: estado.graficos, imagens: estado.imagens,
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
