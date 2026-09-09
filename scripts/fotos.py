# -*- coding: utf-8 -*-
"""Prepara os retratos dos consultores para a apresentação.

    python3 scripts/fotos.py

Lê os originais de `consultores resolve ai/` e escreve `assets/consultores/`.
As fotos chegam muito diferentes entre si — estúdio escuro com o letreiro da
AUVP, externa em luz de dia, estúdio claro — em enquadramentos e proporções que
não combinam. Este script resolve as duas coisas que quebram a consistência:

1. Enquadramento. Detecta o rosto e recorta em 3:4 com o rosto sempre no mesmo
   ponto e no mesmo tamanho relativo. Quando o recorte ideal não cabe na
   imagem, encolhe mantendo a proporção em vez de distorcer.
2. Exposição. Normaliza média e desvio da luminância e tira um pouco da
   saturação, para que a foto clara e a escura não pareçam de produtos
   diferentes quando os documentos são vistos lado a lado.

É um passo de uma vez só: a saída fica versionada e o `npm run build`, que não
tem dependências, apenas embute o resultado. Depende de Pillow e de
opencv-python-headless 4.x — na 5 o CascadeClassifier saiu do módulo raiz.
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGEM = os.path.join(RAIZ, "consultores resolve ai")
DESTINO = os.path.join(RAIZ, "assets", "consultores")

# nome do arquivo de origem -> slug usado no gerador
SLUGS = {
    "Alan": "alan-santanna",
    "André": "andre-arruda",
    "Bolivar": "bolivar-oliveira",
    "Danilo": "danilo-barbosa",
    "Erika": "erika-barreto",
    "Nasser": "nasser-tanure",
    "Yuri": "yuri-machado",
}

PROPORCAO = 3 / 4          # retrato 3:4
ROSTO_LARGURA = 0.42       # largura do rosto como fração da largura do recorte
ROSTO_X, ROSTO_Y = 0.50, 0.36   # onde o centro do rosto fica dentro do recorte
SAIDA = (900, 1200)

L_MEDIA, L_DESVIO = 112.0, 44.0   # alvos de luminância
L_JOELHO, L_TETO = 195.0, 238.0   # a partir do joelho as altas luzes comprimem
SATURACAO = 0.88


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


def altas_luzes(L):
    """Comprime o topo da escala em vez de cortá-lo.

    Esticar o desvio para o alvo empurra tudo o que já era claro contra o 255,
    e o corte vira mancha: o letreiro de neon atrás de um consultor, a janela
    atrás de outro, o realce na testa de quem foi fotografado com luz dura. A
    partir do joelho a curva passa a se aproximar do teto, então o que era
    branco continua claro mas volta a ter desenho.
    """
    alto = L > L_JOELHO
    L[alto] = L_JOELHO + (L_TETO - L_JOELHO) * np.tanh(
        (L[alto] - L_JOELHO) / (255.0 - L_JOELHO))
    return L


def normaliza(im):
    """Aproxima média e desvio da luminância dos alvos, segura as altas luzes
    e reduz a saturação."""
    lab = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2LAB).astype(np.float32)
    L = lab[:, :, 0]
    desvio = L.std() or 1.0
    lab[:, :, 0] = np.clip(
        altas_luzes((L - L.mean()) * (L_DESVIO / desvio) + L_MEDIA), 0, 255)
    for c in (1, 2):                # a e b são centrados em 128
        lab[:, :, c] = np.clip((lab[:, :, c] - 128.0) * SATURACAO + 128.0, 0, 255)
    return Image.fromarray(cv2.cvtColor(lab.astype(np.uint8), cv2.COLOR_LAB2RGB))


def main():
    os.makedirs(DESTINO, exist_ok=True)
    faltando = []
    for nome, slug in sorted(SLUGS.items()):
        caminho = os.path.join(ORIGEM, nome + ".png")
        if not os.path.exists(caminho):
            faltando.append(nome)
            continue
        bgr = cv2.imread(caminho)
        h, w = bgr.shape[:2]
        rosto = acha_rosto(bgr)
        if rosto is None:
            faltando.append(nome + " (rosto não detectado)")
            continue
        caixa = recorte(w, h, rosto)
        im = Image.open(caminho).convert("RGB").crop(caixa).resize(SAIDA, Image.LANCZOS)
        saida = os.path.join(DESTINO, slug + ".jpg")
        normaliza(im).save(saida, "JPEG", quality=86, optimize=True, progressive=True)
        fr = rosto[2] / (caixa[2] - caixa[0])
        print("  %-18s %5dx%-5d -> %s  rosto %.0f%% da largura"
              % (nome, w, h, os.path.basename(saida), fr * 100))
    if faltando:
        print("sem saída: %s" % ", ".join(faltando), file=sys.stderr)
        return 1
    print("%d retrato(s) em assets/consultores/" % len(SLUGS))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
