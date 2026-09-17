# -*- coding: utf-8 -*-
"""Escreve `docs/blocos.json`, a biblioteca de blocos que a ferramenta oferece.

    python3 scripts/blocos.py

Os blocos vivem em `gerador/blocos.py`, escritos no mesmo desenho do resto — é o
que evita que uma página montada na ferramenta pareça de outro documento. Aqui
eles viram JSON: o HTML de cada um, com o número da instância trocado por `@I@`,
e os campos que ele traz, com rótulo e dica.

Quem monta a página é a ferramenta, que numera as instâncias e troca o `@I@`. A
casca da página ela não precisa pedir a ninguém: clona uma página do modelo
aberto e esvazia o corpo, e assim o cabeçalho, a logo e o rodapé são exatamente
os daquele documento.
"""
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "gerador"))

from blocos import BLOCOS  # noqa: E402

SAIDA = os.path.join(RAIZ, "docs", "blocos.json")

# O número da instância, como marca no texto. A ferramenta troca por 1, 2, 3…
MARCA = "@I@"


def main():
    fora = []
    for chave, b in BLOCOS.items():
        # Gera com zero e troca o zero pela marca: os campos se chamam `bl0_x` e
        # o espaço de imagem `bl0`, e os dois viram `bl@I@`.
        html = b["html"](0).replace("bl0", "bl" + MARCA)
        campos = {k.replace("bl0", "bl" + MARCA): v for k, v in b["campos"](0).items()}
        fora.append(dict(chave=chave, nome=b["nome"], descricao=b["descricao"],
                         html=html, campos=campos))
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    with open(SAIDA, "w", encoding="utf-8") as f:
        json.dump(dict(marca=MARCA, blocos=fora), f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("docs/blocos.json: %d blocos, %d campos"
          % (len(fora), sum(len(b["campos"]) for b in fora)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
