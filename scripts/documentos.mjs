/**
 * A tabela de produtos e documentos, e como um arquivo de `modelos/` se
 * encaixa nela.
 *
 * Fica separada porque dois scripts precisam da mesma classificação e não
 * podem discordar: `catalogo.mjs`, para montar o índice da ferramenta, e
 * `render.mjs`, para saber em que pasta de `pdf/` cada arquivo vai.
 */

// Rótulo e ordem dos produtos. A chave é o sufixo do arquivo, exceto no plano
// Me Diz o Que Fazer, cujas variantes são os consultores.
export const PRODUTOS = [
  { chave: 'consultoria', nome: 'Consultoria', descricao: 'Consultoria de investimentos AUVP Capital.' },
  { chave: 'alta-renda', nome: 'Alta Renda', descricao: 'Clientes de alta renda, identidade em verde quase preto.' },
  { chave: 'private', nome: 'Private Banking', descricao: 'Marca própria, paleta em cinzas, sem amarelo.' },
  { chave: 'assessoria', nome: 'Assessoria', descricao: 'Assessoria de investimentos, verde mais claro.' },
  { chave: 'me-diz-o-que-fazer', nome: 'Me Diz o Que Fazer', descricao: 'Apresentação individual dos consultores do plano.' },
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
  const produto = doc.chave === 'apresentacao-consultor' ? 'me-diz-o-que-fazer' : sufixo;
  return { doc, sufixo, produto };
}

/** `danilo-barbosa` -> `Danilo Barbosa`; um segmento vira o nome do produto. */
export function rotuloVariante(sufixo) {
  const p = PRODUTOS.find((x) => x.chave === sufixo);
  if (p) return p.nome;
  return sufixo.split('-').map((s) => s[0].toUpperCase() + s.slice(1)).join(' ');
}
