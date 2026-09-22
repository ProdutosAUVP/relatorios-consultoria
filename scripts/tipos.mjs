/**
 * O tipo de cada campo: o que a ferramenta oferece para preenchê-lo.
 *
 * Um campo de data ganha um seletor de calendário; um de dinheiro ou de
 * percentual, um teclado numérico e a formatação na saída — quem digita
 * `12400` vê `R$ 12.400,00`; um de rating ou de classe, a lista do que costuma
 * ir ali. O documento continua recebendo texto, que é o que o modelo espera:
 * o tipo só muda como o texto é produzido.
 *
 * A origem do tipo, em ordem:
 *
 * 1. O nome, quando ele diz tudo (`data_posicao`, `perfil_investidor`).
 * 2. O cabeçalho da coluna, para campo de tabela. É a fonte mais confiável:
 *    quem escreveu `Meta | Atual | Desvio` sabia o que ia em cada coluna, e
 *    a classe `num` da célula confirma. `alvo_rf_pos` é percentual porque a
 *    coluna se chama Meta, e não porque o nome termina em `pos`.
 * 3. As partes do nome, pelo vocabulário do gerador. Vale para o que fica
 *    fora de tabela — os KPIs, as datas do cabeçalho, os totais.
 *
 * Fora disso é texto, curto ou corrido.
 */

/** As listas oferecidas nos campos de escolha. Sugestão, não restrição: o
 *  campo continua aceitando o que se digitar. */
export const OPCOES = {
  banda: ['Dentro da banda', 'Acima da banda', 'Abaixo da banda'],
  visao: ['Positiva', 'Neutra', 'Negativa'],
  vies: ['De alta', 'Neutro', 'De baixa'],
  grau: ['Alta', 'Média', 'Baixa'],
  simnao: ['Sim', 'Não', 'Parcial'],
  rating: ['AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-', 'BBB+', 'BBB', 'BBB-',
           'BB+', 'BB', 'BB-', 'B+', 'B', 'B-', 'Sem rating'],
  classe: ['Renda fixa pós-fixada', 'Renda fixa prefixada', 'Renda fixa inflação',
           'Renda fixa internacional', 'Multimercado', 'Ações', 'Fundos imobiliários',
           'Renda variável internacional', 'Criptomoedas', 'Alternativos', 'Caixa'],
  operacao: ['Compra', 'Venda', 'Aplicação', 'Resgate', 'Subscrição', 'Amortização',
             'Vencimento', 'Rebalanceamento'],
  provento: ['Dividendos', 'JCP', 'Rendimento de FII', 'Cupom', 'Juros', 'Amortização',
             'Aluguel de ações'],
  liquidez: ['D+0', 'D+1', 'D+2', 'D+30', 'Diária', 'No vencimento'],
  pais: ['Brasil', 'Estados Unidos', 'Zona do Euro', 'China', 'Japão', 'Reino Unido', 'Global'],
  perfil: ['Conservador', 'Moderado', 'Arrojado'],
  horizonte: ['Curto prazo (até 2 anos)', 'Médio prazo (2 a 5 anos)', 'Longo prazo (acima de 5 anos)'],
  cadencia: ['Mensal', 'Bimestral', 'Trimestral', 'Semestral', 'Anual', 'Sob demanda'],
};

const opcoes = (chave) => ({ tipo: 'opcoes', opcoes: chave });

// 1. Pelo nome inteiro.
const POR_NOME = {
  data_apresentacao: 'mes', data_carta: 'mes', mes_referencia: 'mes', mes_seguinte: 'mes',
  ano_vigencia: 'ano', ano_corrente: 'ano', ano_seguinte: 'ano',
  perfil_investidor: opcoes('perfil'), horizonte_principal: opcoes('horizonte'),
  selic_atual: 'percentual', retorno_12m_pct_cdi: 'percentual',
  retorno_esperado_proposta: 'percentual', risco_esperado_proposta: 'percentual',
  custo_perc_patrimonio: 'percentual', custo_proposto_perc: 'percentual',
  custo_proposto_anual: 'dinheiro', economia_estimada_ano: 'dinheiro',
  economia_estimada_10a: 'dinheiro', remun_equivalente_ano: 'dinheiro',
  capacidade_aporte_mensal: 'dinheiro', liquidez_minima: 'dinheiro',
  total_aportes: 'dinheiro', total_custos: 'dinheiro', total_resgates: 'dinheiro',
  qtd_ativos: 'numero', qtd_contas: 'numero', qtd_instituicoes: 'numero',
  resumo_do_mes: 'longo', ponto_de_atencao_mes: 'longo',
};

