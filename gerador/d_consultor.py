# -*- coding: utf-8 -*-
"""Apresentação do consultor.

Um documento longo, de leitura, e não um folheto. O cliente recebe uma peça
sobre a pessoa que vai cuidar do dinheiro dele: quem ela é, o que ela acredita,
o que ela já fez, o que o plano entrega e como a casa pensa investimento. É
texto corrido na maior parte, com o ritmo quebrado de página em página — o
retrato e as credenciais, a linha do tempo, as etiquetas, as duas colunas de
listas, a grade de princípios — para a leitura não virar bloco.

Oito páginas, nesta ordem:

    1  abertura, com retrato, declaração e credenciais
    2  o propósito, em texto corrido
    3  a trajetória, com a linha do tempo ao lado
    4  fora do escritório
    5  o plano: como funciona e o que se pode pedir
    6  o que vem incluído e o que não faz parte
    7  como a casa pensa investimento
    8  remuneração, canais e contato — a única no negativo

O gerador não conhece consultor nenhum: ele produz modelo, não documento
pronto. O consultor entra como campo, preenchido pela ferramenta ou à mão.
Os documentos nominais que já existem ficam em `documentos/consultores/`.

Duas formas, e a diferença é o quanto do plano já vem escrito:

- **Por plano da consultoria** — Se Vira Aí, Me Diz o Que Fazer e Resolve Aí,
  com o texto comercial de cada um.
- **Em branco, por segmento** — o plano também entra como campo, para o
  produto preencher com as suas condições.

O que vale para os dois lados fica escrito nas duas: o método de investimento
e a lógica do fee based são da casa, não do plano.
"""
import re

from layout import *


def _paras(textos, cls=""):
    c = ' class="%s"' % cls if cls else ""
    return "".join("<p%s>%s</p>" % (c, t) for t in textos)


def _lista(itens, cls="lista"):
    return '<ul class="%s">%s</ul>' % (cls, "".join("<li>%s</li>" % i for i in itens))


def _marcos(itens):
    return '<ol class="marcos">%s</ol>' % "".join(
        '<li><span class="q">%s</span><p>%s</p></li>' % (q, t) for q, t in itens)


def _tags(itens):
    return '<div class="tags">%s</div>' % "".join("<span>%s</span>" % i for i in itens)


def _link(href, texto):
    """Âncora sem enfeite: o Chromium leva o link para o PDF, e no papel o texto
    continua igual ao resto — cor e peso não mudam por ser clicável."""
    return '<a href="%s">%s</a>' % (href, texto)


def _whatsapp(numero):
    """O número mostrado é formatado para leitura; o link precisa dele limpo."""
    return _link("https://wa.me/%s" % re.sub(r"\D", "", numero), numero)


def _numerados(base, n, dica=""):
    return [ph("%s_%d" % (base, i), dica) for i in range(1, n + 1)]


