# -*- coding: utf-8 -*-
import re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVGDIR = os.path.join(ROOT, "assets relatórios", "SVG")

def load_svg(name, prefix, extra_attrs="", viewbox=None):
    """Read an SVG, namespace its .cls-N classes and ids, return an inline <svg> string."""
    with open(os.path.join(SVGDIR, name), encoding="utf-8") as f:
        s = f.read()
    s = re.sub(r'<\?xml[^>]*\?>\s*', '', s)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    s = s.replace('cls-', prefix + '-')
    s = re.sub(r'\sid="Camada_1"', '', s)
    s = re.sub(r'\sdata-name="[^"]*"', '', s)
    if viewbox:
        s = re.sub(r'viewBox="[^"]*"', 'viewBox="%s"' % viewbox, s, count=1)
    if extra_attrs:
        s = s.replace('<svg ', '<svg %s ' % extra_attrs, 1)
    return re.sub(r'\n\s*\n', '\n', s).strip()

LOGO_CAPITAL = "LOGO AUVP CAPITAL (ASSESSORIA, CONSULTORIA E ALTA RENDA) BRANCA.svg"
LOGO_PRIVATE = "LOGO PRIVATE BANKING BRANCA.svg"

THEMES = {
    "consultoria": dict(
        nome="Consultoria", nome_full="AUVP Capital · Consultoria", rotulo="Consultoria",
        brand="#023620", ink="#12160F", ink2="#4A5248", line="#E3E6E1", soft="#F5F7F4",
        logo=LOGO_CAPITAL, logo_ratio=1044.44/274.67, marca="AUVP Capital",
        accent="#EFBF4F", ph="rgba(239,191,79,.24)", ph_dk="rgba(239,191,79,.26)",
        warn_bg="rgba(239,191,79,.18)", warn_fg="#8A6A12", warn_bd="rgba(239,191,79,.5)",
        chart=['#023620', '#3E7A52', '#7FAE86', '#B9D3B6', '#EFBF4F', '#8C7A3E'],
        cadencia="trimestral",
    ),
    "alta-renda": dict(
        nome="Alta Renda", nome_full="AUVP Capital · Alta Renda", rotulo="Alta Renda",
        brand="#010F08", ink="#0E1411", ink2="#465049", line="#E1E5E3", soft="#F4F6F5",
        logo=LOGO_CAPITAL, logo_ratio=1044.44/274.67, marca="AUVP Capital",
        accent="#EFBF4F", ph="rgba(239,191,79,.24)", ph_dk="rgba(239,191,79,.26)",
        warn_bg="rgba(239,191,79,.18)", warn_fg="#8A6A12", warn_bd="rgba(239,191,79,.5)",
        chart=['#010F08', '#2E5C3F', '#6A9673', '#A8C4A6', '#EFBF4F', '#8C7A3E'],
        cadencia="trimestral",
    ),
    "private": dict(
        nome="Private Banking", nome_full="AUVP Private Banking", rotulo="",
        brand="#666666", ink="#16181A", ink2="#54595E", line="#E4E6E8", soft="#F4F5F6",
        logo=LOGO_PRIVATE, logo_ratio=1123.56/172.44, marca="AUVP Private Banking",
        # Private Banking não usa amarelo: o acento é neutro, e com ele o realce dos
        # campos preenchíveis e o selo de atenção também saem do amarelo.
        accent="#8C939A", ph="rgba(140,147,154,.26)", ph_dk="rgba(255,255,255,.24)",
        warn_bg="rgba(90,97,104,.14)", warn_fg="#4A5257", warn_bd="rgba(90,97,104,.34)",
        chart=['#3A3E42', '#5C6167', '#82888E', '#A8ADB2', '#CBCFD3', '#E2E5E7'],
        cadencia="mensal",
    ),
    "assessoria": dict(
        nome="Assessoria", nome_full="AUVP Capital · Assessoria", rotulo="Assessoria",
        brand="#005F45", ink="#101613", ink2="#48524D", line="#E2E7E5", soft="#F4F8F6",
        logo=LOGO_CAPITAL, logo_ratio=1044.44/274.67, marca="AUVP Capital",
        accent="#EFBF4F", ph="rgba(239,191,79,.24)", ph_dk="rgba(239,191,79,.26)",
        warn_bg="rgba(239,191,79,.18)", warn_fg="#8A6A12", warn_bd="rgba(239,191,79,.5)",
        chart=['#005F45', '#3E8F6C', '#7CBB99', '#B7DCC6', '#EFBF4F', '#8C7A3E'],
        cadencia="semestral",
    ),
}

CONFID = "DOCUMENTO CONFIDENCIAL · PROIBIDO O COMPARTILHAMENTO"

def _b64(path):
    import base64
    with open(os.path.join(ROOT, path), "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


# Instâncias estáticas da Anek Latin, subconjunto Latin-1 + pontuação, embutidas em
# base64. Estáticas e não variáveis porque o Chromium exporta fonte variável como
# Type3 no PDF — texto deixa de ser selecionável e o arquivo incha várias vezes.
# Embutidas porque os modelos precisam abrir com duplo clique (file://), onde o
# navegador recusa @font-face com URL relativa.
FONT_FACE = "".join(
    """@font-face{font-family:'Anek Latin';font-style:normal;font-weight:%d;font-display:block;
  src:url(data:font/woff2;base64,%s) format('woff2');}
""" % (w, _b64("assets/fonts/AnekLatin-%d.woff2" % w)) for w in (300, 400, 600, 700, 800))

# Grain overlay reproducing the paper texture of the reference cover.
GRAIN = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E"
         "%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.75' numOctaves='4'/%3E"
         "%3C/filter%3E%3Crect width='180' height='180' filter='url(%23n)' opacity='.6'/%3E%3C/svg%3E\")")


