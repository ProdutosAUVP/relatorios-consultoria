# -*- coding: utf-8 -*-
"""Apresentação do consultor — plano Me Diz o Que Fazer.

Duas páginas: a primeira apresenta o consultor, a segunda o plano e a AUVP
Capital. Ao contrário dos outros documentos, este vem escrito: o texto dos
consultores e do segmento já existe. Só ficam como campo preenchível a foto e
os contatos, que não vieram nos originais.

Uma variante por consultor; os dados estão em `consultores.py`.
"""
from consultores import CONSULTORES
from layout import *

POR_SLUG = {c["slug"]: c for c in CONSULTORES}

PLANO = "Me Diz o Que Fazer"

# Este documento é entregue ao cliente, então não leva o aviso de
# confidencialidade que vale para os relatórios de carteira.
RODAPE = "AUVP Capital · Consultoria de investimentos"


def _paras(textos):
    return "".join("<p>%s</p>" % t for t in textos)


def _lista(itens, cls="lista"):
    return '<ul class="%s">%s</ul>' % (cls, "".join("<li>%s</li>" % i for i in itens))


def _banda(c):
    return """    %(foto)s
    <div class="rt-id">
      <div class="rule"></div>
      <span class="ey">%(plano)s</span>
      <h1>%(nome)s</h1>
      <p class="fn">%(papel)s na AUVP Capital</p>
    </div>""" % dict(foto=foto_consultor(c["slug"]), plano=PLANO,
                     nome=c["nome"], papel=c["papel"])


def _faixa(c):
    """Credenciais e contato numa faixa entre a banda e o texto."""
    formacao = list(c["graduacao"])
    especializacao = list(c["pos"])
    return """<div class="faixa">
  <div>
    <h3>Formação</h3>
    %(form)s
  </div>
  <div>
    <h3>%(rot2)s</h3>
    %(esp)s
    <div class="chips" style="margin-top:2.5mm">%(chips)s</div>
  </div>
  <div>
    <h3>Falar com %(primeiro)s</h3>
    <div class="dl">
      <dt>WhatsApp</dt><dd>%(whats)s</dd>
      <dt>E-mail</dt><dd>%(email)s</dd>
    </div>
  </div>
</div>""" % dict(
        form=_lista(formacao),
        rot2="Especialização e certificações" if especializacao else "Certificações",
        esp=_lista(especializacao) if especializacao else "",
        chips="".join('<span class="pill">%s</span>' % x for x in c["certificacoes"]),
        primeiro=c["nome"].split()[0],
        whats=ph("whatsapp_consultor"), email=ph("email_consultor"))


def _fluxo(c):
    return """<div class="fluxo">
  <h2>Sobre mim e meu propósito</h2>
  %(proposito)s
  <h2 class="n">Trajetória no mercado financeiro</h2>
  %(trajetoria)s
  <h2 class="n">Fora do escritório</h2>
  %(fora)s
</div>""" % dict(proposito=_paras(c["proposito"]),
                 trajetoria=_paras(c["trajetoria"]),
                 fora=_paras(c["fora"]))


