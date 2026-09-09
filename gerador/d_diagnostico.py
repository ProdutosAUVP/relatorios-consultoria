# -*- coding: utf-8 -*-
from layout import *

PAPEL = {"consultoria": "Consultor(a)", "alta-renda": "Consultor(a)",
         "private": "Banker", "assessoria": "Assessor(a)"}

FOCO = {
    "consultoria": ("Custo, adequação e disciplina",
                    "Onde a carteira paga caro sem entregar retorno, onde ela foge do perfil e o que precisa de disciplina de rebalanceamento."),
    "alta-renda": ("Eficiência, acesso e diversificação",
                   "Onde a carteira deixa de acessar produtos compatíveis com o volume, onde concentra risco e onde perde eficiência tributária."),
    "private": ("Estrutura, liquidez e sucessão",
                "Como o patrimônio está estruturado entre pessoa física, veículos e jurisdições, e o que isso implica em liquidez, tributação e sucessão."),
    "assessoria": ("Custo embutido, adequação e liquidez",
                   "Quanto a carteira paga em taxas que não aparecem no extrato, o quanto ela corresponde ao perfil declarado e se a liquidez cobre os próximos doze meses."),
}


def build(t, seg):
    set_date_ph("data_diagnostico")
    P = []
    papel = PAPEL[seg]
    foco_t, foco_d = FOCO[seg]

    P.append(cover_a4(t, "Diagnóstico", "de Carteira", "Sua", "Situação Atual",
                      [com_rotulo(t, ph("nome_cliente")),
                       "Patrimônio analisado &middot; " + ph("patrimonio_analisado"),
                       papel + " &middot; " + ph("nome_responsavel"),
                       ph("data_diagnostico")], grafismo=2))

    P.append(page_a4(t, "Abertura", 2, """<span class="eyebrow">Como lemos a sua carteira</span>
<h1 class="t">Escopo e método</h1>
<p class="lead">Este diagnóstico compara a sua carteira atual com a carteira que faria sentido para os seus objetivos, o seu horizonte e a sua tolerância a risco &mdash; sem julgamento sobre decisões passadas.</p>
<h2>O que foi analisado</h2>
%(fluxo)s
<h2>Foco deste diagnóstico &mdash; %(ft)s</h2>
<p class="small mut">%(fd)s</p>
<div class="cols2">
  <div>
    <h2>Base de dados</h2>
    <div class="dl">
      <dt>Instituições</dt><dd>%(inst)s</dd>
      <dt>Data de corte</dt><dd>%(corte)s</dd>
      <dt>Documentos</dt><dd>%(docs)s</dd>
      <dt>Não incluído</dt><dd>%(fora)s</dd>
    </div>
  </div>
  <div>
    <h2>Neste documento</h2>
    <ol class="toc">%(toc)s</ol>
  </div>
</div>""" % dict(
        fluxo=flow([(ph("etapa_%s_prazo" % k), n, ph("etapa_%s" % k)) for n, k in
                    [("Coleta", "coleta"), ("Consolidação", "consolidacao"),
                     ("Análise", "analise"), ("Proposta", "proposta")]]),
        ft=foco_t, fd=foco_d, inst=ph("instituicoes_analisadas"), corte=ph("data_corte"),
        docs=ph("documentos_base"), fora=ph("ativos_fora_do_escopo"),
        toc="".join('<li><span class="n">%02d</span><span>%s</span><span class="d"></span><span class="p">%02d</span></li>'
                    % (i, n, pg) for i, (n, pg) in enumerate([
                        ("Perfil, objetivos e restrições", 3), ("Fotografia da carteira atual", 4),
                        ("Pontos fortes e pontos de atenção", 5), ("Riscos e concentração", 6),
                        ("Custos e eficiência tributária", 7), ("Carteira proposta", 8),
                        ("Plano de transição", 9), ("Notas e avisos", 10)], start=1)))))

    P.append(page_a4(t, "Perfil e objetivos", 3, """<span class="eyebrow">Ponto de partida</span>
<h1 class="t">Perfil, objetivos e restrições</h1>
<p class="lead">Tudo o que vem depois neste documento se apoia nas informações abaixo. Se alguma delas estiver errada, a proposta muda.</p>
<div class="cols2">
  <div>
    <h2>Quem é você como investidor</h2>
    <div class="dl">
      <dt>Perfil (suitability)</dt><dd>%(perf)s</dd>
      <dt>Horizonte principal</dt><dd>%(hor)s</dd>
      <dt>Experiência</dt><dd>%(exp)s</dd>
      <dt>Renda x despesa</dt><dd>%(renda)s</dd>
      <dt>Reserva de emergência</dt><dd>%(res)s</dd>
      <dt>Capacidade de aporte</dt><dd>%(aporte)s</dd>
    </div>
  </div>
  <div>
    <h2>Restrições declaradas</h2>
    <div class="dl">
      <dt>Liquidez mínima</dt><dd>%(liq)s</dd>
      <dt>Classes vetadas</dt><dd>%(veto)s</dd>
      <dt>Situação tributária</dt><dd>%(trib)s</dd>
      <dt>Obrigações futuras</dt><dd>%(obrig)s</dd>
      <dt>Outros patrimônios</dt><dd>%(outros)s</dd>
      <dt>Observações</dt><dd>%(obs)s</dd>
    </div>
  </div>
</div>
<h2>Objetivos priorizados</h2>
%(tab)s""" % dict(
        perf=ph("perfil_investidor"), hor=ph("horizonte_principal"), exp=ph("experiencia_investimentos"),
        renda=ph("relacao_renda_despesa"), res=ph("reserva_emergencia"), aporte=ph("capacidade_aporte_mensal"),
        liq=ph("liquidez_minima"), veto=ph("classes_vetadas"), trib=ph("situacao_tributaria"),
        obrig=ph("obrigacoes_futuras"), outros=ph("outros_patrimonios"), obs=ph("observacoes_perfil"),
        tab=table(["#", "Objetivo", "Valor-alvo", "Prazo", "Prioridade", "Situação hoje"],
                  [[str(i), ph("obj_%d_descricao" % i), ph("obj_%d_valor" % i), ph("obj_%d_prazo" % i),
                    '<span class="pill">' + ph("obj_%d_prioridade" % i) + "</span>", ph("obj_%d_situacao" % i)]
                   for i in (1, 2, 3, 4)], nums=[2]))))

    P.append(page_a4(t, "Carteira atual", 4, """<span class="eyebrow">Fotografia</span>
<h1 class="t">Como está a sua carteira hoje</h1>
<p class="lead">Posição consolidada em %(corte)s, somando todas as instituições informadas.</p>
%(kpis)s
<div class="gap"></div>
<h2>Composição por classe e instituição</h2>
%(tab)s
<div class="cols2u" style="flex:1 1 auto;align-items:stretch;margin-top:5mm">
  %(ch)s
  %(ch2)s
</div>""" % dict(
        corte=ph("data_corte"),
        kpis=kpis([("Patrimônio analisado", ph("patrimonio_analisado"), ph("qtd_ativos") + " ativos"),
                   ("Instituições", ph("qtd_instituicoes"), "Contas: " + ph("qtd_contas")),
                   ("Retorno 12 meses", ph("retorno_12m_atual"), "% CDI: " + ph("retorno_12m_pct_cdi")),
                   ("Custo total anual", ph("custo_total_anual"), ph("custo_total_perc") + " a.a.")]),
        tab=table(["Classe", "Instituição", "Valor", "% do total", "Liquidez", "Retorno 12m", "Custo a.a."],
                  [[ph("at_%d_classe" % i), ph("at_%d_instituicao" % i), ph("at_%d_valor" % i),
                    ph("at_%d_perc" % i), ph("at_%d_liquidez" % i), ph("at_%d_ret12m" % i), ph("at_%d_custo" % i)]
                   for i in range(1, 8)],
                  foot=["<strong>Total</strong>", "", ph("patrimonio_analisado"), "100,0%", "&mdash;",
                        ph("retorno_12m_atual"), ph("custo_total_perc")],
                  nums=[2, 3, 5, 6], sm=True),
        ch=chart("Composição atual", "Peso de cada classe no patrimônio total.",
                 "donut", "min-height:44mm", series=["Renda fixa", "Multimercado", "Renda variável BR", "Internacional", "FIIs", "Alternativos"]),
        ch2=chart("Liquidez da carteira", "Quanto do patrimônio está disponível em D+0, até 30 dias, até 1 ano e acima disso.", "bars", "min-height:44mm"))))

    P.append(page_a4(t, "Diagnóstico", 5, """<span class="eyebrow">Leitura</span>
<h1 class="t">Pontos fortes e pontos de atenção</h1>
<p class="lead">O que já funciona e deve ser preservado, e o que custa dinheiro ou risco desnecessário hoje.</p>
<h2>O que está bem construído</h2>
%(fortes)s
<h2>O que merece atenção</h2>
%(tab)s
<div class="gap"></div>
<div class="note"><p><strong>Resumo em uma frase.</strong> %(resumo)s</p></div>""" % dict(
        fortes=cards([(ph("forte_%d_titulo" % i), ph("forte_%d_detalhe" % i)) for i in (1, 2, 3)]),
        tab=table(["Gravidade", "Ponto de atenção", "Por que importa", "Impacto estimado", "Encaminhamento"],
                  [['<span class="pill %s">%s</span>' % (cls, ph("aten_%d_gravidade" % i)),
                    ph("aten_%d_titulo" % i), ph("aten_%d_motivo" % i),
                    ph("aten_%d_impacto" % i), ph("aten_%d_acao" % i)]
                   for i, cls in [(1, "rk"), (2, "rk"), (3, "at"), (4, "at"), (5, "at")]], nums=[3]),
        resumo=ph("resumo_diagnostico"))))

    P.append(page_a4(t, "Riscos", 6, """<span class="eyebrow">Exposições</span>
<h1 class="t">Riscos e concentração</h1>
<p class="lead">Onde a carteira está concentrada e qual seria o efeito de um cenário adverso em cada frente.</p>
<h2>Concentração por emissor e contraparte</h2>
%(tab)s
<h2>Outras concentrações</h2>
<div class="cols2">
  <div>%(tab2)s</div>
  <div>%(tab3)s</div>
</div>
<div class="gap"></div>
<div class="note"><p><strong>Cobertura do FGC.</strong> %(fgc)s</p></div>""" % dict(
        tab=table(["Emissor / contraparte", "Exposição", "% do total", "Rating", "Coberto pelo FGC", "Limite sugerido"],
                  [[ph("emis_%d_nome" % i), ph("emis_%d_valor" % i), ph("emis_%d_perc" % i),
                    ph("emis_%d_rating" % i), ph("emis_%d_fgc" % i), ph("emis_%d_limite" % i)]
                   for i in (1, 2, 3, 4, 5)], nums=[1, 2, 5], sm=True),
        tab2=table(["Prazo", "Valor", "%"],
                   [[n, ph("prazo_%s_valor" % k), ph("prazo_%s_perc" % k)] for n, k in
                    [("Até 1 ano", "1a"), ("1 a 3 anos", "3a"), ("3 a 5 anos", "5a"), ("Acima de 5 anos", "5mais")]],
                   nums=[1, 2]),
        tab3=table(["Moeda", "Valor", "%"],
                   [[n, ph("moeda_%s_valor" % k), ph("moeda_%s_perc" % k)] for n, k in
                    [("Real (BRL)", "brl"), ("Dólar (USD)", "usd"), ("Euro (EUR)", "eur"), ("Outras", "out")]],
                   nums=[1, 2]),
        fgc=ph("texto_cobertura_fgc"))))

    P.append(page_a4(t, "Custos", 7, """<span class="eyebrow">Eficiência</span>
<h1 class="t">Custos e eficiência tributária</h1>
<p class="lead">Todo custo é aceitável desde que entregue algo em troca. Abaixo, o que a carteira paga hoje e o que dá para recuperar.</p>
<h2>Custos identificados</h2>
%(tab)s
<h2>Eficiência tributária</h2>
%(tab2)s
<div class="gap"></div>
%(kpis)s""" % dict(
        tab=table(["Origem do custo", "Onde incide", "Custo a.a.", "Em R$/ano", "Contrapartida", "Recuperável"],
                  [[ph("custo_%d_origem" % i), ph("custo_%d_onde" % i), ph("custo_%d_perc" % i),
                    ph("custo_%d_reais" % i), ph("custo_%d_contrapartida" % i), ph("custo_%d_recuperavel" % i)]
                   for i in (1, 2, 3, 4, 5)],
                  foot=["<strong>Total</strong>", "", ph("custo_total_perc"), ph("custo_total_anual"), "", ph("custo_recuperavel_total")],
                  nums=[2, 3, 5], sm=True),
        tab2=table(["Situação", "Diagnóstico", "Oportunidade"],
                   [[n, ph("trib_%s_diag" % k), ph("trib_%s_op" % k)] for n, k in
                    [("Come-cotas em fundos", "comecotas"), ("Ativos isentos de IR", "isentos"),
                     ("Prejuízo acumulado a compensar", "prejuizo"), ("Marcação e prazo para alíquota mínima", "prazo")]]),
        kpis=kpis([("Custo atual", ph("custo_total_anual"), ph("custo_total_perc") + " a.a."),
                   ("Custo na proposta", ph("custo_proposto_anual"), ph("custo_proposto_perc") + " a.a."),
                   ("Economia estimada", ph("economia_estimada_ano"), "Por ano"),
                   ("Em 10 anos", ph("economia_estimada_10a"), "Com reinvestimento")]))))

    P.append(page_a4(t, "Proposta", 8, """<span class="eyebrow">Recomendação</span>
<h1 class="t">Carteira proposta</h1>
<p class="lead">Alocação sugerida para o perfil %(perf)s e os objetivos declarados, com o efeito esperado de cada mudança.</p>
%(tab)s
<div class="gap"></div>
<div class="cols2u" style="flex:1 1 auto;align-items:stretch">
  %(ch)s
  <div style="display:flex;flex-direction:column;gap:4mm">
    <div class="note"><p><strong>O que muda na prática.</strong> %(muda)s</p></div>
    <div><h3>Retorno esperado</h3><p class="small mut">%(ret)s</p></div>
    <div><h3>Risco esperado</h3><p class="small mut">%(risco)s</p></div>
  </div>
</div>""" % dict(
        perf=ph("perfil_investidor"),
        tab=table(["Classe", "Hoje", "Proposto", "Variação", "Instrumento sugerido", "Por quê"],
                  [[c, ph("prop_%s_hoje" % k), ph("prop_%s_novo" % k), ph("prop_%s_var" % k),
                    ph("prop_%s_instrumento" % k), ph("prop_%s_motivo" % k)]
                   for c, k in [("Reserva e caixa", "caixa"), ("Renda fixa pós", "rfpos"),
                                ("Renda fixa inflação", "rfipca"), ("Renda fixa prefixada", "rfpre"),
                                ("Multimercado", "multi"), ("Renda variável BR", "rvbr"),
                                ("Internacional", "intl"), ("Alternativos", "alt")]],
                  foot=["<strong>Total</strong>", "100,0%", "100,0%", "&mdash;", "", ""],
                  nums=[1, 2, 3], sm=True),
        ch=chart("Atual x proposta", "Duas roscas comparando o peso de cada classe antes e depois da proposta.",
                 "donut", "min-height:50mm", series=["Renda fixa", "Multimercado", "Renda variável BR", "Internacional", "FIIs", "Alternativos"]),
        muda=ph("texto_o_que_muda"), ret=ph("retorno_esperado_proposta"), risco=ph("risco_esperado_proposta"))))

    P.append(page_a4(t, "Transição", 9, """<span class="eyebrow">Execução</span>
<h1 class="t">Plano de transição</h1>
<p class="lead">Sair da carteira atual custa tempo e, às vezes, imposto. O plano abaixo respeita carências, vencimentos e o momento de mercado.</p>
<h2>Etapas</h2>
%(fluxo)s
<h2>Movimentos previstos</h2>
%(tab)s
<h2>Restrições de saída</h2>
%(cards)s
<div class="sig">
  <div class="ln">%(resp)s<br><span class="mut">%(papel)s &middot; %(cert)s</span></div>
  <div class="ln">%(data)s<br><span class="mut">%(marca)s</span></div>
</div>""" % dict(
        fluxo=flow([(ph("transicao_%d_quando" % i), ph("transicao_%d_titulo" % i),
                     ph("transicao_%d_detalhe" % i)) for i in (1, 2, 3, 4)]),
        tab=table(["Quando", "Movimento", "Ativo / posição", "Valor", "Custo da saída", "Destino"],
                  [[ph("tr_%d_quando" % i), ph("tr_%d_movimento" % i), ph("tr_%d_ativo" % i),
                    ph("tr_%d_valor" % i), ph("tr_%d_custo" % i), ph("tr_%d_destino" % i)]
                   for i in (1, 2, 3, 4, 5)], nums=[3, 4], sm=True),
        cards=cards([("Carências e vencimentos", ph("restricao_carencia")),
                     ("Imposto na saída", ph("restricao_imposto")),
                     ("Marcação a mercado", ph("restricao_marcacao"))]),
        resp=ph("nome_responsavel"), papel=papel, cert=ph("registro_cvm_ou_ancord"),
        data=ph("data_diagnostico"), marca=t["marca"])))

    P.append(page_a4(t, "Notas e avisos", 10, """<span class="eyebrow">Transparência</span>
<h1 class="t">Notas metodológicas e avisos</h1>
<h2>Premissas usadas</h2>
<ul class="small">
  <li>Retornos esperados por classe: %(prem1)s.</li>
  <li>Volatilidade e correlações: %(prem2)s.</li>
  <li>Inflação e juros projetados: %(prem3)s.</li>
  <li>Tributação considerada: %(prem4)s.</li>
  <li>Custos considerados na comparação: %(prem5)s.</li>
</ul>
<h2>Limitações deste diagnóstico</h2>
<p class="small mut">%(lim)s</p>
<h2>Avisos legais</h2>
<p class="legal">%(disc)s</p>
<p class="legal">As projeções e estimativas apresentadas são exercícios baseados em premissas explicitadas acima e não constituem promessa ou garantia de resultado. Rentabilidade passada não representa garantia de rentabilidade futura. Os produtos citados podem não contar com garantia do Fundo Garantidor de Créditos (FGC). Antes de investir, leia o regulamento, a lâmina, o prospecto e o formulário de informações complementares de cada produto.</p>
<p class="legal">Este material é destinado exclusivamente a %(cli)s e foi elaborado com base nas informações prestadas pelo próprio cliente e nos extratos fornecidos. Informações incompletas ou incorretas alteram as conclusões. É proibida a reprodução ou o compartilhamento total ou parcial sem autorização prévia e por escrito.</p>
<h2>Contato</h2>
<div class="dl">
  <dt>Responsável</dt><dd>%(resp)s &middot; %(cert)s</dd>
  <dt>Atendimento</dt><dd>%(canal)s</dd>
  <dt>E-mail</dt><dd>%(email)s</dd>
  <dt>Ouvidoria</dt><dd>%(ouv)s</dd>
  <dt>Razão social</dt><dd>%(razao)s &middot; CNPJ %(cnpj)s</dd>
</div>""" % dict(
        prem1=ph("premissa_retornos"), prem2=ph("premissa_risco"), prem3=ph("premissa_macro"),
        prem4=ph("premissa_tributacao"), prem5=ph("premissa_custos"), lim=ph("limitacoes_diagnostico"),
        disc=ph("disclaimer_regulatorio", "Texto aprovado pelo compliance para este segmento"),
        cli=ph("nome_cliente"), resp=ph("nome_responsavel"), cert=ph("registro_cvm_ou_ancord"),
        canal=ph("canal_atendimento"), email=ph("email_contato"), ouv=ph("canal_ouvidoria"),
        razao=ph("razao_social"), cnpj=ph("cnpj"))))

    return P
