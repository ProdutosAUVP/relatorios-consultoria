# -*- coding: utf-8 -*-
"""Apresentação do consultor.

Três páginas: o consultor, o plano e a AUVP Capital. As duas últimas partilham
a escala `.plano`, e só a última roda no negativo — é o fecho do documento.

O documento existe em duas formas, e a diferença é só o quanto vem escrito:

- **Escrita**, uma por consultor do Me Diz o Que Fazer. O texto das pessoas e
  do plano já existe, e ficam preenchíveis apenas a data e os contatos. Os
  dados estão em `consultores.py`.
- **Em branco**, uma por segmento. Mesma diagramação, mas consultor, plano e
  limites entram como campo, então qualquer produto usa o documento com o seu
  consultor e as suas condições. É o que a ferramenta de preenchimento oferece
  fora do Me Diz o Que Fazer.

O que vale para os dois lados fica escrito nas duas: o método de investimento
e a lógica do fee based são da casa, não do plano.
"""
from consultores import CONSULTORES
from layout import *

POR_SLUG = {c["slug"]: c for c in CONSULTORES}


def _paras(textos):
    return "".join("<p>%s</p>" % t for t in textos)


def _lista(itens, cls="lista"):
    return '<ul class="%s">%s</ul>' % (cls, "".join("<li>%s</li>" % i for i in itens))


def _marcos(itens):
    return '<ol class="marcos">%s</ol>' % "".join(
        '<li><span class="q">%s</span><p>%s</p></li>' % (q, t) for q, t in itens)


def _tags(itens):
    return '<div class="tags">%s</div>' % "".join("<span>%s</span>" % i for i in itens)


def _numerados(base, n, dica=""):
    return [ph("%s_%d" % (base, i), dica) for i in range(1, n + 1)]


def _consultor_vazio():
    """O mesmo formato de `consultores.py`, com campo no lugar do texto.

    As quantidades são fixas — três marcos, dois parágrafos de propósito,
    quatro interesses — porque a página tem altura fechada e foi acertada
    para caber o consultor de texto mais longo. Quem preencher com menos
    deixa o campo em branco, e ele sai destacado no arquivo.
    """
    return dict(
        nome=ph("nome_consultor"),
        papel=ph("papel_consultor", "Consultor de investimentos, especialista, planejador…"),
        frase=ph("frase_consultor", "Uma frase em primeira pessoa sobre como você trabalha."),
        graduacao=_numerados("formacao", 2),
        pos=_numerados("especializacao", 2),
        certificacoes=_numerados("certificacao", 3),
        marcos=[(ph("marco_%d_quando" % i, "2016, Depois, Hoje…"), ph("marco_%d_texto" % i))
                for i in (1, 2, 3)],
        proposito=_numerados("proposito", 2),
        interesses=_numerados("interesse", 4),
        fora=ph("fora_do_escritorio", "Uma ou duas frases sobre a vida fora do trabalho."),
    )


def _pagina_consultor(c, t, plano, foto, primeiro):
    """Retrato e declaração no topo, credenciais em faixa, trajetória como
    linha do tempo e os interesses como fatos curtos no rodapé."""
    cred = []
    if c["graduacao"]:
        cred.append(("Formação", _lista(c["graduacao"])))
    if c["pos"]:
        cred.append(("Especialização", _lista(c["pos"])))
    cred.append(("Certificações",
                 '<div class="chips">%s</div>' % "".join(
                     '<span class="pill">%s</span>' % x for x in c["certificacoes"])))
    return """<div class="pf-topo">
  %(foto)s
  <div>
    <span class="ey">%(plano)s</span>
    <h1>%(nome)s</h1>
    <p class="papel">%(papel)s na %(marca)s</p>
  </div>
  <p class="frase">%(frase)s</p>
</div>
<div class="esp"></div>
<div class="cred" style="--n:%(nc)d">%(cred)s</div>
<div class="esp"></div>
<div class="cols2u">
  <div>
    <h2>Trajetória no mercado financeiro</h2>
    %(marcos)s
  </div>
  <div>
    <h2>O meu propósito</h2>
    %(proposito)s
  </div>
</div>
<div class="esp lg"></div>
<div class="pf-rodape">
  <div>
    <h3>Fora do escritório</h3>
    %(tags)s
  </div>
  <div>
    <h3>Falar com %(primeiro)s</h3>
    <div class="dl">
      <dt>WhatsApp</dt><dd>%(whats)s</dd>
      <dt>E-mail</dt><dd>%(email)s</dd>
    </div>
  </div>
  <p class="small mut desc">%(fora)s</p>
</div>""" % dict(
        foto=foto, plano=plano, nome=c["nome"], papel=c["papel"], marca=t["marca"],
        frase=c["frase"], nc=len(cred),
        cred="".join("<div><h3>%s</h3>%s</div>" % (t_, b) for t_, b in cred),
        marcos=_marcos(c["marcos"]), proposito=_paras(c["proposito"]),
        tags=_tags(c["interesses"]), fora=c["fora"], primeiro=primeiro,
        whats=ph("whatsapp_consultor"), email=ph("email_consultor"))


