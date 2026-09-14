# -*- coding: utf-8 -*-
"""Prepara os retratos dos consultores para a apresentação.

    python3 scripts/fotos.py

Lê os originais de `assets/consultores/originais/` e escreve o recorte ao lado,
em `assets/consultores/`.
As fotos chegam em enquadramentos e proporções que não combinam. Este script
resolve só isso: detecta o rosto e recorta em 3:4 com o rosto sempre no mesmo
ponto e no mesmo tamanho relativo. Quando o recorte ideal não cabe na imagem,
encolhe mantendo a proporção em vez de distorcer.

Cor, brilho e contraste ficam como vieram do original. Normalizar exposição
uniformiza o conjunto, mas altera a foto que o cliente entregou — e o retrato
é dele, não nosso.

É um passo de uma vez só: a saída fica versionada e o `npm run build`, que não
tem dependências, apenas embute o resultado. Depende de Pillow e de
opencv-python-headless 4.x — na 5 o CascadeClassifier saiu do módulo raiz.
"""
import os
import sys

import cv2
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, "assets", "consultores")
ORIGEM = os.path.join(DESTINO, "originais")

# O original tem o nome do slug, e a extensão é a que o arquivo veio: as fotos
# antigas chegaram em PNG, as novas em JPEG, e não há por que converter só para
# alimentar este script. A saída é sempre JPEG, com o mesmo nome.
ORIGINAIS = (".png", ".jpg", ".jpeg")

PROPORCAO = 3 / 4          # retrato 3:4
ROSTO_LARGURA = 0.42       # largura do rosto como fração da largura do recorte
ROSTO_X, ROSTO_Y = 0.50, 0.36   # onde o centro do rosto fica dentro do recorte
SAIDA = (900, 1200)



def acha_rosto(bgr):
    casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    if casc.empty():
        raise RuntimeError("cascade de rosto não carregou")
    cinza = cv2.equalizeHist(cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY))
    achados = casc.detectMultiScale(cinza, 1.08, 5, minSize=(int(bgr.shape[1] * 0.05),) * 2)
    if not len(achados):
        return None
    return max(achados, key=lambda r: r[2] * r[3])


def recorte(w, h, rosto):
    """Caixa 3:4 com o rosto no ponto alvo, encolhida até caber na imagem."""
    x, y, fw, fh = rosto
    cx, cy = x + fw / 2, y + fh / 2
    cw = fw / ROSTO_LARGURA
    ch = cw / PROPORCAO
    if ch > h:                      # não cabe na altura
        ch, cw = h, h * PROPORCAO
    if cw > w:                      # nem na largura
        cw, ch = w, w / PROPORCAO
    esq = min(max(cx - ROSTO_X * cw, 0), w - cw)
    topo = min(max(cy - ROSTO_Y * ch, 0), h - ch)
    return int(esq), int(topo), int(esq + cw), int(topo + ch)


def main():
    os.makedirs(DESTINO, exist_ok=True)
    originais = sorted(f for f in os.listdir(ORIGEM)
                       if f.lower().endswith(ORIGINAIS))
    # Dois originais com o mesmo slug produziriam a mesma saída, e qual deles
    # venceria dependeria da ordem do diretório. Melhor parar e dizer.
    slugs = {}
    for f in originais:
        slugs.setdefault(os.path.splitext(f)[0], []).append(f)
    repetidos = {k: v for k, v in slugs.items() if len(v) > 1}
    if repetidos:
        for slug, arquivos in sorted(repetidos.items()):
            print("%s tem mais de um original: %s" % (slug, ", ".join(arquivos)),
                  file=sys.stderr)
        return 1
    if not originais:
        print("Nenhum original em %s" % os.path.relpath(ORIGEM, RAIZ), file=sys.stderr)
        return 1
    faltando = []
    for arquivo in originais:
        nome = slug = os.path.splitext(arquivo)[0]
        caminho = os.path.join(ORIGEM, arquivo)
        bgr = cv2.imread(caminho)
        h, w = bgr.shape[:2]
        rosto = acha_rosto(bgr)
        if rosto is None:
            faltando.append(nome + " (rosto não detectado)")
            continue
        caixa = recorte(w, h, rosto)
        im = Image.open(caminho).convert("RGB").crop(caixa).resize(SAIDA, Image.LANCZOS)
        saida = os.path.join(DESTINO, slug + ".jpg")
        im.save(saida, "JPEG", quality=90, optimize=True, progressive=True)
        fr = rosto[2] / (caixa[2] - caixa[0])
        print("  %-18s %5dx%-5d -> %s  rosto %.0f%% da largura"
              % (nome, w, h, os.path.basename(saida), fr * 100))
    if faltando:
        print("sem saída: %s" % ", ".join(faltando), file=sys.stderr)
        return 1
    print("%d retrato(s) em assets/consultores/" % len(originais))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
