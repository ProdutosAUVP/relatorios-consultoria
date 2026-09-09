# Como estes documentos são construídos

Guia de arquitetura dos modelos: como o pipeline funciona, o que é fonte e o que é
saída, e o que fazer para acrescentar uma página, um documento ou um segmento sem
reabrir 24 arquivos.

Para preencher um modelo e gerar o PDF, veja o [README](README.md). Para o nome de cada
campo, o [VARIAVEIS.md](VARIAVEIS.md).

## O pipeline

```
gerador/*.py  ──build──▶  modelos/*.html  ──pdf──▶  pdf/<produto>/*.pdf
   fonte                    31 modelos              31 PDFs
                            independentes
                                 │
                                 ├──vars──▶  VARIAVEIS.md
                                 └──check─▶  relatório de estouro de página
```

Quatro comandos, nesta ordem:

```sh
npm run build   # gerador/ -> modelos/    (Python 3, só biblioteca padrão)
npm run vars    # modelos/ -> VARIAVEIS.md
npm run check   # valida modelos/         (falha se algo estoura a página)
npm run pdf     # modelos/ -> pdf/<produto>/  (Chromium via Playwright)

npm run all     # os quatro em sequência
```

`modelos/`, `pdf/` e `VARIAVEIS.md` são **saída**. Nada ali deve ser editado à mão:
o próximo `npm run build` sobrescreve. A fonte é `gerador/`.

### Por que os modelos são independentes se há um gerador

Cada arquivo em `modelos/` carrega o próprio CSS, a própria fonte em base64 e a própria
paleta. Isso é proposital: o modelo abre com duplo clique em qualquer máquina, sem
servidor, sem `npm install`, e pode ser mandado por e-mail para quem for preenchê-lo.

O custo dessa escolha é que uma correção no sistema visual precisaria ser repetida 24
vezes. É exatamente isso que o gerador resolve: a correção é feita uma vez em
`gerador/common.py` e o `npm run build` a propaga. As duas coisas convivem — arquivos
autossuficientes na entrega, fonte única na manutenção.

## Mapa do repositório

| Caminho | O que é |
| --- | --- |
| `gerador/common.py` | temas, tokens, folhas de estilo A4 e 16:9, fontes em base64, leitura dos SVGs |
| `gerador/layout.py` | montagem de página e de slide, e os componentes (`table`, `kpis`, `flow`, `chart`, …) |
| `gerador/d_*.py` | um módulo por tipo de documento; contém o conteúdo e a ordem das seções |
| `gerador/consultores.py` | texto e contatos dos consultores, um dicionário por pessoa |
| `scripts/fotos.py` | prepara os retratos: recorta pelo rosto, sem tocar em cor ou brilho |
| `assets/consultores/` | retratos prontos, saída do `scripts/fotos.py` |
| `consultores resolve ai/` | fotos originais, como vieram |
| `gerador/build.py` | entrada: percorre documentos × segmentos e escreve `modelos/` |
| `scripts/render.mjs` | HTML → PDF, numa subpasta por produto |
| `scripts/documentos.mjs` | a tabela de produtos e documentos, partilhada pelo render e pelo catálogo |
| `scripts/exemplos.mjs` | o exemplo de preenchimento de cada campo, derivado do nome |
| `scripts/check.mjs` | valida estouro de página em modo de impressão |
| `scripts/variaveis.mjs` | gera o `VARIAVEIS.md` a partir dos modelos |
| `scripts/catalogo.mjs` | monta `docs/`: copia os modelos e escreve o índice da ferramenta |
| `docs/` | a ferramenta de preenchimento, publicada no GitHub Pages |
| `assets/fonts/` | Anek Latin, instâncias estáticas em woff2 |
| `assets relatórios/` | logos, grafismos e as referências originais de capa |
| `modelos/`, `pdf/`, `docs/`, `VARIAVEIS.md` | saída |

## Reproduzir do zero

```sh
git clone <repo> && cd relatorios-consultoria
npm install          # só Playwright; o gerador não tem dependências
npm run all
git status --short modelos/ docs/ VARIAVEIS.md   # deve vir vazio
```