PAGINA_PLANO = """<h1 class="t">%(plano)s</h1>
<p class="lead" style="max-width:none">%(resumo)s</p>
<div class="esp"></div>
<h2>Como funciona no dia a dia</h2>
%(funciona)s
<div class="esp"></div>
<div class="cols2">
  <div>
    <h2>O que está incluído</h2>
    %(incluido)s
  </div>
  <div>
    <h2>O que não está incluído</h2>
    %(fora)s
  </div>
</div>"""

PAGINA_CASA = """<h1 class="t">Como pensamos investimento</h1>
<p class="lead" style="max-width:none">A %(marca)s nasceu da metodologia da AUVP Escola. É ela que orienta cada recomendação que você recebe aqui.</p>
<div class="esp"></div>
%(metodo)s
<div class="esp"></div>
<h2>Como somos remunerados</h2>
<div class="cols2">
  <div>
    <p class="small">A %(marca)s trabalha no modelo <em>fee based</em>: neste plano, a consultoria cobra <strong>%(mes)s ao mês</strong> sobre o patrimônio orientado, o que dá <strong>%(ano)s ao ano</strong>. Como a taxa é um percentual do que você tem investido, a consultoria só ganha mais quando o seu patrimônio cresce.</p>
  </div>
  <div>
    <p class="small">No modelo comissionado, quem indica o investimento é pago pelo produto que vende. No <em>fee based</em> esse conflito não aparece: a remuneração é a mesma seja qual for a recomendação, e a comissão que ela geraria volta para a sua conta em forma de cashback.</p>
  </div>
</div>
<div class="esp"></div>
<h2>Onde acompanhar a %(marca)s</h2>
<div class="cols2">
  <div class="dl">
    <dt>Instagram</dt><dd>@auvpcapital</dd>
    <dt>YouTube</dt><dd>@AUVPCapital</dd>
    <dt>Spotify</dt><dd>Podcast da AUVP Capital</dd>
  </div>
  <div>
    <p class="small mut" style="margin:0">Sempre que precisar, é só mandar mensagem para o seu consultor.</p>
  </div>
</div>
<div style="margin-top:auto">
  <p class="legal">%(notas)s</p>
</div>"""

# O método é da casa e vale em qualquer segmento, então fica escrito nas duas
# formas do documento.
METODO = '<div class="principios">%s</div>' % "".join(
    "<p><strong>%s.</strong> %s</p>" % (tit, txt) for tit, txt in (
        ("Longo prazo e Buy and Hold",
         "A gente investe para carregar. Day trade e operação de curto prazo não entram nas recomendações, e girar a carteira atrás de oportunidade rápida também não."),
        ("Empresas perenes",
         "Na renda variável, olhamos para empresas sólidas, com histórico e resultado consistente, que você consegue imaginar funcionando daqui a vinte anos."),
        ("Renda fixa bem escolhida",
         "Duas aplicações com a mesma taxa podem ser bem diferentes. Antes de recomendar, olhamos o emissor, o prazo, o indexador e a garantia."),
        ("Diversificação",
         "Cada classe cumpre um papel: proteger, gerar renda, fazer crescer. Diversificar é distribuir entre esses papéis na proporção do seu momento de vida."),
        ("Explicar antes de recomendar",
         "Toda recomendação vem com o motivo junto. A AUVP começou como escola, e o cliente decide melhor quando entende o que está fazendo."),
    ))

NOTAS = ("¹ Sujeito a análise de crédito. &nbsp; ² As condições e a disponibilidade do Kinvo "
         "devem ser consultadas. &nbsp; ³ Referente às operações de renda variável na conta nacional.")

