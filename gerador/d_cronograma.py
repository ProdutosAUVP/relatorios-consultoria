# -*- coding: utf-8 -*-
from layout import *

PAPEL = {"consultoria": "Consultor(a)", "alta-renda": "Consultor(a)",
         "private": "Banker", "assessoria": "Assessor(a)"}

RITMO = {
    "consultoria": [
        ("Reunião de acompanhamento", "Trimestral", "Revisão de carteira, rebalanceamento e ajuste de rota."),
        ("Relatório mensal", "Mensal", "Enviado por e-mail e WhatsApp até o 5º dia útil."),
        ("Revisão anual de perfil", "Anual", "Reaplicação do suitability e revisão de objetivos."),
        ("Contato sob demanda", "Quando precisar", "Canal direto com o consultor para dúvidas pontuais."),
    ],
    "alta-renda": [
        ("Reunião de acompanhamento", "Trimestral", "Revisão de carteira, oportunidades e rebalanceamento."),
        ("Relatório mensal", "Mensal", "Enviado por e-mail e WhatsApp até o 5º dia útil."),
        ("Revisão de estratégia", "Semestral", "Revisão de alocação estratégica e teses de longo prazo."),
        ("Ofertas e janelas", "Quando houver", "Contato pontual em ofertas com janela limitada."),
    ],
    "private": [
        ("Reunião de carteira", "Mensal", "Acompanhamento de performance, liquidez e movimentações."),
        ("Comitê de investimentos com a família", "Trimestral", "Alocação estratégica, riscos e decisões de maior porte."),
        ("Revisão patrimonial e sucessória", "Semestral", "Estruturas, jurisdições, seguros e plano sucessório."),
        ("Planejamento anual", "Anual", "Orçamento de liquidez, tributos do ano e metas da família."),
    ],
    "assessoria": [
        ("Reunião de acompanhamento", "Semestral", "Revisão da carteira, do perfil e dos objetivos."),
        ("Relatório mensal", "Mensal", "Enviado por e-mail e WhatsApp até o 5º dia útil."),
        ("Contato da mesa", "Quando houver", "Vencimentos, ofertas e ajustes pontuais na carteira."),
        ("Atendimento sob demanda", "Quando precisar", "Canal direto com o assessor para dúvidas e operações."),
    ],
}

MESES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
         "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]


