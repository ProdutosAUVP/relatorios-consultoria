# Modelos de relatórios — AUVP Capital e AUVP Private Banking

Modelos de uso dos relatórios e apresentações entregues aos clientes, prontos para
serem preenchidos e exportados em PDF. São **19 arquivos HTML independentes**: cada
um traz o próprio CSS, a própria fonte e a própria paleta, abre com duplo clique em
qualquer navegador e não depende de nenhum outro arquivo do repositório.

Todo campo preenchível aparece como `{{nome_da_variavel}}`, destacado em dourado no
documento. O dicionário completo está em [`VARIAVEIS.md`](VARIAVEIS.md).

## Os 19 modelos

| Documento | Formato | Páginas | Consultoria | Alta Renda | Private | Assessoria |
| --- | --- | --- | :-: | :-: | :-: | :-: |
| Relatório mensal | A4 retrato | 10 | ✓ | ✓ | ✓ | ✓ |
| Diagnóstico de carteira | A4 retrato | 10 | ✓ | ✓ | ✓ | — |
| Relatório macroeconômico | A4 retrato | 10 | ✓ | ✓ | ✓ | — |
| Apresentação geral | 16:9 | 14 | ✓ | ✓ | ✓ | — |
| Relatório mensal em apresentação | 16:9 | 12 | ✓ | ✓ | ✓ | — |
| Cronograma de reuniões | A4 retrato | 6 | ✓ | ✓ | ✓ | — |

Nomes de arquivo: `modelos/<documento>-<segmento>.html`, com segmento em
`consultoria`, `alta-renda`, `private`, `assessoria`.

## Como usar

**1. Preencher.** Abra o `.html` num editor de texto e substitua cada `{{token}}` —
chaves incluídas — pelo conteúdo real. Linhas de tabela que sobrarem devem ser
apagadas, não deixadas com o token à mostra. Para conferir enquanto edita, abra o
mesmo arquivo no navegador: os campos ainda não preenchidos ficam destacados.

**2. Gerar o PDF.**

```sh
npm install
npm run pdf                          # todos os modelos -> pdf/
npm run pdf -- relatorio-mensal      # só os que casam com o filtro
```

O script usa o Chromium do Playwright, respeita o tamanho de página definido em cada
arquivo e imprime os fundos coloridos. Alternativa sem Node: abrir o HTML no Chrome e
usar *Imprimir → Salvar como PDF*, com **margens em "Nenhuma"** e **"Gráficos de
segundo plano"** ligado.

**3. Conferir.** `npm run check` abre cada modelo em modo de impressão e acusa
qualquer conteúdo que estoure a caixa da página. Rode depois de editar.

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
| Alta Renda | `#022620` | idem | AUVP CAPITAL |
| Assessoria | `#005F45` | idem | AUVP CAPITAL |
| Private Banking | `#666666` | idem | AUVP PRIVATE BANKING |

- **Acento:** `#EFBF4F` (dourado do deck institucional), usado com parcimônia e sempre
  como linha fina: a régua curta do olho-de-boi, a borda esquerda dos cards, os
  marcadores numéricos das linhas do tempo. Nunca em capas.
- **Capas e divisórias são monocromáticas.** Logo, título, réguas, grafismo e campos
  preenchíveis, tudo em branco sobre o gradiente. O dourado só entra nas páginas de
  conteúdo, e apenas onde a cor ajuda a leitura.
- **Peso das linhas:** toda linha decorativa fica entre **0,75 pt e 1 pt** — réguas de
  capa, hairlines de tabela e cabeçalho, molduras tracejadas dos gráficos, traço dos
  grafismos e os acentos dourados. Não há barras espessas: os grafismos usam
  `vector-effect: non-scaling-stroke` para manter 0,75 pt em qualquer escala, em vez de
  afinar junto com o desenho.
- **Grafismos:** o de arcos é o único usado como elemento decorativo em páginas
  internas e divisórias. Os outros dois (leque de quadrados e ampulheta) ficam
  restritos a capas, como nas referências originais.
- **Tipografia:** Anek Latin em cinco pesos estáticos (300, 400, 600, 700, 800),
  subconjunto Latin-1 mais pontuação, embutidos em base64 em cada arquivo. Instâncias
  estáticas e não a fonte variável: o Chromium exporta fonte variável como Type3, o que
  triplica o PDF e quebra a seleção de texto.
- **Textura:** grão sutil sobre as capas, reproduzindo o do deck institucional.
- **Página:** A4 (210 × 297 mm) nos relatórios; 338,667 × 190,5 mm (13,333 × 7,5 pol,
  o 16:9 padrão do PowerPoint) nas apresentações.

## O que cada documento cobre

**Relatório mensal** — carta do responsável e índice; panorama com KPIs e
rentabilidade contra CDI, IPCA+5% e Ibovespa; alocação alvo × realizado; atribuição de
resultado por classe e por ativo; movimentações e proventos; uma página específica do
segmento (renda fixa e vencimentos na consultoria e na assessoria, ofertas exclusivas
na alta renda, estruturas e internacional no private); cenário e posicionamento;
próximos passos; notas metodológicas.

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
trimestral no private.

## Decisões que ficaram em aberto

- **`{{disclaimer_regulatorio}}`** aparece em 16 dos 19 modelos como campo preenchível.
  O texto legal muda conforme o segmento seja consultoria (Resolução CVM 19),
  distribuição/assessoria (Resolução CVM 178) ou private, e precisa vir do compliance —
  não foi redigido aqui. Os demais avisos legais (rentabilidade passada, FGC, proibição
  de compartilhamento) já estão escritos e são comuns aos quatro segmentos.
- **Acento dourado no Private Banking.** Mantido `#EFBF4F` por coerência com o resto da
  marca. Para trocar por prata, basta alterar `--accent` no `:root` dos três arquivos
  `*-private.html`.
- **Assessoria** só tem relatório mensal, conforme o escopo pedido. Os outros cinco
  documentos usam a paleta `#005F45` se precisarem ser estendidos ao segmento.

## Estrutura do repositório

```
modelos/                        19 modelos HTML independentes
pdf/                            PDFs gerados (fora do git, saída do npm run pdf)
scripts/render.mjs              HTML -> PDF via Playwright
scripts/check.mjs               verificação de estouro de página
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