def tokens(t):
    return """:root{
  --brand:%(brand)s; --accent:%(accent)s;
  --ph:%(ph)s; --ph-dk:%(ph_dk)s;
  --warn-bg:%(warn_bg)s; --warn-fg:%(warn_fg)s; --warn-bd:%(warn_bd)s;
  %(chart_vars)s
  --ink:%(ink)s; --ink-2:%(ink2)s; --line:%(line)s; --soft:%(soft)s;
  --paper:#FFFFFF; --pos:#1F7A4C; --neg:#B3402F;
}""" % dict(t, chart_vars=" ".join(
        "--c%d:%s;" % (i, c) for i, c in enumerate(t["chart"], start=1)))


def com_rotulo(t, texto, sep=" &middot; "):
    """Junta o rótulo do segmento a um texto, quando há rótulo. Onde a logo já
    diz o nome — o caso do Private Banking — não se repete o nome ao lado dela."""
    return texto + sep + t["rotulo"] if t["rotulo"] else texto


def ph(name, hint=""):
    """Placeholder token. Rendered highlighted so it is obvious what must be filled."""
    title = ' title="%s"' % hint if hint else ""
    return '<span class="ph"%s>{{%s}}</span>' % (title, name)


def head(title, css):
    return """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<style>
%s
</style>
</head>
<body>
""" % (title, css)

FOOT = "</body>\n</html>\n"


BASE = FONT_FACE + """
*,*::before,*::after{box-sizing:border-box}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;background:#8E938F;color:var(--ink);
  font-family:'Anek Latin','Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased}
p{margin:0 0 3mm}
ul{margin:0 0 3mm;padding-left:4.5mm}
li{margin:0 0 1.2mm}
strong{font-weight:700}
.ph{background:var(--ph);border-radius:.6mm;padding:0 .6mm;font-weight:600;overflow-wrap:break-word;text-transform:none;letter-spacing:0;font-size:.94em}
.dark .ph{background:var(--ph-dk);color:#fff}
/* capas e divisórias são monocromáticas: nada de dourado sobre a arte da capa */
.cover .ph,.divider .ph{background:rgba(255,255,255,.18);color:#fff}
.pos{color:var(--pos);font-weight:700}
.neg{color:var(--neg);font-weight:700}
.mut{color:var(--ink-2)}
.rule{height:1px;background:linear-gradient(90deg,rgba(255,255,255,.18),rgba(255,255,255,.95))}
.grain{position:absolute;inset:0;background-image:%(grain)s;opacity:.22;pointer-events:none}
.logo svg{display:block;width:100%%;height:auto}
.logo-ink svg [class^=lg-]{fill:var(--brand)}
/* Todo grafismo entra a 50%% de opacidade, em capa ou como decoração. Fica no
   componente para valer sozinho em qualquer uso novo. */
.graf{position:absolute;pointer-events:none;opacity:.5}
.graf svg{display:block;width:100%%;height:auto}
/* 1px = 0,75 pt em qualquer escala; sem isto o traço afina junto com o grafismo */
.graf svg *{vector-effect:non-scaling-stroke;stroke-width:1px}
""" % dict(grain=GRAIN)


