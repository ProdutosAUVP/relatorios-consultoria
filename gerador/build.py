# -*- coding: utf-8 -*-
"""Gera os modelos HTML de `modelos/` a partir dos módulos deste diretório.

    python3 gerador/build.py                    # todos
    python3 gerador/build.py relatorio-mensal   # só os que casam com o filtro

Só depende da biblioteca padrão. Depois de rodar, regere os PDFs e o
dicionário com `npm run pdf` e `npm run vars`.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from layout import *  # noqa: E402,F403  (traz também tudo de common)
import consultores
import d_apresentacao_geral
import d_consultor
import d_cronograma
import d_diagnostico
import d_macro
import d_mensal
import d_mensal_apresentacao

OUT = os.path.join(ROOT, "modelos")

SEGMENTOS = ["consultoria", "alta-renda", "private", "assessoria"]

# Cada documento vira um arquivo por variante. Na maioria a variante é o
# segmento, e o tema sai dela; quando `tema` é informado, o tema fica fixo e a
# variante passa a ser outra coisa — no caso da apresentação, o consultor.
DOCUMENTOS = [
    dict(chave="relatorio-mensal", formato="a4",
         titulo="Relatório Mensal — %s", builder=d_mensal.build),
    dict(chave="diagnostico-carteira", formato="a4",
         titulo="Diagnóstico de Carteira — %s", builder=d_diagnostico.build),
    dict(chave="relatorio-macroeconomico", formato="a4",
         titulo="Relatório Macroeconômico — %s", builder=d_macro.build),
    dict(chave="apresentacao-geral", formato="slide",
         titulo="Apresentação Geral — %s", builder=d_apresentacao_geral.build),
    dict(chave="relatorio-mensal-apresentacao", formato="slide",
         titulo="Relatório Mensal (apresentação) — %s", builder=d_mensal_apresentacao.build),
    dict(chave="cronograma-reunioes", formato="a4",
         titulo="Cronograma de Reuniões — %s", builder=d_cronograma.build),
    dict(chave="apresentacao-consultor", formato="a4",
         titulo="%s — AUVP Capital · Me Diz o Que Fazer", builder=d_consultor.build,
         tema="consultoria",
         variantes=[(c["slug"], c["nome"]) for c in consultores.CONSULTORES]),
]


def variantes(doc):
    """(sufixo do arquivo, rótulo do título, chave do tema)."""
    if "variantes" in doc:
        return [(suf, rotulo, doc["tema"]) for suf, rotulo in doc["variantes"]]
    return [(seg, THEMES[seg]["nome_full"], seg) for seg in SEGMENTOS]


def monta(doc, sufixo, rotulo, tema):
    t = THEMES[tema]
    paginas = doc["builder"](t, sufixo if "variantes" in doc else tema)
    css = CSS_A4 if doc["formato"] == "a4" else CSS_SLIDE
    html = head(doc["titulo"] % rotulo, tokens(t) + "\n" + css) + "\n".join(paginas) + "\n" + FOOT
    caminho = os.path.join(OUT, "%s-%s.html" % (doc["chave"], sufixo))
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(html)
    return caminho, len(paginas)


def main(filtros):
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for doc in DOCUMENTOS:
        if filtros and not any(q in doc["chave"] for q in filtros):
            continue
        for sufixo, rotulo, tema in variantes(doc):
            caminho, paginas = monta(doc, sufixo, rotulo, tema)
            print("  %-52s %2d páginas" % (os.path.relpath(caminho, ROOT), paginas))
            n += 1
    if not n:
        print("Nenhum documento casa com: %s" % ", ".join(filtros), file=sys.stderr)
        return 1
    print("%d arquivo(s) em modelos/" % n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
