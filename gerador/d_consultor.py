# -*- coding: utf-8 -*-
"""Apresentação do consultor, numa folha só.

Uma página alta, de 210 por 1420 mm, com tudo: quem é a pessoa, o que ela
acredita, o que já fez, o que o plano entrega e como a casa pensa
investimento. Não é A4, e nem tenta ser — é uma folha de leitura corrida.

Antes eram oito páginas A4, e a divisão era o problema: oito quebras, oito
cabeçalhos repetidos e um vão no pé de cada uma, porque o texto de cada
pessoa tem um tamanho diferente e nenhum deles fecha a página exatamente.
Numa folha só o texto corre, e quem dá o ritmo são as faixas — o alto
escuro com o retrato, o corpo claro, a faixa do plano em fundo suave, o pé
escuro com os contatos.

Não há eyebrow sobre os títulos: sem cabeçalho corrido e sem numeração, o
título de cada seção já diz onde se está, e a linha acima dele só repetia.

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


def _nota_fora(texto, marca):
    """Onde este plano fica, numa caixa sob as duas colunas do que ele entrega.

    As colunas acima dizem o que entra e o que não entra. Isto não é nem uma
    coisa nem outra: é o lugar deste plano entre os três, e para onde ir quando
    se quer justamente o que não entra. A peça antiga dizia o mesmo como último
    item da lista de exclusões — "você não tem uma estratégia montada só para o
    seu caso" —, que era a última coisa que o cliente lia ali e vendia o plano
    de cima às custas do que ele acabou de contratar.

    Fora das colunas, a nota deixa de ser exclusão e vira o fecho da faixa. Mas
    à largura das duas colunas a linha passaria de noventa caracteres, então a
    caixa se divide por dentro: o primeiro parágrafo fica à esquerda, em corpo
    maior — é ele que situa o plano —, e o resto desce à direita. A divisão cai
    na mesma grelha das duas colunas de cima, e nenhuma frase é cortada no meio.

    Só o plano do meio tem esta nota; nos outros a chave não existe e a faixa
    termina nas colunas.
    """
    paras = [p % dict(marca=marca) for p in texto.get("fora_nota") or []]
    if not paras:
        return ""
    abre, resto = paras[0], paras[1:]
    return '<div class="lg-posicao"><p class="abre">%s</p><div>%s</div></div>' % (
        abre, "".join("<p>%s</p>" % r for r in resto))


def _marcos(itens):
    return '<ol class="marcos">%s</ol>' % "".join(
        '<li><span class="q">%s</span><p>%s</p></li>' % (q, t) for q, t in itens)


def _tags(itens):
    # As etiquetas saíram: eram o parágrafo acima repetido em palavras soltas,
    # numa fileira de cápsulas. A lista `interesses` continua nos dados.
    return ""
    # (o que segue ficou para referência do desenho antigo)
    """As etiquetas de interesse, quando há interesse a etiquetar.

    Sem itens não sai nada — nem a caixa. A lista é um resumo em palavras soltas
    do parágrafo logo acima, e há quem ache que ela repete o texto em vez de
    acrescentar; quem pensa assim deixa `interesses` vazio e fica só com o texto.
    """
    if not itens:
        return ""
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
        # Cinco linhas de cada, e não duas: quem tem uma graduação preenche uma
        # e deixa as outras em branco, que saem do documento sem deixar marca.
        # O teto existe porque a faixa de credenciais tem largura fechada, não
        # porque alguém deva ter cinco.
        graduacao=_numerados("formacao", 5),
        pos=_numerados("especializacao", 5),
        certificacoes=_numerados("certificacao", 5),
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


# Quantos caracteres cabem numa linha da faixa de credenciais, com ela em três
# colunas. É estimativa, e só serve para comparar um bloco com o outro.
CRED_LINHA = 38
CRED_CHIPS_POR_LINHA = 3


def _linhas(itens, chips=False):
    """Quantas linhas um bloco de credenciais ocupa, mais ou menos."""
    if chips:
        return -(-len(itens) // CRED_CHIPS_POR_LINHA)
    return sum(1 + (len(re.sub(r"<[^>]+>", "", i)) - 1) // CRED_LINHA for i in itens)


def _faixa_credenciais(c):
    """A faixa de credenciais, e em quantas colunas ela sai.

    Três blocos em três colunas é o caso comum. Mas quando um deles é bem mais
    alto do que os outros dois somados — três especializações, cada uma em duas
    linhas, ao lado de uma graduação de uma linha só —, as três colunas deixam
    dois buracos do tamanho da diferença. Nesse caso os dois blocos leves
    dividem uma coluna e o pesado fica com a outra, e a faixa fecha certa.

    Quem escrever pouco em tudo continua com as três colunas: a regra existe
    para o desequilíbrio, não para uniformizar.
    """
    blocos = []
    if c["graduacao"]:
        blocos.append(("Formação", _lista(c["graduacao"]), _linhas(c["graduacao"])))
    if c["pos"]:
        blocos.append(("Especialização", _lista(c["pos"]), _linhas(c["pos"])))
    blocos.append(("Certificações",
                   '<div class="chips">%s</div>' % "".join(
                       '<span class="pill">%s</span>' % x for x in c["certificacoes"]),
                   _linhas(c["certificacoes"], chips=True)))

    escreve = lambda bs: "<div>%s</div>" % "".join(
        "<h3>%s</h3>%s" % (rot, bloco) for rot, bloco, _ in bs)

    pesos = [n for _, _, n in blocos]
    if len(blocos) == 3 and max(pesos) > sum(pesos) - max(pesos):
        i = pesos.index(max(pesos))
        pesado = blocos[i]
        leves = blocos[:i] + blocos[i + 1:]
        # O bloco pesado vai para o lado que preserva melhor a ordem de
        # leitura: à esquerda se ele for o primeiro dos três, à direita se não.
        colunas = [escreve([pesado]), escreve(leves)] if i == 0 else \
                  [escreve(leves), escreve([pesado])]
        return "".join(colunas), 2

    return "".join(escreve([b]) for b in blocos), len(blocos)


def _contato(c, chave, rotulo, escreve):
    """A linha de contato, quando há o que pôr nela."""
    if c.get(chave):
        return "<dt>%s</dt><dd>%s</dd>" % (rotulo, escreve(c[chave]))
    if not c.get("modelo"):
        return ""
    return "<dt>%s</dt><dd>%s</dd>" % (rotulo, ph("%s_consultor" % chave))


# ------------------------------------------------------------------ a folha

FOLHA = """<section class="page longa" data-sec="Apresentação do consultor">
  <header class="lg-topo">
    <div class="grain"></div>
    <!-- O nome do plano saía por cima do nome da pessoa. É a apresentação do
         consultor: quem abre o documento quer saber quem é ele, e o plano se
         explica sozinho nas faixas de baixo. Fora que a folha vai para cliente
         que já contratou e para cliente que ainda não, e anunciar um plano no
         alto do retrato dava ao documento cara de peça de venda. -->
    <div class="lg-id">
      %(foto)s
      <div>
        <h1>%(nome)s</h1>
        <p class="papel">%(papel)s na %(marca)s</p>
        <p class="lg-frase">%(frase)s</p>
      </div>
    </div>
    <div class="lg-cred" style="--n:%(nc)d">%(cred)s</div>
  </header>

  <div class="lg-corpo">
    <div class="lg-sec">
      <h2>O meu propósito</h2>
      <div class="corrido">%(proposito)s</div>
    </div>
    <div class="esp"></div>
    <div class="lg-sec">
      <h2>Formação acadêmica e qualificações</h2>
      <div class="corrido">%(qualificacoes)s</div>
    </div>
    <div class="esp"></div>
    <div class="lg-sec">
      <h2>A minha trajetória no mercado financeiro</h2>
      <div class="cols2u" style="align-items:start">
        <div class="corrido">%(trajetoria)s</div>
        <div class="side"><h3 style="margin-top:0">Em marcos</h3>%(marcos)s</div>
      </div>
    </div>
    <div class="esp"></div>
    <div class="lg-sec">
      <h2>Além dos investimentos</h2>
      <div class="corrido">%(fora)s</div>%(fora_extra)s
      %(tags)s
    </div>
  </div>

  <div class="lg-faixa">
    <div class="lg-sec">
      <h2>%(plano)s</h2>
      <p class="lead">%(resumo)s</p>
    </div>
    <div class="esp"></div>
    <div class="lg-sec">
      <h2>Como funciona no dia a dia</h2>
      <div class="corrido">%(funciona)s</div>
    </div>%(pedir)s
    <div class="esp"></div>
    <div class="lg-sec">
      <div class="cols2">
        <div>
          <h2>O que já vem incluído</h2>
          %(incluido)s
        </div>
        <div>
          <h2>O que não faz parte deste plano</h2>
          <p class="small mut">%(fora_lead)s</p>
          %(nao_incluido)s
        </div>
      </div>%(fora_nota)s
      <p class="legal" style="margin-top:8mm">%(notas)s</p>
    </div>
  </div>

  <div class="lg-corpo">
    <div class="lg-sec">
      <h2>Como pensamos investimento</h2>
      <p class="lead" style="margin-bottom:7mm">A %(marca)s nasceu da metodologia da AUVP Escola. É ela que orienta cada recomendação que você recebe aqui.</p>
      %(metodo)s
    </div>
    <div class="esp"></div>
    <div class="lg-sec">
      <h2>Como somos remunerados</h2>
      <div class="corrido">%(remuneracao)s</div>
    </div>
  </div>

  <footer class="lg-pe">
    <div class="grain"></div>
    <div class="cols2u" style="align-items:start">
      <div>
        <h2>Onde acompanhar a %(marca)s</h2>
        <p class="small mut" style="margin:0 0 4mm">%(canais_lead)s</p>
        <div class="dl">
          <dt>Instagram</dt><dd>%(instagram)s</dd>
          <dt>YouTube</dt><dd>%(youtube)s</dd>
          <dt>Spotify</dt><dd>%(spotify)s</dd>
        </div>
      </div>
      <div>
        <h2>Falar com %(primeiro)s</h2>
        <div class="dl">%(contatos)s</div>
        <p class="small mut" style="margin:5mm 0 0">Sempre que precisar, é só mandar mensagem para o seu consultor.</p>
      </div>
    </div>
    <div class="lg-assina">
      %(data)s
      %(logo)s
    </div>
  </footer>
