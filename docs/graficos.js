/* Os gráficos, desenhados a partir do que o consultor digitou.
 *
 * Antes, um gráfico no documento era um espaço de imagem: o consultor montava a
 * rosca em outro lugar, exportava um PNG e subia. O PNG chegava numa resolução
 * qualquer, com a fonte de outro sistema e as cores de outro tema, e ninguém
 * conseguia corrigir um número sem refazer tudo.
 *
 * Aqui ele digita rótulo e valor, e o desenho sai em SVG dentro do próprio
 * documento: vetor no PDF, na tipografia da casa, nas cores do segmento — que
 * vêm de `--c1`..`--c6`, as mesmas da legenda — e editável até o último minuto.
 *
 * São quatro formatos, e cada um existe porque um documento pede:
 *
 *   donut  uma rosca: a divisão de um todo em partes.
 *   anel   duas roscas concêntricas: a de fora é o que se tem, a de dentro é a
 *          meta (ou a proposta). É a carteira atual x meta.
 *   bars   barras verticais: uma série ao longo do tempo, como os proventos mês
 *          a mês.
 *   line   uma linha: a evolução do patrimônio.
 *
 * Nada aqui depende de biblioteca: o SVG é montado à mão, o arquivo exportado
 * abre sozinho por `file://` e o Chromium imprime o vetor sem rasterizar.
 */

/* Tudo isto vive dentro de uma função. `app.js` e este arquivo são scripts
 * clássicos, e scripts clássicos dividem um escopo global só: `escapa` daqui
 * colidiu com `escapa` de lá e derrubou a página inteira no carregamento. Com a
 * função em volta, o único nome que sai é `window.Graficos`.
 */