// 2. Pelo cabeçalho da coluna. Os de número vêm com a classe `num` na célula;
//    os outros são escolha entre poucos valores.
const CABECALHO_NUM = [
  [/^(Valor|Posição|Exposição|Resultado no mês|Bruto|IR|Líquido|Em R\$\/ano|Custo da saída|Impacto estimado|Limite sugerido|Valor-alvo|Valor no período|Recuperável|Sob o teto|Posição \((R|US)\$\))$/, 'dinheiro'],
  [/^Desvio$/, 'pp'],
  [/^(Quantidade|Último dado|Último|Anterior)$/, 'numero'],
  [/^(%|% .*|12 meses|24 meses|No mês|No ano|Mês|Ano|12m|24m|Desde o início|Atual|Meta|Alvo|Acumulado|Retorno 12m|Volatilidade 12m|Custo a\.a\.|Variação|Variação no mês|Hoje|Proposto|Mínimo|Máximo|Projeção|Projeção fim do ano|Consenso.*|\{\{ano_(corrente|seguinte)\}\})$/, 'percentual'],
];
const CABECALHO = [
  [/^(Data|Vencimento)$/, 'data'],
  [/^Rating$/, opcoes('rating')],
  [/^Coberto pelo FGC$/, opcoes('simnao')],
  [/^Classe$/, opcoes('classe')],
  [/^(Operação|Movimento|Movimento no mês)$/, opcoes('operacao')],
  [/^Visão$/, opcoes('visao')],
  [/^Viés$/, opcoes('vies')],
  [/^(Prioridade|Gravidade|Relevância|Impacto|Risco|Probabilidade)$/, opcoes('grau')],
  [/^Liquidez$/, opcoes('liquidez')],
  [/^País$/, opcoes('pais')],
];

// 3. Pelas partes do nome, da mais forte para a mais fraca. Um nome como
//    `aporte_liquido_mes` tem termo de dinheiro e termo de período: ganha o
//    dinheiro, porque é o que o campo recebe.
const LONGO = /^(texto|analise|comentario|resumo|nota|observacao|descricao|leitura|contexto|justificativa|recomendacao|conclusao|mensagem|sintese|racional|motivo|detalhe|proposito|frase|bio|paragrafo|cenario|premissa|trajetoria)$/;
const DINHEIRO = /^(valor|pat|patrimonio|saldo|total|custo|custos|bruto|liquido|ir|reais|aporte|aportes|aplicacoes|resgates|ganho|usd|eur|medio|cotacao|limite|ticket|remun|economia)$/;
const PERCENTUAL = /^(perc|pct|alvo|meta|peso|rent|ret|ret12m|ret24m|12m|24m|acum|proj|var|variacao|vol|dy|anual|mensal|cdi|prob|a1|a2|c1|c2|ipca5|ibov|min|max|selic)$/;
const PP = /^(desvio|delta|contrib)$/;
const DATA = /^(data|vencimento)$/;
const NUMERO = /^(qtd|fech|ant|ult|numero)$/;
const PARTES = [
  [/^status$/, opcoes('banda')], [/^visao$/, opcoes('visao')], [/^vies$/, opcoes('vies')],
  [/^(prioridade|gravidade|relevancia|impacto|prob)$/, opcoes('grau')],
  [/^fgc$/, opcoes('simnao')], [/^rating$/, opcoes('rating')], [/^classe$/, opcoes('classe')],
  [/^(movimento|mov|op)$/, opcoes('operacao')], [/^liquidez$/, opcoes('liquidez')],
  [/^pais$/, opcoes('pais')], [/^(freq|cadencia)$/, opcoes('cadencia')],
  [LONGO, 'longo'], [DINHEIRO, 'dinheiro'], [PERCENTUAL, 'percentual'], [PP, 'pp'],
  [DATA, 'data'], [NUMERO, 'numero'],
];

/** O tipo do campo. `cabecalho` e `num` vêm da célula de tabela em que o
 *  campo está, quando está em uma. */
