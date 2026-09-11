# -*- coding: utf-8 -*-
"""Carta de apresentação.

O documento que vai para o cliente depois da reunião de venda, enquanto ele
ainda não decidiu fechar. Não é a proposta — essa é a apresentação geral, que
se mostra na reunião — nem o diagnóstico, que só existe depois do sim. É o que
fica com ele no intervalo: o que entendemos do momento dele, quanto custa, como
trabalhamos, o que ele recebe e quando.

Por isso a carta repete de propósito parte do que já foi dito ao vivo. O método
em cinco etapas é o mesmo da apresentação geral, com os mesmos nomes, e o
relatório estratégico que a carta promete é o diagnóstico de carteira deste
mesmo sistema. Se um dia esses nomes mudarem num lugar, têm de mudar nos dois.

O que a carta traz e não existe em nenhum outro documento é a doutrina de
investimento da casa: as bandas da estrutura meta, as três camadas da renda
fixa e os critérios de seleção de ação, FII e ETF. Isso é texto fixo — é a
posição da casa, não do cliente —, e só as bandas entram como campo, porque
variam com o perfil.

A remuneração é o ponto em que os segmentos se separam: consultoria, alta renda
e private são fee based, com percentual sobre o patrimônio; a assessoria não
cobra taxa do cliente e é remunerada pela distribuição. São dois discursos
opostos, e cada um sai no seu modelo.
"""
from layout import *

TRATAMENTO = {"private": "Prezado(a)", "alta-renda": "Prezado(a)",
              "consultoria": "Olá,", "assessoria": "Olá,"}

PAPEL = {"consultoria": "consultor", "alta-renda": "consultor",
         "private": "banker", "assessoria": "assessor"}

# Fee based em três segmentos, remuneração por distribuição na assessoria.
FEE_BASED = ("consultoria", "alta-renda", "private")

# A sexta etapa do relacionamento. As cinco primeiras são as mesmas da
# apresentação geral; esta é o que cada segmento faz de diferente, e sai do
# terceiro pilar que a apresentação já promete ao cliente.
ETAPA_6 = {
    "consultoria": ("Prestação de contas",
                    "Relatório mensal e reunião trimestral em que cada decisão da carteira "
                    "é explicada e registrada."),
    "alta-renda": ("Acesso e eficiência tributária",
                   "Ofertas restritas avaliadas à luz da sua carteira, e escolha de veículos "
                   "e prazos considerando come-cotas, isenções e compensação."),
    "private": ("Wealth planning e governança",
                "Holdings, seguros, doação e testamento mapeados com assessoria jurídica e "
                "tributária, e a governança da família escrita."),
    "assessoria": ("Transparência de remuneração",
                   "Todo mês, junto do relatório, quanto a casa recebeu pelos produtos que "
                   "estão na sua carteira."),
}

# A etapa do roadmap que muda com o segmento, entre o primeiro e o segundo mês.
ROADMAP_SEG = {
    "consultoria": ("Plano de aportes e reserva", "1º mês",
                    "Definição do valor e da periodicidade dos aportes, e do tamanho da reserva "
                    "de emergência antes de qualquer alocação de risco."),
    "alta-renda": ("Ofertas e eficiência tributária", "2º mês",
                   "Avaliação das ofertas restritas do período e dos veículos mais eficientes "
                   "para o seu nível de patrimônio."),
    "private": ("Wealth planning, tributário e sucessório", "2º mês",
                "Reunião com advogado tributarista para mapear holding, doação, testamento, "
                "previdência e governança familiar."),
    "assessoria": ("Transparência de custos e remuneração", "1º mês",
                   "Abertura de quanto cada produto da carteira remunera a casa, e o que isso "
                   "representa sobre o patrimônio."),
}

