# -*- coding: utf-8 -*-
from layout import *

PAPEL = {"consultoria": "consultor", "alta-renda": "consultor",
         "private": "banker", "assessoria": "assessor"}

PITCH = {
    "consultoria": (
        "Consultoria de investimentos",
        "Um consultor dedicado, remunerado por você e não pelos produtos que vende. A carteira é montada a partir dos seus objetivos, revisada trimestralmente e explicada em linguagem simples.",
        [("Conflito de interesse zerado", "Nossa receita vem da taxa de consultoria, não da comissão dos produtos. Se o melhor produto para você paga menos, ele entra do mesmo jeito."),
         ("Carteira sob medida", "Alocação construída a partir do seu perfil, prazo e objetivos, não de um modelo genérico de prateleira."),
         ("Você entende o que tem", "Relatório mensal e reuniões trimestrais em que cada decisão é explicada e registrada.")]),
    "alta-renda": (
        "Alta Renda",
        "Atendimento consultivo com acesso a ofertas, estruturas e condições que não chegam ao varejo, mantendo a mesma transparência de custos.",
        [("Acesso a ofertas restritas", "Emissões, fundos e estruturas com ticket mínimo elevado, distribuídas com o mesmo racional de adequação ao perfil."),
         ("Eficiência tributária", "Escolha de veículos e prazos considerando come-cotas, isenções e compensação de prejuízo."),
         ("Time por trás do consultor", "Mesa de renda fixa, análise e operações apoiando cada decisão da sua carteira.")]),
    "private": (
        "Private Banking",
        "Gestão do patrimônio da família com estruturas, jurisdições e horizonte de gerações. Um banker dedicado, um comitê por trás e governança para as decisões grandes.",
        [("Visão de patrimônio, não de carteira", "Investimentos, imóveis, participações, seguros e sucessão lidos como um único balanço familiar."),
         ("Estruturas e jurisdições", "Holdings, veículos exclusivos e contas internacionais desenhados com assessoria jurídica e tributária."),
         ("Governança familiar", "Comitês periódicos, políticas de investimento escritas e preparação da próxima geração.")]),
    "assessoria": (
        "Assessoria de investimentos",
        "Um assessor dedicado para montar e acompanhar a sua carteira dentro da plataforma, sem taxa cobrada de você: a remuneração vem da distribuição dos produtos, e você sabe exatamente como.",
        [("Sem taxa de assessoria", "Você não paga mensalidade nem percentual sobre o patrimônio. A remuneração da casa está embutida nos produtos e é informada abertamente."),
         ("Alguém que atende de verdade", "Assessor com WhatsApp direto para dúvidas, ordens e vencimentos, em vez de central de atendimento."),
         ("Transparência de remuneração", "Você recebe, junto do relatório mensal, quanto a casa recebeu pelos produtos que estão na sua carteira.")]),
}


