# -*- coding: utf-8 -*-
from layout import *
from layout import _b64  # noqa: F401  (nome privado não vem no import *)

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


# O plano de trabalho do primeiro ciclo, por segmento.
#
# A consultoria patrimonial tem seis reuniões, agrupadas em três fases, e uma
# data sugerida em cada. É o planejador que o membro percorre do alinhamento ao
# fechamento do semestre; o número da reunião vira o nome do campo da data, e
# por isso mexer na ordem aqui renomeia campos.
#
# O private tem outra forma: nove etapas corridas, sem fase e sem data. O prazo
# é relativo — "Dia 1", "1º mês", "até 10 dias" —, porque o ciclo é anual e a
# agenda se combina na reunião. E a coluna que importa ali não é a pauta, é o
# objetivo estratégico de cada etapa: quem contrata um private quer ler por que
# cada conversa existe, não em que ordem elas acontecem.
PLANO_CICLO = {
    "consultoria": dict(
        colunas=["Reuniões", "Pauta", "Prazo", "Data sugerida"],
        chip_final=True,
        rodape=("Plano do primeiro ciclo. As datas são sugeridas e se ajustam à sua agenda; "
                "a pauta e o prazo de cada encontro são os mesmos para todo cliente."),
        blocos=[
            ("Estruturação", [
                (1, "1ª Reunião", "Alinhamento Consultoria", "Início da consultoria"),
                (2, "2ª Reunião", "KYC / Suitability", "Até 5 dias após o Alinhamento"),
                (3, "3ª Reunião", "Apresentação de Relatório",
                 "Até 10 dias após o KYC/Suitability"),
            ]),
            ("Acompanhamento", [
                (4, "4ª Reunião", "Acompanhamento de Estratégia",
                 "Até 60 dias após a Apresentação de Relatório"),
                (5, "5ª Reunião", "Planejamento Patrimonial e Sucessório",
                 "Até 2 semanas após os Resultados"),
            ]),
            ("Fechamento", [
                (6, "6ª Reunião", "Revisão de Portfólio",
                 "Até 60 dias após a Proteção Patrimonial"),
            ]),
        ],
    ),
    "private": dict(
        colunas=["Etapa", "Prazo", "Objetivo estratégico"],
        chip_final=False,
        rodape=("Plano do primeiro ciclo. Os prazos correm a partir do início da consultoria e "
                "as datas de cada encontro se combinam conforme a sua agenda."),
        blocos=[(None, [
            (None, "KYC/Suitability e Diagnóstico", "Dia 1",
             "Coleta de informações objetivas e subjetivas: perfil de risco, objetivos de vida, "
             "horizonte de investimento, liquidez necessária, estrutura familiar e histórico "
             "patrimonial."),
            (None, "Seguros e Proteção Patrimonial", "1º mês (recorrente)",
             "Avaliação de necessidades de proteção: seguro de vida, seguro sucessório, "
             "responsabilidade civil e coberturas relevantes ao patrimônio familiar."),
            (None, "Entrega da Proposta Estratégica", "Até 10 dias",
             "Apresentação do diagnóstico e proposta inicial de alocação, com avaliação técnica, "
             "contemplando o racional completo da carteira, projeções e próximos passos."),
            (None, "Alinhamento Operacional", "1º mês (mensal)",
             "Revisão dos primeiros movimentos da carteira, cronograma de execução e validação "
             "da alocação prática frente à proposta aprovada."),
            (None, "Wealth Planning / Tributário e Sucessório", "2º mês",
             "Reunião com advogado tributarista para mapear estruturas: holding, doação, "
             "testamento, previdência, governança familiar e eficiência tributária."),
            (None, "Revisão de Carteira e aderência à estratégia", "Mensal + trimestral",
             "Acompanhamento da carteira implementada, avaliando aderência à estratégia e "
             "eventuais ajustes."),
            (None, "Crédito, Liquidez e Eficiência de Caixa", "3º mês",
             "Avaliação de linhas de crédito, financiamento patrimonial, gestão de caixa e uso "
             "eficiente do balanço pessoal/familiar."),
            (None, "Governança Familiar e Consolidação Patrimonial", "4º mês",
             "Visão integrada do patrimônio: bancos, empresas, imóveis, sucessores, "
             "responsabilidades familiares e processo decisório."),
            (None, "Revisão Anual e Planejamento do Próximo Ciclo", "12º mês",
             "Fechamento do ciclo: performance anual, revisão de metas, planejamento tributário "
             "de fim de ano e agenda estratégica do próximo período."),
        ])],
    ),
}
# Alta renda e assessoria seguem o ciclo da consultoria patrimonial.
PLANO_CICLO["alta-renda"] = PLANO_CICLO["consultoria"]
PLANO_CICLO["assessoria"] = PLANO_CICLO["consultoria"]