CSS_A4 = BASE + """
@page{size:A4;margin:0}
.page{position:relative;width:210mm;height:297mm;background:var(--paper);overflow:hidden;
  display:flex;flex-direction:column;padding:13mm 15mm 11mm;margin:0 auto 7mm;
  box-shadow:0 3px 22px rgba(0,0,0,.28);font-size:10pt;line-height:1.5}
@media print{body{background:#fff}.page{margin:0;box-shadow:none;break-after:page}.page:last-child{break-after:auto}}

/* ---------- capa ----------
   Medidas tiradas de "assets relatórios/SVG/ref consultoria.svg":
   réguas em y 86,0 e 245,2 mm ocupando a largura útil; grafismo entre elas com
   exatamente a mesma largura das réguas; título 43,89 pt com entrelinha de 48 pt
   (linhas de base em 56,4 e 73,3 mm); assinatura inferior em 32,13 pt.        */
.cover{padding:0;color:#fff;background:linear-gradient(225deg,var(--brand) 0%,#000 100%)}
.cover>*{position:absolute;z-index:3}
.cover .grain{z-index:1}
.cover .graf{z-index:2}
.cover .rule{left:15.3mm;right:15.3mm}
.cover .r1{top:86mm}
.cover .r2{top:245.2mm}
.cv-logo{left:15.3mm;top:18mm}
.cv-t{left:15.3mm;top:43.6mm;right:68mm;margin:0;font-size:43.89pt;line-height:1.093;
  text-transform:uppercase;letter-spacing:-.015em}
.cv-t .lt{font-weight:300;display:block}
.cv-t .bd{font-weight:800;display:block}
.cv-conf{right:15.3mm;top:67.5mm;width:52mm;text-align:right;font-size:8pt;font-weight:600;
  letter-spacing:.07em;text-transform:uppercase;opacity:.8}
.cv-b-t{left:15.3mm;bottom:21.5mm;font-size:32.13pt;line-height:1;text-transform:uppercase;letter-spacing:-.01em}
.cv-id{right:15.3mm;bottom:22.5mm;text-align:right;font-size:9.5pt;line-height:1.75;opacity:.9}

/* ---------- cabeçalho / rodapé ---------- */
.pg-head{flex:0 0 auto;display:flex;align-items:center;justify-content:space-between;gap:8mm;
  padding-bottom:2.6mm;border-bottom:1px solid var(--line)}
.pg-head .sec{font-size:7pt;letter-spacing:.15em;text-transform:uppercase;color:var(--ink-2);font-weight:600}
.pg-head .rt{display:flex;align-items:center;gap:5mm}
.pg-head .dt{font-size:7pt;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-2)}

.pg-foot{flex:0 0 auto;margin-top:auto;padding-top:2.6mm;border-top:1px solid var(--line);
  display:flex;justify-content:space-between;align-items:baseline;
  font-size:6.2pt;letter-spacing:.12em;text-transform:uppercase;color:#9BA29D}
.pg-foot .no{font-size:9pt;font-weight:800;letter-spacing:0;color:var(--brand)}
.pg-body{flex:1 1 auto;min-height:0;padding-top:7mm;display:flex;flex-direction:column}

/* ---------- tipografia ---------- */
.eyebrow{display:block;font-size:6.8pt;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--brand);margin:0 0 2.5mm}
h1.t{font-size:19pt;font-weight:800;text-transform:uppercase;letter-spacing:-.012em;line-height:1.04;margin:0 0 3mm}
.lead{font-size:10pt;color:var(--ink-2);margin:0 0 6mm;max-width:155mm}
h2{font-size:10pt;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin:6mm 0 2.5mm;
  padding-bottom:1.4mm;border-bottom:1px solid var(--line)}
h2:first-child{margin-top:0}
h3{font-size:9pt;font-weight:700;margin:3.5mm 0 1.2mm}
.small{font-size:8pt}
.legal{font-size:6.8pt;line-height:1.5;color:var(--ink-2)}

/* ---------- grelhas ---------- */
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:7mm}
.cols2>*,.cols3>*,.cols2u>*,.cards>*,.kpis>*{min-width:0}
.cols3{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm}
.cols2u{display:grid;grid-template-columns:1.35fr 1fr;gap:7mm}
.gap{height:5mm}

/* ---------- KPIs ---------- */
.kpis{display:grid;grid-template-columns:repeat(var(--n,4),1fr);gap:3mm}
.kpi{min-width:0;border:1px solid var(--line);border-top:1.33px solid var(--brand);background:var(--soft);padding:3.2mm 3.2mm 3mm}
.kpi .k{font-size:6.4pt;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-2);font-weight:600;line-height:1.3}
.kpi .v{font-size:13.5pt;font-weight:800;line-height:1.15;margin-top:2mm;letter-spacing:-.02em;overflow-wrap:anywhere}
.kpi .s{font-size:7pt;color:var(--ink-2);margin-top:.8mm}

/* ---------- tabelas ---------- */
table.tb{width:100%;border-collapse:collapse;font-size:8.2pt}
.tb.sm{font-size:7.4pt}
.tb.sm td{padding:1.6mm 1.8mm}
.tb.xs{font-size:6.6pt}
.tb.xs td{padding:1.3mm 1.4mm}
.tb.xs thead th{padding:1.5mm 1.4mm;font-size:5.8pt;letter-spacing:.04em}
/* colunas declaradas só valem como limite com layout fixo */
.tb.fix{table-layout:fixed}
.tb.sm thead th{padding:1.8mm 1.8mm;font-size:6.2pt;letter-spacing:.06em}
.tb thead th{background:var(--brand);color:#fff;text-align:left;font-weight:600;
  padding:2.2mm 2.4mm;font-size:6.6pt;letter-spacing:.1em;text-transform:uppercase;line-height:1.3}
.tb td{padding:2mm 2.4mm;border-bottom:1px solid var(--line);vertical-align:top;overflow-wrap:anywhere}
.tb tbody tr:nth-child(even) td{background:var(--soft)}
.tb .num,.tb th.num{text-align:right}
.tb tfoot td{font-weight:700;border-top:1.33px solid var(--ink);background:#fff}
.tb caption{caption-side:bottom;text-align:left;font-size:6.8pt;color:var(--ink-2);padding-top:1.8mm}

/* ---------- cards ---------- */
.cards{display:grid;grid-template-columns:repeat(var(--n,3),1fr);gap:4mm}
.card{border-left:1.33px solid var(--accent);padding-left:3.2mm}
.card h4{font-size:9pt;font-weight:700;margin:0 0 1mm}
.card p{font-size:8pt;color:var(--ink-2);margin:0;line-height:1.45}
.note{background:var(--soft);border-left:1.33px solid var(--brand);padding:3.2mm 3.6mm;font-size:8.2pt}
.note p:last-child{margin-bottom:0}

/* ---------- linha do tempo ---------- */
.tl{counter-reset:tl;list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:4.5mm 8mm}
.tl li{position:relative;padding-left:10mm;margin:0}
.tl li::before{counter-increment:tl;content:counter(tl,decimal-leading-zero);position:absolute;left:0;top:-.5mm;
  font-size:12pt;font-weight:800;color:var(--accent);letter-spacing:-.02em}
.tl h4{font-size:9pt;font-weight:700;margin:0 0 .8mm}
.tl p{font-size:8pt;color:var(--ink-2);margin:0;line-height:1.45}

/* ---------- placeholders de gráfico ---------- */
.chart{max-height:74mm;border:1px dashed var(--brand);background:repeating-linear-gradient(135deg,transparent 0 5px,rgba(0,0,0,.022) 5px 10px);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2mm;text-align:center;padding:5mm}
.chart .cl{font-size:6.6pt;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--brand)}
.chart .cd{font-size:7.6pt;color:var(--ink-2);max-width:105mm;line-height:1.45}
.sk-bars{display:flex;align-items:flex-end;gap:2.5mm;height:16mm;width:70%;opacity:.28}
.sk-bars i{flex:1;background:var(--brand);border-radius:.4mm .4mm 0 0}
.sk-donut{width:22mm;height:22mm;border-radius:50%;opacity:.5;
  background:conic-gradient(var(--c1) 0 42%,var(--c2) 42% 63%,var(--c3) 63% 82%,var(--c4) 82% 100%);
  -webkit-mask:radial-gradient(circle,transparent 52%,#000 53%);mask:radial-gradient(circle,transparent 52%,#000 53%)}
.sk-line{width:75%;height:16mm;opacity:.42;
  background:linear-gradient(transparent,transparent) no-repeat;
  border-bottom:.6pt solid var(--ink-2);position:relative}
.sk-line::after{content:'';position:absolute;inset:0;
  clip-path:polygon(0 82%,14% 66%,28% 74%,42% 48%,56% 55%,70% 30%,85% 36%,100% 12%,100% 100%,0 100%);
  background:linear-gradient(180deg,var(--brand),rgba(255,255,255,0) 92%)}

/* ---------- diversos ---------- */
.dl{display:grid;grid-template-columns:auto 1fr;gap:1.4mm 5mm;font-size:8.4pt;align-items:baseline}
.dl dt{color:var(--ink-2);text-transform:uppercase;font-size:6.6pt;letter-spacing:.1em;font-weight:600}
.dl dd{margin:0;font-weight:600}
.pill{display:inline-block;font-size:6.4pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
  padding:.7mm 2mm;border-radius:6mm;background:var(--soft);color:var(--brand);border:1px solid var(--line)}
.pill.ok{background:rgba(31,122,76,.1);color:var(--pos);border-color:rgba(31,122,76,.25)}
.pill.at{background:var(--warn-bg);color:var(--warn-fg);border-color:var(--warn-bd)}
.pill.rk{background:rgba(179,64,47,.09);color:var(--neg);border-color:rgba(179,64,47,.25)}
.toc{list-style:none;margin:0;padding:0;font-size:9pt}
.toc li{display:flex;align-items:baseline;gap:2mm;padding:2.4mm 0;border-bottom:1px solid var(--line)}
.toc .n{font-weight:800;color:var(--accent);font-size:8pt;min-width:7mm}
.toc .d{flex:1 1 auto;border-bottom:1px dotted var(--line);transform:translateY(-1mm)}
.toc .p{font-weight:700;color:var(--brand)}
.sig{margin-top:6mm;display:grid;grid-template-columns:1fr 1fr;gap:8mm;font-size:8pt}
.sig .ln{border-top:1px solid var(--ink);padding-top:1.6mm;color:var(--ink-2)}
.qr{width:34mm;height:34mm;border:1px dashed var(--brand);display:flex;align-items:center;justify-content:center;
  text-align:center;font-size:6.4pt;letter-spacing:.12em;text-transform:uppercase;color:var(--brand);font-weight:700}
"""


