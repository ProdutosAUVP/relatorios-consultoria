# -*- coding: utf-8 -*-
"""Os blocos com que se monta uma página nova, na ferramenta.

O diagnóstico e o macroeconômico não cabem num molde fixo. O diagnóstico muda
de forma conforme a carteira que se está lendo; o macro precisa abrir espaço
quando o mês traz um evento que ninguém previu — uma eleição, um choque de
juros, uma quebra. Antes disso, quem precisava de uma página a mais tinha duas
saídas ruins: espremer o assunto numa página existente ou pedir alteração no
gerador e esperar.

Aqui a ferramenta ganha uma página em branco no desenho da casa e um punhado de
blocos prontos para pôr nela. Não é um editor livre: cada bloco já vem
diagramado, e o que se escolhe é qual bloco e o que escrever dentro dele. É o
que evita que a página nova pareça de outro documento.

Cada bloco declara:

    nome        como aparece na lista de blocos
    descricao   o que ele é, numa frase
    html(i)     o HTML do bloco, com `i` distinguindo uma instância da outra
    campos(i)   os campos que ele traz, com rótulo e dica

O `i` é o que separa o terceiro bloco de texto do primeiro: os campos se chamam
`bl3_titulo` e `bl1_titulo`, e não colidem. A ferramenta escolhe o número.

`scripts/blocos.py` escreve tudo isto em `docs/blocos.json`, que é o que a
ferramenta lê. O gerador não usa esta biblioteca para montar modelo nenhum: ela
existe para a página que se monta depois.
"""
from layout import *


def _c(i, nome):
    return "bl%d_%s" % (i, nome)


def _campo(i, nome, rotulo, dica=""):
    return {_c(i, nome): dict(rotulo=rotulo, dica=dica)}


def _junta(*ds):
    fora = {}
    for d in ds:
        fora.update(d)
    return fora


# ------------------------------------------------------------------- texto

def _texto_html(i):
    return """<h2>%s</h2>
<p>%s</p>""" % (ph(_c(i, "titulo")), ph(_c(i, "texto")))


def _texto_campos(i):
    return _junta(_campo(i, "titulo", "Título do bloco"),
                  _campo(i, "texto", "Texto", "Um parágrafo corrido."))


def _texto2_html(i):
    return """<h2>%s</h2>
<div class="cols2">
  <p>%s</p>
  <p>%s</p>
</div>""" % (ph(_c(i, "titulo")), ph(_c(i, "texto_a")), ph(_c(i, "texto_b")))


def _texto2_campos(i):
    return _junta(_campo(i, "titulo", "Título do bloco"),
                  _campo(i, "texto_a", "Coluna da esquerda"),
                  _campo(i, "texto_b", "Coluna da direita"))


def _abertura_html(i):
    return """<span class="eyebrow">%s</span>
<h1 class="t">%s</h1>
<p class="lead">%s</p>""" % (ph(_c(i, "chapeu")), ph(_c(i, "titulo")), ph(_c(i, "lead")))


def _abertura_campos(i):
    return _junta(_campo(i, "chapeu", "Chapéu", "A linha pequena acima do título."),
                  _campo(i, "titulo", "Título da página"),
                  _campo(i, "lead", "Linha de abertura", "Uma ou duas frases."))


# ------------------------------------------------------------------ listas

def _topicos_html(i):
    return """<h2>%s</h2>
<ul class="lista">%s</ul>""" % (
        ph(_c(i, "titulo")),
        "".join("<li>%s</li>" % ph(_c(i, "item_%d" % k)) for k in (1, 2, 3, 4, 5)))


def _topicos_campos(i):
    return _junta(_campo(i, "titulo", "Título do bloco"),
                  *[_campo(i, "item_%d" % k, "Tópico %d" % k) for k in (1, 2, 3, 4, 5)])


def _marcos_html(i):
    return """<h2>%s</h2>
<ol class="tl">%s</ol>""" % (
        ph(_c(i, "titulo")),
        "".join("<li><h4>%s</h4><p>%s</p></li>"
                % (ph(_c(i, "marco_%d_titulo" % k)), ph(_c(i, "marco_%d_texto" % k)))
                for k in (1, 2, 3, 4)))


def _marcos_campos(i):
    return _junta(_campo(i, "titulo", "Título do bloco"),
                  *[c for k in (1, 2, 3, 4)
                    for c in (_campo(i, "marco_%d_titulo" % k, "Item %d — título" % k),
                              _campo(i, "marco_%d_texto" % k, "Item %d — texto" % k))])


