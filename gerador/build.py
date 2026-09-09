# -*- coding: utf-8 -*-
"""Gera os modelos HTML de `modelos/` a partir dos módulos deste diretório.

    python3 gerador/build.py                    # os 24 modelos
    python3 gerador/build.py relatorio-mensal   # só os que casam com o filtro

Só depende da biblioteca padrão. Depois de rodar, regere os PDFs e o
dicionário com `npm run pdf` e `npm run vars`.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from layout import *  # noqa: E402,F403  (traz também tudo de common)
import d_apresentacao_geral
import d_cronograma
import d_diagnostico
import d_macro
import d_mensal
import d_mensal_apresentacao

OUT = os.path.join(ROOT, "modelos")

SEGMENTOS = ["consultoria", "alta-renda", "private", "assessoria"]

# chave do arquivo -> (formato, título do documento, função que monta as páginas)
DOCUMENTOS = [
    ("relatorio-mensal", "a4", "Relatório Mensal — %s", d_mensal.build),
    ("diagnostico-carteira", "a4", "Diagnóstico de Carteira — %s", d_diagnostico.build),
    ("relatorio-macroeconomico", "a4", "Relatório Macroeconômico — %s", d_macro.build),
    ("apresentacao-geral", "slide", "Apresentação Geral — %s", d_apresentacao_geral.build),
    ("relatorio-mensal-apresentacao", "slide", "Relatório Mensal (apresentação) — %s",
     d_mensal_apresentacao.build),
    ("cronograma-reunioes", "a4", "Cronograma de Reuniões — %s", d_cronograma.build),
]


def monta(chave, formato, titulo_fmt, builder, seg):
    """Monta um modelo e devolve (caminho, número de páginas)."""
    t = THEMES[seg]
    paginas = builder(t, seg)
    css = CSS_A4 if formato == "a4" else CSS_SLIDE
    html = head(titulo_fmt % t["nome_full"], tokens(t) + "\n" + css) + "\n".join(paginas) + "\n" + FOOT
    caminho = os.path.join(OUT, "%s-%s.html" % (chave, seg))
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(html)
    return caminho, len(paginas)


def main(filtros):
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for chave, formato, titulo_fmt, builder in DOCUMENTOS:
        if filtros and not any(q in chave for q in filtros):
            continue
        for seg in SEGMENTOS:
            caminho, paginas = monta(chave, formato, titulo_fmt, builder, seg)
            print("  %-52s %2d páginas" % (os.path.relpath(caminho, ROOT), paginas))
            n += 1
    if not n:
        print("Nenhum documento casa com: %s" % ", ".join(filtros), file=sys.stderr)
        return 1
    print("%d arquivo(s) em modelos/" % n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