`modelos/`, `docs/` e `VARIAVEIS.md` são **reprodutíveis byte a byte**: se vierem limpos, a saída
no repositório corresponde exatamente à fonte. É essa a verificação que vale.

`pdf/` tem uma subpasta por produto — `consultoria/`, `alta-renda/`, `private/`,
`assessoria/`, `me-diz-o-que-fazer/`. São 31 arquivos: numa lista só, achar o diagnóstico
do Private é ler nome por nome. O nome do arquivo continua completo mesmo dentro da
pasta, para um PDF baixado sozinho não virar `relatorio-mensal.pdf` sem dizer de quem é.
Quem decide a pasta é `classifica()`, em `scripts/documentos.mjs`, a mesma função que o
catálogo da ferramenta usa — as duas saídas não podem discordar sobre a que produto um
arquivo pertence.

`pdf/` **não** é byte a byte. O Chromium carimba data de criação no PDF, então os 31
arquivos aparecem como modificados a cada geração mesmo sem nenhuma mudança de
conteúdo. É esperado; o conteúdo é determinístico, o metadado não. Para comparar dois
PDFs de fato, compare o texto extraído ou a renderização, não os bytes.

Ambiente de referência: Node 22, Python 3.11, Playwright 1.49. O gerador usa apenas
`os`, `re`, `sys` e `base64` — não há `requirements.txt` porque não há o que instalar.

## Anatomia de um modelo

O arquivo gerado é sempre a mesma sequência:

```html
<!doctype html>
<html lang="pt-BR"><head>
  <title>Relatório Mensal — AUVP Capital · Consultoria</title>
  <style>
    :root{ --brand:…; --accent:…; --c1:…; }   ← tokens(t): a única parte que varia por segmento
    @font-face{…base64…}                      ← idêntico nos 24
    /* base + folha do formato (A4 ou 16:9) */
  </style>
</head><body>
  <section class="page cover">…</section>     ← uma section por página
  <section class="page">…</section>
</body></html>
```

Trocar de segmento troca só o bloco `:root`. Trocar de formato troca a folha inteira.

### Uma página A4

```html
<section class="page">
  <header class="pg-head">                    ← papel timbrado: seção, data, logo
    <div class="sec">Resumo da carteira</div>
    <div class="rt"><div class="dt">{{mes_referencia}}</div><div class="logo">…</div></div>
  </header>
  <div class="pg-body">…conteúdo…</div>       ← flex column; cresce e empurra o rodapé
  <footer class="pg-foot">                    ← número e aviso de confidencialidade
    <span class="no">03</span><span>DOCUMENTO CONFIDENCIAL · …</span>
  </footer>
</section>
```

`.page` tem `210mm × 297mm` e `overflow:hidden`. Conteúdo que não cabe **não** vira
segunda página: fica recortado. É por isso que o `npm run check` existe — ele acusa o
recorte antes de virar PDF.

O rodapé traz, por padrão, o aviso de confidencialidade. Documento feito para ser
entregue ao cliente passa outro texto em `page_a4(..., rodape=...)` — é o caso da
apresentação do consultor, que não deve dizer "proibido o compartilhamento".

O slide 16:9 tem a mesma estrutura, com `.slide` no lugar de `.page` e as mesmas classes
de cabeçalho e rodapé. `.slide.dark` inverte para o fundo em degradê.

## Tokens

Definidos em `tokens()` a partir do dicionário do tema, em `gerador/common.py`.

| Token | Para quê |
| --- | --- |
| `--brand` | cor principal do segmento: capa, cabeçalho de tabela, títulos de seção |
| `--accent` | acento, sempre em linha fina; neutro no Private Banking |
| `--c1` … `--c6` | sequência de cores dos gráficos |
| `--ph`, `--ph-dk` | realce dos campos preenchíveis, em fundo claro e escuro |
| `--warn-bg`, `--warn-fg`, `--warn-bd` | selo de atenção |
| `--ink`, `--ink-2` | texto e texto secundário |
| `--line`, `--soft`, `--paper` | fio, fundo de apoio e papel |
| `--pos`, `--neg` | sinal semântico de retorno positivo e negativo |

Nenhuma cor deve ser escrita direto no CSS de componente. Se for preciso uma cor nova,
ela vira token — foi assim que a regra "Private Banking não usa amarelo" passou a valer
sozinha para qualquer elemento novo.