</section>"""

BLOCO_PEDIR = """
    <div class="esp"></div>
    <div class="lg-sec">
      <h2>O que você pode pedir ao seu consultor</h2>
      %(itens)s
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

# A remuneração da casa, escrita por extenso.
#
# Sem número: a taxa muda de plano para plano e de cliente para cliente, e um
# percentual impresso aqui vira a condição que o documento promete. O que esta
# seção explica é o modelo — por que fee based, e o que ele muda para quem
# investe —, e isso não depende de quanto se cobra. A taxa de cada caso se
# combina na proposta, que é onde ela pode ser negociada e revista.
REMUNERACAO = [
    "A %(marca)s trabalha no modelo <em>fee based</em>: a consultoria cobra uma taxa sobre o patrimônio orientado, combinada com você e escrita na proposta.",
    "No modelo comissionado, que é o mais comum no mercado, quem indica o investimento é pago pelo produto que vende. Quanto maior a comissão daquele produto, maior o incentivo para oferecer justamente ele, e para sugerir troca na carteira com mais frequência do que seria necessário. O interesse de quem recomenda acaba ficando diferente do interesse de quem investe.",
    "No <em>fee based</em> (modelo que praticamos) esse conflito não aparece. A nossa remuneração é a mesma seja qual for o investimento recomendado, então a escolha é feita só pelo que serve para você. A comissão que a indicação geraria volta para a sua conta em forma de cashback.",
    "E como a taxa é um percentual do que você tem investido, a consultoria só ganha mais quando o seu patrimônio cresce.",
]