# ------------------------------------------------------------- destaque

def _destaque_html(i):
    return '<div class="note"><p><strong>%s</strong> %s</p></div>' % (
        ph(_c(i, "titulo")), ph(_c(i, "texto")))


def _destaque_campos(i):
    return _junta(_campo(i, "titulo", "Chamada", "As primeiras palavras, em negrito."),
                  _campo(i, "texto", "Texto do destaque"))


def _kpis_html(i):
    return kpis([(ph(_c(i, "kpi_%d_rotulo" % k)), ph(_c(i, "kpi_%d_valor" % k)),
                  ph(_c(i, "kpi_%d_nota" % k))) for k in (1, 2, 3, 4)])


def _kpis_campos(i):
    return _junta(*[c for k in (1, 2, 3, 4)
                    for c in (_campo(i, "kpi_%d_rotulo" % k, "Número %d — rótulo" % k),
                              _campo(i, "kpi_%d_valor" % k, "Número %d — valor" % k),
                              _campo(i, "kpi_%d_nota" % k, "Número %d — nota" % k))])


# --------------------------------------------------------------- tabela

def _tabela_html(i):
    return """<h2>%s</h2>
%s""" % (ph(_c(i, "titulo")),
         table([ph(_c(i, "col_%d" % c)) for c in (1, 2, 3, 4)],
               [[ph(_c(i, "cel_%d_%d" % (l, c))) for c in (1, 2, 3, 4)]
                for l in (1, 2, 3, 4, 5)], sm=True))


def _tabela_campos(i):
    return _junta(_campo(i, "titulo", "Título do bloco"),
                  *[_campo(i, "col_%d" % c, "Cabeçalho da coluna %d" % c) for c in (1, 2, 3, 4)],
                  *[_campo(i, "cel_%d_%d" % (l, c), "Linha %d, coluna %d" % (l, c))
                    for l in (1, 2, 3, 4, 5) for c in (1, 2, 3, 4)])


# --------------------------------------------------------- gráfico e imagem

def _grafico(formato, rotulo):
    def html(i):
        return chart(ph(_c(i, "titulo")), "", formato, "min-height:52mm",
                     ident="bl%d" % i)
    return html, (lambda i: _campo(i, "titulo", "Título do gráfico"))


def _imagem_html(i):
    return imgbox("Imagem para este bloco.", "min-height:52mm", ident="bl%d" % i)


BLOCOS = {}


def _reg(chave, nome, descricao, html, campos):
    BLOCOS[chave] = dict(chave=chave, nome=nome, descricao=descricao, html=html, campos=campos)


_reg("abertura", "Abertura de página",
     "Chapéu, título e linha de abertura. Use no alto de uma página nova.",
     _abertura_html, _abertura_campos)
_reg("texto", "Texto", "Um título e um parágrafo corrido.", _texto_html, _texto_campos)
_reg("texto2", "Texto em duas colunas", "Um título e dois parágrafos lado a lado.",
     _texto2_html, _texto2_campos)
_reg("topicos", "Tópicos", "Um título e até cinco tópicos.", _topicos_html, _topicos_campos)
_reg("marcos", "Linha do tempo", "Quatro itens em sequência, com título e texto.",
     _marcos_html, _marcos_campos)
_reg("destaque", "Destaque", "Uma caixa com o fio da marca, para o que não pode passar batido.",
     _destaque_html, _destaque_campos)
_reg("kpis", "Números", "Quatro números com rótulo e nota.", _kpis_html, _kpis_campos)
_reg("tabela", "Tabela", "Quatro colunas e cinco linhas, com cabeçalho.",
     _tabela_html, _tabela_campos)
for _f, _n, _d in [("donut", "Gráfico de rosca", "A divisão de um todo em partes."),
                   ("bars", "Gráfico de barras", "Uma série ao longo do tempo."),
                   ("line", "Gráfico de linha", "Uma evolução ao longo do tempo.")]:
    _h, _c2 = _grafico(_f, _n)
    _reg("grafico_" + _f, _n, _d + " Você digita os valores e o desenho sai no documento.",
         _h, _c2)
_reg("imagem", "Imagem", "Um espaço para uma imagem que você envia.",
     _imagem_html, lambda i: {})