def build(t, seg):
    set_date_ph("ano_vigencia")
    P = []
    papel = PAPEL[seg]

    P.append(cover_a4(t, "Cronograma", "de Reuniões", "Seu", "Acompanhamento",
                      [com_rotulo(t, ph("nome_cliente")),
                       papel + " &middot; " + ph("nome_responsavel"),
                       "Ciclo " + ph("ano_vigencia"),
                       ph("data_emissao")], grafismo=1))

    P.append(page_a4(t, "Como funciona", 2, """<span class="eyebrow">O acordo de acompanhamento</span>
<h1 class="t">Como funciona o seu acompanhamento</h1>
<p class="lead">Este documento fixa a cadência de contato do ciclo %(ano)s: o que acontece, quando acontece e o que cada encontro entrega. Nada aqui impede um contato extra quando você precisar.</p>
<h2>Ritmo do segmento %(nome)s</h2>
%(tab)s
<h2>Quem participa</h2>
%(tab2)s
<div class="gap"></div>
<div class="note"><p><strong>Antes de cada reunião.</strong> Você recebe a pauta e o material de apoio com %(ante)s de antecedência. Depois do encontro, enviamos o resumo com as decisões e os prazos acordados em até %(depois)s.</p></div>""" % dict(
        ano=ph("ano_vigencia"), nome=t["nome"],
        tab=table(["Encontro / entrega", "Frequência", "O que acontece", "Duração", "Formato"],
                  [[a, '<span class="pill">%s</span>' % b, c, ph("dur_%d" % i), ph("fmt_%d" % i)]
                   for i, (a, b, c) in enumerate(RITMO[seg], start=1)]),
        tab2=table(["Papel", "Nome", "Contato", "Quando aciona"],
                   [[n, ph("time_%s_nome" % k), ph("time_%s_contato" % k), ph("time_%s_quando" % k)]
                    for n, k in [(papel + " responsável", "principal"),
                                 ("Backup do time", "backup"),
                                 ("Mesa de renda fixa", "mesa"),
                                 ("Atendimento e operações", "ops")]]),
        ante=ph("antecedencia_pauta"), depois=ph("prazo_resumo_pos_reuniao"))))

    P.append(page_a4(t, "Calendário", 3, """<span class="eyebrow">Ciclo %(ano)s</span>
<h1 class="t">Calendário do ano</h1>
<p class="lead">Datas propostas para o ciclo. Confirmamos cada uma com pelo menos %(conf)s de antecedência.</p>
%(faixa)s
<div class="gap"></div>
%(tab)s""" % dict(
        ano=ph("ano_vigencia"), conf=ph("antecedencia_confirmacao"),
        faixa=year([ph("cal_%02d_tipo" % i) for i in range(1, 13)]),
        tab=table(["Mês", "Data prevista", "Encontro / entrega", "Pauta principal", "Entregável", "Status"],
                  [[m, ph("cal_%02d_data" % i), ph("cal_%02d_encontro" % i), ph("cal_%02d_pauta" % i),
                    ph("cal_%02d_entregavel" % i), '<span class="pill">' + ph("cal_%02d_status" % i) + "</span>"]
                   for i, m in enumerate(MESES, start=1)], sm=True))))

    P.append(page_a4(t, "As reuniões", 4, """<span class="eyebrow">O que esperar</span>
<h1 class="t">O que acontece em cada encontro</h1>
<p class="lead">Cada tipo de reunião tem uma pauta padrão. Você pode acrescentar temas até %(prazo)s antes da data.</p>
%(blocos)s
<h2>Como se preparar</h2>
%(fluxo)s""" % dict(
        prazo=ph("prazo_inclusao_pauta"),
        fluxo=flow([(ph("preparo_%s_quando" % k), n, ph("preparo_%s" % k)) for n, k in
                    [("Leia o material", "material"), ("Anote as dúvidas", "duvidas"),
                     ("Traga mudanças de vida", "mudancas"), ("Confirme presença", "confirmacao")]]),
        blocos="".join("""<h2>%s</h2>
<div class="cols2u">
  <div><h3>Pauta padrão</h3><p class="small mut">%s</p></div>
  <div><h3>Você sai com</h3><p class="small mut">%s</p></div>
</div>""" % (a, ph("pauta_%d" % i), ph("entrega_%d" % i))
                       for i, (a, b, c) in enumerate(RITMO[seg][:3], start=1)),
        )))

    P.append(page_a4(t, "Canais e prazos", 5, """<span class="eyebrow">Entre uma reunião e outra</span>
<h1 class="t">Canais, prazos e responsáveis</h1>
<p class="lead">Fora do calendário, é por aqui que falamos. Os prazos abaixo valem em dias úteis.</p>
<h2>Canais de atendimento</h2>
%(tab)s
<h2>Prazos de resposta</h2>
%(tab2)s
<div class="gap"></div>
<div class="note"><p><strong>Fora do horário e urgências.</strong> %(urg)s</p></div>
<h2>Ouvidoria e reclamações</h2>
<p class="small mut">%(ouv)s</p>""" % dict(
        tab=table(["Canal", "Para quê", "Horário", "Endereço / número"],
                  [[n, ph("canal_%s_para" % k), ph("canal_%s_horario" % k), ph("canal_%s_endereco" % k)]
                   for n, k in [("WhatsApp direto", "whats"), ("E-mail", "email"),
                                ("Telefone da central", "tel"), ("Portal do cliente", "portal")]]),
        tab2=table(["Tipo de solicitação", "Prazo de resposta", "Prazo de execução", "Quem responde"],
                   [[ph("sla_%d_tipo" % i), ph("sla_%d_resposta" % i), ph("sla_%d_execucao" % i), ph("sla_%d_quem" % i)]
                    for i in (1, 2, 3, 4)], nums=[1, 2]),
        urg=ph("procedimento_urgencia"), ouv=ph("texto_ouvidoria"))))

    P.append(page_a4(t, "Agendamento", 6, """<span class="eyebrow">Confirmação</span>
<h1 class="t">Agendar, remarcar e confirmar</h1>
<p class="lead">Use o link abaixo para escolher horários, remarcar um encontro ou pedir uma conversa fora do calendário.</p>
<div class="cols2u" style="align-items:start">
  <div>
    <h2>Regras de remarcação</h2>
    <ul class="small">
      <li>Avise com pelo menos %(rem)s de antecedência sempre que possível.</li>
      <li>Reuniões remarcadas são reagendadas dentro do mesmo mês de referência.</li>
      <li>%(rem2)s</li>
      <li>%(rem3)s</li>
    </ul>
    <h2>Registro das decisões</h2>
    <p class="small mut">%(reg)s</p>
    <h2>Revisão deste cronograma</h2>
    <p class="small mut">%(rev)s</p>
  </div>
  <div style="display:flex;flex-direction:column;align-items:center;gap:4mm">
    <div class="qr">QR code<br>agendamento</div>
    <div class="small mut" style="text-align:center">%(link)s</div>
  </div>
</div>
<div class="sig">
  <div class="ln">%(resp)s<br><span class="mut">%(papel)s &middot; %(cert)s</span></div>
  <div class="ln">%(cli)s<br><span class="mut">Cliente &middot; ciente do cronograma</span></div>
</div>
<div class="gap"></div>
<p class="legal">Este cronograma reflete o padrão de acompanhamento do segmento %(nome)s e pode ser ajustado de comum acordo. Datas previstas dependem de confirmação e podem mudar por indisponibilidade de qualquer das partes. Este documento não constitui recomendação de investimento. É proibida a reprodução ou o compartilhamento total ou parcial sem autorização prévia e por escrito. %(razao)s &middot; CNPJ %(cnpj)s.</p>""" % dict(
        rem=ph("antecedencia_remarcacao"), rem2=ph("regra_remarcacao_2"), rem3=ph("regra_remarcacao_3"),
        reg=ph("texto_registro_decisoes"), rev=ph("texto_revisao_cronograma"), link=ph("link_agendamento"),
        resp=ph("nome_responsavel"), papel=papel, cert=ph("registro_cvm_ou_ancord"),
        cli=ph("nome_cliente"), nome=t["nome"], razao=ph("razao_social"), cnpj=ph("cnpj"))))

    return P
