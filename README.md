# Modelos de relatórios — AUVP Capital e AUVP Private Banking

Modelos de uso dos relatórios e apresentações entregues aos clientes, prontos para
serem preenchidos e exportados em PDF. São **24 arquivos HTML independentes**: cada
um traz o próprio CSS, a própria fonte e a própria paleta, abre com duplo clique em
qualquer navegador e não depende de nenhum outro arquivo do repositório.

Todo campo preenchível aparece como `{{nome_da_variavel}}`, destacado em dourado no
documento. O dicionário completo está em [`VARIAVEIS.md`](VARIAVEIS.md).

## Os 24 modelos

Os seis documentos existem nos quatro segmentos.

| Documento | Formato | Páginas | Consultoria | Alta Renda | Private | Assessoria |
| --- | --- | --- | :-: | :-: | :-: | :-: |
| Relatório mensal | A4 retrato | 13–14 | ✓ | ✓ | ✓ | ✓ |
| Diagnóstico de carteira | A4 retrato | 10 | ✓ | ✓ | ✓ | ✓ |
| Relatório macroeconômico | A4 retrato | 10 | ✓ | ✓ | ✓ | ✓ |
| Apresentação geral | 16:9 | 14 | ✓ | ✓ | ✓ | ✓ |
| Relatório mensal em apresentação | 16:9 | 12 | ✓ | ✓ | ✓ | ✓ |
| Cronograma de reuniões | A4 retrato | 6 | ✓ | ✓ | ✓ | ✓ |

Nomes de arquivo: `modelos/<documento>-<segmento>.html`, com segmento em
`consultoria`, `alta-renda`, `private`, `assessoria`.

## Como usar

**1. Preencher.** Abra o `.html` num editor de texto e substitua cada `{{token}}` —
chaves incluídas — pelo conteúdo real. Linhas de tabela que sobrarem devem ser
apagadas, não deixadas com o token à mostra. Para conferir enquanto edita, abra o
mesmo arquivo no navegador: os campos ainda não preenchidos ficam destacados.

**2. Gerar o PDF.**

A pasta `pdf/` já traz um PDF de cada um dos 24 modelos, para quem só quer ler o
resultado sem instalar nada. Para regerar depois de editar um modelo:

```sh
npm install
npm run pdf                          # todos os modelos -> pdf/
npm run pdf -- relatorio-mensal      # só os que casam com o filtro
```

Os PDFs são reproduzíveis a partir de `modelos/`; ao editar um modelo, regere o PDF
correspondente no mesmo commit para os dois não saírem de sincronia.

O script usa o Chromium do Playwright, respeita o tamanho de página definido em cada
arquivo e imprime os fundos coloridos. Alternativa sem Node: abrir o HTML no Chrome e
usar *Imprimir → Salvar como PDF*, com **margens em "Nenhuma"** e **"Gráficos de
segundo plano"** ligado.

**3. Conferir.** `npm run check` abre cada modelo em modo de impressão e acusa
qualquer conteúdo que estoure a caixa da página. Se um modelo ganhou ou perdeu campos,
`npm run vars` regenera o `VARIAVEIS.md`. Rode os dois depois de editar.

**4. Gráficos.** Os modelos trazem áreas tracejadas marcando onde entra cada gráfico,
com a descrição do que ele deve mostrar. Substitua o bloco `<div class="chart">…</div>`
pela imagem final (`<img src="..." style="width:100%">`) ou pelo gráfico gerado pela
ferramenta que o time já usa.

Nos blocos de número grande (KPIs), tokens longos como `{{patrimonio_total}}` quebram
em duas linhas — é da largura do token, não do layout, e some quando o valor real entra.

## Sistema visual

Extraído dos arquivos em `assets relatórios/` e do `MODELO SLIDES AUVP CAPITAL.pdf`.

| Segmento | Cor base | Capa | Logo |
| --- | --- | --- | --- |
| Consultoria | `#023620` | gradiente 225° da cor base até `#000` | AUVP CAPITAL |
| Alta Renda | `#010F08` | idem | AUVP CAPITAL |
| Assessoria | `#005F45` | idem | AUVP CAPITAL |
| Private Banking | `#666666` | idem | AUVP PRIVATE BANKING |

- **Acento:** `#EFBF4F` (dourado do deck institucional) na consultoria, na alta renda e
  na assessoria, usado com parcimônia e sempre como linha fina: a régua curta do
  olho-de-boi, a borda esquerda dos cards, os marcadores numéricos das linhas do tempo.
  Nunca em capas.
