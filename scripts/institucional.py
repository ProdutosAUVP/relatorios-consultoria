# -*- coding: utf-8 -*-
"""Prepara as imagens institucionais dos documentos.

    python3 scripts/institucional.py

Lê os originais de `assets/institucional/originais/` e escreve o recorte ao
lado, em `assets/institucional/`.

São as fotos que não mudam de cliente para cliente — a sede, o time — e que por
isso não são campo de imagem na ferramenta: vêm embutidas no modelo. Os
originais vêm da landing page institucional
(github.com/ProdutosAUVP/lp-auvp-institucional); este script só enquadra.

Ao contrário dos retratos dos consultores, aqui não se recorta: a proporção é a
que o fotógrafo enquadrou. A sede é um prédio largo, e espremê-la num retrato
3:4 cortava metade da fachada para caber num lugar que o desenho podia ceder —
foi o desenho que cedeu. O script só reduz o arquivo ao tamanho em que ele vai
ser impresso, e converte para JPEG, que é o que o embutido em base64 aceita.

Cor, brilho e contraste ficam como vieram: a foto é de quem a tirou.

É um passo de uma vez só. A saída fica versionada e o `npm run build`, que não
tem dependências, apenas embute o resultado.
"""
import os
import sys

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, "assets", "institucional")
ORIGEM = os.path.join(DESTINO, "originais")

# Largura máxima do arquivo gerado. A maior caixa em que uma destas fotos entra
# hoje tem uns 12 cm; a 300 dpi isso dá cerca de 1400 px, e o dobro disso só
# engorda o base64 embutido em cada modelo.
LARGURA = 1400


def main():
    if not os.path.isdir(ORIGEM):
        print("Nada em %s/." % os.path.relpath(ORIGEM, RAIZ), file=sys.stderr)
        return 1
    os.makedirs(DESTINO, exist_ok=True)
    n = 0
    for arq in sorted(os.listdir(ORIGEM)):
        nome, ext = os.path.splitext(arq)
        if ext.lower() not in (".webp", ".jpg", ".jpeg", ".png"):
            continue
        im = Image.open(os.path.join(ORIGEM, arq)).convert("RGB")
        if im.width > LARGURA:
            im = im.resize((LARGURA, round(im.height * LARGURA / im.width)), Image.LANCZOS)
        saida = os.path.join(DESTINO, nome + ".jpg")
        im.save(saida, quality=88, optimize=True)
        print("  %-24s  ->  %s.jpg  %dx%d" % (arq, nome, im.width, im.height))
        n += 1
    print("%d imagem(ns) em %s/" % (n, os.path.relpath(DESTINO, RAIZ)))
    return 0


if __name__ == "__main__":
    os.chdir(RAIZ)
    raise SystemExit(main())