# Os três planos da consultoria. O conteúdo é o da peça comercial de cada um.
#
# Só o Me Diz o Que Fazer sai em folha longa hoje (ver `variantes`). O Se Vira
# Aí e o Resolve Aí ficam escritos aqui de propósito, e não por esquecimento: é
# a peça comercial dos dois, aprovada, e apagá-la para o build ficar limpo
# significaria reescrevê-la do zero no dia em que a folha longa voltar a valer
# para eles. Quem mexer neles não tem como conferir na tela, então convém
# confirmar o texto com o produto antes.
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
        notas=NOTAS,
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
        ],
        fora_nota=[
            "Você está no Me Diz o Que Fazer, o plano intermediário da %(marca)s, entre o Se Vira Aí, o nosso plano de autoatendimento, e o Resolve Aí, o nosso plano de acompanhamento mais personalizado.",
            "No Me Diz o Que Fazer, você conta com o suporte da nossa equipe para cuidar dos seus investimentos dentro da proposta do plano. Caso busque uma estratégia de alocação mais personalizada para o seu caso, com um consultor dedicado e reuniões periódicas para acompanhamento da sua carteira e do cenário macroeconômico, esse acompanhamento faz parte do Resolve Aí.",
            "O Resolve Aí é exclusivo para clientes com patrimônio a partir de R$&nbsp;300 mil.",
        ],
        notas=NOTAS,
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
        notas=NOTAS,
    ),
}


def _em_branco():
    return dict(
        # O nome do plano saiu do alto da folha, mas a faixa que descreve o
        # plano continua abrindo com ele: ali é o título da seção, não um selo
        # sobre o retrato de quem assina.
        plano=ph("nome_plano", "O nome comercial do plano."),
        resumo=ph("plano_resumo", "Duas ou três frases sobre o que o cliente contrata."),
        funciona=_numerados("funciona", 3, "Um parágrafo sobre como o plano funciona."),
        pedir=_numerados("pode_pedir", 6),
        incluido=_numerados("incluido", 8),
        fora=_numerados("nao_incluido", 4),
        notas=ph("notas_de_rodape", "As ressalvas numeradas que os itens acima referenciam."),
    )


