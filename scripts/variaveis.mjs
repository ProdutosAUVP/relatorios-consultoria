/**
 * Gera VARIAVEIS.md a partir dos tokens presentes em modelos/*.html.
 *
 *   npm run vars
 *
 * Rode sempre que um modelo ganhar ou perder campos preenchíveis, para o
 * dicionário não descolar dos arquivos.
 */
import { readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, resolve } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const srcDir = join(root, 'modelos');

const SEGS = ['consultoria', 'alta-renda', 'private', 'assessoria'];
const TITULOS = {
  'relatorio-mensal': 'Relatório mensal',
  'diagnostico-carteira': 'Diagnóstico de carteira',
  'relatorio-macroeconomico': 'Relatório macroeconômico',
  'apresentacao-geral': 'Apresentação geral',
  'relatorio-mensal-apresentacao': 'Relatório mensal em formato de apresentação',
  'cronograma-reunioes': 'Cronograma de reuniões',
};
// Campos institucionais, na ordem em que fazem sentido preencher.
const DESCR = [
  ['razao_social', 'Razão social da empresa emissora'],
  ['cnpj', 'CNPJ da empresa emissora'],
  ['registro_cvm_empresa', 'Registro da empresa na CVM'],
  ['canal_ouvidoria', 'Telefone ou e-mail da ouvidoria'],
  ['disclaimer_regulatorio', 'Texto legal aprovado pelo compliance, específico do segmento'],
  ['nome_cliente', 'Nome do cliente destinatário'],
  ['nome_responsavel', 'Consultor, assessor ou banker responsável'],
  ['registro_cvm_ou_ancord', 'Registro do responsável (CVM 19 / Ancord)'],
  ['email_contato', 'E-mail de contato exibido no documento'],
  ['whatsapp_contato', 'WhatsApp direto do responsável'],
  ['canal_atendimento', 'Canal e horário de atendimento'],
  ['link_agendamento', 'URL de agendamento (a mesma do QR code)'],
  ['mes_referencia', 'Mês de referência, ex.: Agosto de 2026'],
  ['data_posicao', 'Data da posição consolidada'],
  ['perfil_investidor', 'Perfil de suitability do cliente'],
  ['patrimonio_total', 'Patrimônio total sob acompanhamento'],
];

const files = readdirSync(srcDir).filter((f) => f.endsWith('.html')).sort();
const toks = (f) => [...readFileSync(join(srcDir, f), 'utf8').matchAll(/\{\{([a-z0-9_]+)\}\}/g)].map((m) => m[1]);

function docKey(f) {
  const base = f.slice(0, -5);
  for (const s of SEGS) if (base.endsWith('-' + s)) return [base.slice(0, -s.length - 1), s];
  return [base, null];
}

const porDoc = new Map();
for (const f of files) {
  const [k, seg] = docKey(f);
  if (!porDoc.has(k)) porDoc.set(k, []);
  porDoc.get(k).push([seg, f]);
}

const emQuantos = new Map();
for (const f of files) for (const t of new Set(toks(f))) emQuantos.set(t, (emQuantos.get(t) ?? 0) + 1);

const cols = (arr) => {
  const out = [];
  for (let i = 0; i < arr.length; i += 3) out.push(arr.slice(i, i + 3).map((x) => x.padEnd(32)).join('  ').trimEnd());
  return out.join('\n');
};

const L = [];
L.push('# Dicionário de variáveis\n');
L.push(`Todo campo preenchível aparece nos modelos como \`{{nome_da_variavel}}\`, destacado em dourado. Substitua o token inteiro, chaves incluídas.\n`);
L.push('Os nomes são estáveis entre documentos: `{{patrimonio_total}}` significa a mesma coisa no relatório mensal e na versão em apresentação, o que permite preencher vários modelos com a mesma fonte de dados.\n');
L.push('Arquivo gerado por `npm run vars`; não edite à mão.\n');
L.push('## Convenções\n');
L.push('| Padrão | Significado | Exemplo |');
L.push('| --- | --- | --- |');
L.push('| `nome_do_campo` | valor único | `{{nome_cliente}}` |');
L.push('| `bloco_N_campo` | linha `N` de uma lista ou tabela | `{{mov_3_ativo}}` |');
L.push('| `prefixo_chave_metrica` | célula de uma tabela de referência fixa | `{{alvo_rf_pos}}` |');
L.push('| `texto_*`, `analise_*`, `comentario_*` | texto corrido escrito pelo responsável | `{{texto_desvio_alocacao}}` |');
L.push('');
L.push('Linhas sobrando numa tabela (por exemplo, só houve 3 movimentações e o modelo traz 6 linhas) devem ser apagadas do HTML, não deixadas com o token à mostra.\n');
L.push('## Campos institucionais e recorrentes\n');
L.push('Estes se repetem na maior parte dos modelos. Vale manter um arquivo único com eles e aplicar em lote antes de partir para o conteúdo específico de cada documento.\n');
L.push('| Variável | O que é | Em quantos modelos |');
L.push('| --- | --- | --- |');
for (const [v, d] of DESCR) L.push(`| \`${v}\` | ${d} | ${emQuantos.get(v) ?? 0} de ${files.length} |`);
L.push('');

const institucionais = new Set(DESCR.map(([v]) => v));
for (const [k, itens] of porDoc) {
  const f0 = itens[0][1];
  const t0 = toks(f0);
  const base = new Set(t0);
  const ordem = [];
  const vistos = new Set();
  for (const x of t0) if (!vistos.has(x) && !institucionais.has(x)) { vistos.add(x); ordem.push(x); }
  L.push(`## ${TITULOS[k]}\n`);
  L.push(`Arquivos: ${itens.map(([, f]) => `\`modelos/${f}\``).join(', ')}\n`);
  L.push(`Segmentos: ${itens.map(([s]) => s).join(', ')} &middot; ${base.size} variáveis\n`);
  L.push(`<details><summary>Ver as ${ordem.length} variáveis específicas deste documento</summary>\n`);
  L.push('```');
  L.push(cols(ordem));
  L.push('```');
  L.push('</details>\n');
  for (const [seg, f] of itens.slice(1)) {
    const extra = [...new Set(toks(f))].filter((x) => !base.has(x)).sort();
    if (!extra.length) continue;
    L.push(`Campos exclusivos da variante **${seg}** (${extra.length}):\n`);
    L.push('```');
    L.push(cols(extra));
    L.push('```\n');
  }
}

writeFileSync(join(root, 'VARIAVEIS.md'), L.join('\n') + '\n');
const distintas = new Set(files.flatMap(toks)).size;
console.log(`VARIAVEIS.md gerado: ${files.length} modelos, ${distintas} variáveis distintas.`);