# As seis classes da estrutura meta. A função de cada uma é posição da casa; as
# bandas variam com o perfil, e por isso entram como campo.
BANDAS = [
    ("Renda fixa", "rf", "Preservação, renda e liquidez"),
    ("Internacional — renda fixa", "irf", "Diversificação cambial e renda em moeda forte"),
    ("Internacional — renda variável", "irv", "Crescimento global"),
    ("Ações", "acoes", "Crescimento patrimonial de longo prazo"),
    ("Fundos imobiliários", "fii", "Renda recorrente isenta"),
    ("Alternativos", "alt", "Diversificação fora das classes tradicionais"),
]

PILARES = [
    ("KYC e suitability aprofundados",
     "Vai além da tolerância a risco: objetivos de vida, estrutura familiar, horizonte de "
     "usufruto, obrigações futuras e o legado desejado."),
    ("Diagnóstico do portfólio",
     "Cinco dimensões: concentração de risco, descasamento de prazo e liquidez, custos "
     "desnecessários, ineficiência tributária e desalinhamento ao perfil."),
    ("Construção da estratégia meta",
     "Alocação com racional fundamentado, classe a classe. Disciplina e horizonte longo como "
     "base, sem movimento especulativo."),
    ("Monitoramento e evolução",
     "Acompanhamento %(cad)s da carteira, revisão da estratégia meta, relatório mensal de "
     "resultado e relatório macroeconômico para contextualizar cada decisão."),
]

RELACIONAMENTO = [
    ("Diagnóstico",
     "Mapeamento do patrimônio atual: ativos, passivos, fluxo, concentrações, exposições e "
     "aderência ao perfil de risco."),
    ("Proposta",
     "Alocação personalizada com racional claro para cada classe, projeções e cenários."),
    ("Transição",
     "Execução gradual, respeitando carências, vencimentos, eficiência fiscal e o momento de "
     "mercado."),
    ("Acompanhamento",
     "Carteira acompanhada de perto, com reuniões periódicas, relatório mensal e ajustes "
     "táticos quando fizerem falta."),
    ("Revisão",
     "Fechamento de ciclo: desempenho do período, revisão de metas e agenda do período "
     "seguinte."),
]

# As três camadas da renda fixa. Doutrina da casa, igual em todos os segmentos.
RENDA_FIXA = [
    ("Objetivo",
     "Liquidez, previsibilidade e reserva de oportunidade.",
     "Proteção do poder de compra e crescimento real no longo prazo.",
     "Captura do prêmio de juros nominais, com retorno previsível até o vencimento."),
    ("Horizonte",
     "Carrego até 2 anos.",
     "Carrego a partir de 4 anos; marcação a mercado a partir de 10 anos.",
     "Carrego até 3 anos."),
    ("Estrutura",
     "Metade em liquidez imediata (D+0 e D+1) e metade em crédito bancário e privado com "
     "vencimento em até 2 anos.",
     "Metade em carrego via crédito bancário e ETFs, com crédito privado limitado a um terço "
     "da parcela; o restante em Tesouro IPCA+ para duration.",
     "Metade em crédito bancário, um quarto em crédito privado e ETFs e um quarto em títulos "
     "soberanos."),
    ("Critérios",
     "Qualidade do emissor, liquidez D+0 ou D+1, cobertura do FGC, taxa contra o CDI e prazo "
     "compatível com o uso do dinheiro.",
     "Taxa real contra o histórico, prazo compatível, qualidade do emissor e cobertura do FGC.",
     "Taxa nominal contra o contexto macro, prazo, qualidade do emissor e liquidez no "
     "secundário."),
]