- **Private Banking não usa amarelo em lugar nenhum.** O acento é o neutro `#8C939A`, e
  com ele saem do amarelo também o realce dos campos preenchíveis e o selo de atenção
  do diagnóstico. São tokens de tema (`--accent`, `--ph`, `--warn-*`), então a regra
  vale para qualquer elemento novo sem precisar ser lembrada caso a caso. Vermelho e
  verde continuam disponíveis como sinal semântico — gravidade de risco, retorno
  positivo ou negativo — onde a cor ajuda a leitura.
- **Capas e divisórias são monocromáticas.** Logo, título, réguas, grafismo e campos
  preenchíveis, tudo em branco sobre o gradiente. O dourado só entra nas páginas de
  conteúdo, e apenas onde a cor ajuda a leitura.
- **Peso das linhas:** toda linha decorativa fica entre **0,75 pt e 1 pt** — réguas de
  capa, hairlines de tabela e cabeçalho, molduras tracejadas dos gráficos, traço dos
  grafismos e os acentos dourados. Não há barras espessas: os grafismos usam
  `vector-effect: non-scaling-stroke` para manter 0,75 pt em qualquer escala, em vez de
  afinar junto com o desenho.
- **Grafismos:** o de arcos é o único usado como elemento decorativo fora de capas.
  Os outros dois (leque de quadrados e ampulheta) ficam restritos a capas, como nas
  referências originais.
- **O grafismo de arcos nunca aparece inteiro.** Suas duas arestas retas — topo e
  direita — saem sempre da página, de modo que só os arcos entrem em cena. Na capa
  16:9 ele é espelhado na vertical para pôr o centro dos arcos no canto inferior
  direito, como na capa do deck de referência; nas divisórias fica na orientação
  nativa, com o centro no canto superior direito. `graf_arcos()` calcula a sangria a
  partir da fração de traço medida no SVG, então a regra vale em qualquer tamanho.
  Em uso decorativo os arcos entram sempre a **50% de opacidade**.
- **Tipografia:** Anek Latin em cinco pesos estáticos (300, 400, 600, 700, 800),
  subconjunto Latin-1 mais pontuação, embutidos em base64 em cada arquivo. Instâncias
  estáticas e não a fonte variável: o Chromium exporta fonte variável como Type3, o que
  triplica o PDF e quebra a seleção de texto. Uma só família nos quatro segmentos — a
  diferenciação é por cor e por logo, não por tipografia.
- **Textura:** granulado sobre todos os degradês — capas, divisórias e slides escuros —
  reproduzindo o do deck institucional. Ruído `feTurbulence` em ladrilho de 180 px a 22%
  de opacidade: sutil, mas perceptível o bastante para quebrar o bandeamento do
  degradê na impressão.
- **Página:** A4 (210 × 297 mm) nos relatórios; 338,667 × 190,5 mm (13,333 × 7,5 pol,
  o 16:9 padrão do PowerPoint) nas apresentações.

### Capas

As duas capas são construídas sobre medidas tiradas das referências, não estimadas.

**A4**, de `assets relatórios/SVG/ref *.svg`:

| Elemento | Medida |
| --- | --- |
| Margens laterais | 15,3 mm |
| Régua superior | y 86,0 mm, da margem à margem |
| Régua inferior | y 245,2 mm |
| Grafismo | entre as réguas, **com exatamente a largura delas** (traço de 15,3 a 194,7 mm), topo em 95,5 mm |
| Opacidade do grafismo | cheia no leque de quadrados; 50% na ampulheta do diagnóstico, cujo traço é bem mais denso |
| Título | 43,89 pt, entrelinha de 48 pt, linhas de base em 56,4 e 73,3 mm |
| Assinatura inferior | 32,13 pt, linha de base em 271,6 mm |

O grafismo é posicionado pela **tinta**, não pela caixa do SVG: os arquivos têm uma
margem interna de cerca de 7,6% de cada lado (o leque de quadrados ocupa 84,5% da
própria caixa), então `graf_span()` corrige isso para o traço bater com a régua nas
duas pontas. As frações do leque vêm da geometria dos 22 retângulos do arquivo; as dos
outros dois, de rasterização a 2400 px com limiar no preto puro — medir com limiar mais
alto perde os traços de 10% de opacidade e desalinha o grafismo em cerca de 4 mm.

