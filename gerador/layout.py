# -*- coding: utf-8 -*-
import os

from common import *
from common import _b64  # nome privado não vem no import *

# Placeholder de data usado no cabeçalho; cada documento define o seu.
DATE_PH = "mes_referencia"


def set_date_ph(name):
    global DATE_PH
    DATE_PH = name


# Cada espaço de imagem ganha um número dentro do documento. É o que deixa a
# ferramenta de preenchimento saber onde encaixar cada foto enviada.
_IMG = [0]


def reset_img():
    _IMG[0] = 0


def proximo_img():
    """O número do próximo espaço de imagem, para quem monta a moldura à mão."""
    _IMG[0] += 1
    return _IMG[0]

def logo_svg(t, h_mm, ink=False, cls=""):
    """A marca do Private Banking é muito mais larga que a do Capital; para as
    duas terem o mesmo peso visual a largura é derivada de uma altura-alvo."""
    svg = load_svg(t["logo"], "lg")
    return '<div class="logo%s%s" style="width:%.1fmm">%s</div>' % (
        " logo-ink" if ink else "", (" " + cls) if cls else "", h_mm * t["logo_ratio"], svg)


# Fração da caixa do SVG efetivamente ocupada por traço. Sem isto o grafismo fica
# menor do que a caixa e não alinha com nada. Os três arquivos saíram da mesma prancha
# e têm praticamente a mesma margem interna. Os valores do leque de quadrados vêm da
# geometria dos 22 retângulos; os outros dois, de rasterização a 2400 px com limiar
# no preto puro — medir com limiar mais alto perde os traços de 10% de opacidade e
# desalinha o grafismo em ~4 mm.
GRAF_INK = {
    1: dict(x0=0.0775, x1=0.9225, y0=0.0680, y1=0.9320, ratio=593.78 / 460.44),
    2: dict(x0=0.0754, x1=0.9242, y0=0.0661, y1=0.9334, ratio=593.78 / 460.44),
    3: dict(x0=0.0754, x1=0.9246, y0=0.0664, y1=0.9328, ratio=593.78 / 581.33),
}


def graf_span(n, x0_mm, x1_mm, y0_mm, opacidade=None):
    """Posiciona o grafismo para que o traço — e não a caixa do SVG — vá de
    x0_mm a x1_mm, começando em y0_mm. É assim que a referência alinha o
    grafismo da capa com a largura das réguas."""
    f = GRAF_INK[n]
    w = (x1_mm - x0_mm) / (f["x1"] - f["x0"])
    h = w / f["ratio"]
    style = "left:%.2fmm;top:%.2fmm;width:%.2fmm" % (x0_mm - f["x0"] * w, y0_mm - f["y0"] * h, w)
    if opacidade is not None:      # sobrepõe o padrão de 50% do componente
        style += ";opacity:%s" % ("%g" % opacidade).lstrip("0")
    return '<div class="graf" style="%s">%s</div>' % (style, load_svg("GRAFISMO %d.svg" % n, "g%d" % n))


# A capa e a divisória mostram o mesmo grafismo em lados opostos da dobra: a
# capa com o centro no canto inferior direito, a divisória no superior. Só
# continuam sendo o mesmo desenho se tiverem a mesma largura — com larguras
# diferentes os raios mudam, e os arcos cruzam a borda em pontos que não se
# encontram. Por isso a medida é uma só.
GRAF_SLIDE_W = 190.0