RENDA_VARIAVEL = [
    ("Objetivo",
     "Renda imobiliária mensal isenta para pessoa física, com liquidez de bolsa e "
     "diversificação setorial.",
     "Crescimento patrimonial de longo prazo, via participação no lucro das empresas e "
     "exposição a ativos reais.",
     "Diversificação cambial, liquidez em moeda forte e eficiência no planejamento "
     "sucessório."),
    ("Estratégia",
     "Prioridade para logística e shoppings, com inquilinos sólidos, contratos consistentes e "
     "capacidade de repassar inflação.",
     "Seleção por fundamento, governança, valuation e vantagem competitiva durável, com "
     "aporte concentrado nos ativos mais descontados.",
     "ETFs passivos em core-satellite, combinados com money market e bonds de grau elevado."),
    ("Riscos monitorados",
     "Vacância, inadimplência, sensibilidade à taxa de juros e risco de gestão.",
     "Concentração setorial, ciclicidade, endividamento e deterioração de fundamento.",
     "Risco cambial, duration, risco de crédito nos bonds e tracking difference dos ETFs."),
    ("Critérios",
     "Múltiplos imóveis e inquilinos, qualidade dos ativos, solidez do gestor, valuation e "
     "liquidez em bolsa.",
     "Lucro recorrente, endividamento controlado, vantagem competitiva, setor perene e "
     "descorrelação real.",
     "Money market com rating alto e liquidez D+1, sem high yield; ETFs com duration moderada, "
     "patrimônio suficiente e tracking difference baixo."),
]

CLASSES = [
    ("Renda fixa", "Proteção, renda e liquidez",
     "Pós-fixados, IPCA+ e prefixados, de olho no FGC, no risco de crédito e nas "
     "oportunidades de marcação a mercado."),
    ("Ações", "Crescimento no longo prazo",
     "Seleção por fundamento, governança, valuation e vantagem competitiva durável."),
    ("Fundos imobiliários", "Renda recorrente e diversificação real",
     "Logística e shoppings, com inquilinos sólidos e contratos que repassam inflação."),
    ("Internacional", "Diversificação global e proteção cambial",
     "ETFs passivos em core-satellite, reduzindo a concentração em um único mercado."),
    ("Caixa e liquidez", "Flexibilidade e oportunidade tática",
     "Reserva calibrada pela sua necessidade de liquidez e pelo aproveitamento de "
     "oportunidades."),
]

ENTREGAS = [
    "Análise da carteira atual e da sua aderência ao perfil de risco declarado",
    "Diagnóstico de concentrações, ineficiências e oportunidades de melhoria",
    "Proposta de alocação personalizada, com racional claro para cada classe",
    "Projeções patrimoniais no seu contexto, considerando aportes e cenários",
    "Estratégia de implementação gradual, respeitando timing de mercado e eficiência fiscal",
    "Próximos passos e cronograma de ação",
]

ANTECIPA = [
    "A estrutura do nosso relacionamento",
    "A metodologia que nos guia",
    "O cronograma de trabalho dos próximos encontros",
    "A estrutura de alocação que orienta as carteiras da casa",
    "O que você recebe em cada etapa desta jornada",
]


