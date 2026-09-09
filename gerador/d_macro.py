# -*- coding: utf-8 -*-
from layout import *

LEITURA = {
    "consultoria": "O que este cenário significa para uma carteira diversificada de perfil moderado.",
    "alta-renda": "O que este cenário significa para carteiras com acesso a produtos estruturados e exclusivos.",
    "private": "O que este cenário significa para patrimônios com exposição internacional, estruturas e horizonte multigeracional.",
    "assessoria": "O que este cenário significa para uma carteira montada na plataforma, com foco em renda fixa e nos produtos disponíveis para distribuição.",
}


def build(t, seg):
    set_date_ph("mes_referencia")
    P = []

    P.append(cover_a4(t, "Relatório", "Macroeconômico", "Cenário", "e Mercados",
                      [x for x in [t["rotulo"], "Elaborado por " + ph("nome_analista"),
                       ph("registro_analista"), ph("mes_referencia")] if x], grafismo=2))

    P.append(page_a4(t, "Resumo executivo", 2, """<span class="eyebrow">%(mes)s em uma página</span>
<h1 class="t">Resumo executivo</h1>
<p class="lead">%(tese)s</p>
<h2>Os cinco fatos do mês</h2>
<ol class="tl" style="grid-template-columns:1fr">
  <li><h4>%(f1t)s</h4><p>%(f1d)s</p></li>
  <li><h4>%(f2t)s</h4><p>%(f2d)s</p></li>
  <li><h4>%(f3t)s</h4><p>%(f3d)s</p></li>
  <li><h4>%(f4t)s</h4><p>%(f4d)s</p></li>
  <li><h4>%(f5t)s</h4><p>%(f5d)s</p></li>
</ol>
<h2>Onde mudamos de opinião</h2>
<div class="note"><p>%(mudanca)s</p></div>
<h2>Neste relatório</h2>
<ol class="toc">%(toc)s</ol>""" % dict(
        mes=ph("mes_referencia"), tese=ph("tese_central", "A leitura do mês em 2-3 frases"),
        **{("f%dt" % i): ph("fato_%d_titulo" % i) for i in range(1, 6)},
        **{("f%dd" % i): ph("fato_%d_detalhe" % i) for i in range(1, 6)},
        mudanca=ph("mudanca_de_visao"),
        toc="".join('<li><span class="n">%02d</span><span>%s</span><span class="d"></span><span class="p">%02d</span></li>'
                    % (i, n, pg) for i, (n, pg) in enumerate([
                        ("Cenário internacional", 3), ("Brasil: atividade e inflação", 4),
                        ("Brasil: juros, fiscal e câmbio", 5), ("Mercados no período", 6),
                        ("Projeções", 7), ("Implicações para a carteira", 8),
                        ("Agenda do próximo mês", 9), ("Notas e avisos", 10)], start=1)))))

    P.append(page_a4(t, "Internacional", 3, """<span class="eyebrow">Global</span>
<h1 class="t">Cenário internacional</h1>
<p class="lead">%(res)s</p>
<h2>Estados Unidos</h2>
<p class="small">%(eua)s</p>
<h2>Europa</h2>
<p class="small">%(eur)s</p>
<h2>China e Ásia</h2>
<p class="small">%(chi)s</p>
<h2>Indicadores acompanhados</h2>
%(tab)s
<div class="gap"></div>
%(ch)s""" % dict(
        res=ph("resumo_internacional"), eua=ph("analise_eua"), eur=ph("analise_europa"), chi=ph("analise_china"),
        tab=table(["Indicador", "Último dado", "Anterior", "Consenso", "Leitura"],
                  [[n, ph("gi_%s_atual" % k), ph("gi_%s_ant" % k), ph("gi_%s_cons" % k), ph("gi_%s_leitura" % k)]
                   for n, k in [("Fed funds", "fed"), ("CPI EUA (a/a)", "cpi"), ("Payroll", "payroll"),
                                ("Treasury 10 anos", "ust10"), ("BCE &mdash; taxa de depósito", "bce"),
                                ("PIB China (a/a)", "pibchina"), ("Petróleo Brent", "brent"),
                                ("Índice DXY", "dxy")]],
                  nums=[1, 2, 3]),
        ch=chart("Juros longos e dólar", "Treasury de 10 anos e índice DXY nos últimos 12 meses.", "line", "min-height:40mm"))))

    P.append(page_a4(t, "Brasil", 4, """<span class="eyebrow">Brasil</span>
<h1 class="t">Atividade e inflação</h1>
<p class="lead">%(res)s</p>
<h2>Atividade</h2>
<p class="small">%(ativ)s</p>
<h2>Mercado de trabalho e renda</h2>
<p class="small">%(trab)s</p>
<h2>Inflação</h2>
<p class="small">%(infl)s</p>
%(tab)s
<div class="gap"></div>
%(ch)s""" % dict(
        res=ph("resumo_brasil_atividade"), ativ=ph("analise_atividade"), trab=ph("analise_trabalho"),
        infl=ph("analise_inflacao"),
        tab=table(["Indicador", "No mês", "12 meses", "Projeção fim do ano", "Meta / referência"],
                  [[n, ph("bi_%s_mes" % k), ph("bi_%s_12m" % k), ph("bi_%s_proj" % k), ph("bi_%s_meta" % k)]
                   for n, k in [("IPCA", "ipca"), ("IPCA núcleo", "nucleo"), ("IGP-M", "igpm"),
                                ("PIB", "pib"), ("Desemprego (PNAD)", "desemp"), ("Massa salarial real", "massa")]],
                  nums=[1, 2, 3]),
        ch=chart("IPCA cheio e núcleos", "IPCA acumulado em 12 meses contra a banda da meta e a média dos núcleos.", "line", "min-height:38mm"))))

    P.append(page_a4(t, "Brasil", 5, """<span class="eyebrow">Brasil</span>
<h1 class="t">Juros, fiscal e câmbio</h1>
<h2>Política monetária</h2>
<p class="small">%(cop)s</p>
<div class="cols2">
  <div><h3>Última decisão do Copom</h3>
    <div class="dl">
      <dt>Selic</dt><dd>%(selic)s</dd>
      <dt>Decisão</dt><dd>%(dec)s</dd>
      <dt>Placar</dt><dd>%(placar)s</dd>
      <dt>Próxima reunião</dt><dd>%(prox)s</dd>
    </div>
  </div>
  <div><h3>Curva de juros</h3><p class="small mut">%(curva)s</p></div>
</div>
<h2>Contas públicas</h2>
<p class="small">%(fisc)s</p>
%(tab)s
<h2>Câmbio e contas externas</h2>
<p class="small">%(cambio)s</p>
<div class="gap"></div>
%(ch)s""" % dict(
        cop=ph("analise_politica_monetaria"), selic=ph("selic_atual"), dec=ph("decisao_copom"),
        placar=ph("placar_copom"), prox=ph("data_proximo_copom"), curva=ph("analise_curva_juros"),
        fisc=ph("analise_fiscal"), cambio=ph("analise_cambio"),
        tab=table(["Indicador", "Último", "12 meses", "Projeção"],
                  [[n, ph("fi_%s_ult" % k), ph("fi_%s_12m" % k), ph("fi_%s_proj" % k)]
                   for n, k in [("Resultado primário (% PIB)", "primario"),
                                ("Dívida bruta (% PIB)", "dbgg"),
                                ("Câmbio (R$/US$)", "cambio"),
                                ("Conta corrente (% PIB)", "cc")]], nums=[1, 2, 3]),
        ch=chart("Curva de juros DI", "Curva atual contra a de um mês atrás e a de um ano atrás.", "line", "min-height:36mm"))))

    P.append(page_a4(t, "Mercados", 6, """<span class="eyebrow">Desempenho</span>
<h1 class="t">Mercados no período</h1>
<p class="lead">Retorno das principais classes e índices em %(mes)s, no ano e em 12 meses.</p>
%(tab)s
<div class="gap"></div>
<div class="cols2">
  <div><h2>Destaques positivos</h2><p class="small mut">%(pos)s</p></div>
  <div><h2>Destaques negativos</h2><p class="small mut">%(neg)s</p></div>
</div>
%(ch)s""" % dict(
        mes=ph("mes_referencia"), pos=ph("destaques_positivos"), neg=ph("destaques_negativos"),
        tab=table(["Classe / índice", "No mês", "No ano", "12 meses", "24 meses", "Volatilidade 12m"],
                  [[n, ph("mk_%s_mes" % k), ph("mk_%s_ano" % k), ph("mk_%s_12m" % k),
                    ph("mk_%s_24m" % k), ph("mk_%s_vol" % k)]
                   for n, k in [("CDI", "cdi"), ("IMA-B (inflação)", "imab"), ("IRF-M (prefixado)", "irfm"),
                                ("Ibovespa", "ibov"), ("Small Caps", "small"), ("IFIX", "ifix"),
                                ("S&amp;P 500 (US$)", "spx"), ("Nasdaq (US$)", "ndx"),
                                ("MSCI Emergentes", "msciem"), ("Dólar (PTAX)", "usd"),
                                ("Ouro (US$)", "gold"), ("Bitcoin (US$)", "btc")]],
                  nums=[1, 2, 3, 4, 5],
                  caption="Retornos nominais em moeda local, salvo indicação em contrário. Fonte: " + ph("fonte_dados_mercado")),
        ch=chart("Retorno das classes no mês", "Barras comparando o retorno de cada classe no período.", "bars", "min-height:34mm"))))

    P.append(page_a4(t, "Projeções", 7, """<span class="eyebrow">Expectativas</span>
<h1 class="t">Projeções</h1>
<p class="lead">Nossas projeções e a mediana do mercado. Onde divergimos, explicamos por quê.</p>
<h2>Brasil</h2>
%(tab)s
<h2>Internacional</h2>
%(tab2)s
<h2>Onde divergimos do consenso</h2>
%(cards)s""" % dict(
        tab=table(["Indicador", "%s" % ph("ano_corrente"), "%s" % ph("ano_seguinte"),
                   "Consenso " + ph("ano_corrente"), "Consenso " + ph("ano_seguinte")],
                  [[n, ph("pj_%s_a1" % k), ph("pj_%s_a2" % k), ph("pj_%s_c1" % k), ph("pj_%s_c2" % k)]
                   for n, k in [("IPCA (%)", "ipca"), ("Selic fim de período (%)", "selic"),
                                ("PIB (%)", "pib"), ("Câmbio (R$/US$)", "cambio"),
                                ("Resultado primário (% PIB)", "primario")]], nums=[1, 2, 3, 4]),
        tab2=table(["Indicador", ph("ano_corrente"), ph("ano_seguinte"), "Viés"],
                   [[n, ph("pg_%s_a1" % k), ph("pg_%s_a2" % k), ph("pg_%s_vies" % k)]
                    for n, k in [("Fed funds (%)", "fed"), ("CPI EUA (%)", "cpi"),
                                 ("PIB EUA (%)", "pibeua"), ("PIB China (%)", "pibchina")]], nums=[1, 2]),
        cards=cards([(ph("divergencia_%d_titulo" % i), ph("divergencia_%d_racional" % i)) for i in (1, 2, 3)]))))

    P.append(page_a4(t, "Implicações", 8, """<span class="eyebrow">%(nome)s</span>
<h1 class="t">Implicações para a carteira</h1>
<p class="lead">%(leitura)s</p>
<h2>Posicionamento por classe</h2>
%(tab)s
<h2>Riscos que monitoramos</h2>
%(tab2)s
<div class="gap"></div>
<div class="note"><p><strong>Em uma frase.</strong> %(frase)s</p></div>""" % dict(
        nome=t["nome"], leitura=LEITURA[seg],
        tab=table(["Classe", "Visão", "Variação x mês anterior", "Racional", "Como implementar"],
                  [[c, '<span class="pill">' + ph("vis_%s_visao" % k) + "</span>",
                    ph("vis_%s_delta" % k), ph("vis_%s_racional" % k), ph("vis_%s_como" % k)]
                   for c, k in [("Renda fixa pós", "rfpos"), ("Renda fixa inflação", "rfipca"),
                                ("Renda fixa prefixada", "rfpre"), ("Multimercado", "multi"),
                                ("Renda variável BR", "rvbr"), ("Internacional", "intl"),
                                ("Fundos imobiliários", "fii"), ("Alternativos", "alt")]]),
        tab2=table(["Risco", "Probabilidade", "Impacto", "Sinal de alerta", "O que faríamos"],
                   [[ph("risco_%d_nome" % i), '<span class="pill">' + ph("risco_%d_prob" % i) + "</span>",
                     '<span class="pill">' + ph("risco_%d_impacto" % i) + "</span>",
                     ph("risco_%d_gatilho" % i), ph("risco_%d_acao" % i)] for i in (1, 2, 3)]),
        frase=ph("sintese_posicionamento"))))

    P.append(page_a4(t, "Agenda", 9, """<span class="eyebrow">O que vem por aí</span>
<h1 class="t">Agenda de %(prox)s</h1>
<p class="lead">Datas e eventos que podem mover os mercados no próximo período.</p>
<h2>Calendário</h2>
%(tab)s
<h2>O que estaremos observando</h2>
%(cards)s""" % dict(
        prox=ph("mes_seguinte"),
        tab=table(["Data", "Evento / indicador", "País", "Relevância", "Por que importa"],
                  [[ph("ag_%d_data" % i), ph("ag_%d_evento" % i), ph("ag_%d_pais" % i),
                    '<span class="pill">' + ph("ag_%d_relevancia" % i) + "</span>", ph("ag_%d_motivo" % i)]
                   for i in range(1, 9)]),
        cards=cards([(ph("observar_%d_titulo" % i), ph("observar_%d_detalhe" % i)) for i in (1, 2, 3)]))))

    P.append(page_a4(t, "Notas e avisos", 10, """<span class="eyebrow">Transparência</span>
<h1 class="t">Notas metodológicas e avisos</h1>
<h2>Fontes</h2>
<div class="dl">
  <dt>Dados de mercado</dt><dd>%(f1)s</dd>
  <dt>Indicadores macro</dt><dd>%(f2)s</dd>
  <dt>Consenso de mercado</dt><dd>%(f3)s</dd>
  <dt>Data de fechamento</dt><dd>%(f4)s</dd>
</div>
<h2>Declaração do analista</h2>
<p class="legal">%(decl)s</p>
<h2>Avisos legais</h2>
<p class="legal">%(disc)s</p>
<p class="legal">Este relatório tem caráter exclusivamente informativo e educacional e não constitui oferta, recomendação individualizada, proposta de investimento ou solicitação de compra ou venda de qualquer ativo. As opiniões refletem a leitura do time na data de fechamento e podem mudar sem aviso prévio. Projeções são exercícios sujeitos a erro e não representam promessa ou garantia de resultado.</p>
<p class="legal">Rentabilidade passada não representa garantia de rentabilidade futura. Antes de investir, avalie a adequação do produto ao seu perfil e leia os documentos oficiais de cada investimento. É proibida a reprodução, redistribuição ou compartilhamento total ou parcial deste documento sem autorização prévia e por escrito.</p>
<h2>Contato</h2>
<div class="dl">
  <dt>Analista responsável</dt><dd>%(an)s &middot; %(reg)s</dd>
  <dt>E-mail</dt><dd>%(email)s</dd>
  <dt>Ouvidoria</dt><dd>%(ouv)s</dd>
  <dt>Razão social</dt><dd>%(razao)s &middot; CNPJ %(cnpj)s</dd>
</div>""" % dict(
        f1=ph("fonte_dados_mercado"), f2=ph("fonte_dados_macro"), f3=ph("fonte_consenso"),
        f4=ph("data_fechamento"), decl=ph("declaracao_analista", "Declaração exigida pela Resolução CVM 20"),
        disc=ph("disclaimer_regulatorio", "Texto aprovado pelo compliance para este segmento"),
        an=ph("nome_analista"), reg=ph("registro_analista"), email=ph("email_contato"),
        ouv=ph("canal_ouvidoria"), razao=ph("razao_social"), cnpj=ph("cnpj"))))

    return P
