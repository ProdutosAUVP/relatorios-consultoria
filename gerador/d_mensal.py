# -*- coding: utf-8 -*-
"""Relatório mensal do cliente.

A cobertura de seções segue a especificação do relatório gerado hoje pelo
Consolidador (AUVP_Capital_Relatorios_Mensais.pdf): capa, carta, resumo da
carteira, carteira consolidada, alocação por estratégia, movimentações e
proventos, renda fixa, ações e FIIs, internacional e notas. As seções marcadas
lá como "quando há dado" continuam condicionais aqui.

O relatório é de posição: ele mostra o que existe na carteira e quanto isso
vale. Preço médio e rentabilidade por ativo não entram — a rentabilidade
aparece uma vez, no resumo, e para a carteira inteira. O CDI também não é
referência aqui; a comparação é contra IPCA + 5% a.a. e o Ibovespa. Leitura de
cenário, posicionamento e plano de ação são assunto de outros documentos, não
deste.
"""
from layout import *

TRATAMENTO = {"private": "Prezado(a)", "alta-renda": "Prezado(a)",
              "consultoria": "Olá,", "assessoria": "Olá,"}

PAPEL = {"consultoria": "Consultor(a)", "alta-renda": "Consultor(a)",
         "private": "Banker", "assessoria": "Assessor(a)"}

# Página extra por segmento, depois das seções comuns. Consultoria e Alta Renda
# não têm: tudo o que as distingue já está nas seções comuns.
EXTRA_TITULO = {
    "consultoria": None,
    "alta-renda": None,
    "private": "Estruturas, internacional e sucessão",
    "assessoria": "Transparência de remuneração",
}

OPCIONAL = ('<span class="pill" style="margin-left:3mm;vertical-align:middle">'
            'Somente quando houver dado</span>')


def pagina_extra(t, seg):
    if seg == "private":
        return """<span class="eyebrow">Private Banking</span>
<h1 class="t">Estruturas e sucessão</h1>
<p class="lead">Acompanhamento das estruturas patrimoniais e do plano sucessório definidos com a família. A exposição internacional está na seção anterior.</p>
<h2>Estruturas e veículos</h2>
%(tab)s
<h2>Planejamento sucessório e patrimonial</h2>
%(cards)s
<div class="gap"></div>
<h2>Liquidez da família nos próximos 12 meses</h2>
%(tab2)s""" % dict(
            tab=table(["Estrutura", "Tipo", "Finalidade", "Jurisdição", "Status", "Próxima revisão"],
                      [[ph("estrutura_%d_nome" % i), ph("estrutura_%d_tipo" % i), ph("estrutura_%d_finalidade" % i),
                        ph("estrutura_%d_jurisdicao" % i), ph("estrutura_%d_status" % i),
                        ph("estrutura_%d_revisao" % i)] for i in (1, 2, 3)], xs=True,
                      widths=[20, 14, 24, 14, 14, 14]),
            cards=cards([("Holding e governança", ph("nota_holding")),
                         ("Seguros e liquidez sucessória", ph("nota_seguros")),
                         ("Doações e testamento", ph("nota_sucessao"))]),
            tab2=table(["Compromisso", "Quando", "Valor", "Origem dos recursos", "Situação"],
                       [[ph("compromisso_%d_nome" % i), ph("compromisso_%d_quando" % i),
                         ph("compromisso_%d_valor" % i), ph("compromisso_%d_origem" % i),
                         ph("compromisso_%d_situacao" % i)] for i in (1, 2, 3)], nums=[2],
                       sm=True, widths=[26, 14, 16, 26, 18]))

    # assessoria
    return """<span class="eyebrow">Assessoria</span>
<h1 class="t">Transparência de remuneração</h1>
<p class="lead">Você não paga taxa de assessoria. A casa é remunerada pela distribuição dos produtos que estão na sua carteira, e o quadro abaixo mostra quanto isso representou no período.</p>
<h2>Remuneração recebida pela casa no período</h2>
%(tab)s
<div class="gap"></div>
%(kpis)s
<div class="gap"></div>
<div class="note"><p><strong>Como ler este quadro.</strong> %(como)s</p></div>
<h2>Conflitos de interesse</h2>
<p class="small mut">%(conf)s</p>""" % dict(
        tab=table(["Produto", "Classe", "Posição", "Forma de remuneração", "Valor no período", "% da posição"],
                  [[ph("remun_%d_produto" % i), ph("remun_%d_classe" % i), ph("remun_%d_posicao" % i),
                    ph("remun_%d_forma" % i), ph("remun_%d_valor" % i), ph("remun_%d_perc" % i)]
                   for i in (1, 2, 3, 4, 5)],
                  foot=["<strong>Total</strong>", "", "", "", ph("remun_total"), ph("remun_total_perc")],
                  nums=[2, 4, 5], sm=True),
        kpis=kpis([("Remuneração no período", ph("remun_total"), "Recebida pela casa"),
                   ("Sobre o patrimônio", ph("remun_total_perc"), "No período"),
                   ("Equivalente ao ano", ph("remun_equivalente_ano"), "Se o ritmo se mantiver"),
                   ("Custo pago por você", "R$ 0,00", "Não há taxa de assessoria")]),
        como=ph("texto_como_ler_remuneracao"), conf=ph("texto_conflito_interesse"))