CSS_SLIDE = BASE + """
@page{size:338.667mm 190.5mm;margin:0}
.slide{position:relative;width:338.667mm;height:190.5mm;background:var(--paper);overflow:hidden;
  display:flex;flex-direction:column;padding:11mm 14mm 9mm;margin:0 auto 8mm;
  box-shadow:0 4px 26px rgba(0,0,0,.3);font-size:11pt;line-height:1.5}
@media print{body{background:#fff}.slide{margin:0;box-shadow:none;break-after:page}.slide:last-child{break-after:auto}}
.slide.dark{color:#fff;background:linear-gradient(225deg,var(--brand) 0%,#000 100%)}
.slide.dark .pg-head,.slide.dark .pg-foot{border-color:rgba(255,255,255,.22)}
.slide.dark .pg-head .sec,.slide.dark .pg-head .dt{color:rgba(255,255,255,.82)}
.slide.dark .pg-foot{color:rgba(255,255,255,.5)}
.slide.dark .pg-foot .no{color:#fff}
.slide.dark h2{border-color:rgba(255,255,255,.22)}
.slide.dark .lead,.slide.dark .mut,.slide.dark .card p{color:rgba(255,255,255,.8)}
.slide.dark .kpi{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.16);border-top-color:#fff}
.slide.dark .kpi .k,.slide.dark .kpi .s{color:rgba(255,255,255,.72)}
.slide.dark .note{background:rgba(255,255,255,.07);border-left-color:var(--accent)}
.slide .in{position:relative;z-index:3;height:100%;display:flex;flex-direction:column}

.pg-head{flex:0 0 auto;display:flex;align-items:center;justify-content:space-between;gap:10mm;
  padding-bottom:3mm;border-bottom:1px solid var(--line)}
.pg-head .sec{font-size:8pt;letter-spacing:.15em;text-transform:uppercase;color:var(--ink-2);font-weight:600}
.pg-head .rt{display:flex;align-items:center;gap:6mm}
.pg-head .dt{font-size:8pt;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-2)}

.pg-foot{flex:0 0 auto;margin-top:auto;padding-top:3mm;display:flex;justify-content:space-between;align-items:baseline;
  font-size:6.8pt;letter-spacing:.12em;text-transform:uppercase;color:#9BA29D}
.pg-foot .no{font-size:11pt;font-weight:800;letter-spacing:0;color:var(--brand)}
.pg-body{flex:1 1 auto;min-height:0;padding-top:8mm;display:flex;flex-direction:column}

.eyebrow{display:block;font-size:7.5pt;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--brand);margin:0 0 3mm}
.slide.dark .eyebrow{color:#fff}
h1.t{font-size:26pt;font-weight:800;text-transform:uppercase;letter-spacing:-.015em;line-height:1.03;margin:0 0 4mm}
.lead{font-size:11pt;color:var(--ink-2);margin:0 0 6mm;max-width:210mm}
h2{font-size:11pt;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin:6mm 0 3mm;
  padding-bottom:1.6mm;border-bottom:1px solid var(--line)}
h2:first-child{margin-top:0}
h3{font-size:10.5pt;font-weight:700;margin:4mm 0 1.5mm}
.small{font-size:9pt}
.legal{font-size:7.4pt;line-height:1.5;color:var(--ink-2)}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:10mm}
/* usa a sobra vertical do slide em vez de deixá-la toda no rodapé */
.center{flex:1 1 auto;display:flex;flex-direction:column;justify-content:center;gap:9mm;min-height:0}
.cols2>*,.cols3>*,.cols2u>*,.cards>*,.kpis>*{min-width:0}
.cols3{display:grid;grid-template-columns:repeat(3,1fr);gap:8mm}
.cols2u{display:grid;grid-template-columns:1.3fr 1fr;gap:10mm}

.kpis{display:grid;grid-template-columns:repeat(var(--n,4),1fr);gap:5mm}
.kpi{min-width:0;border:1px solid var(--line);border-top:1.33px solid var(--brand);background:var(--soft);padding:5mm}
.kpi .k{font-size:7.4pt;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-2);font-weight:600}
.kpi .v{font-size:20pt;font-weight:800;line-height:1.1;margin-top:3mm;letter-spacing:-.025em;overflow-wrap:anywhere}
.kpi .s{font-size:8.4pt;color:var(--ink-2);margin-top:1.5mm}

table.tb{width:100%;border-collapse:collapse;font-size:9.5pt}
.tb thead th{background:var(--brand);color:#fff;text-align:left;font-weight:600;
  padding:3mm 3.2mm;font-size:7.6pt;letter-spacing:.1em;text-transform:uppercase}
.tb td{padding:2.8mm 3.2mm;border-bottom:1px solid var(--line);vertical-align:top;overflow-wrap:anywhere}
.tb tbody tr:nth-child(even) td{background:var(--soft)}
.slide.dark .tb td{border-color:rgba(255,255,255,.16)}
.slide.dark .tb tbody tr:nth-child(even) td{background:rgba(255,255,255,.05)}
.tb .num,.tb th.num{text-align:right}
.tb tfoot td{font-weight:700;border-top:1.33px solid currentColor}

.cards{display:grid;grid-template-columns:repeat(var(--n,3),1fr);gap:6mm}
.card{border-left:1.33px solid var(--accent);padding-left:4.5mm}
.card h4{font-size:11pt;font-weight:700;margin:0 0 1.5mm}
.card p{font-size:9pt;color:var(--ink-2);margin:0;line-height:1.45}
.note{background:var(--soft);border-left:1.33px solid var(--brand);padding:4.5mm 5mm;font-size:9.5pt}
.note p:last-child{margin-bottom:0}
.tl{counter-reset:tl;list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:6mm 12mm}
.tl li{position:relative;padding-left:13mm;margin:0}
.tl li::before{counter-increment:tl;content:counter(tl,decimal-leading-zero);position:absolute;left:0;top:-1mm;
  font-size:16pt;font-weight:800;color:var(--accent);letter-spacing:-.02em}
.tl h4{font-size:10.5pt;font-weight:700;margin:0 0 1mm}
.tl p{font-size:9pt;color:var(--ink-2);margin:0;line-height:1.4}
.chart{border:1px dashed currentColor;background:repeating-linear-gradient(135deg,transparent 0 6px,rgba(0,0,0,.02) 6px 12px);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3mm;text-align:center;padding:7mm}
.slide.dark .chart{background:repeating-linear-gradient(135deg,transparent 0 6px,rgba(255,255,255,.045) 6px 12px)}
.chart .cl{font-size:7.6pt;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--brand)}
.slide.dark .chart .cl{color:#fff}
.chart .cd{font-size:9pt;color:var(--ink-2);max-width:150mm;line-height:1.45}
.slide.dark .chart .cd{color:rgba(255,255,255,.75)}
.sk-bars{display:flex;align-items:flex-end;gap:4mm;height:26mm;width:60%;opacity:.3}
.sk-bars i{flex:1;background:currentColor;border-radius:.6mm .6mm 0 0}
.sk-donut{width:32mm;height:32mm;border-radius:50%;opacity:.35;
  background:conic-gradient(var(--c1) 0 42%,var(--c2) 42% 63%,var(--c3) 63% 82%,var(--c4) 82% 100%);
  -webkit-mask:radial-gradient(circle,transparent 52%,#000 53%);mask:radial-gradient(circle,transparent 52%,#000 53%)}
.pill{display:inline-block;font-size:7.4pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
  padding:1mm 3mm;border-radius:8mm;background:var(--soft);color:var(--brand);border:1px solid var(--line)}
.slide.dark .pill{background:rgba(255,255,255,.1);color:#fff;border-color:rgba(255,255,255,.24)}
.dl{display:grid;grid-template-columns:auto 1fr;gap:2mm 7mm;font-size:9.5pt;align-items:baseline}
.dl dt{color:var(--ink-2);text-transform:uppercase;font-size:7.4pt;letter-spacing:.1em;font-weight:600}
.slide.dark .dl dt{color:rgba(255,255,255,.7)}
.dl dd{margin:0;font-weight:600}
.qr{width:52mm;height:52mm;border:1px dashed currentColor;display:flex;align-items:center;justify-content:center;
  text-align:center;font-size:7.6pt;letter-spacing:.12em;text-transform:uppercase;font-weight:700;opacity:.85}
.imgbox{border:1px dashed currentColor;display:flex;flex-direction:column;align-items:center;justify-content:center;
  gap:2mm;text-align:center;padding:8mm;
  background:repeating-linear-gradient(135deg,transparent 0 7px,rgba(0,0,0,.022) 7px 14px)}
.slide.dark .imgbox{background:repeating-linear-gradient(135deg,transparent 0 7px,rgba(255,255,255,.05) 7px 14px)}
.imgbox .cl{font-size:7.6pt;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--brand)}
.slide.dark .imgbox .cl{color:#fff}
.imgbox .cd{font-size:9pt;max-width:90mm;line-height:1.45;color:var(--ink-2)}
.slide.dark .imgbox .cd{color:rgba(255,255,255,.75)}

/* capa e divisórias ----------
   Medidas tiradas de "MODELO SLIDES AUVP CAPITAL.pdf", página 1, reescaladas de
   1440x810 pt para 338,667x190,5 mm: faixa branca de 0 a 26,3 mm, régua curta em
   x 24,6..74,9 e y 68,4 mm, título 44,6 pt com base em 106,7 mm, subtítulo
   25,3 pt com base em 120,2 mm. Arcos sangrando no canto inferior direito.   */
.slide.cover,.slide.divider{padding:0}
.cv-band{position:absolute;left:0;right:0;top:0;height:26.3mm;background:#fff;z-index:4;
  display:flex;align-items:center;justify-content:space-between;padding:0 8.3mm}
.cv-band .logo{margin-left:auto}
.cv-band .nm{font-size:13.3pt;font-weight:600;color:var(--ink);letter-spacing:.01em}
.cv-band .logo svg [class^=lg-]{fill:var(--brand)}
.cv-block{position:absolute;left:24.6mm;right:24.6mm;top:68mm;z-index:4}
.cv-block .rule{width:50.3mm;margin-bottom:26mm}
.cv-t{margin:0;font-size:44.6pt;line-height:1;font-weight:800;text-transform:uppercase;letter-spacing:-.02em}
.cv-t .lt{font-weight:300}
.cv-sub{margin-top:3mm;font-size:25.3pt;line-height:1.1;text-transform:uppercase;opacity:.92}
.cv-foot{position:absolute;left:24.6mm;right:24.6mm;bottom:11mm;z-index:4;
  display:flex;align-items:flex-end;gap:12mm}
.cv-foot .cf{font-size:7.6pt;letter-spacing:.14em;text-transform:uppercase;opacity:.55}
.cv-foot .id{margin-left:auto;text-align:right;font-size:9.5pt;line-height:1.7;opacity:.9}
.slide.cover .graf{z-index:2}
.slide.divider .graf{z-index:2}
.divider .in{padding:12mm 16mm;display:flex;flex-direction:column;justify-content:center}
.dv-n{font-size:60pt;font-weight:800;line-height:1;color:#fff;opacity:.5;letter-spacing:-.03em}
.dv-t{font-size:32pt;font-weight:800;text-transform:uppercase;line-height:1.05;margin-top:3mm;letter-spacing:-.015em}
.dv-sub{font-size:12pt;letter-spacing:.02em;margin-top:3mm;opacity:.9;text-transform:uppercase}
"""

