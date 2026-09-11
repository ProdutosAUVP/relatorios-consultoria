# -*- coding: utf-8 -*-
"""Apresentação do consultor, versão simplificada.

Uma página só, sobre a pessoa e mais nada: retrato, nome, o que ela faz,
um texto corrido e como falar com ela. É o cartão de apresentação que se manda
antes de uma primeira conversa, quando explicar o plano ainda não é o assunto
— para isso existe a apresentação completa, de três páginas, em `d_consultor`.

A estrutura vem do modelo de referência que a casa já usava: carreira,
abordagem, vida fora do trabalho e contatos, nessa ordem, em texto corrido.
Aqui a mesma sequência entra na grelha do sistema, com o retrato e as
credenciais na coluna de apoio.

Não tem data. Uma folha de apresentação de uma pessoa não é de um período, e
carimbar uma data nela só encurtaria a validade do arquivo.
"""
from d_consultor import (_consultor_vazio, _link, _numerados, _tags, _whatsapp,
                         POR_SLUG)
from layout import *


def _bio(c):
    """O texto corrido: o propósito de quem escreveu, e o fecho sobre a vida
    fora do trabalho. São os mesmos campos da apresentação completa — quem
    mantém `consultores.py` não precisa escrever duas vezes."""
    return "".join("<p>%s</p>" % p for p in c["proposito"]) + \
        '<p class="mut">%s</p>' % c["fora"]


PAGINA = """<div class="sp-topo">
  %(foto)s
  <div>
    <h1>%(nome)s</h1>
    <p class="papel">%(papel)s na %(marca)s</p>
    <p class="frase">%(frase)s</p>
  </div>
</div>
<div class="esp"></div>
<div class="cols2u">
  <div class="sp-bio">%(bio)s</div>
  <div>
    <h2>Formação e certificações</h2>
    %(cred)s
    <h2>Fora do escritório</h2>
    %(tags)s
  </div>
</div>
<div class="esp lg"></div>
<div class="pf-rodape">
  <div>
    <h3>Falar com %(primeiro)s</h3>
    <div class="dl">
      <dt>WhatsApp</dt><dd>%(whats)s</dd>
      <dt>E-mail</dt><dd>%(email)s</dd>
    </div>
  </div>
  <div>
    <h3>Acompanhar</h3>
    <div class="dl">
      <dt>Instagram</dt><dd>%(insta)s</dd>
      <dt>%(marca_curta)s</dt><dd>%(site)s</dd>
    </div>
  </div>
</div>"""


def _credenciais(c):
    """Formação e especialização numa lista só, e as certificações em pílulas.
    Na página cheia elas ocupam uma faixa de três colunas; aqui, onde a coluna
    de apoio é estreita, ficam empilhadas."""
    itens = list(c["graduacao"]) + list(c["pos"])
    return ('<ul class="lista">%s</ul>' % "".join("<li>%s</li>" % i for i in itens)
            + '<div class="chips" style="margin-top:3mm">%s</div>' % "".join(
                '<span class="pill">%s</span>' % x for x in c["certificacoes"]))


def variantes(consultores, temas, segmentos):
    """Uma por consultor, escrita, e uma em branco por segmento.

    Não há variante por plano: esta folha não fala de plano nenhum.
    """
    return ([(c["slug"], c["nome"], "consultoria") for c in consultores]
            + [(seg, temas[seg]["nome_full"], seg) for seg in segmentos])


def build(t, variante):
    if variante in POR_SLUG:
        c = POR_SLUG[variante]
        foto, primeiro = foto_consultor(c["slug"]), c["nome"].split()[0]
    else:
        c = _consultor_vazio()
        foto, primeiro = foto_vaga(), "o seu consultor"

    return [page_a4(t, "O seu consultor", 1, '<div class="perfil">%s</div>' % (PAGINA % dict(
        foto=foto, nome=c["nome"], papel=c["papel"], marca=t["marca"],
        marca_curta=t["nome"], frase=c["frase"], bio=_bio(c), cred=_credenciais(c),
        tags=_tags(c["interesses"]), primeiro=primeiro,
        whats=_whatsapp(c["whatsapp"]) if c.get("whatsapp") else ph("whatsapp_consultor"),
        email=_link("mailto:" + c["email"], c["email"]) if c.get("email")
        else ph("email_consultor"),
        insta=ph("instagram_consultor", "@usuario"),
        site=_link("https://auvpcapital.com.br", "auvpcapital.com.br"),
    )), rodape=t["nome_full"], cls="simples", data=False)]