**16:9**, da página 1 de `MODELO SLIDES AUVP CAPITAL.pdf`:

| Elemento | Medida |
| --- | --- |
| Faixa branca | de 0 a 26,3 mm, com o rótulo do segmento à esquerda e a logo à direita |
| Régua curta | x 24,6 a 74,9 mm, y 68,4 mm |
| Título | 44,6 pt, linha de base em 106,7 mm |
| Subtítulo | 25,3 pt, linha de base em 120,2 mm |
| Grafismo de arcos | sangrando no canto inferior direito, a 50% de opacidade |

## Cobertura do relatório gerado hoje

O relatório mensal cobre, seção a seção, tudo o que a especificação do Consolidador
lista como conteúdo atual. As seções marcadas lá como "quando há dado" continuam
condicionais aqui e trazem o selo *Somente quando houver dado*.

| Seção do relatório atual | O que mostra hoje | Onde está no modelo |
| --- | --- | --- |
| Capa | cliente, perfil e consultor sobre a arte de fundo | capa |
| Resumo da carteira | patrimônio, rentabilidade no mês e no ano, ganhos, aplicações e tabela do portfólio | **Resumo da carteira** (8 cards, incluindo ganho em R$ e aplicações) + **Carteira consolidada** |
| Rentabilidade | gráfico da carteira contra benchmark (IPCA + 5% a.a.) | Resumo da carteira: tabela de referências e gráfico "Carteira x IPCA + 5% a.a." |
| Movimentações e proventos | ativos comprados no mês e gráfico de proventos | **Movimentações e proventos**, com a tabela de operações e o gráfico de proventos por mês |
| Alocação por estratégia | carteira atual contra a carteira meta | **Alocação por estratégia** |
| Renda fixa | indexadores, liquidez projetada e controle por emissor | **Renda fixa**, com as três tabelas |
| Ações e FIIs | distribuição por setor/segmento e lista de ativos | **Ações e fundos imobiliários**, duas roscas e duas listas |
| Internacional | renda fixa e renda variável em US$ | **Carteira internacional**, condicional |
| Encerramento | mensagem, assinatura do consultor e contatos | **Encerramento e próximos passos** |

Os elementos recorrentes citados como necessitando padrão único têm cada um a sua
classe: capa (`.cover`), papel timbrado (`.pg-head` / `.pg-foot`), cards de indicadores
(`.kpi`), tabelas (`.tb`, com `thead`, `tbody` e `tfoot`), gráficos (`.chart`) e bloco
de assinatura (`.sig`).

## Insumos para a implementação

A especificação pede um conjunto fechado de insumos por segmento. Todos estão no
`:root` de cada arquivo, como tokens CSS.

**Paleta.** `--brand` é a principal e `--accent` a de apoio. A sequência dos gráficos
são `--c1` a `--c6`, definida por segmento:

| Segmento | `--c1` | `--c2` | `--c3` | `--c4` | `--c5` | `--c6` |
| --- | --- | --- | --- | --- | --- | --- |
| Consultoria | `#023620` | `#3E7A52` | `#7FAE86` | `#B9D3B6` | `#EFBF4F` | `#8C7A3E` |
| Alta Renda | `#010F08` | `#2E5C3F` | `#6A9673` | `#A8C4A6` | `#EFBF4F` | `#8C7A3E` |
| Assessoria | `#005F45` | `#3E8F6C` | `#7CBB99` | `#B7DCC6` | `#EFBF4F` | `#8C7A3E` |
| Private Banking | `#3A3E42` | `#5C6167` | `#82888E` | `#A8ADB2` | `#CBCFD3` | `#E2E5E7` |

**Fontes e pesos.** Anek Latin em 300, 400, 600, 700 e 800, nos quatro segmentos.

**Tamanhos.** A4: título de capa 43,89 pt, assinatura de capa 32,13 pt, título de
página 19 pt, seção 10 pt, texto 10 pt, tabela 8,2 pt (`.sm` 7,4 pt, `.xs` 6,6 pt),
rodapé 6,2 pt. 16:9: título de capa 44,6 pt, subtítulo 25,3 pt, título de slide 26 pt,
texto 11 pt, tabela 9,5 pt.

**Logos.** Os SVGs originais entram embutidos e são recoloridos por CSS; a largura sai
de uma altura-alvo, porque a marca do Private Banking é bem mais larga que a do Capital.
Ao lado de uma logo o texto só traz o que ela não diz: a marca do Capital não nomeia o
segmento, então "Consultoria", "Alta Renda" e "Assessoria" aparecem; a do Private
Banking já o nomeia, então ali não há rótulo nenhum. É o token `rotulo` do tema, vazio
no private.