CSS_SLIDE += """
/* ---------- tela de planos ---------- */
.plans{display:grid;grid-template-columns:repeat(var(--n,3),1fr);gap:6mm;flex:1 1 auto;min-height:0}
.plans>*{min-width:0}
.plan{border:1px solid var(--line);border-top:1.33px solid var(--line);display:flex;flex-direction:column;padding:5mm}
.plan.hl{border-color:var(--line);border-top-color:var(--accent);background:var(--soft)}
.plan .nm{font-size:11.5pt;font-weight:800;text-transform:uppercase;line-height:1.12;letter-spacing:-.01em}
.plan .tag{font-size:7.4pt;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-2)}
.plan .pr{margin:3.5mm 0;padding:2.6mm 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.plan .pr b{display:block;font-size:14pt;font-weight:800;color:var(--brand);letter-spacing:-.02em}
.plan .pr span{font-size:8.4pt;color:var(--ink-2)}
.plan ul{list-style:none;padding:0;margin:0;font-size:8.6pt;line-height:1.4}
.plan li{position:relative;padding-left:4.5mm;margin-bottom:1.8mm}
.plan li::before{content:"";position:absolute;left:0;top:2mm;width:2.4mm;height:1.33px;background:var(--accent)}
.plan .ft{margin-top:auto;padding-top:4mm;font-size:8.2pt;color:var(--ink-2)}
.steps{display:grid;grid-template-columns:repeat(var(--n,4),1fr);gap:8mm;counter-reset:st;list-style:none;padding:0;margin:0}
.steps>li{min-width:0;position:relative;padding-top:11mm}
.steps>li::before{counter-increment:st;content:counter(st,decimal-leading-zero);position:absolute;left:0;top:0;
  font-size:18pt;font-weight:800;color:var(--accent);letter-spacing:-.02em}
.steps>li::after{content:"";position:absolute;left:0;top:9mm;width:100%;height:1px;background:var(--line)}
.steps h4{font-size:10.5pt;font-weight:700;margin:0 0 1.5mm}
.steps p{font-size:9pt;color:var(--ink-2);margin:0;line-height:1.45}
.slide.dark .steps>li::after{background:rgba(255,255,255,.25)}
.big{font-size:34pt;font-weight:800;line-height:1;letter-spacing:-.03em;color:var(--brand)}
.slide.dark .big{color:#fff}
.stat{display:flex;flex-direction:column;gap:1.5mm}
.stat .lb{font-size:8.6pt;color:var(--ink-2);line-height:1.35}
.slide.dark .stat .lb{color:rgba(255,255,255,.78)}
"""

