/**
 * Exemplo de preenchimento para cada campo dos modelos.
 *
 * São 1743 campos distintos; escrever um exemplo para cada um à mão daria uma
 * tabela impossível de manter em dia. Mas os nomes são sistemáticos — o
 * gerador os monta com um vocabulário fechado —, então o exemplo sai do nome:
 * `pos_7_valor` é dinheiro, `mk_spx_vol` é volatilidade, `emis_5_rating` é
 * uma nota de crédito.
 *
 * Os poucos campos institucionais que não seguem esse vocabulário vêm escritos
 * em `POR_NOME`. Fora eles, a resolução varre as partes do nome do fim para o começo, e para na primeira
 * que tem regra: `pos_7_valor` casa em `valor`, `analise_china` só em
 * `analise`, `mes_referencia` em `mes`. É de trás para frente porque o último
 * termo costuma ser o tipo do dado e os primeiros dizem apenas de que linha da
 * tabela ele é. O que não casa em nada cai no formato do campo: texto corrido
 * ganha uma frase, campo curto ganha um lembrete do que se espera ali.
 *
 * O exemplo vira o `placeholder` do campo na ferramenta — some assim que se
 * digita, e nunca entra no documento exportado. É sugestão de formato, não
 * conteúdo aprovado: número, data e texto de compliance saem daqui como
 * ilustração e devem ser substituídos.
 */

// Campos institucionais, um de cada. Não seguem o vocabulário das tabelas, e
// são poucos o bastante para virem escritos.
const POR_NOME = {
  razao_social: 'AUVP Capital Consultoria de Valores Mobiliários Ltda.',
  cnpj: '00.000.000/0001-00', site: 'auvpcapital.com.br',
  custodiante: 'Banco BTG Pactual S.A.',
  historia_auvp: 'Dois ou três parágrafos sobre a origem da casa.',
  modelo_remuneracao: 'Fee based, percentual sobre o patrimônio orientado.',
  link_agendamento: 'auvpcapital.com.br/agenda',
  procedimento_urgencia: 'Mensagem no WhatsApp do consultor, com retorno em até 1 dia útil.',
  preparo_material: 'Carteira consolidada e extratos do período.',
  preparo_duvidas: 'A lista de dúvidas que você quer tirar na reunião.',
  preparo_mudancas: 'Mudanças de renda, objetivo ou prazo desde o último encontro.',
  etapa_coleta: 'Envio dos extratos e do questionário de perfil.',
  etapa_consolidacao: 'Consolidação das posições nas instituições informadas.',
  instituicoes_analisadas: 'BTG Pactual, XP e Tesouro Direto',
  contas_consideradas: 'Conta nacional e conta internacional',
  documentos_base: 'Extratos de agosto e informe de rendimentos',
  fonte_dados: 'Consolidador AUVP e API do BTG',
  fonte_dados_macro: 'Banco Central, IBGE e Focus',
  fonte_dados_mercado: 'B3 e Bloomberg', fonte_consenso: 'Relatório Focus',
  metodo_rentabilidade: 'Cota diária, líquida de custos e bruta de impostos.',
  ptax_utilizada: 'PTAX de fechamento de 31/08/2026',
  premissa_macro: 'Selic a 10,5% e IPCA a 4,0% em 12 meses.',
  premissa_retornos: 'CDI + 2% na renda fixa e 10% a.a. na renda variável.',
  premissa_custos: 'Sem corretagem; custódia isenta.',
  premissa_tributacao: 'Tabela regressiva, alíquota de 15%.',
  economia_estimada_10a: 'R$ 84.000,00',
  reserva_emergencia: 'R$ 60.000,00, seis meses de despesas',
  relacao_renda_despesa: 'Sobra mensal de R$ 5.000,00',
  experiencia_investimentos: 'Cinco anos investindo por conta própria.',
  obrigacoes_futuras: 'Faculdade dos filhos a partir de 2029',
  outros_patrimonios: 'Imóvel próprio e participação em empresa',
  ativos_fora_do_escopo: 'Imóveis e participações societárias',
  classes_vetadas: 'Criptoativos e derivativos',
  restricao_carencia: 'CDB com carência até 2028',
  restricao_imposto: 'Resgate antes de 720 dias eleva a alíquota.',
  restricao_marcacao: 'Venda antecipada sujeita a marcação a mercado.',
  destaques_positivos: 'PETR4 e Tesouro IPCA+ 2035',
  destaques_negativos: 'HGLG11 e Ações internacionais',
  comentario_destaques: 'Uma frase sobre o que puxou a carteira para cima.',
  comentario_detratores: 'Uma frase sobre o que puxou a carteira para baixo.',
  cenario_brasil: 'Dois ou três parágrafos sobre o cenário local.',
  resumo_brasil_atividade: 'Uma frase sobre a atividade econômica no período.',
  sintese_posicionamento: 'Duas ou três frases sobre como a carteira está posicionada.',
  tese_central: 'Uma frase com a tese que orienta o período.',
  mensagem_encerramento: 'Uma ou duas frases de fechamento.',
  chamada_final: 'Fale com o seu consultor para ajustar a carteira.',
  notas_de_rodape: 'As ressalvas numeradas que os itens acima referenciam.',
  fmt_1: 'R$', fmt_2: '%', fmt_3: 'p.p.', fmt_4: 'x',
};