def _remuneracao(t, seg):
    """A página de remuneração. É a primeira coisa depois da carta de abertura,
    e não a última, porque quem ainda não decidiu quer saber o preço antes de
    ouvir o método."""
    if seg in FEE_BASED:
        return """<span class="eyebrow">Remuneração</span>
<h1 class="t">Fee based, e só</h1>
<div class="center"><div class="cols2u" style="align-items:center">
  <div>
    <div class="big">%(taxa)s</div>
    <p class="lead" style="margin-top:4mm">ao ano, para o seu cenário e o seu nível de
    complexidade patrimonial. Cobrada mensalmente de forma proporcional ao patrimônio sob
    orientação e debitada na sua conta de investimentos.</p>
    <div class="note"><p><strong>Antes do método, o preço.</strong> Você precisa conhecer os
    termos da nossa remuneração antes de avaliar qualquer benefício do modelo. %(nota)s</p></div>
  </div>
  <div>%(cards)s</div>
</div></div>""" % dict(
            taxa=ph("taxa_anual", "Ex.: 0,9% ao ano"),
            cards=cards([
                ("Percentual fixo sobre o patrimônio",
                 "Cobrado mensalmente, de forma proporcional ao que está sob orientação."),
                ("Única forma de remuneração",
                 "Sem comissão, rebate ou incentivo vinculado a produto financeiro."),
                ("Alinhamento de interesses",
                 "Se o melhor produto para você paga menos à casa, ele entra do mesmo jeito.")],
                n=1),
            nota=ph("nota_taxas", "Base de cálculo, cobrança, impostos e condições"))

    return """<span class="eyebrow">Remuneração</span>
<h1 class="t">Você não paga taxa de assessoria</h1>
<div class="center"><div class="cols2u" style="align-items:center">
  <div>
    <div class="big">R$ 0,00</div>
    <p class="lead" style="margin-top:4mm">é o que você paga de taxa. Não há mensalidade nem
    percentual cobrado de você: a casa é remunerada pela distribuição dos produtos que ficam na
    sua carteira, e você passa a receber, todo mês, quanto isso representou.</p>
    <div class="note"><p><strong>Antes do método, o preço.</strong> Preferimos abrir como a casa
    ganha dinheiro antes de falar do que ela faz. %(nota)s</p></div>
  </div>
  <div>%(cards)s</div>
</div></div>""" % dict(
        cards=cards([
            ("Custo direto para você", "R$ 0,00. Não há taxa de assessoria."),
            ("Como a casa é remunerada",
             "Pela distribuição dos produtos da carteira, informada abertamente."),
            ("O que você recebe todo mês",
             "O quadro de remuneração no relatório mensal: produto a produto, quanto a casa "
             "recebeu e quanto isso é do seu patrimônio.")], n=1),
        nota=ph("nota_remuneracao", "Como o quadro de remuneração deve ser lido"))


def _beneficios(t, seg):
    if seg in FEE_BASED:
        texto = ("O modelo fee based permite uma atuação transparente, independente e alinhada "
                 "aos seus objetivos. A casa não depende de comissão, rebate ou incentivo "
                 "vinculado a produto, então a recomendação é feita por critério técnico. Esse "
                 "alinhamento é estrutural: o nosso único interesse é a evolução do seu "
                 "patrimônio.")
        segundo = ("O formato reduz conflito de interesse, elimina o incentivo à indicação "
                   "inadequada e à movimentação desnecessária da carteira, e deixa claro quanto "
                   "custa o serviço e quanto custam os produtos.")
    else:
        texto = ("Você não paga taxa, e mesmo assim sabe exatamente quanto a casa ganha com a "
                 "sua carteira. A remuneração vem da distribuição, vai aberta no relatório "
                 "mensal e é a única coisa que a casa recebe pelo seu dinheiro.")
        segundo = ("Abrir o número muda o incentivo: uma recomendação que remunera mais precisa "
                   "se justificar tecnicamente diante de você, com o número na mesa, e não "
                   "apenas internamente.")
    return """<span class="eyebrow">Modelo de atuação</span>
<h1 class="t">O nosso único interesse é a evolução do seu patrimônio</h1>
<div class="center"><div class="cols2u" style="align-items:start">
  <div>
    <p class="lead">%(t1)s</p>
    <p>%(t2)s</p>
  </div>
  <div>
    <h2 style="margin-top:0">Vantagens estruturais</h2>
    <ul class="lista">
      <li>Cashback de rebate, reduzindo o custo embutido nos produtos</li>
      <li>Spreads menores nas operações, com ganho de eficiência a cada movimentação</li>
      <li>Alocação executada por nós e aceita por você no aplicativo, o que dá fluidez aos aportes</li>
      <li>Equipe técnica próxima, com resposta rápida e aporte tático quando a janela aparece</li>
    </ul>
  </div>
</div></div>""" % dict(t1=texto, t2=segundo)