CSS_A4 += """
.steps{display:grid;grid-template-columns:repeat(var(--n,4),1fr);gap:5mm;counter-reset:st;list-style:none;padding:0;margin:0}
.steps>li{min-width:0;position:relative;padding-top:8mm}
.steps>li::before{counter-increment:st;content:counter(st,decimal-leading-zero);position:absolute;left:0;top:0;
  font-size:13pt;font-weight:800;color:var(--accent);letter-spacing:-.02em}
.steps>li::after{content:"";position:absolute;left:0;top:6.5mm;width:100%;height:1px;background:var(--line)}
.steps h4{font-size:9pt;font-weight:700;margin:0 0 1mm}
.steps p{font-size:8pt;color:var(--ink-2);margin:0;line-height:1.4}
.big{font-size:22pt;font-weight:800;line-height:1;letter-spacing:-.03em;color:var(--brand)}
.stat{display:flex;flex-direction:column;gap:1mm}
.stat .lb{font-size:7.6pt;color:var(--ink-2);line-height:1.35}
"""

CSS_A4 += """
/* ---------- processo: nós numerados sobre um trilho contínuo ---------- */
.flow{list-style:none;margin:0;padding:0;counter-reset:fl;
  display:grid;grid-template-columns:repeat(var(--n,4),1fr);column-gap:5mm}
.flow>li{position:relative;min-width:0;padding-top:10mm}
.flow>li::after{content:"";position:absolute;left:0;right:calc(-1 * 5mm);top:4mm;height:1px;background:var(--line)}
.flow>li:last-child::after{right:0}
.flow .node{position:absolute;left:0;top:0;z-index:2;width:8mm;height:8mm;border-radius:50%;
  border:1px solid var(--brand);background:var(--paper);color:var(--brand);
  display:flex;align-items:center;justify-content:center;font-weight:800;font-size:8pt;letter-spacing:-.01em}
.flow .node::before{counter-increment:fl;content:counter(fl,decimal-leading-zero)}
.flow .tag{display:block;font-size:5.8pt;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
  color:var(--ink-2);margin-bottom:1mm}
.flow h4{font-size:9pt;font-weight:700;margin:0 0 1mm}
.flow p{font-size:8pt;color:var(--ink-2);margin:0;line-height:1.45}

/* ---------- legenda de série, com a paleta do segmento ---------- */
.legend{list-style:none;display:flex;flex-wrap:wrap;justify-content:center;gap:1.5mm 4mm;
  margin:3mm 0 0;padding:0;font-size:6.6pt;color:var(--ink-2)}
.legend li{display:flex;align-items:center;gap:1.6mm}
.legend i{width:4mm;height:1.33px;flex:0 0 auto}

/* ---------- ano em dois semestres ---------- */
.year{list-style:none;margin:0;padding:0;counter-reset:yr;display:grid;
  grid-template-columns:repeat(6,1fr);gap:6mm 4mm}
.year>li{position:relative;min-width:0;padding-top:8mm}
.year>li::after{content:"";position:absolute;left:0;right:-4mm;top:3.2mm;height:1px;background:var(--line)}
.year>li:nth-child(6)::after,.year>li:last-child::after{right:0}
.year .mo{position:absolute;left:0;top:0;z-index:2;width:6.4mm;height:6.4mm;border-radius:50%;
  border:1px solid var(--line);background:var(--paper);color:var(--ink-2);
  display:flex;align-items:center;justify-content:center;font-size:6pt;font-weight:700}
.year>li.on .mo{border-color:var(--brand);color:var(--brand)}
.year .nm{display:block;font-size:7.4pt;font-weight:700;margin-bottom:.6mm}
.year .ev{display:block;font-size:6.8pt;color:var(--ink-2);line-height:1.35}
"""