def build(t, seg):
    set_date_ph("mes_referencia")
    papel = PAPEL[seg]
    P = []

    # ------------------------------------------------------------------ capa
    P.append(cover_a4(
        t, "Relatório", "Mensal", "Sua", "Carteira",
        [com_rotulo(t, ph("nome_cliente")),
         "Perfil de investidor &middot; " + ph("perfil_investidor"),
         papel + " &middot; " + ph("nome_responsavel"),
         ph("mes_referencia")]))

    # o sumário precisa dos números de página reais, então as seções são
    # montadas primeiro e a paginação vem depois
    secoes = []          # (rótulo no cabeçalho, título no sumário, corpo)

    def add(sec, titulo_sumario, corpo):
        secoes.append((sec, titulo_sumario, corpo))

    # ------------------------------------------------------- resumo da carteira
    add("Resumo da carteira", "Resumo da carteira", """<span class="eyebrow">Visão geral</span>
<h1 class="t">Resumo da carteira</h1>
<p class="lead">Posição consolidada em %(dtpos)s, considerando todas as contas e instituições sob acompanhamento.</p>
%(kpis)s
<div class="gap"></div>
%(kpis2)s
<h2>Rentabilidade x referências</h2>
%(tab)s
<h2>Evolução do patrimônio</h2>
%(ch)s""" % dict(
        dtpos=ph("data_posicao"),
        kpis=kpis([("Patrimônio total", ph("patrimonio_total"), "Em " + ph("data_posicao")),
                   ("Rentabilidade no mês", ph("rent_mes"), "No ano: " + ph("rent_ano")),
                   ("Rentabilidade em 12 meses", ph("rent_12m"), "Desde o início: " + ph("rent_inicio")),
                   ("Ganho no mês", ph("ganho_mes_reais"), "No ano: " + ph("ganho_ano_reais"))]),
        kpis2=kpis([("Aplicações no mês", ph("aplicacoes_mes"), "Bruto"),
                    ("Resgates no mês", ph("resgates_mes"), "Bruto"),
                    ("Aporte líquido", ph("aporte_liquido_mes"), "Aplicações menos resgates"),
                    ("Proventos recebidos", ph("total_proventos"), "Líquido de IR")]),
        tab=table(["Indicador", "No mês", "No ano", "12 meses", "24 meses", "Desde o início"],
                  [["<strong>Sua carteira</strong>", ph("rent_mes"), ph("rent_ano"), ph("rent_12m"), ph("rent_24m"), ph("rent_inicio")],
                   ["IPCA + 5% a.a.", ph("ipca5_mes"), ph("ipca5_ano"), ph("ipca5_12m"), ph("ipca5_24m"), ph("ipca5_inicio")],
                   ["Ibovespa", ph("ibov_mes"), ph("ibov_ano"), ph("ibov_12m"), ph("ibov_24m"), ph("ibov_inicio")]],
                  caption="Rentabilidades líquidas de custos e brutas de impostos, salvo indicação em contrário. Rentabilidade passada não é garantia de rentabilidade futura.",
                  nums=[1, 2, 3, 4, 5]),
        ch=chart("Carteira x IPCA + 5% a.a.",
                 "Linha da carteira acumulada contra o benchmark, e barras de aportes e resgates no eixo secundário.",
                 "line", "min-height:46mm")))

    # ------------------------------------------------------ tabela do portfólio
    add("Carteira", "Carteira consolidada", """<span class="eyebrow">Posições</span>
<h1 class="t">Carteira consolidada</h1>
<p class="lead">Todas as posições em %(dt)s, com a instituição em que estão custodiadas.</p>
%(tab)s""" % dict(
        dt=ph("data_posicao"),
        tab=table(["Ativo", "Classe", "Instituição", "Quantidade", "Posição", "% da carteira"],
                  [[ph("pos_%d_ativo" % i), ph("pos_%d_classe" % i), ph("pos_%d_instituicao" % i),
                    ph("pos_%d_qtd" % i), ph("pos_%d_valor" % i), ph("pos_%d_perc" % i)]
                   for i in range(1, 15)],
                  foot=["<strong>Total</strong>", "", "", "", ph("patrimonio_total"), "100,0%"],
                  nums=[3, 4, 5], xs=True, widths=[24, 17, 17, 13, 16, 13],
                  caption="Repita as linhas conforme o número de posições. Ativos zerados no período aparecem na seção de movimentações.")))

    # --------------------------------------------------- alocação por estratégia
    add("Alocação por estratégia", "Alocação por estratégia", """<span class="eyebrow">Distribuição</span>
<h1 class="t">Alocação por estratégia</h1>
<p class="lead">Comparação entre a carteira meta do perfil %(perf)s e a posição efetiva na data de referência.</p>
%(tab)s
<div class="gap"></div>
%(ch)s""" % dict(
        perf=ph("perfil_investidor"),
        tab=table(["Classe de ativo", "Meta", "Atual", "Desvio", "Valor", "Leitura"],
                  [[c, ph("alvo_%s" % k), ph("atual_%s" % k), ph("desvio_%s" % k), ph("valor_%s" % k),
                    '<span class="pill">' + ph("status_%s" % k) + "</span>"]
                   for c, k in [("Renda fixa pós-fixada", "rf_pos"), ("Renda fixa prefixada", "rf_pre"),
                                ("Renda fixa inflação", "rf_ipca"), ("Multimercado", "multi"),
                                ("Renda variável Brasil", "rv_br"), ("Internacional", "intl"),
                                ("Fundos imobiliários", "fii"), ("Alternativos e private", "alt"),
                                ("Caixa e liquidez", "caixa")]],
                  foot=["<strong>Total</strong>", "100,0%", "100,0%", "&mdash;", ph("patrimonio_total"), ""],
                  nums=[1, 2, 3, 4],
                  caption="Meta conforme o diagrama do cerrado / carteira recomendada vigente para o perfil. Desvios acima da banda de tolerância acionam rebalanceamento."),
        ch=chart("Carteira atual x meta", "Duas roscas concêntricas: a interna com a meta, a externa com a posição atual.",
                  "donut", "flex:1 1 auto;min-height:52mm",
                  series=["Renda fixa", "Multimercado", "Renda variável BR", "Internacional", "FIIs", "Alternativos"])))

    # ------------------------------------------------ movimentações e proventos
    add("Movimentações e proventos", "Movimentações e proventos", """<span class="eyebrow">Período</span>
<h1 class="t">Movimentações e proventos</h1>
<p class="lead">Todas as operações executadas entre %(ini)s e %(fim)s, com o motivo de cada decisão.</p>
<h2>Operações executadas</h2>
%(tab)s
<h2>Proventos e rendimentos recebidos</h2>
<div class="cols2u" style="flex:1 1 auto;align-items:stretch">
  <div>%(tab2)s</div>
  %(ch)s
</div>""" % dict(
        ini=ph("data_inicio_periodo"), fim=ph("data_fim_periodo"),
        tab=table(["Data", "Operação", "Ativo", "Classe", "Quantidade", "Valor", "Motivo"],
                  [[ph("mov_%d_data" % i), ph("mov_%d_tipo" % i), ph("mov_%d_ativo" % i),
                    ph("mov_%d_classe" % i), ph("mov_%d_qtd" % i), ph("mov_%d_valor" % i),
                    ph("mov_%d_motivo" % i)] for i in range(1, 7)], nums=[4, 5], sm=True),
        tab2=table(["Data", "Origem", "Tipo", "Bruto", "IR", "Líquido"],
                   [[ph("prov_%d_data" % i), ph("prov_%d_origem" % i), ph("prov_%d_tipo" % i),
                     ph("prov_%d_bruto" % i), ph("prov_%d_ir" % i), ph("prov_%d_liquido" % i)]
                    for i in (1, 2, 3, 4)],
                   foot=["<strong>Total</strong>", "", "", ph("prov_total_bruto"), ph("prov_total_ir"), ph("total_proventos")],
                   nums=[3, 4, 5], sm=True),
        ch=chart("Proventos por mês", "Barras com os proventos recebidos nos últimos 12 meses, empilhadas por origem (dividendos, JCP, aluguel, cupom).", "bars", "min-height:48mm")))

    # -------------------------------------------------------------- renda fixa
    add("Renda fixa", "Renda fixa: indexadores e liquidez", """<span class="eyebrow">Renda fixa</span>
<h1 class="t">Indexadores e liquidez projetada</h1>
<p class="lead">Como a renda fixa está distribuída entre indexadores e quando ela vira caixa.</p>
<h2>Posições por indexador</h2>
<div class="cols2u">
  <div>%(tab)s</div>
  %(ch)s
</div>
<h2>Liquidez projetada</h2>
%(tab2)s""" % dict(
        tab=table(["Indexador", "Valor", "% da RF", "Taxa média", "Prazo médio"],
                  [[n, ph("rf_%s_valor" % k), ph("rf_%s_perc" % k), ph("rf_%s_taxa" % k), ph("rf_%s_prazo" % k)]
                   for n, k in [("Pós-fixado (CDI)", "pos"), ("Prefixado", "pre"),
                                ("Inflação (IPCA+)", "ipca"), ("Isentos (LCI/LCA/CRI/CRA/deb.)", "isento")]],
                  foot=["<strong>Total</strong>", ph("rf_total_valor"), "100,0%", ph("rf_taxa_media"), ph("rf_prazo_medio")],
                  nums=[1, 2, 3, 4], sm=True),
        ch=chart("Renda fixa por indexador", "Rosca com a divisão entre pós-fixado, prefixado, inflação e isentos.",
                 "donut", "min-height:44mm", series=["Pós-fixado", "Prefixado", "Inflação", "Isentos"]),
        tab2=table(["Faixa", "Valor", "% da RF", "% do patrimônio", "Acumulado", "Observação"],
                   [[n, ph("liq_%s_valor" % k), ph("liq_%s_perc_rf" % k), ph("liq_%s_perc_pat" % k),
                     ph("liq_%s_acum" % k), ph("liq_%s_obs" % k)]
                    for n, k in [("D+0", "d0"), ("D+30", "d30"), ("D+60", "d60"),
                                 ("D+90", "d90"), ("D+180", "d180"), ("1 ano", "a1"),
                                 ("2 anos", "a2"), ("3 anos", "a3"), ("4 anos", "a4"),
                                 ("5 anos", "a5"), ("Acima de 5 anos", "a5mais")]],
                   nums=[1, 2, 3, 4], xs=True,
                   caption="Liquidez projetada considera carência, vencimento e liquidez de mercado do papel.")))

    add("Renda fixa", "Renda fixa: emissores", """<span class="eyebrow">Renda fixa</span>
<h1 class="t">Controle por emissor</h1>
<p class="lead">A quem você está emprestando, quanto, com qual risco de crédito e até onde vai a cobertura do FGC.</p>
%(tab)s
<div class="gap"></div>
<div class="note"><p><strong>Limite interno por emissor.</strong> %(nota)s</p></div>""" % dict(
        tab=table(["Emissor", "Exposição", "% da RF", "% do patrimônio", "Rating", "Coberto pelo FGC", "Limite interno"],
                  [[ph("emissor_%d_nome" % i), ph("emissor_%d_valor" % i), ph("emissor_%d_perc_rf" % i),
                    ph("emissor_%d_perc_pat" % i), ph("emissor_%d_rating" % i), ph("emissor_%d_fgc" % i),
                    ph("emissor_%d_limite" % i)] for i in (1, 2, 3, 4, 5, 6)],
                  nums=[1, 2, 3, 6], sm=True,
                  widths=[24, 14, 11, 14, 10, 13, 14]),
        nota=ph("texto_limite_emissor")))

    # ----------------------------------------------------------- ações e FIIs
    add("Ações e FIIs", "Ações e fundos imobiliários", """<span class="eyebrow">Renda variável</span>
<h1 class="t">Ações e fundos imobiliários</h1>
<p class="lead">Distribuição por setor e por segmento, e a lista completa das posições em bolsa.</p>
<div class="cols2">
  %(ch)s
  %(ch2)s
</div>
<h2>Posições em ações</h2>
%(tab)s
<h2>Posições em fundos imobiliários</h2>
%(tab2)s""" % dict(
        ch=chart("Ações por setor", "Rosca com a distribuição setorial das ações, na curadoria de setor da AUVP.", "donut", "min-height:40mm"),
        ch2=chart("FIIs por segmento", "Rosca com a distribuição por segmento.",
                   "donut", "min-height:40mm", series=["Tijolo", "Papel", "Híbrido", "Fundo de fundos"]),
        tab=table(["Ativo", "Empresa", "Setor", "Qtd.", "Cotação", "Posição", "% da carteira"],
                  [[ph("acao_%d_ticker" % i), ph("acao_%d_empresa" % i), ph("acao_%d_setor" % i),
                    ph("acao_%d_qtd" % i), ph("acao_%d_cotacao" % i), ph("acao_%d_valor" % i),
                    ph("acao_%d_perc" % i)]
                   for i in (1, 2, 3, 4, 5)], nums=[3, 4, 5, 6], xs=True,
                  widths=[12, 19, 16, 10, 15, 15, 13]),
        tab2=table(["Ativo", "Segmento", "Qtd.", "Cotação", "Posição", "% da carteira"],
                   [[ph("fii_%d_ticker" % i), ph("fii_%d_segmento" % i), ph("fii_%d_qtd" % i),
                     ph("fii_%d_cotacao" % i), ph("fii_%d_valor" % i), ph("fii_%d_perc" % i)]
                    for i in (1, 2, 3, 4)],
                   nums=[2, 3, 4, 5], sm=True,
                   widths=[14, 28, 12, 15, 16, 15])))

    # ----------------------------------------------------------- internacional
    add("Internacional", "Internacional", """<span class="eyebrow">Internacional %(op)s</span>
<h1 class="t">Carteira internacional</h1>
<p class="lead">Posições denominadas em moeda estrangeira, convertidas pela PTAX de %(ptax)s. A página mostra a posição no exterior; o resultado da carteira está no resumo. Esta seção só entra quando houver posição no exterior.</p>
%(kpis)s
<div class="gap"></div>
<h2>Renda fixa internacional</h2>
%(tab)s
<h2>Renda variável internacional</h2>
%(tab2)s""" % dict(
        op=OPCIONAL, ptax=ph("data_ptax"),
        kpis=kpis([("Total no exterior", ph("intl_total_usd"), "Em reais: " + ph("intl_total_brl")),
                   ("% do patrimônio", ph("intl_perc_patrimonio"), "Meta: " + ph("alvo_intl")),
                   ("Câmbio da conversão", ph("ptax_utilizada"), "PTAX de " + ph("data_ptax"))], n=3),
        tab=table(["Ativo", "Emissor", "Moeda", "Vencimento", "Taxa", "Posição (US$)", "% do exterior"],
                  [[ph("irf_%d_ativo" % i), ph("irf_%d_emissor" % i), ph("irf_%d_moeda" % i),
                    ph("irf_%d_vencimento" % i), ph("irf_%d_taxa" % i), ph("irf_%d_valor_usd" % i),
                    ph("irf_%d_perc" % i)] for i in (1, 2, 3)], nums=[4, 5, 6], sm=True),
        tab2=table(["Ativo", "Nome", "Tipo", "Qtd.", "Cotação (US$)", "Posição (US$)", "% do exterior"],
                   [[ph("irv_%d_ticker" % i), ph("irv_%d_nome" % i), ph("irv_%d_tipo" % i),
                     ph("irv_%d_qtd" % i), ph("irv_%d_cotacao" % i), ph("irv_%d_valor_usd" % i),
                     ph("irv_%d_perc" % i)] for i in (1, 2, 3, 4)],
                   nums=[3, 4, 5, 6], xs=True,
                   widths=[13, 22, 13, 11, 15, 15, 11])))

    # ------------------------------------------------------- página do segmento
    if EXTRA_TITULO[seg]:
        add(EXTRA_TITULO[seg], EXTRA_TITULO[seg], pagina_extra(t, seg))

    # ------------------------------------------------------------------ notas
    add("Notas e avisos", "Notas metodológicas e avisos", """<span class="eyebrow">Transparência</span>
<h1 class="t">Notas metodológicas e avisos</h1>
<h2>Avisos legais</h2>
<p class="legal">%(disc)s</p>
<p class="legal">Rentabilidade passada não representa garantia de rentabilidade futura. Os investimentos apresentados podem não ser adequados a todos os investidores e não contam, salvo quando expressamente indicado, com garantia do Fundo Garantidor de Créditos (FGC) nem de qualquer mecanismo de seguro. Antes de investir, leia atentamente os documentos de cada produto, incluindo regulamento, lâmina, prospecto e formulário de informações complementares.</p>
<p class="legal">Este material é destinado exclusivamente a %(cli)s, tem caráter informativo e não constitui oferta, recomendação pública, proposta de investimento ou solicitação de compra ou venda de qualquer ativo. É proibida a reprodução, redistribuição ou compartilhamento total ou parcial deste documento sem autorização prévia e por escrito.</p>
<h2>Contato e ouvidoria</h2>
<div class="dl">
  <dt>Responsável</dt><dd>%(resp)s &middot; %(cert)s</dd>
  <dt>Atendimento</dt><dd>%(canal)s</dd>
  <dt>E-mail</dt><dd>%(email)s</dd>
  <dt>Ouvidoria</dt><dd>%(ouv)s</dd>
  <dt>Razão social</dt><dd>%(razao)s &middot; CNPJ %(cnpj)s</dd>
</div>""" % dict(
        disc=ph("disclaimer_regulatorio", "Texto aprovado pelo compliance para este segmento"),
        cli=ph("nome_cliente"), resp=ph("nome_responsavel"), cert=ph("registro_cvm_ou_ancord"),
        canal=ph("canal_atendimento"), email=ph("email_contato"), ouv=ph("canal_ouvidoria"),
        razao=ph("razao_social"), cnpj=ph("cnpj")))

    # ----------------- carta e sumário, agora que a paginação é conhecida ------
    toc = "".join('<li><span class="n">%02d</span><span>%s</span><span class="d"></span>'
                  '<span class="p">%02d</span></li>' % (i, titulo, i + 2)
                  for i, (_, titulo, _) in enumerate(secoes, start=1))
    P.append(page_a4(t, "Abertura", 2, """<span class="eyebrow">Carta do %(papel)s</span>
<h1 class="t">O que aconteceu com a sua carteira em %(mes)s</h1>
<p>%(trat)s %(cli)s,</p>
<p>%(p1)s</p>
<p>%(p2)s</p>
<p>%(p3)s</p>
<div class="sig">
  <div class="ln">%(resp)s<br><span class="mut">%(papel)s &middot; %(cert)s</span></div>
  <div class="ln">%(contato)s<br><span class="mut">%(email)s</span></div>
</div>
<h2>Neste relatório</h2>
<ol class="toc">%(toc)s</ol>""" % dict(
        papel=papel, mes=ph("mes_referencia"), trat=TRATAMENTO[seg], cli=ph("nome_cliente"),
        p1=ph("carta_paragrafo_1", "Resumo do mês em 2-3 frases"),
        p2=ph("carta_paragrafo_2", "O que foi feito na carteira e por quê"),
        p3=ph("carta_paragrafo_3", "O que esperar do próximo período"),
        resp=ph("nome_responsavel"), cert=ph("registro_cvm_ou_ancord"),
        contato=ph("telefone_contato"), email=ph("email_contato"), toc=toc)))

    for i, (sec, _, corpo) in enumerate(secoes, start=3):
        P.append(page_a4(t, sec, i, corpo))
    return P