def build(t, seg):
    set_date_ph("data_carta")
    papel = PAPEL[seg]
    S = []

    # --------------------------------------------------------------- capa
    S.append(cover_slide(
        t, "Carta de", "Apresentação",
        ph("subtitulo_carta", "Ex.: o que conversamos e o que vem a seguir"),
        [ph("nome_cliente"), "Elaborada por " + ph("nome_responsavel"), ph("data_carta")]))

    # ------------------------------------------------------- carta de abertura
    S.append(slide(t, "Síntese", 2, """<span class="eyebrow">Síntese estratégica</span>
<h1 class="t">O que entendemos até aqui</h1>
<div class="cols2u" style="flex:1 1 auto;align-items:center">
  <div>
    <p class="lead">%(trat)s %(cli)s,</p>
    <p>Foi um prazer a nossa primeira conversa, em %(data)s. É o começo de uma jornada
    estruturada, que existe para que o seu patrimônio não seja apenas cuidado, mas construído e
    preservado ao longo do tempo.</p>
    <p>Dessa conversa, passamos a entender o seu momento: %(momento)s. E ficou claro que o seu
    principal objetivo patrimonial hoje é %(objetivo)s.</p>
    <p>A condução da estratégia fica com o %(papel)s %(resp)s, com o apoio da equipe técnica
    da %(marca)s.</p>
  </div>
  <div>
    <h2 style="margin-top:0">O que este documento antecipa</h2>
    <ul class="lista">%(toc)s</ul>
  </div>
</div>
<div class="note" style="margin-top:auto"><p>%(frase)s</p></div>""" % dict(
        trat=TRATAMENTO[seg], cli=ph("nome_cliente"), data=ph("data_primeira_reuniao"),
        momento=ph("momento_do_cliente", "Ex.: transição de carreira, com liquidez recente"),
        objetivo=ph("objetivo_principal"), papel=papel, resp=ph("nome_responsavel"),
        marca=t["marca"],
        frase=ph("frase_de_abertura",
                 "Ex.: patrimônio construído ao longo de uma vida deve ter caráter perpétuo."),
        toc="".join("<li>%s</li>" % n for n in ANTECIPA))))

    # -------------------------------------------------------------- remuneração
    S.append(slide(t, "Remuneração", 3, _remuneracao(t, seg), dark=True))

    # ------------------------------------------------------- o relacionamento
    etapas = RELACIONAMENTO + [ETAPA_6[seg]]
    S.append(slide(t, "Relacionamento", 4, """<span class="eyebrow">Visão estratégica</span>
<h1 class="t">Como o relacionamento se estrutura</h1>
<div class="center"><ol class="steps" style="--n:3">%(st)s</ol></div>""" % dict(
        st="".join("<li><h4>%s</h4><p>%s</p></li>" % (a, b) for a, b in etapas))))

    # ------------------------------------------------------------- metodologia
    S.append(slide(t, "Metodologia", 5, """<span class="eyebrow">Metodologia</span>
<h1 class="t">Os pilares que sustentam cada decisão</h1>
<p class="lead">Investir bem é mais do que escolher bons ativos: é ter uma filosofia
consistente, que guie a decisão independentemente do momento de mercado. É ela que nos mantém
disciplinados quando o mercado oscila e atentos quando a oportunidade aparece.</p>
<div class="center">%(cards)s</div>""" % dict(
        cards=cards([(a, b % dict(cad=t["cadencia"]) if "%(cad)s" in b else b)
                     for a, b in PILARES], n=2))))

    # ----------------------------------------------------------------- roadmap
    extra = ROADMAP_SEG[seg]
    linhas = [
        ("KYC, suitability e diagnóstico", "Dia 1",
         "Coleta objetiva e subjetiva: perfil de risco, objetivos de vida, horizonte, liquidez "
         "necessária, estrutura familiar e histórico patrimonial."),
        ("Entrega da proposta estratégica", "Até 10 dias",
         "Diagnóstico e proposta inicial de alocação, com o racional completo da carteira, "
         "projeções e próximos passos."),
        ("Seguros e proteção patrimonial", "1º mês",
         "Necessidade de proteção: vida, sucessório, responsabilidade civil e demais coberturas "
         "relevantes ao patrimônio da família."),
        ("Alinhamento operacional", "1º mês",
         "Revisão dos primeiros movimentos, cronograma de execução e validação da alocação "
         "prática contra a proposta aprovada."),
        extra,
        ("Revisão de carteira e aderência à estratégia", t["cadencia"].capitalize(),
         "Acompanhamento da carteira implementada, avaliando aderência à estratégia meta e "
         "eventuais ajustes."),
        ("Crédito, liquidez e eficiência de caixa", "3º mês",
         "Linhas de crédito, financiamento patrimonial, gestão de caixa e uso eficiente do "
         "balanço pessoal e familiar."),
        ("Consolidação patrimonial", "4º mês",
         "Visão integrada: bancos, empresas, imóveis, sucessores, responsabilidades e processo "
         "de decisão."),
        ("Revisão anual e próximo ciclo", "12º mês",
         "Fechamento do ciclo: desempenho do ano, revisão de metas, planejamento tributário de "
         "fim de ano e agenda do período seguinte."),
    ]
    S.append(slide(t, "Cronograma", 6, """<span class="eyebrow">Roadmap inicial</span>
<h1 class="t">O primeiro ano, encontro a encontro</h1>
%(tab)s
<div class="note" style="margin-top:auto"><p><strong>Depois do primeiro ano.</strong> O
calendário do ciclo de acompanhamento, com pauta e entregável de cada encontro, está no
cronograma de reuniões.</p></div>""" % dict(
        tab=table(["Etapa", "Prazo", "Objetivo estratégico"],
                  [[n, q, d] for n, q, d in linhas], sm=True,
                  widths=[26, 12, 62]))))

    # --------------------------------------------------- o que vem a seguir
    S.append(slide(t, "Próximos passos", 7, """<span class="eyebrow">O que esperar</span>
<h1 class="t">Em até 10 dias, o seu relatório estratégico</h1>
<div class="center"><div class="cols2u" style="align-items:start">
  <div>
    <p class="lead">Depois da reunião de KYC, suitability e diagnóstico patrimonial, você recebe
    o relatório estratégico de proposta de investimentos: um documento técnico, completo e
    construído para o seu patrimônio.</p>
    <p>É a espinha dorsal do relacionamento. Um mapa feito para o seu momento de vida e os seus
    objetivos, que serve de referência para toda decisão que vier depois.</p>
  </div>
  <div>
    <h2 style="margin-top:0">O que ele traz</h2>
    <ul class="lista">%(itens)s</ul>
  </div>
</div></div>""" % dict(itens="".join("<li>%s</li>" % i for i in ENTREGAS))))

    # ---------------------------------------------------- estrutura de alocação
    S.append(slide(t, "Alocação", 8, """<span class="eyebrow">Visão macro</span>
<h1 class="t">A função de cada classe no portfólio</h1>
<p class="lead">A proposta se estrutura em grandes classes, cada uma com função definida, sem se
limitar a elas quando o seu perfil e os seus objetivos pedirem outra coisa. A combinação entre
elas é que busca o equilíbrio entre preservação, renda e crescimento.</p>
<div class="center">%(tab)s</div>""" % dict(
        tab=table(["Classe", "Função", "Como trabalhamos"],
                  [[n, f, c] for n, f, c in CLASSES], sm=True, widths=[18, 24, 58]))))

    # ------------------------------------------------------------ estrutura meta
    S.append(slide(t, "Alocação", 9, """<span class="eyebrow">Prévia da implementação</span>
<h1 class="t">As bandas da estrutura meta</h1>
<p class="lead">Cada classe trabalha dentro de uma banda, e não de um número fixo: é o que
permite acomodar o momento de mercado sem sair da estratégia. As bandas abaixo são as do seu
perfil %(perf)s.</p>
%(tab)s
<p class="legal" style="margin-top:auto">Este material não constitui promessa de rentabilidade
nem carteira definitiva. A alocação final depende da análise completa do seu perfil, objetivos,
restrições e suitability.</p>""" % dict(
        perf=ph("perfil_investidor"),
        tab=table(["Classe", "Mínimo", "Máximo", "Função no portfólio"],
                  [[n, ph("banda_%s_min" % k), ph("banda_%s_max" % k), f]
                   for n, k, f in BANDAS],
                  nums=[1, 2], sm=True, widths=[26, 12, 12, 50]))))

    # -------------------------------------------------------- doutrina: RF e RV
    S.append(slide(t, "Estratégia", 10, """<span class="eyebrow">Renda fixa</span>
<h1 class="t">A carteira de renda fixa em três camadas</h1>
<p class="lead">A renda fixa é a espinha dorsal do portfólio: Tesouro como base soberana,
crédito bancário para prêmio com risco mitigado pelo FGC e crédito privado para spreads
maiores, com análise rigorosa. Em todos os casos, o ativo só é escolhido depois de definido o
papel daquela parcela na carteira.</p>
<div class="center">%(tab)s</div>""" % dict(
        tab=table(["", "Pós-fixado (CDI e Selic)", "Inflação (IPCA+)", "Prefixado"],
                  [["<strong>%s</strong>" % l[0], l[1], l[2], l[3]] for l in RENDA_FIXA],
                  sm=True, widths=[13, 29, 29, 29]))))

    S.append(slide(t, "Estratégia", 11, """<span class="eyebrow">Renda variável</span>
<h1 class="t">Ações, fundos imobiliários e internacional</h1>
<p class="lead">As três classes têm papéis diferentes — renda, crescimento e proteção cambial —
e por isso são selecionadas por critérios diferentes. O que elas têm em comum é a exigência de
fundamento: nenhuma posição entra por movimento de preço.</p>
<div class="center">%(tab)s</div>""" % dict(
        tab=table(["", "Fundos imobiliários", "Ações", "Internacional"],
                  [["<strong>%s</strong>" % l[0], l[1], l[2], l[3]] for l in RENDA_VARIAVEL],
                  sm=True, widths=[16, 28, 28, 28]))))

    # ------------------------------------------------------- modelo e vantagens
    S.append(slide(t, "Modelo de atuação", 12, _beneficios(t, seg)))

    # ------------------------------------------------------------- compromisso
    S.append(slide(t, "Compromisso", 13, """<div style="display:flex;gap:16mm;flex:1 1 auto;align-items:center">
  <div style="flex:1 1 auto">
    <span class="eyebrow">Nosso compromisso</span>
    <h1 class="t">O nosso trabalho começa agora</h1>
    <p class="lead" style="margin-top:4mm">%(trat)s %(cli)s, entendemos que a confiança
    depositada aqui vai além de uma relação comercial: é confiança sobre o que representa anos
    de dedicação e construção.</p>
    <p>O nosso papel é ser o parceiro estratégico que você não precisa gerenciar — o que cuida
    com rigor, comunica com clareza e age com integridade. Você fica com mais espaço para o que
    importa, com a certeza de que o seu patrimônio está sendo tratado com o mesmo cuidado com
    que foi construído.</p>
    <div class="dl" style="margin-top:6mm">
      <dt>%(papelc)s</dt><dd>%(resp)s</dd>
      <dt>WhatsApp</dt><dd>%(whats)s</dd>
      <dt>E-mail</dt><dd>%(email)s</dd>
    </div>
  </div>
  <div style="display:flex;flex-direction:column;align-items:center;gap:4mm">
    <div class="qr">QR code<br>agendamento</div>
    <div class="small mut" style="text-align:center;max-width:52mm">%(link)s</div>
  </div>
</div>""" % dict(
        trat=TRATAMENTO[seg], cli=ph("nome_cliente"), papelc=papel.capitalize(),
        resp=ph("nome_responsavel"), whats=ph("whatsapp_contato"), email=ph("email_contato"),
        link=ph("link_agendamento")), dark=True))

    return S
