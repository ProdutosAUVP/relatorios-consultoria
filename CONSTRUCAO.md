# Como estes documentos são construídos

Guia de arquitetura dos modelos: como o pipeline funciona, o que é fonte e o que é
saída, e o que fazer para acrescentar uma página, um documento ou um segmento sem
reabrir 24 arquivos.

Para preencher um modelo e gerar o PDF, veja o [README](README.md). Para o nome de cada
campo, o [VARIAVEIS.md](VARIAVEIS.md).

## O pipeline

```
gerador/*.py  ──build──▶  modelos/*.html  ──pdf──▶  pdf/*.pdf
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
npm run pdf     # modelos/ -> pdf/        (Chromium via Playwright)

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
| `gerador/consultores.py` | texto de apresentação dos consultores, um dicionário por pessoa |
| `gerador/build.py` | entrada: percorre documentos × segmentos e escreve `modelos/` |
| `scripts/render.mjs` | HTML → PDF |
| `scripts/check.mjs` | valida estouro de página em modo de impressão |
| `scripts/variaveis.mjs` | gera o `VARIAVEIS.md` a partir dos modelos |
| `assets/fonts/` | Anek Latin, instâncias estáticas em woff2 |
| `assets relatórios/` | logos, grafismos e as referências originais de capa |
| `modelos/`, `pdf/`, `VARIAVEIS.md` | saída |

## Reproduzir do zero

```sh
git clone <repo> && cd relatorios-consultoria
npm install          # só Playwright; o gerador não tem dependências
npm run all
git status --short modelos/ VARIAVEIS.md    # deve vir vazio
```

`modelos/` e `VARIAVEIS.md` são **reprodutíveis byte a byte**: se vierem limpos, a saída
no repositório corresponde exatamente à fonte. É essa a verificação que vale.

`pdf/` **não** é byte a byte. O Chromium carimba data de criação no PDF, então os 24
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
| `ph(nome, dica)` | `.ph` | campo preenchível `{{nome}}` |

Modificadores de página, aplicados como `class` num `div` que envolve o conteúdo:
`.densa` aperta a escala inteira, para documento de página fechada que não pode
transbordar; `.principios` põe título e texto no mesmo parágrafo, em duas colunas.

Auxiliares de grelha, usados como `class`: `.cols2`, `.cols3`, `.cols2u` (1,35 : 1),
`.center` (usa a sobra vertical do slide), `.gap`.

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

**`BASE` passa por formatação `%`.** Qualquer `%` literal no CSS dessa string precisa
ser escrito `%%`. Um `50%` esquecido derruba o build com `TypeError`.

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
