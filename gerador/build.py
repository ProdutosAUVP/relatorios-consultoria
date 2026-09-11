# -*- coding: utf-8 -*-
"""Gera os modelos HTML de `modelos/` a partir dos módulos deste diretório.

    python3 gerador/build.py                    # todos
    python3 gerador/build.py relatorio-mensal   # só os que casam com o filtro

Só depende da biblioteca padrão. Depois de rodar, regere os PDFs e o
dicionário com `npm run pdf` e `npm run vars`.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from layout import *  # noqa: E402,F403  (traz também tudo de common)
import d_apresentacao_geral
import d_carta_apresentacao
import d_consultor
import d_consultor_simples
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
    # Vai para quem ouviu a proposta e ainda não decidiu: fica entre a
    # apresentação geral, que é da reunião, e o diagnóstico, que só existe
    # depois do sim.
    dict(chave="carta-apresentacao", formato="slide",
         titulo="Carta de Apresentação — %s", builder=d_carta_apresentacao.build),
    dict(chave="cronograma-reunioes", formato="a4",
         titulo="Cronograma de Reuniões — %s", builder=d_cronograma.build),
    # A apresentação do consultor varia por plano da consultoria e por
    # segmento, e a em branco sai também sem data. A lista é montada no próprio
    # módulo, e as variantes trazem o tema junto em vez de sair do sufixo.
    dict(chave="apresentacao-consultor", formato="a4",
         titulo="Apresentação do consultor — %s", builder=d_consultor.build,
         variantes=d_consultor.variantes(THEMES, SEGMENTOS)),
    # A versão de uma página: só a pessoa, sem o plano e sem data. É o cartão
    # que se manda antes de uma primeira conversa.
    dict(chave="apresentacao-consultor-simples", formato="a4",
         titulo="Apresentação do consultor — %s", builder=d_consultor_simples.build,
         variantes=d_consultor_simples.variantes(THEMES, SEGMENTOS)),
]


def variantes(doc):
    """(sufixo do arquivo, rótulo do título, chave do tema)."""
    if "variantes" in doc:
        return doc["variantes"]
    return [(seg, THEMES[seg]["nome_full"], seg) for seg in SEGMENTOS]


# Última palavra de um bloco de texto, com o espaço que a antecede. Prender as
# duas com espaço inquebrável evita a linha final de uma palavra só, que num
# documento com muita coluna estreita aparece o tempo todo. Só vale para texto
# corrido: o casamento não acontece se o bloco terminar em tag.
VIUVA = re.compile(r"\s+([^\s<>]+)(\s*</(?:p|li|h1|h2|h3|h4|dd|dt|td|th|div|span|strong|em)>)")


def sem_viuvas(html):
    return VIUVA.sub(lambda m: "&nbsp;" + m.group(1) + m.group(2), html)


def monta(doc, sufixo, rotulo, tema):
    t = THEMES[tema]
    reset_img()
    paginas = doc["builder"](t, sufixo)
    css = CSS_A4 if doc["formato"] == "a4" else CSS_SLIDE
    html = head(doc["titulo"] % rotulo, tokens(t) + "\n" + css) + \
        sem_viuvas("\n".join(paginas)) + "\n" + FOOT
    caminho = os.path.join(OUT, "%s-%s.html" % (doc["chave"], sufixo))
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(html)
    return caminho, len(paginas)


def main(filtros):
    os.makedirs(OUT, exist_ok=True)
    escritos = set()
    for doc in DOCUMENTOS:
        if filtros and not any(q in doc["chave"] for q in filtros):
            continue
        for sufixo, rotulo, tema in variantes(doc):
            caminho, paginas = monta(doc, sufixo, rotulo, tema)
            print("  %-52s %2d páginas" % (os.path.relpath(caminho, ROOT), paginas))
            escritos.add(os.path.basename(caminho))
    if not escritos:
        print("Nenhum documento casa com: %s" % ", ".join(filtros), file=sys.stderr)
        return 1

    # Sem filtro, o build é a lista completa: um modelo que sobrou de uma
    # variante renomeada continuaria em `modelos/` e apareceria na ferramenta
    # como um documento que o gerador já não sabe produzir.
    if not filtros:
        for f in sorted(set(os.listdir(OUT)) - escritos):
            if f.endswith(".html"):
                os.remove(os.path.join(OUT, f))
                print("  removido %s (não é mais gerado)" % f)

    print("%d arquivo(s) em modelos/" % len(escritos))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
