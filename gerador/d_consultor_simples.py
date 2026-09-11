# -*- coding: utf-8 -*-
"""Apresentação do consultor, versão de uma página.

Uma folha só, sobre a pessoa e mais nada: retrato, nome, o que ela faz, um
texto corrido e como falar com ela. É o cartão que se manda antes de uma
primeira conversa, quando explicar o plano ainda não é o assunto — para isso
existe a apresentação completa, de três páginas, em `d_consultor`.

A diagramação segue o modelo que a casa já usava: fundo no negativo, retrato
em círculo cercado de anéis concêntricos no alto à esquerda, nome ao lado,
texto corrido justificado ocupando a largura inteira, contatos com ícone e,
no pé, a régua à esquerda e a marca à direita. Não tem cabeçalho corrido nem
numeração: a página é uma só, e o que estaria no topo já está nela.

As medidas saem das proporções do original — 285,8 x 357,2 mm — reescritas
para A4, que é o formato do resto do sistema.

Não tem data. Uma folha de apresentação de uma pessoa não é de um período, e
carimbar uma data nela só encurtaria a validade do arquivo.
"""
from d_consultor import _consultor_vazio, _link, _whatsapp, POR_SLUG
from layout import *  # noqa: F403

# Geometria, em mm sobre a folha A4, derivada das frações do original.
FOLHA = dict(
    margem=24.0,          # 11,3% da largura: onde começam texto, régua e ícones
    centro_x=50.7,        # centro do retrato, 24,1% da largura
    centro_y=58.5,        # 19,7% da altura
    raio_foto=29.0,       # o retrato ocupa 27,6% da largura
    raio_anel=50.0,       # os anéis vazam pela esquerda, como no original
    aneis=9,
)


def aneis(f=FOLHA):
    """Os anéis concêntricos em volta do retrato.

    São desenhados aqui, e não num SVG de assets, porque a medida deles
    depende do retrato: os raios saem do raio da foto até o ponto em que o
    conjunto sangra pela esquerda da página. O traço é branco e fraco — no
    original ele é dourado, mas amarelo sobre o verde não entra nestes
    documentos.
    """
    r0, r1, n = f["raio_foto"] + 2.0, f["raio_anel"], f["aneis"]
    passo = (r1 - r0) / (n - 1)
    circulos = "".join(
        '<circle cx="%(c)g" cy="%(c)g" r="%(r).2f"/>' % dict(c=r1, r=r0 + i * passo)
        for i in range(n))
    return ('<svg class="fl-aneis" viewBox="0 0 %(d)g %(d)g" '
            'style="left:%(x).2fmm;top:%(y).2fmm;width:%(w).2fmm;height:%(w).2fmm">'
            '%(c)s</svg>') % dict(
        d=r1 * 2, x=f["centro_x"] - r1, y=f["centro_y"] - r1, w=r1 * 2, c=circulos)


def _bio(c):
    """O texto corrido: o propósito de quem escreveu, e o fecho sobre a vida
    fora do trabalho. São os mesmos campos da apresentação completa — quem
    mantém `consultores.py` não escreve duas vezes."""
    return "".join("<p>%s</p>" % p for p in c["proposito"]) + "<p>%s</p>" % c["fora"]


# Ícones de contato: traço fino, dentro de um círculo, como no original.
ICONES = dict(
    email='<rect x="4.5" y="6.5" width="15" height="11" rx="1.5"/>'
          '<path d="M4.5 8.5 12 13.5 19.5 8.5"/>',
    telefone='<path d="M8.2 4.8c.6 0 1 .3 1.2.9l1 2.4c.2.5.1 1-.3 1.3l-1 .9c1 2 2.6 3.6 '
             '4.6 4.6l.9-1c.3-.4.8-.5 1.3-.3l2.4 1c.6.2.9.6.9 1.2v2.1c0 .8-.6 1.4-1.4 '
             '1.4C11.6 19.3 4.7 12.4 4.7 6.2c0-.8.6-1.4 1.4-1.4z"/>',
    instagram='<rect x="4.5" y="4.5" width="15" height="15" rx="4.5"/>'
              '<circle cx="12" cy="12" r="3.7"/><circle cx="16.7" cy="7.3" r=".9"/>',
)


def _contato(icone, texto):
    return ('<div class="fl-ct"><span class="ic"><svg viewBox="0 0 24 24">%s</svg></span>'
            '<span>%s</span></div>') % (ICONES[icone], texto)


# `data-sec` dá nome à página para o catálogo da ferramenta. As páginas normais
# tiram esse nome do cabeçalho corrido; esta não tem cabeçalho.
FOLHA_HTML = """<section class="page dark folha" data-sec="O seu consultor">
  <div class="grain"></div>
  %(aneis)s
  %(foto)s
  <div class="fl-nome">
    <h1>%(nome)s</h1>
    <p>%(papel)s</p>
  </div>
  <div class="fl-corpo">
    <div class="fl-bio">%(bio)s</div>
    <div class="fl-vao"></div>
    <div class="fl-contatos">%(contatos)s</div>
  </div>
  <div class="fl-pe"><span class="rule"></span>%(logo)s</div>
</section>"""


def _retrato(c, escrito, f=FOLHA):
    """O retrato entra recortado em círculo. Na versão em branco é o mesmo
    círculo vazio, para a página não mudar de forma."""
    pos = 'style="left:%.2fmm;top:%.2fmm;width:%.2fmm;height:%.2fmm"' % (
        f["centro_x"] - f["raio_foto"], f["centro_y"] - f["raio_foto"],
        f["raio_foto"] * 2, f["raio_foto"] * 2)
    if escrito:
        return '<div class="fl-foto" %s>%s</div>' % (pos, foto_consultor(c["slug"]))
    # A moldura vazia leva a classe `imgbox` para ser reconhecida como espaço de
    # imagem pelo catálogo da ferramenta, e para a foto enviada herdar a classe
    # que faz o recorte circular.
    return ('<div class="imgbox fl-foto" %s data-img="%d"><div class="cl">Retrato</div>'
            '<div class="cd">Foto vertical, recortada em círculo.</div></div>') % (
        pos, proximo_img())


def variantes(consultores, temas, segmentos):
    """Uma por consultor, escrita, e uma em branco por segmento.

    Não há variante por plano: esta folha não fala de plano nenhum.
    """
    return ([(c["slug"], c["nome"], "consultoria") for c in consultores]
            + [(seg, temas[seg]["nome_full"], seg) for seg in segmentos])


def build(t, variante):
    escrito = variante in POR_SLUG
    c = POR_SLUG[variante] if escrito else _consultor_vazio()

    contatos = [
        _contato("email", _link("mailto:" + c["email"], c["email"]) if c.get("email")
                 else ph("email_consultor")),
        _contato("telefone", _whatsapp(c["whatsapp"]) if c.get("whatsapp")
                 else ph("whatsapp_consultor")),
        _contato("instagram", ph("instagram_consultor", "@usuario")),
    ]

    return [FOLHA_HTML % dict(
        aneis=aneis(), foto=_retrato(c, escrito), nome=c["nome"], papel=c["papel"],
        bio=_bio(c), contatos="".join(contatos),
        logo=logo_svg(t, 9.0, cls="fl-logo"))]