PAGINA_SEGMENTO = """<span class="eyebrow">AUVP Capital &middot; Consultoria de investimentos</span>
<h1 class="t">Me Diz o Que Fazer</h1>
<p class="lead">Você tem um consultor de investimentos à disposição para dizer o que fazer com o seu dinheiro. A conta continua sendo sua e quem executa é você. O nosso trabalho é trazer a análise e a recomendação de cada decisão.</p>
<div class="cols2">
  <div>
    <h2>Como funciona no dia a dia</h2>
    %(funciona)s
  </div>
  <div>
    <h2>O que você pode pedir ao seu consultor</h2>
    %(pedir)s
  </div>
</div>
<div class="cols2">
  <div>
    <h2>O que já vem incluído</h2>
    %(incluido)s
  </div>
  <div>
    <h2>O que não faz parte deste plano</h2>
    %(fora)s
  </div>
</div>
<h2>Como pensamos investimento</h2>
<p class="small mut" style="margin-bottom:2.5mm">A AUVP Capital nasceu da metodologia da AUVP Escola. É ela que orienta cada recomendação que você recebe aqui.</p>
%(metodo)s
<div class="cols2" style="margin-top:4.5mm">
  <div>
    <h2>Como somos remunerados</h2>
    <p class="small">A AUVP Capital trabalha no modelo <em>fee based</em>: neste plano, a consultoria cobra <strong>0,075%% ao mês</strong> sobre o patrimônio orientado, o que dá <strong>0,9%% ao ano</strong>.</p>
    <p class="small">No modelo comissionado, o mais comum no mercado, quem indica o investimento é pago pelo produto que vende — quanto maior a comissão, maior o incentivo para oferecer justamente aquele produto e para sugerir troca na carteira mais vezes do que seria necessário.</p>
    <p class="small">No <em>fee based</em> esse conflito não aparece: a remuneração é a mesma seja qual for o investimento recomendado, e a comissão que a indicação geraria volta para a sua conta em forma de cashback. Como a taxa é um percentual do que você tem investido, a consultoria só ganha mais quando o seu patrimônio cresce.</p>
  </div>
  <div>
    <h2>Onde acompanhar a AUVP Capital</h2>
    <div class="dl">
      <dt>Instagram</dt><dd>@auvpcapital</dd>
      <dt>YouTube</dt><dd>@AUVPCapital</dd>
      <dt>Spotify</dt><dd>Podcast da AUVP Capital</dd>
    </div>
    <p class="small mut" style="margin-top:3mm">Sempre que precisar, é só mandar mensagem para o seu consultor.</p>
    <p class="legal" style="margin-top:3mm">¹ Referente às operações de renda variável na conta nacional. ² Sujeitos a análise de crédito. ³ Conforme disponibilidade; as condições devem ser consultadas.</p>
  </div>
</div>""" % dict(
    funciona=_lista([
        "O atendimento é pelo WhatsApp e funciona sob demanda: você chama quando precisa, sem depender da nossa agenda.",
        "Não tem limite de conversa nem dia certo para falar com a gente, e também não existe reunião marcada de tempos em tempos.",
        "Quem compra e quem vende é você, na sua conta. O consultor diz o que faz sentido, quanto e por quê, e fica com você tirando dúvida até a hora de executar.",
    ]),
    pedir=_lista([
        "Uma carteira recomendada, montada a partir do seu perfil de investidor e dos seus objetivos.",
        "Análise da carteira que você já tem, para saber o que vale manter e o que ficou repetido.",
        "Direcionamento dos aportes, para saber onde colocar o dinheiro que entrou este mês.",
        "As recomendações de renda fixa que a gente filtra toda semana.",
        "Explicação sobre um produto ou uma estratégia que você não entendeu.",
        "Dúvidas sobre mercado e notícias, e o que elas mudam na sua estratégia.",
    ]),
    incluido=_lista([
        "Cashback do spread da renda fixa e do aluguel de ações.",
        "Operações sem taxa de corretagem. ¹",
        "Carteiras recomendadas para diferentes perfis de investidor.",
        "Relatório semanal com seleção de notícias e análise de mercado.",
        "Relatório mensal com a análise do cenário macroeconômico.",
        "Acesso aos grupos fechados e aos eventos da AUVP Capital.",
        "Cartões de crédito AUVP Capital. ²",
        "Kinvo Premium por até 12 meses. ³",
    ]),
    fora=_lista([
        "O consultor não acompanha a sua carteira todo dia para agir sozinho quando o mercado se mexe. Ele responde quando você chama.",
        "Nenhuma ordem é executada por nós. A compra e a venda são sempre suas.",
        "O atendimento é por escrito. Ligações e reuniões periódicas não fazem parte do plano.",
        "Não há uma estratégia de alocação montada só para o seu caso, com ajustes conforme o cenário muda. Esse acompanhamento é o do <strong>Resolve Aí</strong>, o plano de consultoria completa para quem tem R$ 300 mil ou mais, com consultor dedicado e reuniões bimestrais.",
    ], cls="lista mut"),
    metodo='<div class="principios">%s</div>' % "".join(
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
    )),
)


def build(t, variante):
    set_date_ph("data_apresentacao")
    c = POR_SLUG[variante]
    return [
        page_retrato(t, 1, _banda(c), _faixa(c) + _fluxo(c), rodape=RODAPE),
        page_a4(t, "O plano e a AUVP Capital", 2,
                '<div class="densa">%s</div>' % PAGINA_SEGMENTO, rodape=RODAPE),
    ]