def build(t, seg):
    set_date_ph("data_apresentacao")
    S = []
    titulo, sub, pilares = PITCH[seg]
    papel = PAPEL[seg]

    S.append(cover_slide(t, "AUVP", titulo,
                         ph("subtitulo_apresentacao", "Ex.: proposta de atendimento"),
                         [ph("nome_cliente"), ph("nome_responsavel"), ph("data_apresentacao")]))

    S.append(divider_slide(t, 1, "Quem somos", "A casa, o time e o modelo de remuneração"))

    S.append(slide(t, "Quem somos", 3, """<span class="eyebrow">A casa</span>
<h1 class="t">%(tit)s</h1>
<div class="cols2u" style="flex:1 1 auto;align-items:stretch">
  <div>
    <p class="lead" style="margin-bottom:5mm">%(sub)s</p>
    <p class="small">%(hist)s</p>
    <div class="gap"></div>
    <div class="dl">
      <dt>Fundação</dt><dd>%(fund)s</dd>
      <dt>Registro</dt><dd>%(reg)s</dd>
      <dt>Modelo de remuneração</dt><dd>%(remun)s</dd>
      <dt>Custódia</dt><dd>%(cust)s</dd>
    </div>
  </div>
  %(img)s
</div>""" % dict(tit=titulo, sub=sub, hist=ph("historia_auvp"), fund=ph("ano_fundacao"),
                 reg=ph("registro_cvm_empresa"), remun=ph("modelo_remuneracao"), cust=ph("custodiante"),
                 img=imgbox("Foto do escritório, do time ou do cliente em reunião. Formato retrato, mínimo 1200&nbsp;px de largura."))))

    S.append(slide(t, "Quem somos", 4, """<span class="eyebrow">Em números</span>
<h1 class="t">A AUVP hoje</h1>
<div class="center">%(hero)s</div>
<p class="legal">%(nota)s</p>""" % dict(
        hero=hero(ph("numero_1"), ph("numero_1_legenda"),
                  [(ph("numero_%d" % i), ph("numero_%d_legenda" % i)) for i in range(2, 7)]),
        nota=ph("nota_fonte_numeros", "Data-base e fonte dos números acima"))))

    S.append(divider_slide(t, 2, "Como trabalhamos", "Método, entregas e cadência"))

    S.append(slide(t, "Como trabalhamos", 6, """<span class="eyebrow">Método</span>
<h1 class="t">Do primeiro papo à carteira rodando</h1>
<div class="center">%(flow)s</div>
<div class="note"><p><strong>Prazo típico do ciclo completo.</strong> %(prazo)s</p></div>""" % dict(
        flow=flow([(ph("metodo_%d_prazo" % i), titulo, ph("metodo_%d_detalhe" % i))
                   for i, titulo in enumerate(["Diagnóstico", "Proposta", "Transição",
                                               "Acompanhamento", "Revisão"], start=1)]),
        prazo=ph("prazo_implantacao"))))

    S.append(slide(t, "Como trabalhamos", 7, """<span class="eyebrow">Diferenciais</span>
<h1 class="t">Por que %(nome)s</h1>
<div class="cards" style="--n:3;margin-bottom:8mm">%(pil)s</div>
<h2>O que você recebe todo mês</h2>
%(ent)s""" % dict(
        nome=t["nome"],
        pil="".join('<div class="card"><h4>%s</h4><p>%s</p></div>' % (a, b) for a, b in pilares),
        ent=table(["Entrega", "Frequência", "Como chega", "Para quê"],
                  [[ph("entrega_%d_nome" % i), ph("entrega_%d_freq" % i),
                    ph("entrega_%d_canal" % i), ph("entrega_%d_para" % i)] for i in (1, 2, 3, 4, 5)]))))

    S.append(slide(t, "Como trabalhamos", 8, """<span class="eyebrow">Governança</span>
<h1 class="t">Quem decide o quê</h1>
<div class="cols2" style="flex:1 1 auto">
  <div>
    <h2>Decisões e alçadas</h2>
    %(tab)s
  </div>
  <div>
    <h2>Cadência de contato</h2>
    %(tab2)s
    <div class="gap"></div>
    <div class="note"><p><strong>Seu %(papel)s.</strong> %(sobre)s</p></div>
  </div>
</div>""" % dict(
        papel=papel,
        tab=table(["Decisão", "Quem propõe", "Quem aprova"],
                  [[ph("alcada_%d_decisao" % i), ph("alcada_%d_propoe" % i), ph("alcada_%d_aprova" % i)]
                   for i in (1, 2, 3, 4)]),
        tab2=table(["Encontro", "Frequência"],
                   [[ph("cadencia_%d_encontro" % i), ph("cadencia_%d_freq" % i)] for i in (1, 2, 3, 4)]),
        sobre=ph("texto_sobre_responsavel"))))

    S.append(divider_slide(t, 3, "Condições", "Planos, taxas e o que está incluído"))

    S.append(slide(t, "Condições", 10, """<span class="eyebrow">Planos</span>
<h1 class="t">Quanto custa e o que entra</h1>
<div class="plans" style="--n:3">
  %(p1)s
  %(p2)s
  %(p3)s
</div>
<p class="legal" style="margin-top:5mm">%(nota)s</p>""" % dict(
        **{("p%d" % i): """<div class="plan%(hl)s">
    <div class="tag">%(tag)s</div>
    <div class="nm">%(nm)s</div>
    <div class="pr"><b>%(tx)s</b><span>%(base)s</span></div>
    <ul>%(itens)s</ul>
    <div class="ft">%(para)s</div>
  </div>""" % dict(hl=" hl" if i == 3 else "", tag=ph("plano_%d_tag" % i), nm=ph("plano_%d_nome" % i),
                   tx=ph("plano_%d_taxa" % i), base=ph("plano_%d_base_calculo" % i),
                   itens="".join("<li>%s</li>" % ph("plano_%d_item_%d" % (i, j)) for j in range(1, 7)),
                   para=ph("plano_%d_para_quem" % i)) for i in (1, 2, 3)},
        nota=ph("nota_taxas", "Base de cálculo, cobrança, impostos e condições"))))

    S.append(slide(t, "Condições", 11, """<span class="eyebrow">Time</span>
<h1 class="t">Quem cuida da sua conta</h1>
<div class="cols3" style="flex:1 1 auto">
  %(cards)s
</div>""" % dict(
        cards="".join("""<div style="display:flex;flex-direction:column;gap:4mm">
    <div class="imgbox" style="flex:0 0 auto;height:52mm"><div class="cl">Foto</div><div class="cd">Retrato %d, 1:1</div></div>
    <div>
      <h3 style="margin-top:0">%s</h3>
      <div class="small mut">%s</div>
      <p class="small" style="margin-top:2mm">%s</p>
    </div>
  </div>""" % (i, ph("pessoa_%d_nome" % i), ph("pessoa_%d_cargo" % i), ph("pessoa_%d_bio" % i))
                      for i in (1, 2, 3)))))

    S.append(slide(t, "Próximos passos", 12, """<span class="eyebrow">Começar</span>
<h1 class="t">Como damos o primeiro passo</h1>
<div class="center">%(flow)s
<div><h2 style="margin-top:0">O que precisamos de você</h2>
<div class="cols3">%(need)s</div></div></div>""" % dict(
        flow=flow([(ph("passo_%d_prazo" % i), titulo, ph("passo_%d_detalhe" % i))
                   for i, titulo in enumerate(["Conversa inicial", "Diagnóstico", "Proposta",
                                               "Abertura e transferência"], start=1)]),
        need="".join('<div class="card"><h4>%s</h4><p>%s</p></div>'
                     % (ph("requisito_%d_titulo" % i), ph("requisito_%d_detalhe" % i)) for i in (1, 2, 3)))))

    S.append(slide(t, "Contato", 13, """<div style="display:flex;gap:16mm;flex:1 1 auto;align-items:center">
  <div style="flex:1 1 auto">
    <span class="eyebrow">Vamos conversar</span>
    <h1 class="t">%(chamada)s</h1>
    <div class="dl" style="margin-top:6mm">
      <dt>%(papel)s</dt><dd>%(resp)s</dd>
      <dt>WhatsApp</dt><dd>%(whats)s</dd>
      <dt>E-mail</dt><dd>%(email)s</dd>
      <dt>Site</dt><dd>%(site)s</dd>
      <dt>Endereço</dt><dd>%(end)s</dd>
    </div>
  </div>
  <div style="display:flex;flex-direction:column;align-items:center;gap:4mm">
    <div class="qr">QR code<br>agendamento</div>
    <div class="small mut" style="text-align:center;max-width:52mm">%(link)s</div>
  </div>
</div>""" % dict(chamada=ph("chamada_final", "Ex.: Agende seu diagnóstico gratuito"),
                 papel=papel.capitalize(), resp=ph("nome_responsavel"), whats=ph("whatsapp_contato"),
                 email=ph("email_contato"), site=ph("site"), end=ph("endereco_escritorio"),
                 link=ph("link_agendamento")), dark=True))

    S.append(slide(t, "Avisos", 14, """<span class="eyebrow">Transparência</span>
<h1 class="t">Avisos importantes</h1>
<div class="center"><div class="cols2">
  <div>
    <p class="legal">%(disc)s</p>
    <p class="legal">Este material tem caráter informativo e publicitário e não constitui oferta, recomendação individualizada ou proposta de investimento. Números, taxas e condições apresentados referem-se à data de elaboração e podem ser alterados sem aviso prévio.</p>
  </div>
  <div>
    <p class="legal">Rentabilidade passada não representa garantia de rentabilidade futura. Investimentos envolvem risco de perda, inclusive do capital principal, e podem não contar com garantia do Fundo Garantidor de Créditos (FGC). Antes de investir, avalie a adequação do produto ao seu perfil e leia os documentos oficiais de cada investimento.</p>
    <p class="legal">%(razao)s &middot; CNPJ %(cnpj)s &middot; %(reg)s. Ouvidoria: %(ouv)s. É proibida a reprodução ou o compartilhamento total ou parcial deste material sem autorização prévia e por escrito.</p>
  </div>
</div></div>""" % dict(disc=ph("disclaimer_regulatorio", "Texto aprovado pelo compliance para este segmento"),
                 razao=ph("razao_social"), cnpj=ph("cnpj"), reg=ph("registro_cvm_empresa"),
                 ouv=ph("canal_ouvidoria"))))

    return S