CSS_SLIDE += """
/* ---------- processo: nós numerados sobre um trilho contínuo ---------- */
.flow{list-style:none;margin:0;padding:0;counter-reset:fl;
  display:grid;grid-template-columns:repeat(var(--n,4),1fr);column-gap:8mm}
.flow>li{position:relative;min-width:0;padding-top:15mm}
.flow>li::after{content:"";position:absolute;left:0;right:calc(-1 * 8mm);top:6mm;height:1px;background:var(--line)}
.flow>li:last-child::after{right:0}
.flow .node{position:absolute;left:0;top:0;z-index:2;width:12mm;height:12mm;border-radius:50%;
  border:1px solid var(--brand);background:var(--paper);color:var(--brand);
  display:flex;align-items:center;justify-content:center;font-weight:800;font-size:11pt;letter-spacing:-.01em}
.flow .node::before{counter-increment:fl;content:counter(fl,decimal-leading-zero)}
.flow .tag{display:block;font-size:7pt;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
  color:var(--ink-2);margin-bottom:1mm}
.flow h4{font-size:10.5pt;font-weight:700;margin:0 0 1mm}
.flow p{font-size:9pt;color:var(--ink-2);margin:0;line-height:1.45}

/* ---------- legenda de série, com a paleta do segmento ---------- */
.legend{list-style:none;display:flex;flex-wrap:wrap;justify-content:center;gap:1.5mm 6mm;
  margin:4mm 0 0;padding:0;font-size:8pt;color:var(--ink-2)}
.legend li{display:flex;align-items:center;gap:1.6mm}
.legend i{width:6mm;height:1.33px;flex:0 0 auto}

.slide.dark .flow>li::after{background:rgba(255,255,255,.25)}
.slide.dark .flow .node{background:transparent;border-color:rgba(255,255,255,.55);color:#fff}
.slide.dark .flow .tag,.slide.dark .flow p,.slide.dark .legend{color:rgba(255,255,255,.78)}

/* ---------- número de destaque com números de apoio ---------- */
.hero{display:grid;grid-template-columns:auto 1fr;align-items:end;gap:0 8mm;
  padding-bottom:6mm;border-bottom:1px solid var(--line)}
.hero .n{font-size:64pt;font-weight:800;line-height:.9;letter-spacing:-.04em;color:var(--brand)}
.slide.dark .hero .n{color:#fff}
.hero .l{font-size:11pt;color:var(--ink-2);line-height:1.4;padding-bottom:2mm}
.slide.dark .hero .l{color:rgba(255,255,255,.8)}
.stats{display:grid;grid-template-columns:repeat(var(--n,5),1fr);margin-top:7mm}
.stats>div{min-width:0;padding:0 5mm;border-left:1px solid var(--line)}
.stats>div:first-child{padding-left:0;border-left:0}
.slide.dark .stats>div{border-color:rgba(255,255,255,.22)}
.stats .n{font-size:22pt;font-weight:800;line-height:1;letter-spacing:-.03em;color:var(--brand)}
.slide.dark .stats .n{color:#fff}
.stats .l{font-size:8.4pt;color:var(--ink-2);line-height:1.35;margin-top:2mm}
.slide.dark .stats .l{color:rgba(255,255,255,.75)}
"""