def graf_arcos(w_mm, canto="bottom-right", sangria=8.0):
    """O grafismo de arcos tem duas arestas retas (topo e direita). Como
    grafismo ele só pode mostrar arcos, então as duas retas saem sempre da
    página. 'bottom-right' espelha na vertical para pôr o centro dos arcos no
    canto inferior direito, como na capa do deck de referência."""
    f = GRAF_INK[3]
    h = w_mm / f["ratio"]
    fora_x = (1 - f["x1"]) * w_mm + sangria      # empurra a reta da direita para fora
    fora_y = f["y0"] * h + sangria               # empurra a reta do topo para fora
    if canto == "bottom-right":
        pos = "right:-%.2fmm;bottom:-%.2fmm;transform:scaleY(-1)" % (fora_x, fora_y)
    else:                                        # top-right, orientação nativa
        pos = "right:-%.2fmm;top:-%.2fmm" % (fora_x, fora_y)
    return '<div class="graf" style="%s;width:%.2fmm">%s</div>' % (
        pos, w_mm, load_svg("GRAFISMO 3.svg", "g3"))


# ---------------------------------------------------------------- A4

def cover_a4(t, kicker_light, kicker_bold, bottom_light, bottom_bold, ident_lines,
             grafismo=1, graf_opacidade=None):
    """Capa A4 nas medidas de "ref consultoria.svg": réguas em 86,0 e 245,2 mm,
    grafismo entre elas com exatamente a largura das réguas."""
    assert grafismo in (1, 2), "fora das capas só entra o grafismo de arcos; nas capas, 1 ou 2"
    ident = "".join("<div>%s</div>" % l for l in ident_lines)
    return """<section class="page cover">
  <div class="grain"></div>
  %(graf)s
  %(logo)s
  <h1 class="cv-t"><span class="lt">%(kl)s</span><span class="bd">%(kb)s</span></h1>
  <div class="cv-conf">%(confid)s</div>
  <div class="rule r1"></div>
  <div class="rule r2"></div>
  <div class="cv-b-t"><span style="font-weight:300">%(bl)s </span><span style="font-weight:800">%(bb)s</span></div>
  <div class="cv-id">%(ident)s</div>
</section>""" % dict(
        graf=graf_span(grafismo, 15.3, 194.7, 95.5, graf_opacidade),
        logo=logo_svg(t, 9.0, cls="cv-logo"), kl=kicker_light, kb=kicker_bold,
        confid=CONFID.replace(" · ", "<br>"), bl=bottom_light, bb=bottom_bold, ident=ident)


def page_a4(t, sec, no, body, date_ph=None, rodape=None, dark=False, cls="", data=True):
    """`data=False` tira a data do cabeçalho.

    Vale para material que não é de um período: uma apresentação com data
    carimbada nasce vencida, e quem imprime um lote hoje não quer refazê-lo em
    janeiro.
    """
    return """<section class="page%(cls)s%(dk)s">
  %(grain)s
  <header class="pg-head">
    <div class="sec">%(sec)s</div>
    <div class="rt">%(dt)s%(logo)s</div>
  </header>
  <div class="pg-body">
%(body)s
  </div>
  <footer class="pg-foot"><span class="no">%(no)s</span><span>%(confid)s</span></footer>
</section>""" % dict(dk=" dark" if dark else "", cls=" " + cls if cls else "",
                     grain='<div class="grain"></div>' if dark else "",
                     sec=sec, logo=logo_svg(t, 4.6, ink=not dark),
                     dt='<div class="dt">%s</div>' % ph(date_ph or DATE_PH) if data else "",
                     body=body, no="%02d" % no, confid=rodape or CONFID)


# ---------------------------------------------------------------- 16:9

def cover_slide(t, title_light, title_bold, subtitle, ident_lines):
    """Capa 16:9 nas medidas da página 1 de "MODELO SLIDES AUVP CAPITAL.pdf":
    faixa branca até 26,3 mm, régua curta em 68,4 mm, título 44,6 pt."""
    ident = "".join("<div>%s</div>" % l for l in ident_lines)
    lt = '<span class="lt">%s </span>' % title_light if title_light else ""
    return """<section class="slide dark cover">
  <div class="grain"></div>
  %(graf)s
  <div class="cv-band">%(rotulo)s%(logo)s</div>
  <div class="cv-block">
    <div class="rule"></div>
    <h1 class="cv-t">%(lt)s%(tb)s</h1>
    <div class="cv-sub">%(sub)s</div>
  </div>
  <div class="cv-foot"><div class="cf">%(confid)s</div><div class="id">%(ident)s</div></div>
</section>""" % dict(graf=graf_arcos(GRAF_SLIDE_W, "bottom-right"),
                     rotulo='<div class="nm">%s</div>' % t["rotulo"] if t["rotulo"] else "",
                     logo=logo_svg(t, 7.0, ink=True), lt=lt, tb=title_bold, sub=subtitle,
                     confid=CONFID, ident=ident)