## Espaçamento e fios

Duas escalas fechadas, e é o que mantém os documentos consistentes entre si.

**Espaçamento**, em mm: `1 · 1,5 · 2 · 3 · 4 · 5 · 6 · 8 · 10 · 12 · 16`. Toda margem,
padding e gap sai daí. Fora da escala ficam apenas a geometria medida das capas e as
margens de página, que têm origem própria.

**Fios**: `1px` (0,75 pt) para todo fio — régua, hairline de tabela, borda de cabeçalho,
moldura tracejada, traço de grafismo — e `1.33px` (1 pt) para acento: borda esquerda de
card, topo de card de indicador, linha de total de tabela, traço de tópico de lista. Não
há um terceiro peso.

**Ritmo vertical das listas em px inteiros.** O traço de tópico é um retângulo de altura
fracionária posicionado dentro do `li`. Se o passo entre os itens for medido em mm — que
nunca dá px inteiro —, cada traço cai numa fase de subpixel diferente e a rasterização
engorda uns e afina outros, o que se vê como fio de espessura variável na mesma lista.
Por isso `line-height`, `margin-bottom` e o `top` do marcador de `.lista`, `.plan` e
`.marcos` são os únicos valores do sistema declarados em px inteiros: assim todos os
traços herdam a mesma fase da origem da lista e saem idênticos. Se mexer na escala
dessas listas, ajuste os três juntos e mantenha-os inteiros.

A escala é generosa por decisão: este é um material de produto financeiro, e o espaço em
branco faz parte do acabamento. Quando um conteúdo não cabe na página, a resposta certa é
**dar-lhe outra página**, e não reduzir a escala. A exceção é a apresentação do consultor,
de número de páginas fixo, que usa a escala `.perfil`.

**Respiro elástico.** Numa página de altura fechada sobra espaço, e ele varia de um
documento para outro — a trajetória de um consultor tem três marcos, a de outro tem
quatro. Empurrar o rodapé para a borda com `margin-top:auto` resolve o encaixe mas abre
um vão enorme numa junta só. A classe `.esp` faz o contrário: é um respiro `flex:1 1 0`
entre duas faixas de conteúdo, com piso e teto (`4mm` a `11mm`, ou `17mm` na variante
`.esp.lg`). O excedente é dividido igualmente entre os respiros da página, cada um cresce
até o seu teto, e o que sobrar fica na margem inferior. No documento mais denso todos
encostam no piso; no mais curto, no teto. Em ambos a página mantém o mesmo ritmo.

Para auditar depois de mexer:

```sh
python3 - <<'EOF'
import re, sys, collections
sys.path.insert(0, "gerador"); import common
css = common.CSS_A4 + common.CSS_SLIDE
print(collections.Counter(re.findall(r"border[a-z-]*:\s*([\d.]+(?:px|pt))", css)))
v = collections.Counter()
for d in re.findall(r"(?:margin|padding|gap)[a-z-]*:\s*([^;}]+)", css):
    v.update(float(x) for x in re.findall(r"([\d.]+)mm", d))
print(sorted(v))
EOF
```

## Componentes

Cada um é uma função em `gerador/layout.py` que devolve HTML.

| Função | Classe | Para quê |
| --- | --- | --- |
| `table(headers, rows, foot, caption, nums, widths, sm, xs)` | `.tb` | tabela com cabeçalho, corpo e total. `nums` alinha colunas à direita; `sm`/`xs` reduzem o corpo; `widths` fixa as colunas |
| `kpis(items, n)` | `.kpi` | cards de indicadores |
| `cards(items, n)` | `.card` | blocos curtos com fio de acento à esquerda |
| `flow(itens, n)` | `.flow` | etapas sobre um trilho contínuo, com nó numerado e etiqueta de prazo |
| `hero(numero, legenda, apoio)` | `.hero` `.stats` | um número em destaque e uma fileira de apoio |
| `year(eventos)` | `.year` | doze meses em dois semestres |
| `timeline(items)` | `.tl` | lista numerada em duas colunas |
| `chart(label, desc, skeleton, style, series)` | `.chart` | moldura do gráfico: descreve o que ele mostra e pinta a legenda com `--c1`…`--c6` |
| `imgbox(desc)` | `.imgbox` | espaço reservado para foto, com a especificação |
| `foto_consultor(slug)` | `.rt-img` | retrato pronto, embutido em base64 |
| `ph(nome, dica)` | `.ph` | campo preenchível `{{nome}}` |