(function () {

  /* O quadro de desenho. A caixa do documento tem a proporção que tiver, então o
   * SVG trabalha num sistema de coordenadas fixo e o `viewBox` o encaixa. */
  /* A caixa de desenho.
   *
   *  Era fixa em 400 por 260, e por isso um gráfico numa faixa larga e baixa —
   *  a evolução do patrimônio ocupa a página inteira e uns quatro centímetros
   *  de altura — encolhia até caber na altura e deixava metade da largura vazia.
   *  Agora a proporção vem da caixa que o documento reservou: o desenho se
   *  estica no eixo em que há espaço.
   *
   *  A largura é sempre 400 porque é ela que fixa a escala do texto; o que muda
   *  é a altura, limitada para o gráfico não virar nem uma tira nem um poste. */
  const LARGURA = 400;
  const ALTURA_MIN = 120;
  const ALTURA_MAX = 640;
  const ALTURA_PADRAO = 260;

  function geometria(caixa) {
    if (!caixa || !caixa.w || !caixa.h) return { W: LARGURA, H: ALTURA_PADRAO };
    const alta = Math.round(LARGURA * (caixa.h / caixa.w));
    return { W: LARGURA, H: Math.min(ALTURA_MAX, Math.max(ALTURA_MIN, alta)) };
  }

  const CORES = 8;
  const cor = (i) => `var(--c${(i % CORES) + 1})`;

  /** Um número a partir do que a pessoa digitou. Aceita "1.234,56", "1234.56",
   *  "R$ 1.234", "12%" e devolve 0 para o que não for número — uma linha em
   *  branco não deve derrubar o gráfico inteiro. */
  function numero(v) {
    if (typeof v === 'number') return v;
    const t = String(v || '').replace(/[^\d,.\-]/g, '');
    if (!t) return 0;
    // Vírgula depois do último ponto quer dizer decimal brasileiro.
    const br = t.lastIndexOf(',') > t.lastIndexOf('.');
    const n = Number(br ? t.replace(/\./g, '').replace(',', '.') : t.replace(/,/g, ''));
    return Number.isFinite(n) ? n : 0;
  }

  const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  /** Cada linha vira `{r, v: [...]}`, com um valor por série.
   *
   *  Um gráfico pode ter mais de uma série: o juro longo contra o dólar, a
   *  carteira contra o benchmark, a curva de hoje contra a de um ano atrás. A
   *  rosca dupla é o mesmo caso — a série de fora é a posição atual e a de
   *  dentro é a meta —, e por isso o par `atual/meta` deixou de ser especial.
   *
   *  Rascunho salvo antes disto guardava `{r, v, m}`: continua sendo lido. */
  function normaliza(linhas) {
    return (linhas || []).map((l) => {
      if (Array.isArray(l.v)) return { r: l.r || '', v: l.v };
      return { r: l.r || '', v: [l.v, l.m].filter((x) => x !== undefined) };
    });
  }

  /** As linhas que valem: as que têm rótulo ou algum valor. */
  const validas = (linhas) => normaliza(linhas).filter(
    (l) => l.r.trim() || l.v.some((x) => numero(x)));

  /** Quantas séries o gráfico tem de fato. */
  const quantas = (l) => Math.max(1, ...l.map((x) => x.v.length));

  /* ------------------------------------------------------------------ roscas */

  /** Um arco de rosca, em coordenadas polares. `de` e `ate` em voltas (0 a 1). */
  function arco(cx, cy, raio, de, ate) {
    // Uma fatia que dá a volta inteira não tem arco: os dois pontos coincidem e
    // o caminho some. Desenha-se como dois semicírculos.
    if (ate - de >= 0.9999) {
      return `M ${cx - raio} ${cy} A ${raio} ${raio} 0 1 1 ${cx + raio} ${cy}`
           + ` A ${raio} ${raio} 0 1 1 ${cx - raio} ${cy}`;
    }
    const p = (t) => {
      const a = (t - 0.25) * 2 * Math.PI;   // começa no topo
      return [cx + raio * Math.cos(a), cy + raio * Math.sin(a)];
    };
    const [x1, y1] = p(de);
    const [x2, y2] = p(ate);
    return `M ${x1} ${y1} A ${raio} ${raio} 0 ${ate - de > 0.5 ? 1 : 0} 1 ${x2} ${y2}`;
  }

  /** Um ponto da circunferência; `t` em voltas, começando no topo. */
  function polar(cx, cy, raio, t) {
    const a = (t - 0.25) * 2 * Math.PI;
    return [cx + raio * Math.cos(a), cy + raio * Math.sin(a)];
  }

  /** Um setor de coroa: arco de fora, lado, arco de dentro ao contrário. */
  function setor(cx, cy, rFora, rDentro, de, ate) {
    const grande = ate - de > 0.5 ? 1 : 0;
    const [x1, y1] = polar(cx, cy, rFora, de);
    const [x2, y2] = polar(cx, cy, rFora, ate);
    const [x3, y3] = polar(cx, cy, rDentro, ate);
    const [x4, y4] = polar(cx, cy, rDentro, de);
    return `M ${x1} ${y1} A ${rFora} ${rFora} 0 ${grande} 1 ${x2} ${y2} L ${x3} ${y3}`
         + ` A ${rDentro} ${rDentro} 0 ${grande} 0 ${x4} ${y4} Z`;
  }

  /** As fatias de uma rosca, no padrão do design system: separadas por um
   *  pequeno vão (paddingAngle 3°) e com os cantos arredondados (cornerRadius
   *  4). O canto redondo vem de um traço da mesma cor com junção redonda por
   *  cima do preenchimento — o truque encolhe a geometria pelo raio do canto,
   *  e o traço devolve o tamanho. A fatia fina demais para o vão sai inteira,
   *  reta: sumir com ela seria mentir sobre o dado. Uma fatia só é o anel
   *  inteiro, sem vão. */
  function rosca(valores, g, cx, cy, raio, largura) {
    const total = valores.reduce((a, b) => a + b, 0);
    if (total <= 0) return '';
    const fatias = valores.filter((v) => v > 0).length;
    const canto = Math.min(4, largura / 3);
    const rFora = raio + largura / 2 - canto;
    const rDentro = raio - largura / 2 + canto;
    const vao = 3 / 360;
    const recuo = vao / 2 + canto / (2 * Math.PI * rDentro);
    let t = 0;
    return valores.map((v, i) => {
      const de = t;
      t += v / total;
      if (v <= 0) return '';
      if (fatias === 1) {
        return `<path d="${arco(cx, cy, raio, 0, 1)}" fill="none" stroke="${cor(i)}" stroke-width="${largura}"/>`;
      }
      if (t - de <= 2 * recuo + 0.003) {
        return `<path d="${setor(cx, cy, raio + largura / 2, raio - largura / 2, de, t)}" fill="${cor(i)}"/>`;
      }
      return `<path d="${setor(cx, cy, rFora, rDentro, de + recuo, t - recuo)}" fill="${cor(i)}"`
           + ` stroke="${cor(i)}" stroke-width="${canto * 2}" stroke-linejoin="round"/>`;
    }).join('');
  }

  const NOTA_ANEL = 'Rosca externa: posição atual &middot; rosca interna: meta';

  function donut(l, duplo, g) {
    // A rosca é redonda: cresce com o lado menor da caixa, e fica no meio dela.
    const raio = Math.min(g.W, g.H) * 0.38;
    const grossura = raio * 0.36;
    const cx = g.W / 2;
    const cy = g.H / 2;
    const fora = rosca(l.map((x) => numero(x.v[0])), g, cx, cy, raio, grossura);
    const dentro = duplo && quantas(l) > 1
      ? rosca(l.map((x) => numero(x.v[1])), g, cx, cy, raio * 0.54, grossura * 0.76)
      : '';
    return { svg: fora + dentro, chaves: l.map((x) => x.r), nota: dentro ? NOTA_ANEL : '' };
  }

  /* ------------------------------------------------------- barras e linha */

  /** O topo do eixo, arredondado para um número redondo. */
  function teto(max) {
    if (max <= 0) return 1;
    const ordem = 10 ** Math.floor(Math.log10(max));
    return Math.ceil(max / (ordem / 2)) * (ordem / 2);
  }

  const curto = (n) => {
    const a = Math.abs(n);
    if (a >= 1e9) return (n / 1e9).toFixed(1).replace('.', ',') + ' bi';
    if (a >= 1e6) return (n / 1e6).toFixed(1).replace('.', ',') + ' mi';
    if (a >= 1e3) return Math.round(n / 1e3) + ' mil';
    return String(Math.round(n * 100) / 100).replace('.', ',');
  };

  /** A moldura de quem tem eixo: guias, escala e rótulos do eixo horizontal. */
  function comEixo(l, series, desenho, g) {
    const n = quantas(l);
    const vals = l.map((x) => Array.from({ length: n }, (_, k) => numero(x.v[k])));
    const alvo = teto(Math.max(0, ...vals.flat()));
    // Valor negativo puxa o eixo para baixo do zero: a barra desce, a linha
    // cruza a linha do zero. Antes o negativo era cortado em zero.
    const menor = Math.min(0, ...vals.flat());
    const chao = menor < 0 ? -teto(-menor) : 0;
    const esq = 54;
    const base = g.H - 34;
    const alto = base - 16;
    const larg = g.W - esq - 14;
    const y = (v) => base - ((v - chao) / (alvo - chao || 1)) * alto;
    const marcas = chao < 0 ? [chao, 0, alvo] : [0, alvo / 2, alvo];
    const guias = marcas.map((v) => {
      const py = y(v);
      return `<line x1="${esq}" y1="${py}" x2="${esq + larg}" y2="${py}" class="${v === 0 && chao < 0 ? 'g-zero' : 'g-guia'}"/>`
           + `<text x="${esq - 7}" y="${py + 4}" class="g-eixo" text-anchor="end">${curto(v)}</text>`;
    }).join('');
    // Com muitos pontos, um rótulo em cada vira uma tarja preta: mostra um a
    // cada dois, e sempre o primeiro e o último.
    const passo = Math.ceil(l.length / 8);
    const rotulos = l.map((x, i) => {
      if (i % passo && i !== l.length - 1) return '';
      const px = esq + larg * ((i + 0.5) / l.length);
      return `<text x="${px}" y="${base + 16}" class="g-eixo" text-anchor="middle">${esc(x.r)}</text>`;
    }).join('');
    return {
      svg: guias + desenho({ vals, n, alvo, chao, y, esq, base, alto, larg }) + rotulos,
      // A legenda de quem tem eixo nomeia as séries, e não as linhas: o eixo
      // horizontal já diz o que é cada ponto.
      chaves: n > 1 ? Array.from({ length: n }, (_, k) => (series || [])[k] || `Série ${k + 1}`) : [],
    };
  }

  const bars = (l, series, g) => comEixo(l, series, ({ vals, n, chao, y, esq, larg }) => {
    const passo = larg / vals.length;
    const w = Math.min(38, (passo * 0.62) / n);
    const y0 = y(0);
    // Série única com sinal é dado divergente: verde acima do zero, vermelho
    // abaixo, como o design system pede para rentabilidade e variação.
    const divergente = n === 1 && chao < 0;
    return vals.map((linha, i) => linha.map((v, k) => {
      const yv = y(v);
      const x = esq + passo * (i + 0.5) - (w * n) / 2 + w * k;
      const fill = divergente ? (v < 0 ? 'var(--g-neg)' : 'var(--g-pos)') : cor(k);
      return `<rect x="${x}" y="${Math.min(y0, yv)}" width="${w}" height="${Math.abs(y0 - yv)}" fill="${fill}" rx="1.5"/>`;
    }).join('')).join('');
  }, g);

  const line = (l, series, g) => comEixo(l, series, ({ vals, n, y, esq, larg }) => {
    const passo = larg / vals.length;
    const ponto = (v, i) => [esq + passo * (i + 0.5), y(v)];
    let fora = '';
    for (let k = 0; k < n; k += 1) {
      const pts = vals.map((linha, i) => ponto(linha[k], i));
      const d = pts.map(([x, y], i) => `${i ? 'L' : 'M'} ${x} ${y}`).join(' ');
      // A área só embaixo da primeira série: com duas ou três sombreadas, uma
      // tapa a outra e o gráfico vira mancha.
      if (k === 0 && n === 1) {
        const y0 = y(0);
        fora += `<path d="${d} L ${pts[pts.length - 1][0]} ${y0} L ${pts[0][0]} ${y0} Z" class="g-area"/>`;
      }
      fora += `<path d="${d}" class="g-linha" style="stroke:${cor(k)}"/>`;
      // Com muitos pontos e várias séries os marcadores viram ruído.
      if (vals.length <= 14 && n <= 2) {
        fora += pts.map(([x, y]) =>
          `<circle cx="${x}" cy="${y}" r="3.2" class="g-ponto" style="stroke:${cor(k)}"/>`).join('');
      }
    }
    return fora;
  }, g);

  const FORMATOS = {
    donut: (l, series, g) => donut(l, false, g),
    anel: (l, series, g) => donut(l, true, g),
    bars,
    line,
  };

  /** A legenda. Nas roscas nomeia as fatias; nos de eixo, as séries. */
  function legenda(chaves) {
    if (!chaves.length) return '';
    return '<ul class="legend">' + chaves.map((x, i) =>
      `<li><i style="background:${cor(i)}"></i>${esc(x || '—')}</li>`).join('') + '</ul>';
  }

  /** O gráfico pronto, como HTML, para entrar no lugar da moldura vazia.
   *  Devolve '' quando não há dado: sem dado, a moldura vazia continua sendo a
   *  resposta certa — ela diz o que falta. */
  function desenha(tipo, linhas, series, caixa) {
    const f = FORMATOS[tipo];
    if (!f) return '';
    const l = validas(linhas);
    if (!l.length) return '';
    const g = geometria(caixa);
    const { svg, chaves, nota } = f(l, series, g);
    if (!svg) return '';
    return `<svg class="g-svg" viewBox="0 0 ${g.W} ${g.H}" preserveAspectRatio="xMidYMid meet"`
         + ` role="img">${svg}</svg>${legenda(chaves)}`
         + (nota ? `<div class="g-nota">${nota}</div>` : '');
  }

  /* Sem `export`: `app.js` é script clássico e o site não tem build. O punhado de
   * nomes que o resto precisa sai por aqui, e o resto do arquivo fica fechado. */
  window.Graficos = {
    desenha, numero,
    // Rótulo sem valor não é dado: a tabelinha abre com os doze meses escritos,
    // e desenhar um gráfico só porque eles estão lá daria uma linha rente ao
    // zero no lugar da moldura que pede preenchimento.
    temDados: (l) => normaliza(l).some((x) => x.v.some((v) => numero(v))),
    // Quantas colunas de valor a tabelinha oferece, e com que nome. É o que faz
    // o juro longo e o dólar caberem no mesmo gráfico sem a ferramenta precisar
    // saber o que é um gráfico.
    colunas: (tipo, series, eixo) => {
      if (tipo === 'anel') return ['Atual', 'Meta'];
      if (series && series.length && (tipo === 'line' || tipo === 'bars')) return series.slice();
      return [eixo || 'Valor'];
    },
  };
}());
