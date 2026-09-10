/**
 * A tabela de produtos e documentos, e como um arquivo de `modelos/` se
 * encaixa nela.
 *
 * Fica separada porque dois scripts precisam da mesma classificação e não
 * podem discordar: `catalogo.mjs`, para montar o índice da ferramenta, e
 * `render.mjs`, para saber em que pasta de `pdf/` cada arquivo vai.
 */

// Rótulo e ordem dos produtos. A chave é o sufixo do arquivo.
export const PRODUTOS = [
  { chave: 'consultoria', nome: 'Consultoria', descricao: 'Consultoria de investimentos AUVP Capital.' },
  { chave: 'alta-renda', nome: 'Alta Renda', descricao: 'Clientes de alta renda, identidade em verde quase preto.' },
  { chave: 'private', nome: 'Private Banking', descricao: 'Marca própria, paleta em cinzas, sem amarelo.' },
  { chave: 'assessoria', nome: 'Assessoria', descricao: 'Assessoria de investimentos, verde mais claro.' },
];

export const DOCUMENTOS = [
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

// Ordem dos planos da consultoria na ferramenta, do autoatendimento à
// consultoria completa. O gerador é a fonte dos planos; aqui fica só a ordem
// de exibição, e um plano que não esteja nesta lista cai no fim, em ordem
// alfabética, junto com os consultores.
export const PLANOS = ['se-vira-ai', 'me-diz-o-que-fazer', 'resolve-ai'];

// A apresentação do consultor sai duas vezes: com e sem a data no cabeçalho.
// O sufixo não muda a que produto a variante pertence nem onde ela entra na
// lista — só a põe logo depois da gêmea com data.
export const SEM_DATA = '-sem-data';

export const semData = (sufixo) => sufixo.endsWith(SEM_DATA);
export const base = (sufixo) => (semData(sufixo) ? sufixo.slice(0, -SEM_DATA.length) : sufixo);

/** Posição da variante na lista: primeiro o segmento, depois os planos, depois
 *  as pessoas, e cada uma seguida da sua versão sem data. */
export function ordemVariante(sufixo) {
  const b = base(sufixo);
  const data = semData(sufixo) ? 1 : 0;
  const seg = PRODUTOS.findIndex((p) => p.chave === b);
  if (seg >= 0) return [0, seg, data];
  const plano = PLANOS.indexOf(b);
  if (plano >= 0) return [1, plano, data];
  return [2, 0, data];
}

// A chave mais longa primeiro: `relatorio-mensal-apresentacao` também começa
// com `relatorio-mensal`.
const POR_TAMANHO = [...DOCUMENTOS].sort((a, b) => b.chave.length - a.chave.length);

/**
 * Classifica um arquivo de `modelos/`: que documento é, qual a variante e a
 * que produto ela pertence. Devolve `null` para arquivo que não casa com
 * nenhum documento — quem chama decide se isso é erro.
 */
export function classifica(arquivo) {
  const doc = POR_TAMANHO.find((d) => arquivo.startsWith(d.chave + '-'));
  if (!doc) return null;
  const sufixo = arquivo.slice(doc.chave.length + 1).replace(/\.(html|pdf|json)$/, '');
  // Quando a variante é um segmento, o produto é ela mesma. Quando não é, é um
  // plano ou um consultor — e os três planos e os sete consultores são todos
  // da consultoria. O `-sem-data` não conta: `alta-renda-sem-data` continua
  // sendo Alta Renda.
  const b = base(sufixo);
  const produto = PRODUTOS.some((p) => p.chave === b) ? b : 'consultoria';
  return { doc, sufixo, produto };
}

/**
 * O rótulo da variante. Um segmento vira o nome do produto; o resto — planos e
 * consultores — vem do `<title>` do próprio modelo, que o gerador escreve com
 * a grafia certa. Deduzir do sufixo daria `Se Vira Ai` e `Resolve Ai`.
 */
export function rotuloVariante(sufixo, html) {
  if (semData(sufixo)) return `${rotuloVariante(base(sufixo), html)}, sem data`;
  const p = PRODUTOS.find((x) => x.chave === sufixo);
  if (p) return p.nome;
  const titulo = html && html.match(/<title>([^<]*)<\/title>/)?.[1];
  const depois = titulo && titulo.split('—').slice(1).join('—').trim().replace(/, sem data$/, '');
  return depois || sufixo.split('-').map((s) => s[0].toUpperCase() + s.slice(1)).join(' ');
}