# Os fatos da casa. Não são campos: não mudam de um cliente para o outro, e
# pedir que o consultor os digite a cada apresentação é convidar a divergência —
# uma versão diz uma custódia, a seguinte diz outra.
#
# O registro na CVM saiu da lista. Ele não é o que o cliente pergunta nesta
# página, e a habilitação de quem assina o relatório continua onde precisa
# estar: no pé dos documentos que a exigem.
CASA = dict(
    historia=("A AUVP Capital nasceu da metodologia da AUVP Escola. É a mesma leitura de "
              "investimento que ensinou milhares de pessoas a cuidar do próprio dinheiro, "
              "agora aplicada por um consultor ao lado de quem investe — com a casa remunerada "
              "pelo cliente, e não pelo produto."),
    fatos=[("Fundação", "2020"),
           ("Modelo de remuneração", "Fee based, percentual sobre o patrimônio orientado"),
           ("Custódia", "Banco BTG Pactual S.A.")],
    # A foto da sede, e não um espaço de imagem. É a mesma casa em toda
    # apresentação, então não há o que escolher — e o que se escolhia, na
    # prática, era entre mandar sem foto e mandar com a que estivesse à mão.
    # O arquivo sai de `scripts/institucional.py`, que só reduz o original da
    # landing page institucional: a proporção é a que o fotógrafo enquadrou.
    foto="assets/institucional/sede.jpg",
)

# O que a casa manda todo mês, para todo cliente do segmento. É padrão, então
# vem escrito; o que varia de um cliente para o outro entra na nota de baixo.
ENTREGAS = [
    ["Relatório mensal da carteira", "Mensal", "E-mail e WhatsApp",
     "Onde o patrimônio está, o que rendeu e o que mudou no mês."],
    ["Relatório macroeconômico", "Mensal", "E-mail e WhatsApp",
     "O cenário do período e o que ele muda — ou não — na sua estratégia."],
    ["Carteiras recomendadas", "Quando houver revisão", "Portal e WhatsApp",
     "A alocação sugerida para cada perfil, com o racional de cada classe."],
    ["Recomendações de renda fixa", "Semanal", "WhatsApp",
     "O que passou pelo filtro de emissor, prazo e taxa na semana."],
    ["Acesso ao seu consultor", "Quando precisar", "WhatsApp",
     "Dúvida de mercado, aporte que entrou, decisão para tomar."],
]