def _consultor_vazio():
    """O consultor como campo, um por parágrafo do texto dele.

    As quantidades são fixas — quatro parágrafos de propósito, três de
    trajetória, três de vida fora do trabalho — porque a página tem altura
    fechada e foi acertada para caber o consultor de texto mais longo. Quem
    escrever menos deixa o campo em branco, e ele sai destacado no arquivo.
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
        proposito=_numerados("proposito", 4),
        formacao_paras=_numerados("qualificacoes", 2),
        trajetoria=_numerados("trajetoria", 3),
        fora_paras=_numerados("fora_do_escritorio", 3),
        interesses=_numerados("interesse", 6),
        # `modelo` separa as duas situações em que um contato vem vazio. No
        # modelo, vazio quer dizer "preencha aqui", e sai como campo destacado.
        # Num documento pronto quer dizer que a pessoa não tem aquele canal, e
        # a linha inteira sai fora — ninguém manda ao cliente um documento com
        # o telefone de ninguém escrito no lugar do telefone.
        modelo=True, whatsapp=None, email=None, instagram=None,
    )


def _contato(c, chave, rotulo, escreve):
    """A linha de contato, quando há o que pôr nela."""
    if c.get(chave):
        return "<dt>%s</dt><dd>%s</dd>" % (rotulo, escreve(c[chave]))
    if not c.get("modelo"):
        return ""
    return "<dt>%s</dt><dd>%s</dd>" % (rotulo, ph("%s_consultor" % chave))


# ----------------------------------------------------------------- páginas

def _abertura(c, t, plano, foto, indice):
    """Retrato e declaração no topo, credenciais em faixa, sumário no pé.

    O sumário não é enfeite: o documento tem oito páginas, e quem recebe
    precisa saber o que vem pela frente antes de começar a ler.
    """
    cred = []
    if c["graduacao"]:
        cred.append(("Formação", _lista(c["graduacao"])))
    if c["pos"]:
        cred.append(("Especialização", _lista(c["pos"])))
    cred.append(("Certificações",
                 '<div class="chips">%s</div>' % "".join(
                     '<span class="pill">%s</span>' % x for x in c["certificacoes"])))
    toc = "".join('<li><span class="n">%02d</span><span>%s</span><span class="d"></span>'
                  '<span class="p">%02d</span></li>' % (i, nome, pg)
                  for i, (nome, pg) in enumerate(indice, start=1))
    return """<div class="pf-topo">
  %(foto)s
  <div>
    <span class="ey">%(plano)s</span>
    <h1>%(nome)s</h1>
    <p class="papel">%(papel)s na %(marca)s</p>
  </div>
  <p class="frase">%(frase)s</p>
</div>
<div class="esp lg"></div>
<div class="cred" style="--n:%(nc)d">%(cred)s</div>
<div class="esp lg"></div>
<div>
  <h2>Neste documento</h2>
  <ol class="toc">%(toc)s</ol>
</div>""" % dict(
        foto=foto, plano=plano, nome=c["nome"], papel=c["papel"], marca=t["marca"],
        frase=c["frase"], nc=len(cred),
        cred="".join("<div><h3>%s</h3>%s</div>" % (t_, b) for t_, b in cred),
        toc=toc)


PAGINA_PROPOSITO = """<span class="eyebrow">Sobre mim</span>
<h1 class="t">O meu propósito</h1>
<div class="corrido">%(texto)s</div>"""

# A faixa de credenciais da abertura é a leitura rápida — diploma e sigla de
# certificação. Aqui vem o que a pessoa escreveu sobre a própria formação, por
# extenso, que é o que diz o que ela sabe fazer.
PAGINA_TRAJETORIA = """<span class="eyebrow">Percurso</span>
<h1 class="t">Formação e trajetória</h1>
<div class="cols2u" style="flex:1 1 auto;align-items:stretch">
  <div style="display:flex;flex-direction:column">
    <h2 style="margin-top:0">Formação acadêmica e qualificações</h2>
    <div class="corrido">%(formacao)s</div>
    <div class="esp lg"></div>
    <h2>No mercado financeiro</h2>
    <div class="corrido">%(texto)s</div>
  </div>
  <div class="side">
    <h3>Em marcos</h3>
    %(marcos)s
  </div>
</div>"""

PAGINA_FORA = """<span class="eyebrow">Fora do escritório</span>
<h1 class="t">Além dos investimentos</h1>
<div class="corrido">%(texto)s</div>%(extra)s
<div style="margin-top:auto;padding-top:10mm">
  <h2>O que me ocupa quando não é mercado</h2>
  %(tags)s
</div>"""

PAGINA_PLANO = """<span class="eyebrow">O seu plano</span>
<h1 class="t">%(plano)s</h1>
<p class="lead" style="max-width:none">%(resumo)s</p>
<div class="esp"></div>
<h2>Como funciona no dia a dia</h2>
<div class="corrido">%(funciona)s</div>%(pedir)s"""

BLOCO_PEDIR = """
<div class="esp"></div>
<div>
  <h2>O que você pode pedir ao seu consultor</h2>
  %(itens)s