SEM_DATA = "-sem-data"


def variantes(temas, segmentos):
    """(sufixo, rótulo, tema) de cada variante.

    Dos três planos da consultoria, só o Me Diz o Que Fazer sai nesta folha. O
    Se Vira Aí e o Resolve Aí passam a ser atendidos pela folha de uma página,
    `d_consultor_simples`: são planos cujo consultor se apresenta, não explica
    um serviço página a página. O Me Diz o Que Fazer é a exceção porque é nele
    que o cliente precisa saber, escrito, o que pode pedir e o que não entra.

    Os modelos em branco por segmento continuam: não são planos, são a folha
    vazia para as outras marcas da casa preencherem com as condições delas. E
    saem também sem data — é o documento que o consultor manda para um cliente
    novo a qualquer momento, e uma data carimbada nele nasce vencida.
    """
    return ([("me-diz-o-que-fazer", PLANOS["me-diz-o-que-fazer"]["rotulo"], "consultoria")]
            + [v for seg in segmentos if seg != "consultoria"
               for v in ((seg, temas[seg]["nome_full"], seg),
                         (seg + SEM_DATA, temas[seg]["nome_full"] + ", sem data", seg))])


def folha(t, variante, c=None, foto=None, primeiro=None, data=True):
    """A folha inteira, num pedaço só de HTML.

    Recebe o consultor escrito ou monta o modelo em branco. Os documentos
    nominais de `documentos/consultores/` passam `c`, `foto` e o primeiro nome;
    o gerador não passa nada e continua sem saber o nome de ninguém.
    """
    c = c or _consultor_vazio()
    foto = foto or foto_vaga()
    primeiro = primeiro or "o seu consultor"
    texto = PLANOS.get(variante) or _em_branco()

    cred, ncred = _faixa_credenciais(c)

    return FOLHA % dict(
        # o alto
        foto=foto, nome=c["nome"], papel=c["papel"], plano=texto["plano"],
        marca=t["marca"], frase=c["frase"], nc=ncred, cred=cred,
        # a pessoa
        proposito=_paras(c["proposito"]),
        qualificacoes=_paras(c["formacao_paras"]),
        trajetoria=_paras(c["trajetoria"]), marcos=_marcos(c["marcos"]),
        fora=_paras(c["fora_paras"]),
        tags=('<div style="margin-top:7mm">%s</div>' % _tags(c["interesses"])
              if c["interesses"] else ""),
        # onde o texto termina anunciando uma lista, a lista vem depois dele,
        # como no original — e não diluída dentro do parágrafo
        fora_extra=(_lista(c["fora_lista"]) if c.get("fora_lista") else ""),
        # o plano
        resumo=texto["resumo"], funciona=_paras(texto["funciona"]),
        pedir=(BLOCO_PEDIR % dict(itens=_lista(texto["pedir"]))) if texto.get("pedir") else "",
        incluido=_lista(texto["incluido"]), fora_lead=FORA_LEAD,
        nao_incluido=_lista(texto["fora"], cls="lista mut"),
        fora_nota=_nota_fora(texto, t["marca"]), notas=texto["notas"],
        # a casa
        metodo=METODO,
        remuneracao=_paras([par % dict(marca=t["marca"]) for par in REMUNERACAO]),
        # o pé
        canais_lead=CANAIS_LEAD, primeiro=primeiro,
        contatos=(_contato(c, "whatsapp", "WhatsApp", _whatsapp)
                  + _contato(c, "email", "E-mail", lambda e: _link("mailto:" + e, e))),
        # Só a data, e do outro lado a marca — a logo. Escrever "AUVP Capital"
        # ao lado dela era dizer duas vezes a mesma coisa.
        data=('<span class="data">%s</span>' % ph("data_apresentacao")) if data else "<span></span>",
        logo=logo_svg(t, 8.0),
        **CANAIS)


def build(t, variante):
    """`variante` é um plano da consultoria ou um segmento.

    Plano traz o texto comercial já escrito; segmento deixa também o plano em
    branco, para o produto preencher com as suas condições. Nos dois o
    consultor é campo.

    O sufixo `-sem-data` devolve a mesma folha sem a data no pé. Este documento
    não é de um período: uma apresentação carimbada nasce vencida, e quem
    imprime um lote hoje não quer refazê-lo em janeiro.
    """
    set_date_ph("data_apresentacao")
    data = not variante.endswith(SEM_DATA)
    if not data:
        variante = variante[:-len(SEM_DATA)]
    return [folha(t, variante, data=data)]