# Os três planos da consultoria. O conteúdo é o da tabela comercial: descrição,
# taxa, o que está incluído e o que não está. A página não muda de forma entre
# eles — muda o texto —, então trocar de plano é trocar este dicionário.
PLANOS = {
    "se-vira-ai": dict(
        plano="Se Vira Aí",
        rotulo="Se Vira Aí (autoatendimento)",
        resumo="Você investe com autonomia total, usando a plataforma e usufruindo dos benefícios de ser membro da AUVP Capital.",
        funciona=[
            "A decisão é sua, do começo ao fim: você escolhe o que comprar, quanto e quando, direto na plataforma.",
            "O material de apoio chega toda semana — curadoria de notícias e leitura do cenário — para você decidir com informação.",
            "Não há consultor designado nem recomendação individual. O plano é o acesso à plataforma e aos benefícios de membro.",
        ],
        incluido=[
            "Uso da plataforma de investimentos.",
            "Cashback em renda fixa e aluguel de ações.",
            "Relatório semanal com curadoria de notícias e análise do cenário macroeconômico.",
            "Operações sem cobrança de corretagem. ³",
            "Acesso a cartões de crédito AUVP Capital. ¹",
            "Kinvo Premium por até 12 meses. ²",
        ],
        fora=[
            "Suporte para dúvidas técnicas de investimentos.",
            "Monitoramento ativo da carteira.",
            "Estratégia de alocação personalizada.",
            "Gestão ativa.",
        ],
        mes="0,025% a 0,033%", ano="0,3% a 0,4%", notas=NOTAS,
    ),
    "me-diz-o-que-fazer": dict(
        plano="Me Diz o Que Fazer",
        rotulo="Me Diz o Que Fazer (básico)",
        resumo="Orientação em investimentos para quem quer clareza e direção na hora de montar ou ajustar a carteira. A conta continua sendo sua e quem executa é você.",
        funciona=[
            "O atendimento é pelo WhatsApp e funciona sob demanda: você chama quando precisa, sem depender da nossa agenda.",
            "Não tem limite de conversa nem dia certo para falar com a gente, e também não existe reunião marcada de tempos em tempos.",
            "Quem compra e quem vende é você, na sua conta. O consultor diz o que faz sentido, quanto e por quê, e fica com você tirando dúvida até a hora de executar.",
        ],
        incluido=[
            "Tudo o que você precisa para investir com estratégia profissional.",
            "Direcionamento para os seus investimentos, sob demanda.",
            "Carteiras recomendadas de acordo com o perfil do investidor.",
            "Recomendações semanais filtradas dos melhores investimentos em renda fixa.",
            "Atendimento para esclarecimento de dúvidas.",
            "Apoio para entender produtos, estratégias e organização da carteira.",
            "Relatórios mensais de análise do cenário macroeconômico.",
        ],
        fora=[
            "Monitoramento ativo da carteira.",
            "Estratégia de alocação personalizada.",
            "Gestão ativa.",
        ],
        mes="0,075%", ano="0,9%", notas=NOTAS,
    ),
    "resolve-ai": dict(
        plano="Resolve Aí",
        rotulo="Resolve Aí (consultoria completa)",
        resumo="Serviço de consultoria completa, com acompanhamento ativo, personalização e responsabilidade técnica sobre o patrimônio orientado.",
        funciona=[
            "Você tem um consultor dedicado, pelo WhatsApp, acompanhando a carteira junto com você.",
            "A estratégia de alocação é montada para o seu caso e vai sendo ajustada conforme o cenário e o seu momento mudam.",
            "A cada dois meses há uma reunião de alinhamento, além do contato contínuo ao longo do período.",
        ],
        incluido=[
            "Tudo o que você precisa para investir com estratégia profissional.",
            "Acompanhamento ativo da carteira.",
            "Estratégia de alocação personalizada.",
            "Ajustes contínuos conforme o cenário e o perfil.",
            "Atendimento com consultor dedicado via WhatsApp.",
            "Apoio contínuo na tomada de decisão ao longo do tempo.",
            "Reuniões bimestrais de alinhamento.",
        ],
        fora=[
            "A execução das ordens continua sendo sua: a consultoria recomenda, não opera pela sua conta.",
        ],
        mes="definida conforme o patrimônio orientado", ano="variável", notas=NOTAS,
    ),
}


def _em_branco():
    return dict(
        plano=ph("nome_plano", "O nome comercial do plano."),
        resumo=ph("plano_resumo", "Duas ou três frases sobre o que o cliente contrata."),
        funciona=_numerados("funciona", 3),
        incluido=_numerados("incluido", 7),
        fora=_numerados("nao_incluido", 4),
        mes=ph("taxa_mensal", "Ex.: 0,075%"), ano=ph("taxa_anual", "Ex.: 0,9%"),
        notas=ph("notas_de_rodape", "As ressalvas numeradas que os itens acima referenciam."),
    )


def build(t, variante):
    """`variante` é um consultor, um plano da consultoria ou um segmento.

    Consultor traz o texto da pessoa e o plano do Me Diz o Que Fazer; plano traz
    o texto comercial com o consultor em branco; segmento deixa os dois em
    branco, para o produto preencher com o seu consultor e as suas condições.
    """
    set_date_ph("data_apresentacao")

    if variante in POR_SLUG:
        c = POR_SLUG[variante]
        texto = PLANOS["me-diz-o-que-fazer"]
        foto, primeiro = foto_consultor(c["slug"]), c["nome"].split()[0]
    else:
        c = _consultor_vazio()
        texto = PLANOS.get(variante) or _em_branco()
        foto, primeiro = foto_vaga(), "o seu consultor"

    # Documento entregue ao cliente: sem o aviso de confidencialidade que vale
    # para os relatórios de carteira.
    rodape = t["nome_full"]

    return [
        page_a4(t, "O seu consultor", 1,
                '<div class="perfil">%s</div>'
                % _pagina_consultor(c, t, texto["plano"], foto, primeiro), rodape=rodape),
        page_a4(t, "O plano", 2, PAGINA_PLANO % dict(
            plano=texto["plano"], resumo=texto["resumo"],
            funciona=_lista(texto["funciona"]), incluido=_lista(texto["incluido"]),
            fora=_lista(texto["fora"], cls="lista mut")), rodape=rodape, cls="plano"),
        page_a4(t, t["marca"], 3, PAGINA_CASA % dict(
            marca=t["marca"], metodo=METODO, mes=texto["mes"], ano=texto["ano"],
            notas=texto["notas"]), rodape=rodape, cls="plano", dark=True),
    ]