// Pelo fim do nome. É o passo que resolve a maioria: o último termo diz o tipo
// do dado, e o começo diz apenas a que linha da tabela ele pertence.
const POR_FIM = {
  // dinheiro
  valor: 'R$ 128.400,00', pat: 'R$ 1.284.000,00', patrimonio: 'R$ 1.284.000,00',
  atual: 'R$ 128.400,00', aporte: 'R$ 5.000,00', saldo: 'R$ 128.400,00',
  total: 'R$ 1.284.000,00', custo: 'R$ 0,00', medio: 'R$ 9,80', cotacao: 'R$ 11,23',
  limite: 'R$ 250.000,00', caixa: 'R$ 42.000,00', ticket: 'R$ 5.000,00',
  bruto: 'R$ 12.400,00', liquido: 'R$ 10.540,00', ir: 'R$ 1.860,00',
  reais: 'R$ 5.420,00', usd: 'US$ 1.000,00', eur: 'EUR 1.000,00', moeda: 'R$ 5,42',
  // percentuais e variações
  perc: '12,4%', pct: '12,4%', meta: '35%', peso: '18%', alvo: '20%',
  ret: '+8,7%', ret12m: '+8,7%', ret24m: '+19,2%', '12m': '+8,7%', '24m': '+19,2%',
  acum: '+8,7%', proj: '+6,0%', var: '+1,2%', variacao: '+1,2%', vol: '14,2%',
  contrib: '+1,8 p.p.', delta: '+0,4 p.p.', desvio: '+4,2 p.p.', dy: '8,4%',
  anual: '0,9%', mensal: '0,075%', cdi: '10,75%', prob: '65%',
  a1: '+8,7%', a2: '+19,2%', c1: '+2,1%', c2: '+1,4%',
  fech: '135.420', ant: '133.100', hoje: '135.420', ult: '135.420',
  // datas e prazos
  mes: 'Agosto', ano: '2026', data: '31/08/2026', quando: 'Setembro',
  prazo: '2029', vencimento: '15/05/2029', periodo: 'Agosto de 2026',
  inicio: '01/09/2026', horario: '14h', dur: '3,2 anos', janela: 'D+0',
  freq: 'Trimestral', liquidez: 'D+1', seguinte: '2027',
  // instrumentos e nomes
  nome: 'Tesouro IPCA+ 2035', ativo: 'PETR4', ticker: 'ITSA4', posicao: 'PETR4',
  pos: 'PETR4', classe: 'Renda fixa', tipo: 'CDB', instrumento: 'CDB', produto: 'CDB',
  emissor: 'Banco BTG Pactual', instituicao: 'Banco BTG Pactual', banco: 'Banco BTG Pactual',
  corretora: 'BTG Pactual', contrapartida: 'Banco BTG Pactual', empresa: 'Itaúsa',
  setor: 'Financeiro', rf: 'CDB Banco BTG 2029', fii: 'HGLG11', intl: 'IVVB11',
  multi: 'Fundo multimercado', ipca: 'Tesouro IPCA+ 2035', pre: 'Tesouro Prefixado 2029',
  br: 'Ações Brasil', alt: 'Tesouro Selic 2029', novo: 'Tesouro IPCA+ 2035',
  antigo: 'CDB Banco X 2027', para: 'Tesouro IPCA+ 2035', destino: 'Tesouro IPCA+ 2035',
  oferta: 'CDB Banco BTG 2029', comp: 'CDI', qtd: '300', numero: '12', conta: '000000-0',
  taxa: 'CDI + 2,10%', indexador: 'IPCA+', rating: 'AA-', fgc: 'Sim', recuperavel: 'Sim',
  // pessoas e contato
  cliente: 'Maria Oliveira', responsavel: 'Danilo Barbosa', consultor: 'Danilo Barbosa',
  quem: 'Danilo Barbosa', papel: 'Consultor de investimentos', cargo: 'Consultor de investimentos',
  email: 'nome@auvpcapital.com.br', whatsapp: '(48) 99999-0000', contato: '(48) 99999-0000',
  canal: 'WhatsApp', endereco: 'Reunião on-line', onde: 'No app da corretora',
  // classificações
  status: 'Concluído', situacao: 'Em andamento', visao: 'Neutra', vies: 'Neutro',
  prioridade: 'Alta', gravidade: 'Média', relevancia: 'Alta', impacto: 'Baixo',
  origem: 'Corretagem', forma: 'Transferência', movimento: 'Compra', mov: 'Compra',
  op: 'Compra', acao: 'Reduzir a posição pela metade', execucao: 'Cliente',
  perfil: 'Moderado', risco: 'Moderado', horizonte: 'Longo prazo', segmento: 'Consultoria',
  jurisdicao: 'Brasil', pais: 'Estados Unidos', internacional: 'Estados Unidos',
  aprova: 'Comitê de investimentos', propoe: 'Consultor',
  // frases e títulos
  titulo: 'Rebalancear a renda variável', pauta: 'Revisão da carteira e aportes do trimestre',
  encontro: 'Reunião de acompanhamento', reuniao: 'Reunião de acompanhamento',
  entregavel: 'Carteira recomendada atualizada', entrega: 'Carteira recomendada atualizada',
  evento: 'Reunião do Copom', copom: 'Reunião do Copom', gatilho: 'Desvio acima de 5%',
  legenda: 'Alocação por classe, em % do patrimônio', finalidade: 'Acompanhamento da carteira',
  revisao: 'Revisão trimestral', proposta: 'Rebalancear a renda variável',
  diag: 'Concentração em renda variável', diagnostico: 'Concentração em renda variável',
  decisao: 'Rebalanceamento acima de 5%', resposta: 'Em até 1 dia útil',
  remarcacao: 'Com 48h de aviso', confirmacao: 'Por WhatsApp, com 48h de antecedência',
  como: 'Pelo WhatsApp, sob demanda.', funciona: 'O atendimento é pelo WhatsApp, sob demanda.',
  incluido: 'Relatório semanal de mercado', pedir: 'Uma carteira recomendada para o meu perfil',
  item: 'Um item da lista.', obs: 'Sem ressalvas.',
  objetivo: 'Aposentadoria em 20 anos', compromisso: 'Compra do imóvel',
  ouvidoria: '0800 000 0000', escritorio: 'Florianópolis, SC',
  plano: 'Me Diz o Que Fazer', apresentacao: 'Setembro de 2026',
  marco: '2016', formacao: 'Administração de Empresas', especializacao: 'Análise de Dados',
  certificacao: 'CPA-20', interesse: 'Ciclismo', registro: 'CVM 00000',
  referencia: 'Agosto de 2026', investidor: 'Moderado', analista: 'Danilo Barbosa',
  disclaimer: 'Texto aprovado pelo compliance.', assinatura: 'Danilo Barbosa',
  // texto corrido
  detalhe: 'Uma frase dizendo o que muda e por quê.',
  racional: 'Uma frase com o motivo da recomendação.',
  motivo: 'Concentração acima do limite definido no plano.',
  descricao: 'Uma frase descrevendo o item.',
  leitura: 'Uma frase sobre o que o dado significa para a carteira.',
  texto: 'Dois ou três parágrafos.', paragrafo: 'Um parágrafo.',
  bio: 'Dois ou três parágrafos em primeira pessoa.',
  nota: 'Uma frase de nota.', cons: '+0,3%',
  proposito: 'Um parágrafo sobre o seu propósito.',
  frase: 'Uma frase em primeira pessoa sobre como você trabalha.',
};