def build(t, seg):
    set_date_ph("data_apresentacao")
    S = []
    plano = PLANO_CICLO[seg]
    titulo, sub, pilares = PITCH[seg]
    papel = PAPEL[seg]

    S.append(cover_slide(t, "AUVP", titulo,
                         ph("subtitulo_apresentacao", "Ex.: proposta de atendimento"),
                         [ph("nome_cliente"), ph("nome_responsavel"), ph("data_apresentacao")]))

    S.append(divider_slide(t, 1, "Quem somos", "A casa, o time e o modelo de remuneração"))

    S.append(slide(t, "Quem somos", 3, """<span class="eyebrow">A casa</span>
<h1 class="t">%(tit)s</h1>
<div class="cols2u" style="flex:1 1 auto">
  <div>
    <p class="lead" style="margin-bottom:5mm">%(sub)s</p>
    <p class="small">%(hist)s</p>
  </div>
  <div>
    %(img)s
    <div class="dl" style="margin-top:6mm">%(fatos)s</div>
  </div>
</div>""" % dict(tit=titulo, sub=sub, hist=CASA["historia"],
                 fatos="".join("<dt>%s</dt><dd>%s</dd>" % (r, v) for r, v in CASA["fatos"]),
                 img='<img class="imgfixa" alt="Sede da AUVP Capital" '
                     'src="data:image/jpeg;base64,%s">' % _b64(CASA["foto"]))))


    S.append(divider_slide(t, 2, "Como trabalhamos", "Método, entregas e cadência"))

    S.append(slide(t, "Como trabalhamos", 6, """<span class="eyebrow">Método</span>
<h1 class="t">Do primeiro papo à carteira rodando</h1>
<div class="center">%(flow)s</div>
<div class="note"><p><strong>Prazo típico do ciclo completo.</strong> %(prazo)s</p></div>""" % dict(
        # Os nomes vêm de ENCONTROS, e não de uma lista à parte: o método e o
        # cronograma descrevem a mesma coisa, e nomeá-la de dois jeitos fazia o
        # cliente procurar na tabela uma "Transição" que lá se chama outra coisa.
        flow=flow([(ph("metodo_%d_prazo" % i), etapa, ph("metodo_%d_detalhe" % i))
                   for i, etapa in enumerate(
                       [l[2] for _, itens in plano["blocos"] for l in itens][:5], start=1)]),
        prazo=ph("prazo_implantacao"))))

    # O cronograma vinha num documento à parte, e quem ouvia a proposta saía com
    # dois arquivos para casar na cabeça: a apresentação, que diz o que a casa
    # faz, e o cronograma, que diz quando. Aqui ele entra na apresentação, logo
    # depois do método: as etapas acima viram datas na linha de baixo.
    #
    # Pauta e prazo são o processo da casa e vêm escritos — não há por que pedir
    # ao consultor que digite "KYC / Suitability" toda vez. O que muda de cliente
    # para cliente é a data de cada encontro, e é só isso que fica como campo.
    S.append(slide(t, "Como trabalhamos", 7, """<span class="eyebrow">%(seg)s</span>
<h1 class="t">Cronograma de reuniões</h1>
%(crono)s
<p class="legal" style="margin-top:4mm">%(rodape)s</p>""" % dict(
        seg=t["nome_full"], rodape=plano["rodape"],
        crono=cronograma(
            [(fase, [tuple(c for c in linha[1:]) + ((ph("reuniao_%d_data" % linha[0]),)
                                                    if plano["chip_final"] else ())
                     for linha in itens])
             for fase, itens in plano["blocos"]],
            plano["colunas"], chip_final=plano["chip_final"]))))

    S.append(slide(t, "Como trabalhamos", 8, """<h1 class="t">Por que %(nome)s</h1>
<div class="cards" style="--n:3;margin-bottom:8mm">%(pil)s</div>
<h2>O que você recebe todo mês</h2>
%(ent)s""" % dict(
        nome=t["nome"],
        pil="".join('<div class="card"><h4>%s</h4><p>%s</p></div>' % (a, b) for a, b in pilares),
        # As entregas são as mesmas para todo cliente do segmento: é o que a casa
        # manda todo mês, não o que se combina caso a caso. Vêm escritas, e o
        # único campo é a linha de baixo, para o consultor detalhar o que aquele
        # cliente recebe além disto.
        ent=table(["Entrega", "Frequência", "Como chega", "Para quê"], ENTREGAS, sm=True)
            + '<div class="note" style="margin-top:4mm"><p><strong>Para o seu caso.</strong> '
            + ph("entregas_detalhe", "O que este cliente recebe além do padrão") + "</p></div>")))

    # O slide de governança saiu: "quem propõe e quem aprova" descrevia uma
    # alçada que, na prática, é sempre a mesma — o consultor recomenda e o
    # cliente decide —, e a cadência de contato agora está no cronograma.
    S.append(divider_slide(t, 3, "Condições", "Planos, taxas e o que está incluído"))

    # A grade de três planos só existe na consultoria. No alta renda, no private e
    # na assessoria não há planos distintos para comparar: a condição é uma só,
    # negociada caso a caso, e três colunas iguais anunciavam uma escolha que o
    # cliente não tem.
    if seg == "consultoria":
        S.append(slide(t, "Condições", 11, """<span class="eyebrow">Planos</span>
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

    S.append(slide(t, "Condições", 12, """<span class="eyebrow">Time</span>
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

    S.append(slide(t, "Próximos passos", 13, """<h1 class="t">Como damos o primeiro passo</h1>
<div class="center">%(flow)s
<div class="note" style="margin:6mm 0"><p><strong>Nada começa antes da assinatura.</strong> %(assina)s</p></div>
<div><h2 style="margin-top:0">O que precisamos de você</h2>
<div class="cols3">%(need)s</div></div></div>""" % dict(
        flow=flow([(ph("passo_%d_prazo" % i), titulo, ph("passo_%d_detalhe" % i))
                   for i, titulo in enumerate(["Conversa inicial", "Diagnóstico", "Proposta",
                                               "Abertura e transferência"], start=1)]),
        # O aviso da assinatura é da casa e não muda: é o que separa a conversa
        # do serviço, e o cliente precisa ler isso antes da lista do que trazer.
        assina=("A consultoria começa a correr com o contrato assinado. Até lá, tudo o que "
                "acontece é conversa e diagnóstico — nenhuma recomendação é emitida, nenhuma "
                "conta é aberta e nada é cobrado."),
        # Eram três, e a terceira acabava sendo "o resto". O que o cliente
        # precisa reunir é uma lista: os documentos, os extratos de cada casa em
        # que ele investe hoje, e as apólices — que quase sempre ficam de fora
        # porque ninguém pensa em seguro como parte do patrimônio, e são elas que
        # dizem o que já está protegido.
        need="".join('<div class="card"><h4>%s</h4><p>%s</p></div>' % (a, ph(k))
                     for a, k in [("Documentos e cadastro", "requisito_cadastro"),
                                  ("Extratos das suas contas", "requisito_extratos"),
                                  ("Extrato internacional", "requisito_extrato_intl"),
                                  ("Apólices de seguro", "requisito_apolices"),
                                  ("Dívidas e compromissos", "requisito_compromissos"),
                                  ("Objetivos e prazos", "requisito_objetivos")]))))

    S.append(slide(t, "Contato", 14, """<div style="display:flex;gap:16mm;flex:1 1 auto;align-items:center">
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

    S.append(slide(t, "Avisos", 15, """<h1 class="t">Avisos importantes</h1>
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