Modificadores de página, aplicados como `class` num `div` que envolve o conteúdo:
`.principios` põe título e texto no mesmo parágrafo, em duas colunas.

`page_a4(..., dark=True)` roda a página no negativo: fundo em degradê com granulado,
texto e fios em branco, logo em branco. É o que fecha a apresentação do consultor sem
acrescentar ornamento — mesma grelha, mesma tipografia, mesmos fios, só o fundo troca.
Cor e ritmo são coisas separadas: `.dark` cuida da cor, `page_a4(..., cls="plano")`
cuida do respiro e da escala, e por isso as páginas 2 e 3 são iguais em diagramação com
fundos diferentes. No negativo o acento amarelo sai de cena: sobre o verde ele fica
estridente, então marcador de lista, fio de card e destaque em negrito passam a branco.
No fundo branco vale o contrário — a logo da AUVP é sempre preta. `.perfil` é a escala da primeira página, um pouco menor que a padrão
mas com entrelinha mais generosa, para acomodar o consultor de texto mais longo sem
apertar o de texto mais curto.

### Links

Âncora comum: o Chromium leva `<a href>` para dentro do PDF, então WhatsApp, e-mail e os
canais da casa ficam clicáveis no arquivo entregue. O que não pode mudar é a aparência —
`a{color:inherit;text-decoration:none}` mantém azul e sublinhado fora da página.

O número mostrado é formatado para leitura (`+55 (62) 3095-8142`) e o link usa a versão
limpa (`https://wa.me/556230958142`), derivada do mesmo campo. O e-mail vira `mailto:`. O
consultor que não tem número guarda `whatsapp=None` e o campo volta a ser preenchível: é
melhor sair `{{whatsapp_consultor}}` no documento do que o telefone de outra pessoa.

### Retratos

Os originais chegam muito diferentes entre si — estúdio escuro com o letreiro da AUVP,
externa em luz de dia, estúdio claro — em enquadramentos e proporções que não combinam.
`scripts/fotos.py` resolve o que quebra a consistência sem tocar na imagem:

- **enquadramento**: detecta o rosto com o classificador Haar do OpenCV e recorta em 3:4
  com o rosto sempre no mesmo ponto e no mesmo tamanho relativo — nos sete, entre 42% e
  45% da largura do recorte. Quando o recorte ideal não cabe, encolhe mantendo a
  proporção em vez de distorcer.

Cor, brilho e contraste ficam como vieram do original. Normalizar exposição uniformiza o
conjunto, mas altera a foto que a pessoa entregou — e o retrato é dela, não nosso.

É um passo de uma vez só, rodado à mão: `python3 scripts/fotos.py`. A saída fica
versionada em `assets/consultores/` e o `npm run build` só a embute em base64, o que
mantém o build sem dependências. Precisa de Pillow e de **opencv-python-headless 4.x** —
na 5 o `CascadeClassifier` saiu do módulo raiz.

### Palavras órfãs

Coluna estreita e texto em português produzem linha final de uma palavra só o tempo todo.
`sem_viuvas()`, em `gerador/build.py`, roda sobre o HTML pronto e troca por `&nbsp;` o
espaço que antecede a última palavra de cada bloco de texto — `p`, `li`, títulos, células
de tabela e os inline que fecham um bloco. As duas últimas palavras passam a quebrar
juntas, então a linha final nunca fica sozinha. Casos em que o bloco termina em tag
(`…</span></p>`) ficam de fora por construção; se aparecer um, é sinal de que o texto
precisa de outra redação, não de outra regra.

Auxiliares de grelha, usados como `class`: `.cols2`, `.cols3`, `.cols2u` (1,5 : 1),
`.center` (usa a sobra vertical do slide), `.gap`.

## A ferramenta de preenchimento