CSS_A4 += """
/* ---------- lista com marcador em fio, e retrato ---------- */
.lista{list-style:none;margin:0 0 3mm;padding:0;font-size:8.4pt;line-height:1.45}
.lista li{position:relative;padding-left:4.6mm;margin-bottom:1.6mm}
.lista li::before{content:"";position:absolute;left:0;top:2mm;width:2.6mm;height:1.33px;background:var(--accent)}
.lista.mut li{color:var(--ink-2)}
.foto{border:1px dashed var(--brand);display:flex;flex-direction:column;align-items:center;
  justify-content:center;gap:1.5mm;text-align:center;padding:4mm;
  background:repeating-linear-gradient(135deg,transparent 0 5px,rgba(0,0,0,.022) 5px 10px)}
.foto .cl{font-size:6.6pt;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--brand)}
.foto .cd{font-size:7.2pt;color:var(--ink-2);line-height:1.4}
.chips{display:flex;flex-wrap:wrap;gap:1.6mm;margin-bottom:1mm}
.side h3{font-size:6.8pt;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
  color:var(--ink-2);margin:5mm 0 1.8mm;padding-bottom:1.2mm;border-bottom:1px solid var(--line)}
.side h3:first-child{margin-top:0}
.side .lista{font-size:8pt;margin-bottom:0}
.side .dl{font-size:8pt}
"""

CSS_A4 += """
/* ---------- densidade para páginas de texto corrido longo ----------
   A apresentação do consultor tem duas páginas fechadas, sem chance de
   transbordar para uma terceira: o conteúdo tem de caber. Esta classe aperta a
   escala sem mexer nos outros documentos. */
.densa h2{margin:3.8mm 0 1.8mm;font-size:9pt}
.densa h2:first-child{margin-top:0}
.densa .lead{font-size:9.2pt;margin-bottom:3.8mm}
.densa p{margin-bottom:2.2mm}
.densa .lista{font-size:7.7pt;line-height:1.36;margin-bottom:0}
.densa .lista li{margin-bottom:1.2mm;padding-left:4mm}
.densa .lista li::before{top:1.7mm;width:2.2mm}
.densa p.small{font-size:7.8pt;line-height:1.45}
.densa .cols2{gap:7mm}
.densa .dl{font-size:8pt;gap:1.2mm 5mm}
.densa .legal{font-size:6.4pt}
/* princípios em duas colunas: título embutido no parágrafo ocupa bem menos
   altura que cinco cards estreitos */
.principios{display:grid;grid-template-columns:1fr 1fr;gap:1.3mm 7mm}
.principios p{font-size:7.7pt;line-height:1.4;margin:0}
.principios strong{color:var(--brand)}
"""