**Componentes.** Rosca, barra e linha têm esqueleto em `.sk-donut`, `.sk-bars` e
`.sk-line`, dentro da moldura `.chart` que descreve o que o gráfico deve mostrar.
Tabelas, cards, capa, papel timbrado e assinatura estão nas classes listadas acima.

## O que cada documento cobre

**Relatório mensal** — carta do responsável e índice; resumo da carteira; carteira
consolidada; alocação por estratégia; desempenho por classe e por ativo; movimentações
e proventos; renda fixa; ações e FIIs; internacional; cenário e posicionamento;
encerramento; notas metodológicas. Três dos quatro segmentos ganham ainda uma página
própria: ofertas exclusivas na alta renda, estruturas e sucessão no private e
transparência de remuneração na assessoria — esta última fecha o que a apresentação
geral do segmento promete ao cliente.

**Diagnóstico de carteira** — escopo e método; perfil, objetivos e restrições;
fotografia da carteira atual; pontos fortes e pontos de atenção; concentração por
emissor, prazo e moeda; custos e eficiência tributária; carteira proposta; plano de
transição; premissas e limitações.

**Relatório macroeconômico** — resumo executivo com os cinco fatos do mês e onde a
casa mudou de opinião; cenário internacional; Brasil em atividade e inflação; juros,
fiscal e câmbio; desempenho dos mercados; projeções contra o consenso; implicações
para a carteira do segmento; agenda do mês seguinte.

**Apresentação geral** — capa, divisórias de seção, quem somos, números, método em
cinco etapas, diferenciais e entregas, governança e alçadas, tela de planos e taxas,
time, primeiros passos e contato com QR code.

**Relatório mensal em apresentação** — a mesma informação do relatório mensal no ritmo
de uma reunião: agenda, fechamento do mês, rentabilidade contra referências, alocação,
destaques e detratores, movimentações, página do segmento, cenário, próximos passos e
encerramento.

**Cronograma de reuniões** — ritmo de acompanhamento do segmento, calendário dos doze
meses, pauta e entregável de cada tipo de encontro, canais e SLA de resposta, regras de
remarcação e QR de agendamento. A cadência já vem diferente por segmento: trimestral na
consultoria, trimestral com revisão semestral na alta renda, mensal com comitê
trimestral no private e semestral com contatos da mesa na assessoria.

## Decisões que ficaram em aberto

- **`{{disclaimer_regulatorio}}`** aparece em 16 dos 19 modelos como campo preenchível.
  O texto legal muda conforme o segmento seja consultoria (Resolução CVM 19),
  distribuição/assessoria (Resolução CVM 178) ou private, e precisa vir do compliance —
  não foi redigido aqui. Os demais avisos legais (rentabilidade passada, FGC, proibição
  de compartilhamento) já estão escritos e são comuns aos quatro segmentos.
- **Conteúdo da assessoria.** As variantes de assessoria partem do princípio de que o
  segmento opera por distribuição remunerada por comissão, e não por taxa cobrada do
  cliente: a apresentação geral fala em "sem taxa de assessoria" e em transparência de
  remuneração, e o diagnóstico foca em custo embutido. Se o modelo comercial for outro,
  esses três blocos precisam ser reescritos.

## Estrutura do repositório

```
modelos/                        24 modelos HTML independentes
pdf/                            um PDF de cada modelo, versionado (saída do npm run pdf)
scripts/render.mjs              HTML -> PDF via Playwright
scripts/check.mjs               verificação de estouro de página
scripts/variaveis.mjs           gera o VARIAVEIS.md a partir dos modelos
assets/fonts/                   Anek Latin (woff2)
assets relatórios/              logos, grafismos e referências originais (fonte de verdade)
MODELO SLIDES AUVP CAPITAL.pdf  deck institucional de referência
VARIAVEIS.md                    dicionário de todos os campos preenchíveis
```

Os modelos são arquivos independentes por decisão de projeto: cada um pode divergir dos
outros sem efeito colateral. Em compensação, uma correção no sistema visual precisa ser
repetida em cada arquivo — o CSS fica no topo de cada `.html`, entre `<style>` e
`</style>`, e é idêntico entre os modelos do mesmo formato, exceto pelo bloco `:root`
com as cores do segmento.