</div>"""

PAGINA_INCLUIDO = """<span class="eyebrow">O combinado</span>
<h1 class="t">O que entra e o que não entra</h1>
<div class="cols2" style="flex:1 1 auto;align-items:start">
  <div>
    <h2>O que já vem incluído</h2>
    %(incluido)s
  </div>
  <div>
    <h2>O que não faz parte deste plano</h2>
    <p class="small mut">%(fora_lead)s</p>
    %(fora)s
  </div>
</div>
<p class="legal" style="margin-top:auto">%(notas)s</p>"""

PAGINA_CASA = """<span class="eyebrow">Metodologia</span>
<h1 class="t">Como pensamos investimento</h1>
<p class="lead" style="max-width:none">A %(marca)s nasceu da metodologia da AUVP Escola. É ela que orienta cada recomendação que você recebe aqui.</p>
<div class="esp"></div>
%(metodo)s"""

PAGINA_FECHO = """<span class="eyebrow">Transparência</span>
<h1 class="t">Como somos remunerados</h1>
<div class="corrido">%(remuneracao)s</div>
<div class="esp"></div>
<div class="cols2u" style="align-items:start">
  <div>
    <h2>Onde acompanhar a %(marca)s</h2>
    <p class="small mut" style="margin:0 0 3mm">%(canais_lead)s</p>
    <div class="dl">
      <dt>Instagram</dt><dd>%(instagram)s</dd>
      <dt>YouTube</dt><dd>%(youtube)s</dd>
      <dt>Spotify</dt><dd>%(spotify)s</dd>
    </div>
  </div>
  <div>
    <h2>Falar com %(primeiro)s</h2>
    <div class="dl">%(contatos)s</div>
    <p class="small mut" style="margin:4mm 0 0">Sempre que precisar, é só mandar mensagem para o seu consultor.</p>
  </div>
</div>
<div style="margin-top:auto">
  <p class="legal">%(notas)s</p>