`docs/` é um site estático, sem build e sem dependência, publicado no GitHub Pages. Ele
não redesenha nada: baixa o próprio modelo deste repositório, troca `{{campo}}` pelo que
foi digitado e devolve o arquivo. É por isso que o que sai da ferramenta é idêntico ao que
sai do gerador — só existe um desenho, e ele mora em `gerador/`.

| Arquivo | Papel |
| --- | --- |
| `scripts/catalogo.mjs` | lê `modelos/*.html` e escreve `docs/catalogo.json`, `docs/campos/*.json` e `docs/modelos/*.html` |
| `docs/catalogo.json` | índice leve: produtos, documentos e variantes. É o primeiro fetch |
| `docs/campos/<modelo>.json` | campos, seções e espaços de imagem daquele modelo |
| `docs/index.html`, `app.css`, `app.js` | a interface, nos tokens do design system da AUVP |

Quatro decisões que valem explicação:

**A estrutura fica num arquivo por variante, não no índice.** As variantes não são iguais
— o relatório mensal de Alta Renda tem ofertas de renda fixa, o de Private tem
compromissos de liquidez. Juntar tudo num índice só faria a primeira tela baixar 1,5 MB
para mostrar cinco cartões.

**O preenchimento é feito no DOM, não por regex.** O modelo é parseado uma vez com
`DOMParser`; cada tecla clona o documento, escreve nos `span.ph` e serializa. É mais
robusto que substituir texto — um campo que aparece dentro de um atributo, ou um bloco de
imagem com marcação aninhada, não quebra a montagem.

**Os espaços de imagem são numerados no gerador.** `imgbox()` e `chart()` marcam cada
espaço com `data-img`, e é por esse número que a foto enviada encontra o lugar dela. Sem
isso a ferramenta dependeria da ordem dos elementos na página, que muda a cada edição de
um documento.

**O que é digitado fica guardado, e em dois lugares.** O texto vai para o `localStorage`,
que é síncrono e sobrevive a qualquer coisa; as imagens vão para o IndexedDB, porque um
data URL de foto passa de 1 MB e estouraria a cota de 5 MB do `localStorage` no primeiro
documento com três gráficos. Guardar tudo junto faria o texto se perder junto com as
imagens quando a cota acabasse.

**Todo campo mostra um exemplo.** São 1743 nomes distintos, então a tabela de exemplos
não é escrita à mão: `scripts/exemplos.mjs` deriva o exemplo do nome, varrendo as partes
do fim para o começo — `pos_7_valor` casa em `valor`, `mes_referencia` em `mes`. O
exemplo é o `placeholder` do campo, some ao digitar e nunca entra no documento. Os poucos
campos institucionais que fogem ao vocabulário vêm escritos um a um.

O PDF sai pela impressão do navegador, não por uma biblioteca: o `@page` dos modelos já
tem o tamanho certo e `print-color-adjust:exact` garante os fundos, então o resultado é o
mesmo do `npm run pdf`, que também é o Chromium imprimindo. A janela aberta pela
ferramenta chama a impressão sozinha.

Documento novo em `gerador/build.py` aparece na ferramenta sem mexer em `docs/` — só
precisa de uma entrada em `DOCUMENTOS`, no `scripts/catalogo.mjs`, com o nome e a
descrição que o cartão mostra.


## Como fazer

### Acrescentar uma página a um documento

Há dois padrões, e o certo depende do documento.

**No relatório mensal**, que tem sumário, as seções são declaradas com `add()` e a
paginação sai da lista — acrescente no ponto da sequência em que a página deve entrar e
o número da página e a linha do sumário se ajustam sozinhos:

```python
add("Renda fixa",                 # rótulo do cabeçalho
    "Renda fixa",                 # título no sumário
    """<span class="eyebrow">Renda fixa</span>
<h1 class="t">Indexadores, liquidez e emissores</h1>
<p class="lead">…</p>
%(tab)s""" % dict(tab=table([...], [...])))
```

**Nos demais**, as páginas são anexadas direto, com o número explícito:

```python
P.append(page_a4(t, "Calendário", 3, """…"""))
```

Aqui a renumeração é manual: ao inserir uma página no meio, corrija os números
seguintes e o sumário, quando houver. Se um documento crescer a ponto de isso incomodar,
vale migrá-lo para o padrão do mensal.

Nos dois casos, `npm run build && npm run check` fecha o ciclo.

