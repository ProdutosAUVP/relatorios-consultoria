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
  const W = 400;
  const H = 260;

  const CORES = 6;
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

  const escapa = (s) => String(s ?? '').replace(/[&<>"]/g, (c) =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  /** As linhas que valem: as que têm rótulo ou valor. */
  const validas = (linhas) => (linhas || []).filter((l) => (l.r || '').trim() || numero(l.v) || numero(l.m));

  /* ------------------------------------------------------------------ roscas */

  /** Um arco de rosca, em coordenadas polares. `de` e `ate` em voltas (0 a 1). */
  function arco(cx, cy, raio, largura, de, ate) {
    // Uma fatia que dá a volta inteira não tem arco: os dois pontos coincidem e o
    // caminho some. Desenha-se como dois semicírculos.
    if (ate - de >= 0.9999) {
      const r = raio;
      return `M ${cx - r} ${cy} A ${r} ${r} 0 1 1 ${cx + r} ${cy}`
           + ` A ${r} ${r} 0 1 1 ${cx - r} ${cy}`;
    }
    const p = (t) => {
      const a = (t - 0.25) * 2 * Math.PI;   // começa no topo
      return [cx + raio * Math.cos(a), cy + raio * Math.sin(a)];
    };
    const [x1, y1] = p(de);
    const [x2, y2] = p(ate);
    return `M ${x1} ${y1} A ${raio} ${raio} 0 ${ate - de > 0.5 ? 1 : 0} 1 ${x2} ${y2}`;
  }

  function anelSvg(valores, cx, cy, raio, largura) {
    const total = valores.reduce((a, b) => a + b, 0);
    if (total <= 0) return '';
    let t = 0;
    return valores.map((v, i) => {
      const de = t;
      t += v / total;
      if (v <= 0) return '';
      return `<path d="${arco(cx, cy, raio, largura, de, t)}" fill="none" stroke="${cor(i)}"`
           + ` stroke-width="${largura}"/>`;
    }).join('');
  }

  const nota = 'Rosca externa: posição atual &middot; rosca interna: meta';

  function donut(linhas, opcoes = {}) {
    const l = validas(linhas);
    const fora = anelSvg(l.map((x) => numero(x.v)), W / 2, H / 2, 78, 34);
    const dentro = opcoes.duplo
      ? anelSvg(l.map((x) => numero(x.m)), W / 2, H / 2, 42, 26)
      : '';
    // A legenda das duas roscas vai embaixo, e não no miolo: o furo do anel
    // interno tem menos de dois centímetros, e a frase que cabia ali não cabia.
    return { svg: fora + dentro, itens: l, nota: opcoes.duplo ? nota : '' };
  }

  /* ------------------------------------------------------- barras e linha */

  /** A escala vertical: o topo do eixo, arredondado para um número redondo. */
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

  function comEixo(linhas, desenho) {
    const l = validas(linhas);
    if (!l.length) return { svg: '', itens: [] };
    const vals = l.map((x) => numero(x.v));
    const alvo = teto(Math.max(...vals, 0));
    const esq = 54;
    const base = H - 34;
    const alto = base - 16;
    const larg = W - esq - 14;
    const guias = [0, 0.5, 1].map((f) => {
      const y = base - f * alto;
      return `<line x1="${esq}" y1="${y}" x2="${esq + larg}" y2="${y}" class="g-guia"/>`
           + `<text x="${esq - 7}" y="${y + 4}" class="g-eixo" text-anchor="end">${curto(alvo * f)}</text>`;
    }).join('');
    const rotulos = l.map((x, i) => {
      const px = esq + larg * ((i + 0.5) / l.length);
      return `<text x="${px}" y="${base + 16}" class="g-eixo" text-anchor="middle">${escapa(x.r || '')}</text>`;
    }).join('');
    return { svg: guias + desenho({ l, vals, alvo, esq, base, alto, larg }) + rotulos, itens: [] };
  }

  const bars = (linhas) => comEixo(linhas, ({ l, vals, alvo, esq, base, alto, larg }) => {
    const passo = larg / l.length;
    const w = Math.min(38, passo * 0.56);
    return vals.map((v, i) => {
      const h = alvo > 0 ? Math.max(0, (v / alvo) * alto) : 0;
      const x = esq + passo * (i + 0.5) - w / 2;
      return `<rect x="${x}" y="${base - h}" width="${w}" height="${h}" fill="var(--c1)" rx="1.5"/>`;
    }).join('');
  });

  const line = (linhas) => comEixo(linhas, ({ l, vals, alvo, esq, base, alto, larg }) => {
    const passo = larg / l.length;
    const pt = (v, i) => [esq + passo * (i + 0.5), base - (alvo > 0 ? (v / alvo) * alto : 0)];
    const pontos = vals.map(pt);
    const d = pontos.map(([x, y], i) => `${i ? 'L' : 'M'} ${x} ${y}`).join(' ');
    const area = `${d} L ${pontos[pontos.length - 1][0]} ${base} L ${pontos[0][0]} ${base} Z`;
    return `<path d="${area}" class="g-area"/><path d="${d}" class="g-linha"/>`
         + pontos.map(([x, y]) => `<circle cx="${x}" cy="${y}" r="3.2" class="g-ponto"/>`).join('');
  });

  const FORMATOS = {
    donut: (l) => donut(l),
    anel: (l) => donut(l, { duplo: true }),
    bars,
    line,
  };

  /** A legenda, quando o formato tem séries nomeadas por cor. */
  function legenda(itens) {
    if (!itens.length) return '';
    return '<ul class="legend">' + itens.map((x, i) =>
      `<li><i style="background:${cor(i)}"></i>${escapa(x.r || '—')}</li>`).join('') + '</ul>';
  }

  /** O gráfico pronto, como HTML, para entrar no lugar da moldura vazia.
   *  Devolve '' quando não há dado: sem dado, a moldura vazia continua sendo a
   *  resposta certa — ela diz o que falta. */
  function desenha(tipo, linhas) {
    const f = FORMATOS[tipo];
    if (!f) return '';
    if (!validas(linhas).length) return '';
    const { svg, itens, nota: rodape } = f(linhas);
    if (!svg) return '';
    return `<svg class="g-svg" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid meet"`
         + ` role="img">${svg}</svg>${legenda(itens)}`
         + (rodape ? `<div class="g-nota">${rodape}</div>` : '');
  }
  /* Sem `export`: `app.js` é script clássico e o site não tem build. O punhado de
   * nomes que o resto precisa sai por aqui, e o resto do arquivo fica fechado. */
  window.Graficos = { desenha, numero, temDados: (l) => validas(l).length > 0 };
}());