def divider_slide(t, no, title, sub=""):
    return """<section class="slide dark divider">
  <div class="grain"></div>
  %(graf)s
  <div class="in" style="padding:12mm 16mm">
    <div style="margin-top:auto;margin-bottom:auto">
      <div class="dv-n">%(no)s</div>
      <div class="dv-t">%(title)s</div>
      %(sub)s
    </div>
    <div style="font-size:7.6pt;letter-spacing:.14em;text-transform:uppercase;opacity:.5">%(confid)s</div>
  </div>
</section>""" % dict(graf=graf_arcos(GRAF_SLIDE_W, "top-right"), no="%02d" % no,
                     title=title, confid=CONFID,
                     sub='<div class="dv-sub">%s</div>' % sub if sub else "")


def slide(t, sec, no, body, dark=False, date_ph=None):
    return """<section class="slide%(dk)s">
  %(grain)s
  <div class="in">
    <header class="pg-head">
      <div class="sec">%(sec)s</div>
      <div class="rt"><div class="dt">%(dt)s</div>%(logo)s</div>
    </header>
    <div class="pg-body">
%(body)s
    </div>
    <footer class="pg-foot"><span class="no">%(no)s</span><span>%(confid)s</span></footer>
  </div>
</section>""" % dict(dk=" dark" if dark else "", grain='<div class="grain"></div>' if dark else "",
                     sec=sec, dt=ph(date_ph or DATE_PH), logo=logo_svg(t, 6.3, ink=not dark), body=body,
                     no="%02d" % no, confid=CONFID)


# ---------------------------------------------------------------- blocos

def chart(label, desc, skeleton="bars", style="", series=None):
    sk = {"bars": '<div class="sk-bars">%s</div>' % "".join(
              '<i style="height:%d%%"></i>' % h for h in (42, 68, 55, 88, 72, 96)),
          "donut": '<div class="sk-donut"></div>',
          "line": '<div class="sk-line"></div>',
          "none": ""}[skeleton]
    # `flex` só tem efeito dentro de .pg-body (flex column); em grelha é ignorado.
    lg = legend(series) if series else ""
    _IMG[0] += 1
    return ('<div class="chart" data-img="%d" style="flex:1 1 auto;%s">%s'
            '<div class="cl">%s</div>'
            '<div class="cd">%s</div>%s</div>') % (_IMG[0], style, sk, label, desc, lg)


def foto_vaga(desc="Foto vertical do consultor. Recorte 3:4, mínimo 900&nbsp;px de largura."):
    """O lugar do retrato na versão sem consultor definido.

    Sai como espaço de imagem numerado, igual aos gráficos, para a ferramenta
    de preenchimento tratar os dois do mesmo jeito. A classe extra carrega a
    geometria do retrato — proporção e canto arredondado — e sobrevive à troca
    pela imagem enviada.
    """
    _IMG[0] += 1
    return ('<div class="imgbox rt-vaga" data-img="%d"><div class="cl">Retrato</div>'
            '<div class="cd">%s</div></div>') % (_IMG[0], desc)


def imgbox(desc, style=""):
    _IMG[0] += 1
    return ('<div class="imgbox" data-img="%d" style="flex:1 1 auto;%s">'
            '<div class="cl">Imagem</div>'
            '<div class="cd">%s</div></div>') % (_IMG[0], style, desc)