### Acrescentar um documento

1. Crie `gerador/d_novo.py` com uma função `build(t, seg)` que devolve uma lista de
   páginas — comece copiando `d_cronograma.py`, que é o menor.
2. Registre em `gerador/build.py`, na lista `DOCUMENTOS`:

```python
("nome-do-arquivo", "a4", "Título — %s", d_novo.build),
```

3. `npm run all`. Saem quatro arquivos novos, um por segmento.

O formato é `"a4"` ou `"slide"`; é o que escolhe entre `CSS_A4` e `CSS_SLIDE`.

### Um documento cujas variantes não são segmentos

Na maioria dos documentos a variante é o segmento e o tema sai dela. Quando não for o
caso — a apresentação do consultor tem uma variante por pessoa —, declare `tema` fixo e
a lista de `variantes`, com `(sufixo do arquivo, rótulo do título)`:

```python
dict(chave="apresentacao-consultor", formato="a4",
     titulo="%s — AUVP Capital · Me Diz o Que Fazer", builder=d_consultor.build,
     tema="consultoria",
     variantes=[(c["slug"], c["nome"]) for c in consultores.CONSULTORES]),
```

O `builder` recebe `(tema, sufixo)` em vez de `(tema, segmento)`. Acrescentar um
consultor é somar uma entrada em `gerador/consultores.py`.

O `scripts/variaveis.mjs` reconhece o documento pelo prefixo do nome do arquivo, então
uma chave nova precisa entrar no `TITULOS` dele — os prefixos são ordenados do mais
longo para o mais curto, para `relatorio-mensal-apresentacao` casar antes de
`relatorio-mensal`.

### Acrescentar um segmento

Uma entrada em `THEMES`, em `gerador/common.py`, e ele passa a existir em **todos** os
documentos:

```python
"novo-segmento": dict(
    nome="Novo", nome_full="AUVP Capital · Novo", rotulo="Novo",
    brand="#…", accent="#…", ph="…", ph_dk="…",
    warn_bg="…", warn_fg="…", warn_bd="…",
    chart=["#…", "#…", "#…", "#…", "#…", "#…"],
    ink="#…", ink2="#…", line="#…", soft="#…",
    logo=LOGO_CAPITAL, logo_ratio=1044.44 / 274.67,
    marca="AUVP Capital", cadencia="trimestral",
),
```

Acrescente a chave em `SEGMENTOS`, em `build.py`. Os módulos de documento têm
dicionários por segmento — `PAPEL`, `PITCH`, `RITMO`, `EXTRA_TITULO` — e o build falha
com `KeyError` apontando qual falta. É de propósito: um segmento novo tem de decidir o
próprio conteúdo, não herdar o de outro em silêncio.

`rotulo` é o que aparece ao lado da logo. Deixe vazio se a marca do segmento já disser
o nome, como no Private Banking.

### Mudar a paleta ou a tipografia

Paleta: só o dicionário do tema. Tipografia: `FONT_FACE` em `common.py`. Para trocar a
família é preciso gerar as instâncias estáticas em woff2 e o subconjunto — veja
*Armadilhas*, o primeiro item.

### Trocar a moldura pelo gráfico real

Substitua o bloco inteiro:

```html
<div class="chart" …>…</div>
→
<img src="…" style="width:100%">
```

A moldura já traz, no próprio HTML, o que o gráfico deve mostrar e a legenda de série
com as cores do segmento — é a especificação para quem for implementá-lo.

## Medidas, e de onde vieram

Nada aqui foi estimado. As capas saem de medição das referências:

- **A4**, de `assets relatórios/SVG/ref *.svg`: réguas em y 86,0 e 245,2 mm; grafismo
  entre elas com exatamente a largura das réguas; título 43,89 pt com entrelinha de
  48 pt; assinatura 32,13 pt.
- **16:9**, da página 1 de `MODELO SLIDES AUVP CAPITAL.pdf`: faixa branca até 26,3 mm;
  régua curta em x 24,6–74,9 e y 68,4 mm; título 44,6 pt; subtítulo 25,3 pt.

O detalhamento está na seção *Capas* do README.

## Armadilhas