</div>"""


# Os canais da casa. O endereço do Instagram e do YouTube sai do próprio
# identificador; o do Spotify é o do programa.
CANAIS = dict(
    instagram=_link("https://instagram.com/auvpcapital", "@auvpcapital"),
    youtube=_link("https://youtube.com/@AUVPCapital", "@AUVPCapital"),
    spotify=_link("https://open.spotify.com/show/4FUAeRg9G0ntPVDuC8Zpjp",
                  "Podcast da AUVP Capital"),
)

CANAIS_LEAD = ("A gente publica conteúdo aberto sobre mercado e investimentos "
               "nestes canais:")

# O método é da casa e vale em qualquer segmento, então fica escrito nas duas
# formas do documento. O texto é o da peça comercial, na íntegra.
METODO = '<div class="principios">%s</div>' % "".join(
    "<p><strong>%s.</strong> %s</p>" % (tit, txt) for tit, txt in (
        ("Longo prazo e Buy and Hold",
         "A gente investe para carregar. Compra bons ativos e fica com eles, deixando o tempo e os juros compostos fazerem o trabalho. Day trade e operação de curto prazo não entram nas nossas recomendações, e girar a carteira atrás de oportunidade rápida também não."),
        ("Empresas perenes",
         "Na renda variável, olhamos para empresas sólidas, com histórico e resultado consistente, que você consegue imaginar funcionando daqui a vinte anos. Negócio que depende de um momento específico do mercado para dar certo fica de fora."),
        ("Renda fixa bem escolhida",
         "Duas aplicações com a mesma taxa podem ser bem diferentes uma da outra. Antes de recomendar, a gente olha quem é o emissor, qual o prazo, qual o indexador e qual a garantia envolvida."),
        ("Diversificação",
         "Cada classe de ativo cumpre um papel na carteira. Umas protegem o patrimônio, outras geram renda, outras fazem ele crescer. Diversificar bem é distribuir o seu dinheiro entre esses papéis na proporção que faz sentido para o seu momento de vida."),
        ("Explicar antes de recomendar",
         "Toda recomendação vem com o motivo dela junto. A AUVP começou como escola de investimentos, e a gente continua achando que o cliente decide melhor quando entende o que está fazendo."),
    ))

NOTAS = ("¹ Referente às operações de renda variável na conta nacional. &nbsp; "
         "² Sujeitos a análise de crédito. &nbsp; "
         "³ Conforme disponibilidade. As condições devem ser consultadas.")

FORA_LEAD = ("Algumas coisas não estão incluídas aqui, e é melhor deixar isso "
             "combinado desde o começo.")

# A remuneração da casa, escrita por extenso. Vale nos três planos: o que muda
# entre eles é a taxa, que entra na primeira frase.
REMUNERACAO = [
    "A %(marca)s trabalha no modelo <em>fee based</em>. Neste plano, a consultoria cobra uma taxa sobre o patrimônio orientado, de <strong>%(mes)s ao mês</strong>, o que dá <strong>%(ano)s ao ano</strong>.",
    "No modelo comissionado, que é o mais comum no mercado, quem indica o investimento é pago pelo produto que vende. Quanto maior a comissão daquele produto, maior o incentivo para oferecer justamente ele, e para sugerir troca na carteira com mais frequência do que seria necessário. O interesse de quem recomenda acaba ficando diferente do interesse de quem investe.",
    "No <em>fee based</em> esse conflito não aparece. A nossa remuneração é a mesma seja qual for o investimento recomendado, então a escolha é feita só pelo que serve para você. A comissão que a indicação geraria volta para a sua conta em forma de cashback.",
    "E como a taxa é um percentual do que você tem investido, a consultoria só ganha mais quando o seu patrimônio cresce.",
]

# Os três planos da consultoria. O conteúdo é o da peça comercial de cada um.
# A página não muda de forma entre eles — muda o texto —, então trocar de plano
# é trocar este dicionário.
#
# `funciona` é texto corrido, não lista: são os parágrafos da peça, na ordem em
# que foram escritos. `pedir` é opcional, e só existe onde há consultor a quem
# pedir alguma coisa.
PLANOS = {
    "se-vira-ai": dict(
        plano="Se Vira Aí",
        rotulo="Se Vira Aí (autoatendimento)",
        resumo="Você investe com autonomia total, usando a plataforma e usufruindo dos benefícios de ser membro da AUVP Capital.",
        funciona=[
            "A decisão é sua, do começo ao fim: você escolhe o que comprar, quanto e quando, direto na plataforma.",
            "O material de apoio chega toda semana — curadoria de notícias e leitura do cenário — para você decidir com informação.",
            "O plano é o acesso à plataforma e aos benefícios de ser membro da casa. Recomendação individual e consultor designado são o assunto dos outros dois planos.",
        ],
        incluido=[
            "Uso da plataforma de investimentos.",
            "Cashback em renda fixa e aluguel de ações.",
            "Relatório semanal com curadoria de notícias e análise do cenário macroeconômico.",
            "Operações sem cobrança de corretagem. ¹",
            "Acesso a cartões de crédito AUVP Capital. ²",
            "Kinvo Premium por até 12 meses. ³",
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
        resumo="Você tem um consultor de investimentos à disposição para dizer o que fazer com o seu dinheiro. A conta continua sendo sua e quem executa é você. O nosso trabalho é trazer a análise e a recomendação de cada decisão.",
        funciona=[
            "O atendimento é pelo WhatsApp e funciona sob demanda. Quer dizer que você chama quando precisa, sem depender da nossa agenda. Recebeu um dinheiro para investir, ficou na dúvida sobre um ativo ou quer conferir se a carteira ainda faz sentido, é só mandar mensagem.",
            # A peça dizia aqui que não existe reunião marcada de tempos em
            # tempos. O fato continua no documento, na página do que não faz
            # parte do plano, que é onde ele se lê como combinado e não como
            # aviso. Nesta página, que é a de como o plano funciona, o mesmo
            # fato entra pelo lado afirmativo: o canal é um só, e é o WhatsApp.
            "Não tem limite de conversa nem dia certo para falar com a gente. O atendimento é feito exclusivamente pelo WhatsApp — é lá que o seu consultor está, e é para lá que você manda mensagem sempre que precisar.",
            "Quem compra e quem vende é você, na sua conta. O consultor diz o que faz sentido, quanto e por quê, e fica com você tirando dúvida até a hora de executar.",
        ],
        pedir=[
            "Uma carteira recomendada, montada a partir do seu perfil de investidor e dos seus objetivos.",
            "Análise da carteira que você já tem, para saber o que vale manter e o que ficou repetido.",
            "Direcionamento dos aportes, para saber onde colocar o dinheiro que entrou este mês.",
            "As recomendações de renda fixa que a gente filtra toda semana.",
            "Explicação sobre um produto ou uma estratégia que você não entendeu.",
            "Dúvidas sobre mercado e notícias, e o que elas mudam na sua estratégia.",
        ],
        incluido=[
            "Cashback do spread da renda fixa e do aluguel de ações.",
            "Operações sem taxa de corretagem. ¹",
            "Carteiras recomendadas para diferentes perfis de investidor.",
            "Relatório semanal com seleção de notícias e análise de mercado.",
            "Relatório mensal com a análise do cenário macroeconômico.",
            "Acesso aos grupos fechados e aos eventos da AUVP Capital.",
            "Cartões de crédito AUVP Capital. ²",
            "Kinvo Premium por até 12 meses. ³",
        ],
        fora=[
            "O consultor não acompanha a sua carteira todo dia para agir sozinho quando o mercado se mexe. Ele responde quando você chama.",
            "Nenhuma ordem é executada por nós. A compra e a venda são sempre suas.",
            "O atendimento é por escrito. Ligações e reuniões periódicas não fazem parte do plano.",
            "Você não tem uma estratégia de alocação montada só para o seu caso, com ajustes conforme o cenário muda. Esse acompanhamento é o do Resolve Aí, o plano de consultoria completa para quem tem R$ 300 mil ou mais, com consultor dedicado e reuniões bimestrais.",
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
        pedir=[
            "Uma estratégia de alocação montada para o seu caso, e não para um perfil médio.",
            "Revisão da carteira sempre que o cenário ou o seu momento de vida mudarem.",
            "Direcionamento dos aportes, com o racional de cada decisão junto.",
            "Leitura do que uma notícia ou um movimento de mercado muda — ou não muda — na sua estratégia.",
            "Apoio na decisão ao longo do tempo, e não só na hora de montar a carteira.",
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
        funciona=_numerados("funciona", 3, "Um parágrafo sobre como o plano funciona."),
        pedir=_numerados("pode_pedir", 6),
        incluido=_numerados("incluido", 8),
        fora=_numerados("nao_incluido", 4),
        mes=ph("taxa_mensal", "Ex.: 0,075%"), ano=ph("taxa_anual", "Ex.: 0,9%"),
        notas=ph("notas_de_rodape", "As ressalvas numeradas que os itens acima referenciam."),
    )


SEM_DATA = "-sem-data"


def variantes(temas, segmentos):
    """(sufixo, rótulo, tema) de cada variante.

    A lista mora aqui, e não em `build.py`, porque os planos são deste módulo:
    acrescentar um plano em `PLANOS` já o coloca no build.

    O modelo em branco sai também sem data. É o documento que o consultor manda
    para um cliente novo a qualquer momento, e uma data carimbada nele nasce
    vencida. Os planos continuam só com data: ali ela diz de quando são as
    condições comerciais.
    """
    return ([(chave, dados["rotulo"], "consultoria") for chave, dados in PLANOS.items()]
            + [v for seg in segmentos if seg != "consultoria"
               for v in ((seg, temas[seg]["nome_full"], seg),
                         (seg + SEM_DATA, temas[seg]["nome_full"] + ", sem data", seg))])


def paginas(t, variante, c=None, foto=None, primeiro=None):
    """As páginas do documento, na ordem, como (seção, corpo, opções).

    Separada do `build` porque os documentos nominais de
    `documentos/consultores/` montam as mesmas páginas com o consultor escrito
    em vez de campo, e não devem repetir esta composição.
    """
    data = True
    c = c or _consultor_vazio()
    foto = foto or foto_vaga()
    primeiro = primeiro or "o seu consultor"
    texto = PLANOS.get(variante) or _em_branco()

    # O sumário precisa do número real de cada página, e o número depende de
    # quais páginas existem — a do plano só traz "o que você pode pedir" quando
    # há consultor a quem pedir. Então a lista vem primeiro, e a abertura é
    # montada depois dela.
    corpo = [
        ("O meu propósito", "O propósito",
         PAGINA_PROPOSITO % dict(texto=_paras(c["proposito"])), dict(cls="plano")),
        ("Formação e trajetória", "Formação e trajetória",
         PAGINA_TRAJETORIA % dict(formacao=_paras(c["formacao_paras"]),
                                  texto=_paras(c["trajetoria"]),
                                  marcos=_marcos(c["marcos"])),
         dict(cls="plano")),
        ("Fora do escritório", "Fora do escritório",
         PAGINA_FORA % dict(
             texto=_paras(c["fora_paras"]), tags=_tags(c["interesses"]),
             # Onde o texto termina anunciando uma lista, a lista vem depois
             # dele, como no original — e não diluída dentro do parágrafo.
             extra=_lista(c["fora_lista"]) if c.get("fora_lista") else ""),
         dict(cls="plano")),
        ("O plano", texto["plano"],
         PAGINA_PLANO % dict(
             plano=texto["plano"], resumo=texto["resumo"],
             funciona=_paras(texto["funciona"]),
             pedir=(BLOCO_PEDIR % dict(itens=_lista(texto["pedir"]))) if texto.get("pedir") else ""),
         dict(cls="plano")),
        ("O combinado", "O que entra e o que não entra",
         PAGINA_INCLUIDO % dict(
             incluido=_lista(texto["incluido"]), fora_lead=FORA_LEAD,
             fora=_lista(texto["fora"], cls="lista mut"), notas=texto["notas"]),
         dict(cls="plano")),
        (t["marca"], "Como pensamos investimento",
         PAGINA_CASA % dict(marca=t["marca"], metodo=METODO), dict(cls="plano")),
        ("Transparência", "Como somos remunerados",
         PAGINA_FECHO % dict(
             remuneracao=_paras([p % dict(marca=t["marca"], mes=texto["mes"], ano=texto["ano"])
                                 for p in REMUNERACAO]),
             marca=t["marca"], canais_lead=CANAIS_LEAD, primeiro=primeiro,
             notas=texto["notas"],
             contatos=(_contato(c, "whatsapp", "WhatsApp", _whatsapp)
                       + _contato(c, "email", "E-mail",
                                  lambda e: _link("mailto:" + e, e))),
             **CANAIS),
         dict(cls="plano", dark=True)),
    ]

    indice = [(titulo, i) for i, (_, titulo, _, _) in enumerate(corpo, start=2)]
    abertura = ("O seu consultor",
                '<div class="perfil">%s</div>'
                % _abertura(c, t, texto["plano"], foto, indice),
                dict())
    return [abertura] + [(sec, corpo_, opts) for sec, _, corpo_, opts in corpo]


def build(t, variante):
    """`variante` é um plano da consultoria ou um segmento.

    Plano traz o texto comercial já escrito; segmento deixa também o plano em
    branco, para o produto preencher com as suas condições. Nos dois o
    consultor é campo.

    O sufixo `-sem-data` devolve a mesma variante sem a data no cabeçalho. Este
    documento não é de um período: uma apresentação carimbada nasce vencida, e
    quem imprime um lote hoje não quer refazê-lo em janeiro.
    """
    set_date_ph("data_apresentacao")

    data = not variante.endswith(SEM_DATA)
    if not data:
        variante = variante[:-len(SEM_DATA)]

    # Documento entregue ao cliente: sem o aviso de confidencialidade que vale
    # para os relatórios de carteira.
    rodape = t["nome_full"]

    return [page_a4(t, sec, i, corpo, rodape=rodape, data=data, **opts)
            for i, (sec, corpo, opts) in enumerate(paginas(t, variante), start=1)]