export function tipoDoCampo(nome, cabecalho = null, num = false) {
  const t = POR_NOME[nome];
  if (t) return typeof t === 'string' ? { tipo: t } : t;

  if (/^email_|_email$|^canal_email_endereco$/.test(nome)) return { tipo: 'email' };
  if (/^(whatsapp|telefone)_|_(whatsapp|telefone)$|^canal_(whats|tel)_endereco$/.test(nome)) return { tipo: 'telefone' };
  if (/^reuniao_\d+_data$/.test(nome)) return { tipo: 'data' };
  // Na tabela de proventos a origem é o ativo e o tipo é dividendo, JCP, cupom.
  if (/^prov_\d+_tipo$/.test(nome)) return opcoes('provento');

  if (cabecalho) {
    const cab = cabecalho.replace(/\s+/g, ' ').trim();
    for (const [re, tipo] of (num ? CABECALHO_NUM : CABECALHO)) {
      if (re.test(cab)) return typeof tipo === 'string' ? { tipo } : tipo;
    }
    // Célula numérica com cabeçalho desconhecido: ainda é número, só não se
    // sabe de que unidade. Fica sem formatação, mas com o teclado certo.
    if (num) return { tipo: 'numero' };
  }

  const partes = nome.replace(/_\d+$/, '').split('_').filter((p) => !/^\d+$/.test(p));
  for (const [re, tipo] of PARTES) {
    if (!partes.some((p) => re.test(p))) continue;
    // Célula de texto numa tabela não vira dinheiro por causa do prefixo da
    // linha: `custo_1_onde` é onde o custo incide, `remun_2_forma` é como se
    // paga. O que as partes ainda podem dizer ali é texto corrido ou escolha.
    if (cabecalho && !num && typeof tipo === 'string' && tipo !== 'longo') break;
    return typeof tipo === 'string' ? { tipo } : tipo;
  }
  if (cabecalho) return { tipo: 'texto' };
  // `rent_mes`, `mk_spx_ano`: o período no fim do nome é variação no período.
  // `mes_referencia` e `ano_vigencia` já saíram pelo nome inteiro.
  if (/_(mes|ano)$/.test(nome) && !/^(mes|ano)_/.test(nome)) return { tipo: 'percentual' };
  if (/^mes_/.test(nome)) return { tipo: 'mes' };
  if (/^ano_/.test(nome)) return { tipo: 'ano' };
  return { tipo: 'texto' };
}

/** O exemplo que o formato pede, quando o tipo é numérico ou de data. Fica
 *  no lugar do exemplo pelo nome, que para célula de tabela acertava a linha
 *  e errava a coluna — `alvo_rf_pos` saía "PETR4". */
export function exemploDoTipo(tipo) {
  return {
    dinheiro: 'R$ 128.400,00', percentual: '12,4%', pp: '+0,4 p.p.', numero: '135.420',
    data: '31/08/2026', mes: 'Setembro de 2026', ano: '2026',
  }[tipo] || null;
}

/** Exemplo para célula de texto, pelo cabeçalho da coluna. O exemplo pelo
 *  nome vinha do prefixo da linha — a coluna Ativo da tabela de movimentações
 *  mostrava "Compra", porque o campo se chama `mov_1_ativo`. */
export function exemploDoCabecalho(cabecalho) {
  const cab = (cabecalho || '').replace(/\s+/g, ' ').trim();
  return {
    'Ativo': 'PETR4', 'Ativo / posição': 'PETR4', 'Origem': 'PETR4', 'Item': 'Tesouro IPCA+ 2035',
    'Instituição': 'Banco BTG Pactual', 'Emissor': 'Banco BTG Pactual',
    'Emissor / contraparte': 'Banco BTG Pactual', 'Contrapartida': 'Corretora',
    'Motivo': 'Concentração acima do limite definido no plano.',
    'Prazo': '2029', 'Vencimento': '15/05/2029', 'Setor': 'Financeiro',
    'Instrumento sugerido': 'Tesouro IPCA+ 2035', 'Destino': 'Tesouro IPCA+ 2035',
    'Recorte': 'Financeiro', 'Classes custodiadas': 'Renda fixa e ações',
    'Evento / indicador': 'Reunião do Copom', 'Quando': 'Setembro',
    'Onde incide': 'No app da corretora', 'Origem do custo': 'Corretagem',
    'Observação': 'Sem ressalvas.', 'Racional': 'Uma frase com o motivo.',
    'Leitura': 'Uma frase sobre o que o dado significa.',
  }[cab] || null;
}