Cada item abaixo custou uma iteração. Se algo parecer arbitrário no código, o motivo
provavelmente está aqui.

**Fonte variável vira Type3 no PDF.** O Chromium exporta fonte variável como Type3: o
texto deixa de ser selecionável e o arquivo incha várias vezes. Por isso a Anek Latin
entra como cinco instâncias estáticas geradas com `fontTools.varLib.instancer`, e não
como o arquivo variável do Google Fonts.

**`@font-face` com URL relativa não carrega em `file://`.** O modelo precisa abrir com
duplo clique, e nesse contexto o navegador recusa a fonte. Daí o base64 embutido.

**Cuidado com `%` no CSS, nos dois sentidos.** `BASE` e as folhas montadas com o
operador `%` exigem `%%` para um `%` literal — um `50%` esquecido derruba o build com
`TypeError`. Já os blocos acrescentados com `CSS_A4 += """…"""` **não** passam por
formatação: ali `%%` vai para o arquivo como `%%` literal e invalida a regra em silêncio,
sem erro nenhum. Foi assim que um `width:100%%` deixou um retrato aparecer em tamanho
natural dentro da banda.

**`<style>` dentro de SVG inline vaza para o documento.** Os SVGs da AUVP usam classes
`.cls-1`, `.cls-2`… e colidiriam entre si. `load_svg()` renomeia com um prefixo por
arquivo.

**O grafismo é posicionado pela tinta, não pela caixa do SVG.** Os arquivos têm cerca de
7,6% de margem interna de cada lado. Alinhar pela caixa deixa o traço fora da régua.
`graf_span()` corrige pelas frações em `GRAF_INK`.

**Medir traço por rasterização exige limiar no preto puro.** Os grafismos têm traços de
10% de opacidade. Um limiar mais alto os perde e desloca o alinhamento em cerca de 4 mm.
As frações do leque de quadrados vêm da geometria dos 22 retângulos, que é exata; as dos
outros dois, de rasterização a 2400 px — e batem com a analítica em 0,0004.

**O grafismo de arcos tem duas arestas retas.** Topo e direita. Como grafismo ele só
pode mostrar arcos, então `graf_arcos()` calcula a sangria a partir da fração de traço e
põe as duas retas fora da página, em qualquer tamanho.

**`.ph` precisa neutralizar herança.** Dentro de bloco em caixa alta, o token viraria
`{{MES_REFERENCIA}}` e deixaria de ser localizável. Daí `text-transform:none` e
`letter-spacing:0`.

**Item de grelha não encolhe abaixo do conteúdo.** Sem `min-width:0`, um token longo num
card de indicador estoura a página para a direita. A regra está aplicada em `.kpis`,
`.cards`, `.cols*`.

**Tabela larga precisa de largura declarada.** Acima de sete colunas, use `xs=True` e
`widths=[…]`; `widths` ativa `table-layout:fixed`, sem o qual as colunas declaradas são
só sugestão.

**O PDF depende de dois parâmetros.** `printBackground: true`, senão as capas saem
brancas, e `preferCSSPageSize: true`, para respeitar o `@page` de cada arquivo. No Chrome
manual, o equivalente é margens em "Nenhuma" e "Gráficos de segundo plano" ligado.

**O Chromium do ambiente pode não bater com a versão do Playwright.** `render.mjs` e
`check.mjs` tentam o lançamento normal e, se falhar, procuram o executável em
`PLAYWRIGHT_BROWSERS_PATH`.

**A verificação roda em `media: print`.** É o modo usado na exportação; validar em
`screen` deixaria passar recorte que só aparece no PDF.

## Antes de commitar

```sh
npm run all
```

- `check` tem de fechar com "24 modelos sem estouro de página".
- `modelos/`, `pdf/` e `VARIAVEIS.md` entram no mesmo commit da mudança em `gerador/`,
  para que fonte e saída não saiam de sincronia.
- Os 24 PDFs vão aparecer como modificados mesmo que nada tenha mudado neles, por causa
  do carimbo de data. Se a mudança não era para tocar em PDF nenhum, confira pelo
  `modelos/`: é ele que diz o que de fato mudou.
- Mudou a paleta ou a tipografia? Confira uma capa de cada segmento: são elas que
  concentram as decisões visuais.