// Blocos do documento. Aparecem no começo do nome e dizem de que parte do
// relatório o campo é, o que já basta para sugerir um formato quando nenhum
// termo mais específico casa.
const POR_COMECO = {
  analise: 'Dois ou três parágrafos de análise.',
  alcada: 'Comitê de investimentos', cal: 'Reunião de acompanhamento',
  mk: '135.420', vis: 'Neutra', emis: 'Banco BTG Pactual', irv: 'PETR4',
  mov: 'Compra', seg: 'Renda fixa', remun: 'R$ 1.240,00',
  pendencia: 'Assinatura do termo', observar: 'Curva de juros longa',
  divergencia: 'Alocação fora da faixa', passo: 'Enviar a carteira recomendada',
  cadencia: 'Trimestral', prop: 'Tesouro IPCA+ 2035', desvio: '+4,2 p.p.',
  declaracao: 'Texto aprovado pelo compliance.', origem: 'Corretagem',
  plano: 'Rebalancear a renda variável', compromisso: 'Compra do imóvel',
  oferta: 'CDB Banco BTG 2029', nota: 'Uma frase de nota.',
};

/** Campo de texto corrido, pelo sufixo do nome. Espelha o critério da
 *  ferramenta, que usa o mesmo para decidir entre `input` e `textarea`. */
const CORRIDO = /(texto|analise|comentario|resumo|nota|observacao|descricao|leitura|contexto|justificativa|recomendacao|conclusao|mensagem|sintese|racional|motivo|detalhe|proposito|frase|bio)$/;

export function exemplo(nome) {
  if (POR_NOME[nome]) return POR_NOME[nome];
  const semNumero = nome.replace(/_\d+$/, '');
  const partes = semNumero.split('_').filter((p) => !/^\d+$/.test(p));
  for (let i = partes.length - 1; i >= 0; i--) {
    const p = partes[i];
    if (POR_FIM[p]) return POR_FIM[p];
    if (POR_COMECO[p]) return POR_COMECO[p];
  }
  return CORRIDO.test(semNumero) ? 'Uma ou duas frases.' : 'Um dado curto.';
}
