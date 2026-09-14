# -*- coding: utf-8 -*-
"""Gera as apresentações nominais dos consultores, aqui nesta pasta.

    python3 documentos/consultores/gerar.py                # todos
    python3 documentos/consultores/gerar.py danilo         # só quem casa

Fora do pipeline de propósito. `npm run all` monta `modelos/`, que são modelos
em branco; isto monta documento pronto, com nome, texto e retrato de gente de
verdade. São coisas diferentes, e o build não deve apagar uma achando que é a
outra.

O desenho, porém, é o mesmo: as páginas saem de `gerador/d_consultor.py` e de
`gerador/d_consultor_simples.py`, com o consultor escrito no lugar do campo.
Quando a diagramação mudar lá, rode isto de novo e os documentos prontos
acompanham.

Depois de rodar, gere os PDFs com:

    npm run pdf -- --dir=documentos/consultores --out=documentos/consultores
"""
import datetime
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(RAIZ, "gerador"))
sys.path.insert(0, AQUI)

from layout import *  # noqa: E402,F403  (traz também tudo de common)
from layout import _b64  # noqa: E402  (nome privado não vem no import *)
import d_consultor  # noqa: E402
import d_consultor_simples  # noqa: E402
from build import sem_viuvas  # noqa: E402
from consultores import CONSULTORES  # noqa: E402

# Todos são da consultoria, no plano Me Diz o Que Fazer.
TEMA = "consultoria"
PLANO = "me-diz-o-que-fazer"

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
         "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]


def mes_de_hoje():
    """A data do cabeçalho da versão datada.

    Documento pronto leva a data em que foi feito, e não um campo. Quem quiser
    um sem data tem a gêmea `-sem-data`, que é a que se imprime em lote.
    """
    hoje = datetime.date.today()
    return "%s de %d" % (MESES[hoje.month - 1].capitalize(), hoje.year)


def foto(slug, cls="rt-img"):
    """Retrato embutido em base64, para o arquivo continuar abrindo sozinho."""
    return '<img class="%s" alt="" src="data:image/jpeg;base64,%s">' % (
        cls, _b64(os.path.join("assets", "consultores", slug + ".jpg")))


def foto_redonda(slug, f=d_consultor_simples.FOLHA):
    """O mesmo retrato na caixa circular da folha de uma página."""
    pos = 'style="left:%.2fmm;top:%.2fmm;width:%.2fmm;height:%.2fmm"' % (
        f["centro_x"] - f["raio_foto"], f["centro_y"] - f["raio_foto"],
        f["raio_foto"] * 2, f["raio_foto"] * 2)
    return '<div class="fl-foto" %s>%s</div>' % (pos, foto(slug, cls=""))


def escreve(nome_arquivo, titulo, paginas, css=None):
    t = THEMES[TEMA]
    html = (head(titulo, tokens(t) + "\n" + (css or CSS_A4))
            + sem_viuvas("\n".join(paginas)) + "\n" + FOOT)
    # O único campo que sobra num documento pronto é a data, e ela se resolve
    # sozinha. Se sobrar outro — o WhatsApp de quem não tem número, por exemplo
    # —, ele sai destacado no arquivo, que é como o gerador avisa que falta
    # dado. A conferência é de quem manda para o cliente.
    html = html.replace(ph("data_apresentacao"), mes_de_hoje())
    caminho = os.path.join(AQUI, nome_arquivo)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(html)
    print("  %s" % os.path.relpath(caminho, RAIZ))
    return nome_arquivo


def completa(c, data):
    """A folha inteira, com e sem a data no pé."""
    t = THEMES[TEMA]
    reset_img()
    set_date_ph("data_apresentacao")
    return [d_consultor.folha(t, PLANO, c=c, foto=foto(c["slug"]),
                              primeiro=c["nome"].split()[0], data=data)]


def simples(c):
    t = THEMES[TEMA]
    reset_img()
    return d_consultor_simples.build(t, TEMA, c=c, foto=foto_redonda(c["slug"]))


def main(filtros):
    escritos = set()
    for c in CONSULTORES:
        if filtros and not any(q.lower() in (c["slug"] + " " + c["nome"]).lower()
                               for q in filtros):
            continue
        titulo = "Apresentação do consultor — %s" % c["nome"]
        longa = CSS_A4 + CSS_LONGA
        escritos.add(escreve("apresentacao-consultor-%s.html" % c["slug"],
                             titulo, completa(c, data=True), css=longa))
        escritos.add(escreve("apresentacao-consultor-%s-sem-data.html" % c["slug"],
                             titulo, completa(c, data=False), css=longa))
        escritos.add(escreve("apresentacao-consultor-simples-%s.html" % c["slug"],
                             titulo, simples(c)))

    if not escritos:
        print("Nenhum consultor casa com: %s" % ", ".join(filtros), file=sys.stderr)
        return 1

    # Sem filtro, isto é a lista completa: um arquivo que sobrou de um slug
    # renomeado não deve continuar aqui se ninguém mais o produz. O PDF vai
    # junto, porque um PDF órfão é o que alguém acaba mandando para o cliente.
    if not filtros:
        for f in sorted(os.listdir(AQUI)):
            if f.endswith(".html") and f not in escritos:
                os.remove(os.path.join(AQUI, f))
                print("  removido %s (não é mais gerado)" % f)
            elif f.endswith(".pdf") and f[:-4] + ".html" not in escritos:
                os.remove(os.path.join(AQUI, f))
                print("  removido %s (não é mais gerado)" % f)

    print("%d documento(s) em documentos/consultores/" % len(escritos))
    return 0


if __name__ == "__main__":
    os.chdir(RAIZ)      # os caminhos de asset são relativos à raiz
    raise SystemExit(main(sys.argv[1:]))