def table(headers, rows, foot=None, caption=None, nums=None, widths=None, sm=False, xs=False):
    nums = nums or []
    th = "".join('<th class="num">%s</th>' % h if i in nums else "<th>%s</th>" % h
                 for i, h in enumerate(headers))
    body = ""
    for r in rows:
        tds = "".join('<td class="num">%s</td>' % c if i in nums else "<td>%s</td>" % c
                      for i, c in enumerate(r))
        body += "<tr>%s</tr>" % tds
    tf = ""
    if foot:
        tf = "<tfoot><tr>%s</tr></tfoot>" % "".join(
            '<td class="num">%s</td>' % c if i in nums else "<td>%s</td>" % c
            for i, c in enumerate(foot))
    cap = '<caption>%s</caption>' % caption if caption else ""
    cg = ('<colgroup>%s</colgroup>' % "".join('<col style="width:%s%%">' % w for w in widths)) if widths else ""
    cls = (" xs" if xs else " sm" if sm else "") + (" fix" if widths else "")
    return '<table class="tb%s">%s%s<thead><tr>%s</tr></thead><tbody>%s</tbody>%s</table>' % (cls, cap, cg, th, body, tf)


def kpi(k, v, s="", n=4):
    return '<div class="kpi"><div class="k">%s</div><div class="v">%s</div><div class="s">%s</div></div>' % (k, v, s)


def kpis(items, n=4):
    return '<div class="kpis" style="--n:%d">%s</div>' % (n, "".join(kpi(*i) for i in items))


def cards(items, n=3):
    inner = "".join('<div class="card"><h4>%s</h4><p>%s</p></div>' % (a, b) for a, b in items)
    return '<div class="cards" style="--n:%d">%s</div>' % (n, inner)


def timeline(items):
    return '<ol class="tl">%s</ol>' % "".join(
        '<li><h4>%s</h4><p>%s</p></li>' % (a, b) for a, b in items)


def flow(itens, n=None):
    """Sequência de etapas sobre um trilho contínuo. Cada item é
    (etiqueta, título, descrição); a etiqueta costuma ser o prazo."""
    li = "".join('<li><span class="node"></span><span class="tag">%s</span>'
                 '<h4>%s</h4><p>%s</p></li>' % (a, b, c) for a, b, c in itens)
    return '<ol class="flow" style="--n:%d">%s</ol>' % (n or len(itens), li)


def legend(series):
    """Legenda de série usando a sequência de cores do segmento."""
    return '<ul class="legend">%s</ul>' % "".join(
        '<li><i style="background:var(--c%d)"></i>%s</li>' % (i, nome)
        for i, nome in enumerate(series[:6], start=1))


def hero(numero, legenda, apoio):
    """Um número em destaque e uma fileira de números de apoio."""
    return ('<div class="hero"><div class="n">%s</div><div class="l">%s</div></div>'
            '<div class="stats" style="--n:%d">%s</div>') % (
        numero, legenda, len(apoio),
        "".join('<div><div class="n">%s</div><div class="l">%s</div></div>' % (a, b) for a, b in apoio))


MESES_CURTOS = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
                "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


def year(eventos):
    """Faixa de doze meses em dois semestres. `eventos` traz o rótulo curto de
    cada mês; o detalhe fica na tabela abaixo."""
    return '<ol class="year">%s</ol>' % "".join(
        '<li class="on"><span class="mo">%02d</span><span class="nm">%s</span>'
        '<span class="ev">%s</span></li>' % (i, MESES_CURTOS[i - 1], ev)
        for i, ev in enumerate(eventos, start=1))


def foto_consultor(slug):
    """Retrato preparado por `scripts/fotos.py`, embutido em base64 para o
    modelo continuar abrindo sozinho."""
    return '<img class="rt-img" alt="" src="data:image/jpeg;base64,%s">' % _b64(
        os.path.join("assets", "consultores", slug + ".jpg"))
