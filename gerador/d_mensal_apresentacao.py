# -*- coding: utf-8 -*-
from layout import *

PAPEL = {"consultoria": "Consultor(a)", "alta-renda": "Consultor(a)",
         "private": "Banker", "assessoria": "Assessor(a)"}

EXTRA = {
    "consultoria": ("Renda fixa e vencimentos",
                    "Posições por indexador e o que vence nos próximos 12 meses."),
    "alta-renda": ("Ofertas do período",
                   "O que esteve disponível para o segmento e o que entrou na sua carteira."),
    "private": ("Estruturas e internacional",
                "Exposição por moeda e jurisdição, e o andamento das estruturas da família."),
    "assessoria": ("Renda fixa e vencimentos",
                   "Posições por indexador e o que vence nos próximos 12 meses."),
}


def build(t, seg):
    set_date_ph("mes_referencia")
    S = []
    papel = PAPEL[seg]
    ex_t, ex_d = EXTRA[seg]

    S.append(cover_slide(t, "Relatório", "Mensal",
                         com_rotulo(t, ph("mes_referencia")),
                         [ph("nome_cliente"), papel + " &middot; " + ph("nome_responsavel"),
                          "Posição em " + ph("data_posicao")]))

    S.append(slide(t, "Agenda", 2, """<span class="eyebrow">Nossa conversa de hoje</span>
<h1 class="t">Agenda</h1>
<ol class="tl" style="grid-template-columns:1fr 1fr;flex:1 1 auto;align-content:start">
  <li><h4>Como fechou o mês</h4><p>Patrimônio, rentabilidade e comparação com as referências.</p></li>
  <li><h4>Alocação</h4><p>Onde a carteira está em relação ao alvo do seu perfil.</p></li>
  <li><h4>Destaques e detratores</h4><p>O que puxou o resultado para cima e para baixo.</p></li>
  <li><h4>Movimentações</h4><p>O que foi comprado, vendido e por quê.</p></li>
  <li><h4>%(ext)s</h4><p>%(exd)s</p></li>
  <li><h4>Cenário e próximos passos</h4><p>O que esperamos e o que vamos fazer a respeito.</p></li>
</ol>
<div class="note" style="margin-top:auto"><p><strong>Tempo previsto.</strong> %(tempo)s &middot; <strong>Dúvidas:</strong> pode interromper a qualquer momento.</p></div>""" % dict(
        ext=ex_t, exd=ex_d, tempo=ph("duracao_reuniao"))))

    S.append(slide(t, "Resultado do mês", 3, """<span class="eyebrow">%(mes)s</span>
<h1 class="t">Como fechou o mês</h1>
%(kpis)s
<div class="gap"></div>
<div class="cols2u" style="flex:1 1 auto;align-items:stretch">
  %(ch)s
  <div>
    <h2>Em uma frase</h2>
    <p>%(frase)s</p>
    <div class="note"><p><strong>Atenção do mês.</strong> %(aten)s</p></div>
  </div>
</div>""" % dict(
        mes=ph("mes_referencia"),
        kpis=kpis([("Patrimônio total", ph("patrimonio_total"), "Em " + ph("data_posicao")),
                   ("No mês", ph("rent_mes"), ph("rent_mes_pct_cdi") + " do CDI"),
                   ("No ano", ph("rent_ano"), ph("rent_ano_pct_cdi") + " do CDI"),
                   ("Aportes líquidos", ph("aporte_liquido_mes"), "Resgates: " + ph("resgates_mes"))]),
        ch=chart("Patrimônio nos últimos 12 meses", "Linha de patrimônio com barras de aportes e resgates.", "line", "min-height:52mm"),
        frase=ph("resumo_do_mes"), aten=ph("ponto_de_atencao_mes")), dark=True))

    S.append(slide(t, "Rentabilidade", 4, """<span class="eyebrow">Comparação</span>
<h1 class="t">Sua carteira x referências</h1>
<div class="cols2u" style="flex:1 1 auto;align-items:stretch">
  <div>%(tab)s</div>
  %(ch)s
</div>
<p class="legal" style="margin-top:4mm">Rentabilidades líquidas de custos e brutas de impostos, salvo indicação em contrário. Rentabilidade passada não é garantia de rentabilidade futura.</p>""" % dict(
        tab=table(["Indicador", "Mês", "Ano", "12m", "24m"],
                  [["<strong>Sua carteira</strong>", ph("rent_mes"), ph("rent_ano"), ph("rent_12m"), ph("rent_24m")],
                   ["CDI", ph("cdi_mes"), ph("cdi_ano"), ph("cdi_12m"), ph("cdi_24m")],
                   ["IPCA + 5%", ph("ipca5_mes"), ph("ipca5_ano"), ph("ipca5_12m"), ph("ipca5_24m")],
                   ["Ibovespa", ph("ibov_mes"), ph("ibov_ano"), ph("ibov_12m"), ph("ibov_24m")],
                   ["<strong>Carteira x CDI</strong>", ph("vs_cdi_mes"), ph("vs_cdi_ano"), ph("vs_cdi_12m"), ph("vs_cdi_24m")]],
                  nums=[1, 2, 3, 4]),
        ch=chart("Carteira x CDI acumulado", "Duas linhas acumuladas desde o início do relacionamento.", "line", "min-height:60mm"))))

    S.append(slide(t, "Alocação", 5, """<span class="eyebrow">Distribuição</span>
<h1 class="t">Alvo x realizado</h1>
<div class="cols2u" style="flex:1 1 auto;align-items:stretch">
  <div>%(tab)s</div>
  <div style="display:flex;flex-direction:column;gap:5mm">
    %(ch)s
    <div class="note"><p><strong>Rebalanceamento.</strong> %(reb)s</p></div>
  </div>
</div>""" % dict(
        tab=table(["Classe", "Alvo", "Atual", "Desvio"],
                  [[c, ph("alvo_%s" % k), ph("atual_%s" % k), ph("desvio_%s" % k)]
                   for c, k in [("Renda fixa pós", "rf_pos"), ("Renda fixa inflação", "rf_ipca"),
                                ("Renda fixa prefixada", "rf_pre"), ("Multimercado", "multi"),
                                ("Renda variável BR", "rv_br"), ("Internacional", "intl"),
                                ("Fundos imobiliários", "fii"), ("Alternativos", "alt"),
                                ("Caixa", "caixa")]],
                  foot=["<strong>Total</strong>", "100,0%", "100,0%", "&mdash;"], nums=[1, 2, 3]),
        ch=chart("Composição atual", "Rosca com o peso de cada classe.", "donut", "min-height:46mm"),
        reb=ph("texto_rebalanceamento"))))

    S.append(slide(t, "Atribuição", 6, """<span class="eyebrow">O que moveu o resultado</span>
<h1 class="t">Destaques e detratores</h1>
<div class="cols2" style="flex:1 1 auto">
  <div>
    <h2>Contribuíram para o resultado</h2>
    %(tp)s
    <div class="gap"></div>
    <p class="small mut">%(cp)s</p>
  </div>
  <div>
    <h2>Puxaram o resultado para baixo</h2>
    %(tn)s
    <div class="gap"></div>
    <p class="small mut">%(cn)s</p>
  </div>
</div>""" % dict(
        tp=table(["Ativo", "Retorno", "Contribuição"],
                 [[ph("top_%d_ativo" % i), ph("top_%d_ret" % i), ph("top_%d_contrib" % i)] for i in (1, 2, 3, 4)],
                 nums=[1, 2]),
        tn=table(["Ativo", "Retorno", "Contribuição"],
                 [[ph("bot_%d_ativo" % i), ph("bot_%d_ret" % i), ph("bot_%d_contrib" % i)] for i in (1, 2, 3, 4)],
                 nums=[1, 2]),
        cp=ph("comentario_destaques"), cn=ph("comentario_detratores"))))

    S.append(slide(t, "Movimentações", 7, """<span class="eyebrow">O que fizemos</span>
<h1 class="t">Movimentações do período</h1>
%(tab)s
<div class="gap"></div>
%(kpis)s""" % dict(
        tab=table(["Data", "Operação", "Ativo", "Classe", "Valor", "Motivo"],
                  [[ph("mov_%d_data" % i), ph("mov_%d_tipo" % i), ph("mov_%d_ativo" % i),
                    ph("mov_%d_classe" % i), ph("mov_%d_valor" % i), ph("mov_%d_motivo" % i)]
                   for i in (1, 2, 3, 4, 5)], nums=[4]),
        kpis=kpis([("Aportado", ph("total_aportes"), "No período"),
                   ("Resgatado", ph("total_resgates"), "No período"),
                   ("Proventos", ph("total_proventos"), "Líquido de IR"),
                   ("Custos", ph("total_custos"), ph("custo_perc_patrimonio") + " do patrimônio")]))))

    S.append(slide(t, ex_t, 8, """<span class="eyebrow">%(nome)s</span>
<h1 class="t">%(ext)s</h1>
<p class="lead">%(exd)s</p>
<div class="cols2u" style="flex:1 1 auto;align-items:stretch">
  <div>%(tab)s</div>
  %(ch)s
</div>""" % dict(
        nome=t["nome"], ext=ex_t, exd=ex_d,
        tab=table(["Item", "Detalhe", "Valor", "%", "Observação"],
                  [[ph("seg_%d_item" % i), ph("seg_%d_detalhe" % i), ph("seg_%d_valor" % i),
                    ph("seg_%d_perc" % i), ph("seg_%d_obs" % i)] for i in (1, 2, 3, 4, 5)], nums=[2, 3]),
        ch=chart("Visão do segmento",
                 {"consultoria": "Renda fixa por indexador e calendário de vencimentos.",
                  "assessoria": "Renda fixa por indexador e calendário de vencimentos.",
                  "alta-renda": "Ofertas acessadas no período e peso na carteira.",
                  "private": "Patrimônio por moeda e por jurisdição."}[seg], "donut", "min-height:50mm"))))

    S.append(slide(t, "Cenário", 9, """<span class="eyebrow">Contexto</span>
<h1 class="t">Cenário e posicionamento</h1>
<div class="cols2" style="margin-bottom:6mm">
  <div><h2>Brasil</h2><p class="small">%(br)s</p></div>
  <div><h2>Internacional</h2><p class="small">%(int)s</p></div>
</div>
%(tab)s""" % dict(
        br=ph("cenario_brasil"), int=ph("cenario_internacional"),
        tab=table(["Classe", "Visão", "Movimento no mês", "Racional"],
                  [[c, '<span class="pill">' + ph("pos_%s_visao" % k) + "</span>",
                    ph("pos_%s_mov" % k), ph("pos_%s_racional" % k)]
                   for c, k in [("Renda fixa pós", "rfpos"), ("Renda fixa inflação", "rfipca"),
                                ("Renda variável BR", "rvbr"), ("Internacional", "intl"),
                                ("Alternativos", "alt")]])), dark=True))

    S.append(slide(t, "Próximos passos", 10, """<span class="eyebrow">Plano de ação</span>
<h1 class="t">Próximos passos</h1>
<div class="cols2u" style="flex:1 1 auto;align-items:start">
  <div>
    <h2>O que vamos fazer</h2>
    %(tab)s
  </div>
  <div>
    <h2>O que depende de você</h2>
    %(cards)s
    <div class="gap"></div>
    <div class="dl">
      <dt>Próxima reunião</dt><dd>%(reu)s</dd>
      <dt>Formato</dt><dd>%(fmt)s</dd>
      <dt>Canal direto</dt><dd>%(canal)s</dd>
    </div>
  </div>
</div>""" % dict(
        tab=table(["Prioridade", "Ação", "Prazo"],
                  [['<span class="pill">' + ph("acao_%d_prioridade" % i) + "</span>",
                    ph("acao_%d_descricao" % i), ph("acao_%d_prazo" % i)] for i in (1, 2, 3, 4)]),
        cards="".join('<div class="card"><h4>%s</h4><p>%s</p></div>'
                      % (ph("pendencia_%d_titulo" % i), ph("pendencia_%d_detalhe" % i)) for i in (1, 2)),
        reu=ph("data_proxima_reuniao"), fmt=ph("formato_reuniao"), canal=ph("canal_atendimento"))))

    S.append(slide(t, "Encerramento", 11, """<div style="display:flex;gap:16mm;flex:1 1 auto;align-items:center">
  <div style="flex:1 1 auto">
    <span class="eyebrow">Obrigado</span>
    <h1 class="t">Alguma dúvida?</h1>
    <p class="lead" style="margin-top:4mm">%(fecho)s</p>
    <div class="dl" style="margin-top:6mm">
      <dt>%(papel)s</dt><dd>%(resp)s</dd>
      <dt>WhatsApp</dt><dd>%(whats)s</dd>
      <dt>E-mail</dt><dd>%(email)s</dd>
    </div>
  </div>
  <div style="display:flex;flex-direction:column;align-items:center;gap:4mm">
    <div class="qr">QR code<br>agendamento</div>
    <div class="small mut" style="text-align:center;max-width:52mm">%(link)s</div>
  </div>
</div>""" % dict(fecho=ph("mensagem_encerramento"), papel=papel, resp=ph("nome_responsavel"),
                 whats=ph("whatsapp_contato"), email=ph("email_contato"), link=ph("link_agendamento")),
                   dark=True))

    S.append(slide(t, "Avisos", 12, """<span class="eyebrow">Transparência</span>
<h1 class="t">Notas e avisos</h1>
<div class="cols2" style="flex:1 1 auto">
  <div>
    <h2>Como os números foram apurados</h2>
    <ul class="small">
      <li>Base e data de corte: %(base)s.</li>
      <li>Cálculo de rentabilidade: %(met)s.</li>
      <li>Contas consideradas: %(contas)s.</li>
    </ul>
    <p class="legal">%(disc)s</p>
  </div>
  <div>
    <p class="legal">Rentabilidade passada não representa garantia de rentabilidade futura. Os investimentos apresentados podem não contar com garantia do Fundo Garantidor de Créditos (FGC). Antes de investir, leia os documentos oficiais de cada produto.</p>
    <p class="legal">Material destinado exclusivamente a %(cli)s. Não constitui oferta, recomendação pública ou solicitação de compra ou venda de ativos. É proibida a reprodução ou o compartilhamento total ou parcial sem autorização prévia e por escrito. %(razao)s &middot; CNPJ %(cnpj)s. Ouvidoria: %(ouv)s.</p>
  </div>
</div>""" % dict(base=ph("fonte_dados"), met=ph("metodo_rentabilidade"), contas=ph("contas_consideradas"),
                 disc=ph("disclaimer_regulatorio", "Texto aprovado pelo compliance para este segmento"),
                 cli=ph("nome_cliente"), razao=ph("razao_social"), cnpj=ph("cnpj"), ouv=ph("canal_ouvidoria"))))

    return S
