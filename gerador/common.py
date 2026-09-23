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
        chart=['#0F8A51', '#8C47D1', '#F6A823', '#0DA2E7', '#E23670', '#E64D19', '#669E2E', '#3E5074'],
        cadencia="trimestral",
    ),
    "alta-renda": dict(
        nome="Alta Renda", nome_full="AUVP Capital · Alta Renda", rotulo="Alta Renda",
        brand="#010F08", ink="#0E1411", ink2="#465049", line="#E1E5E3", soft="#F4F6F5",
        logo=LOGO_CAPITAL, logo_ratio=1044.44/274.67, marca="AUVP Capital",
        accent="#EFBF4F", ph="rgba(239,191,79,.24)", ph_dk="rgba(239,191,79,.26)",
        warn_bg="rgba(239,191,79,.18)", warn_fg="#8A6A12", warn_bd="rgba(239,191,79,.5)",
        chart=['#0F8A51', '#8C47D1', '#F6A823', '#0DA2E7', '#E23670', '#E64D19', '#669E2E', '#3E5074'],
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
        chart=['#3E5074', '#0F8A51', '#0DA2E7', '#F6A823', '#8C47D1', '#E23670', '#E64D19', '#669E2E'],
        cadencia="mensal",
    ),
    "assessoria": dict(
        nome="Assessoria", nome_full="AUVP Capital · Assessoria", rotulo="Assessoria",
        brand="#005F45", ink="#101613", ink2="#48524D", line="#E2E7E5", soft="#F4F8F6",
        logo=LOGO_CAPITAL, logo_ratio=1044.44/274.67, marca="AUVP Capital",
        accent="#EFBF4F", ph="rgba(239,191,79,.24)", ph_dk="rgba(239,191,79,.26)",
        warn_bg="rgba(239,191,79,.18)", warn_fg="#8A6A12", warn_bd="rgba(239,191,79,.5)",
        chart=['#0F8A51', '#8C47D1', '#F6A823', '#0DA2E7', '#E23670', '#E64D19', '#669E2E', '#3E5074'],
        cadencia="semestral",
    ),
}

CONFID = "DOCUMENTO CONFIDENCIAL. PROIBIDO O COMPARTILHAMENTO"

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
  --g-pos:#047B4A; --g-neg:#DC2828; --g-neu:#F1EDE4;
  --g-seq-1:#E2F3E9; --g-seq-2:#ABE3C7; --g-seq-3:#5CD69D; --g-seq-4:#19B370; --g-seq-5:#023620;
}""" % dict(t, chart_vars=" ".join(
        "--c%d:%s;" % (i, c) for i, c in enumerate(t["chart"], start=1)))


def com_rotulo(t, texto, sep=", "):
    """Junta o rótulo do segmento a um texto, quando há rótulo. Onde a logo já
    diz o nome — o caso do Private Banking — não se repete o nome ao lado dela."""
    return texto + sep + t["rotulo"] if t["rotulo"] else texto


# Campos que são endereço de alguma coisa, e o que se faz com o valor deles. A
# tabela mora aqui, e não em cada documento, porque o mesmo `email_contato`
# aparece em vinte e quatro modelos e não pode sair clicável num e morto noutro.
#
# O modelo em branco não vira link: `{{email_contato}}` não é endereço de nada.
# O que ele leva é a marca `data-link`, e quem monta o link é a ferramenta, com
# o valor na mão — é lá que se sabe se o telefone veio com o código do país.
LINKS = {
    "email_contato": "mailto",
    "email_consultor": "mailto",
    "canal_email_endereco": "mailto",
    "whatsapp_contato": "whatsapp",
    "whatsapp_consultor": "whatsapp",
    "canal_whats_endereco": "whatsapp",
    "telefone_contato": "tel",
    "canal_tel_endereco": "tel",
    "instagram_consultor": "instagram",
    "site": "url",
    "link_agendamento": "url",
    "canal_portal_endereco": "url",
    # Estes chegam como telefone numa casa e como e-mail ou portal noutra.
    # Quem decide é o valor, na hora de preencher.
    "canal_ouvidoria": "auto",
    "time_principal_contato": "auto",
    "time_backup_contato": "auto",
    "time_mesa_contato": "auto",
    "time_ops_contato": "auto",
}


def ph(name, hint="", padrao=None):
    """Um campo do documento.

    Sem `padrao`, sai como `{{nome}}` destacado: é o pedido de preenchimento, e
    ele tem de saltar aos olhos no modelo.

    Com `padrao`, sai já preenchido com o texto padrão, e continua sendo campo —
    a ferramenta o oferece com esse texto dentro, para o consultor corrigir o
    que for do caso e deixar o resto como está. É o que serve para o conteúdo
    que é quase sempre o mesmo mas envelhece: as bandas da estrutura meta, o
    racional de cada camada da renda fixa. Travar obrigava a mexer no gerador a
    cada revisão; deixar em branco obrigava a redigitar tudo toda vez.

    O nome vai no `data-campo` em vez de ficar só dentro das chaves, porque com
    padrão não há chaves — o que está escrito ali é o texto, e o nome do campo
    precisa de um lugar próprio.
    """
    title = ' title="%s"' % hint if hint else ""
    link = ' data-link="%s"' % LINKS[name] if name in LINKS else ""
    if padrao is None:
        return '<span class="ph" data-campo="%s"%s%s>{{%s}}</span>' % (name, title, link, name)
    return '<span class="ph pronto" data-campo="%s"%s%s>%s</span>' % (name, title, link, padrao)


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
/* Link no papel é link: o Chromium leva a âncora para o PDF. O que não pode
   mudar é a aparência — azul e sublinhado quebrariam a página. */
a{color:inherit;text-decoration:none}
p{margin:0 0 3mm}
ul{margin:0 0 3mm;padding-left:4mm}
li{margin:0 0 1mm}
strong{font-weight:700}
.ph{background:var(--ph);border-radius:.6mm;padding:0 1mm;font-weight:600;overflow-wrap:break-word;text-transform:none;letter-spacing:0;font-size:.94em}
/* O campo que já vem preenchido não é lacuna: lê-se como o texto que é, e o
   realce só serviria para o consultor achar que falta algo ali. Continua sendo
   campo — a ferramenta o oferece para edição —, mas isso é assunto da
   ferramenta, não do papel. */
.ph.pronto{background:none;padding:0;font-weight:inherit;font-size:inherit}
.dark .ph{background:var(--ph-dk);color:#fff}
/* capas e divisórias são monocromáticas: nada de dourado sobre a arte da capa */
.cover .ph,.divider .ph{background:rgba(255,255,255,.18);color:#fff}
.mut{color:var(--ink-2)}
.rule{height:1px;background:linear-gradient(90deg,rgba(255,255,255,.18),rgba(255,255,255,.95))}
.grain{position:absolute;inset:0;background-image:%(grain)s;opacity:.22;pointer-events:none}
.logo svg{display:block;width:100%%;height:auto}
/* sobre fundo branco a marca é sempre preta */
.logo-ink svg [class^=lg-]{fill:#000}
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
  display:flex;flex-direction:column;padding:15mm 15.3mm 13mm;margin:0 auto 6mm;
  box-shadow:0 3px 22px rgba(0,0,0,.28);font-size:10pt;line-height:1.55}
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
  padding-bottom:3mm;border-bottom:1px solid var(--line)}
.pg-head .sec{font-size:7pt;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2);font-weight:600}
.pg-head .rt{display:flex;align-items:center;gap:5mm}
.pg-head .dt{font-size:7pt;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2)}

.pg-foot{flex:0 0 auto;margin-top:auto;padding-top:3mm;border-top:1px solid var(--line);
  display:flex;justify-content:space-between;align-items:baseline;
  font-size:6.2pt;letter-spacing:.08em;text-transform:uppercase;color:#9BA29D}
.pg-foot .no{font-size:9pt;font-weight:800;letter-spacing:0;color:var(--brand)}
.pg-body{flex:1 1 auto;min-height:0;padding-top:8mm;display:flex;flex-direction:column}

/* ---------- tipografia ---------- */
.eyebrow{display:block;font-size:6.8pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--brand);margin:0 0 2mm}
h1.t{font-size:19pt;font-weight:800;text-transform:uppercase;letter-spacing:-.012em;line-height:1.04;margin:0 0 3mm}
.lead{font-size:10pt;color:var(--ink-2);margin:0 0 8mm;max-width:155mm}
h2{font-size:10pt;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin:8mm 0 4mm;
  padding-bottom:2mm;border-bottom:1px solid var(--line)}
h2:first-child{margin-top:0}
h3{font-size:9pt;font-weight:700;margin:5mm 0 2mm}
.small{font-size:8pt}
.legal{font-size:7.2pt;line-height:1.5;color:var(--ink-2)}

/* ---------- grelhas ---------- */
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:10mm}
.cols2>*,.cols3>*,.cols2u>*,.cards>*,.kpis>*{min-width:0}
.cols3{display:grid;grid-template-columns:repeat(3,1fr);gap:8mm}
.cols2u{display:grid;grid-template-columns:1.5fr 1fr;gap:10mm}
.gap{height:5mm}

/* ---------- KPIs ---------- */
.kpis{display:grid;grid-template-columns:repeat(var(--n,4),1fr);gap:4mm}
.kpi{min-width:0;border:1px solid var(--line);border-top:1.33px solid var(--brand);background:var(--soft);padding:4mm}
/* Um número manda: o primeiro KPI ocupa duas colunas com o valor maior. A
   segunda fileira, de apoio, sai sem moldura — só o fio à esquerda. */
.kpi.grande{grid-column:span 2}
.kpi.grande .v{font-size:22pt;margin-top:1.5mm}
.kpis.leve .kpi{border:0;border-left:1px solid var(--line);background:none;padding:.5mm 0 .5mm 3mm}
.kpi .k{font-size:6.4pt;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2);font-weight:600;line-height:1.3}
.kpi .v{font-size:13.5pt;font-weight:800;line-height:1.15;margin-top:2mm;letter-spacing:-.02em;overflow-wrap:anywhere}
.kpi .s{font-size:7pt;color:var(--ink-2);margin-top:1mm}

/* ---------- tabelas ---------- */
table.tb{width:100%;border-collapse:collapse;font-size:8.2pt}
.tb.sm{font-size:7.4pt}
.tb.sm td{padding:2mm 2.5mm}
.tb.xs{font-size:6.6pt}
.tb.xs td{padding:1.5mm 2mm}
.tb.xs thead th{padding:1.5mm 1.5mm;font-size:5.8pt;letter-spacing:.04em}
/* colunas declaradas só valem como limite com layout fixo */
.tb.fix{table-layout:fixed}
.tb.sm thead th{padding:2mm 2mm;font-size:6.2pt;letter-spacing:.06em}
.tb thead th{background:var(--brand);color:#fff;text-align:left;font-weight:600;
  padding:2mm 2mm;font-size:6.6pt;letter-spacing:.08em;text-transform:uppercase;line-height:1.3}
.tb td{padding:3mm;border-bottom:1px solid var(--line);vertical-align:top;overflow-wrap:anywhere}
.tb tbody tr:nth-child(even) td{background:var(--soft)}

/* ---------- cronograma de reuniões ----------
   A sequência do primeiro ciclo, com as fases numa trilha à esquerda. A trilha
   é uma célula só por fase, com `rowspan`, e o rótulo deitado: são três
   palavras longas — Estruturação, Acompanhamento, Fechamento — e em pé elas
   roubariam uma coluna inteira da tabela para dizer o que é só a divisão.

   As datas são as únicas células que mudam de cliente para cliente, e por isso
   vêm dentro de uma cápsula: quem preenche vê onde escrever, e quem lê vê o que
   é combinado e o que é processo da casa. */
.crono{width:100%;border-collapse:collapse;font-size:8.4pt}
.crono thead th{background:var(--brand);color:#fff;text-align:left;font-weight:600;
  font-size:7pt;letter-spacing:.08em;text-transform:uppercase;padding:2.6mm 4mm}
.crono td{padding:2mm 4mm;border-bottom:1px solid var(--line);vertical-align:middle}
.crono tbody tr:nth-child(even) td{background:var(--soft)}
.crono .qual{font-weight:700;color:var(--brand);white-space:nowrap}
.crono .pauta{font-weight:600}
.crono .prazo{color:var(--ink-2);white-space:nowrap}
/* o objetivo estratégico é a coluna larga do plano do private: leva a frase
   inteira, e as outras três só o que precisam */
.crono .obj{color:var(--ink-2);width:100%}
.crono .quando{text-align:right;white-space:nowrap}
.crono .quando span{display:inline-block;padding:1.2mm 3.5mm;border:1px solid var(--line);
  border-radius:9mm;background:var(--paper);font-weight:700;font-size:8.2pt}
.crono td.fase{background:var(--brand);padding:0;width:9mm;border-bottom:1px solid var(--paper)}
.crono td.fase span{display:block;writing-mode:vertical-rl;transform:rotate(180deg);
  margin:0 auto;padding:4mm 0;color:var(--accent);font-size:6.8pt;font-weight:700;
  letter-spacing:.08em;text-transform:uppercase;white-space:nowrap}
.tb .num,.tb th.num{text-align:right}
.tb tfoot td{font-weight:700;border-top:1.33px solid var(--ink);background:#fff}
.tb caption{caption-side:bottom;text-align:left;font-size:6.8pt;color:var(--ink-2);padding-top:2mm}

/* ---------- cards ---------- */
.cards{display:grid;grid-template-columns:repeat(var(--n,3),1fr);gap:6mm}
.card{border-left:1.33px solid var(--accent);padding-left:3mm}
.card h4{font-size:9pt;font-weight:700;margin:0 0 1mm}
.card p{font-size:8pt;color:var(--ink-2);margin:0;line-height:1.45}
.note{background:var(--soft);border-left:1.33px solid var(--brand);padding:4mm 5mm;font-size:8.2pt}
.note p:last-child{margin-bottom:0}

/* ---------- linha do tempo ---------- */
.tl{counter-reset:tl;list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:4mm 8mm}
.tl li{position:relative;padding-left:10mm;margin:0}
.tl li::before{counter-increment:tl;content:counter(tl,decimal-leading-zero);position:absolute;left:0;top:-.5mm;
  font-size:12pt;font-weight:800;color:var(--accent);letter-spacing:-.02em}
.tl h4{font-size:9pt;font-weight:700;margin:0 0 1mm}
.tl p{font-size:8pt;color:var(--ink-2);margin:0;line-height:1.45}

/* ---------- placeholders de gráfico ---------- */
.chart{max-height:100mm;border:1px dashed var(--brand);background:repeating-linear-gradient(135deg,transparent 0 5px,rgba(0,0,0,.022) 5px 10px);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2mm;text-align:center;padding:5mm}
.chart .cl{font-size:6.6pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--brand)}
.chart .cd{font-size:7.6pt;color:var(--ink-2);max-width:105mm;line-height:1.45}
/* Com o gráfico desenhado dentro, a moldura deixa de ser um pedido de
   preenchimento: some o tracejado e a hachura, e fica só o desenho. */
.chart.feito{border:0;background:none;padding:0;gap:1.5mm}
.sk-bars{display:flex;align-items:flex-end;gap:2mm;height:16mm;width:70%;opacity:.28}
.sk-bars i{flex:1;background:var(--brand);border-radius:.4mm .4mm 0 0}
.sk-donut{width:22mm;height:22mm;border-radius:50%;opacity:.5;
  background:conic-gradient(var(--c1) 0 42%,var(--c2) 42% 63%,var(--c3) 63% 82%,var(--c4) 82% 100%);
  -webkit-mask:radial-gradient(circle,transparent 52%,#000 53%);mask:radial-gradient(circle,transparent 52%,#000 53%)}
.sk-line{width:75%;height:16mm;opacity:.42;
  background:linear-gradient(transparent,transparent) no-repeat;
  border-bottom:1px solid var(--ink-2);position:relative}
.sk-line::after{content:'';position:absolute;inset:0;
  clip-path:polygon(0 82%,14% 66%,28% 74%,42% 48%,56% 55%,70% 30%,85% 36%,100% 12%,100% 100%,0 100%);
  background:linear-gradient(180deg,var(--brand),rgba(255,255,255,0) 92%)}

/* ---------- diversos ---------- */
.dl{display:grid;grid-template-columns:auto 1fr;gap:1.5mm 5mm;font-size:8.4pt;align-items:baseline}
.dl dt{color:var(--ink-2);text-transform:uppercase;font-size:6.6pt;letter-spacing:.08em;font-weight:600}
.dl dd{margin:0;font-weight:600}
.pill{display:inline-block;font-size:6.4pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  padding:1mm 2mm;border-radius:8mm;background:var(--soft);color:var(--brand);border:1px solid var(--line)}
.pill.ok{background:rgba(31,122,76,.1);color:var(--pos);border-color:rgba(31,122,76,.25)}
.pill.at{background:var(--warn-bg);color:var(--warn-fg);border-color:var(--warn-bd)}
.pill.rk{background:rgba(179,64,47,.09);color:var(--neg);border-color:rgba(179,64,47,.25)}
.toc{list-style:none;margin:0;padding:0;font-size:9pt}
.toc li{display:flex;align-items:baseline;gap:2mm;padding:2mm 0;border-bottom:1px solid var(--line)}
.toc .n{font-weight:800;color:var(--accent);font-size:8pt;min-width:7mm}
.toc .d{flex:1 1 auto;border-bottom:1px dotted var(--line);transform:translateY(-1mm)}
.toc .p{font-weight:700;color:var(--brand)}
.sig{margin-top:6mm;display:grid;grid-template-columns:1fr 1fr;gap:8mm;font-size:8pt}
.sig .ln{border-top:1px solid var(--ink);padding-top:1.5mm;color:var(--ink-2)}
.qr{width:34mm;height:34mm;border:1px dashed var(--brand);display:flex;align-items:center;justify-content:center;
  text-align:center;font-size:6.4pt;letter-spacing:.08em;text-transform:uppercase;color:var(--brand);font-weight:700}
"""


CSS_SLIDE = BASE + """
@page{size:338.667mm 190.5mm;margin:0}
.slide{position:relative;width:338.667mm;height:190.5mm;background:var(--paper);overflow:hidden;
  display:flex;flex-direction:column;padding:12mm 16mm 10mm;margin:0 auto 8mm;
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
.pg-head .sec{font-size:8pt;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2);font-weight:600}
.pg-head .rt{display:flex;align-items:center;gap:6mm}
.pg-head .dt{font-size:8pt;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2)}

.pg-foot{flex:0 0 auto;margin-top:auto;padding-top:3mm;display:flex;justify-content:space-between;align-items:baseline;
  font-size:6.8pt;letter-spacing:.08em;text-transform:uppercase;color:#9BA29D}
.pg-foot .no{font-size:11pt;font-weight:800;letter-spacing:0;color:var(--brand)}
.pg-body{flex:1 1 auto;min-height:0;padding-top:8mm;display:flex;flex-direction:column}

.eyebrow{display:block;font-size:7.5pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--brand);margin:0 0 3mm}
.slide.dark .eyebrow{color:#fff}
h1.t{font-size:26pt;font-weight:800;text-transform:uppercase;letter-spacing:-.015em;line-height:1.03;margin:0 0 4mm}
.lead{font-size:11pt;color:var(--ink-2);margin:0 0 6mm;max-width:210mm}
h2{font-size:11pt;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin:8mm 0 4mm;
  padding-bottom:2mm;border-bottom:1px solid var(--line)}
h2:first-child{margin-top:0}
h3{font-size:10.5pt;font-weight:700;margin:4mm 0 1.5mm}
.small{font-size:9pt}
/* No slide o `.legal` não é rodapé: na página de avisos ele é o conteúdo,
   quatro parágrafos em duas colunas. E o slide tem 1,6 vez a largura do A4,
   então o mesmo corpo em pontos aparece proporcionalmente menor quando a
   página é reduzida para caber na tela. */
.legal{font-size:9.4pt;line-height:1.55;color:var(--ink-2)}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:10mm}
/* usa a sobra vertical do slide em vez de deixá-la toda no rodapé */
.center{flex:1 1 auto;display:flex;flex-direction:column;justify-content:center;gap:8mm;min-height:0}
.cols2>*,.cols3>*,.cols2u>*,.cards>*,.kpis>*{min-width:0}
.cols3{display:grid;grid-template-columns:repeat(3,1fr);gap:8mm}
.cols2u{display:grid;grid-template-columns:1.3fr 1fr;gap:10mm}

.kpis{display:grid;grid-template-columns:repeat(var(--n,4),1fr);gap:5mm}
.kpi{min-width:0;border:1px solid var(--line);border-top:1.33px solid var(--brand);background:var(--soft);padding:5mm}
.kpi.grande{grid-column:span 2}
.kpi.grande .v{font-size:30pt;margin-top:2mm}
.kpis.leve .kpi{border:0;border-left:1px solid var(--line);background:none;padding:1mm 0 1mm 4mm}
.kpi .k{font-size:7.4pt;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2);font-weight:600}
.kpi .v{font-size:20pt;font-weight:800;line-height:1.1;margin-top:3mm;letter-spacing:-.025em;overflow-wrap:anywhere}
.kpi .s{font-size:8.4pt;color:var(--ink-2);margin-top:1.5mm}

table.tb{width:100%;border-collapse:collapse;font-size:9.5pt}
.tb thead th{background:var(--brand);color:#fff;text-align:left;font-weight:600;
  padding:3mm 3mm;font-size:7.6pt;letter-spacing:.08em;text-transform:uppercase}
/* mesmas variantes do A4: a classe tem de significar a mesma coisa nos dois formatos */
.tb.sm{font-size:8.4pt}
.tb.sm td{padding:2.5mm 3mm}
.tb.sm thead th{padding:2.5mm 3mm;font-size:7pt}
.tb.xs{font-size:7.6pt}
.tb.xs td{padding:2mm 2.5mm}
.tb.xs thead th{padding:2mm 2.5mm;font-size:6.4pt}
.tb.fix{table-layout:fixed}
.tb td{padding:3mm 3mm;border-bottom:1px solid var(--line);vertical-align:top;overflow-wrap:anywhere}
.tb tbody tr:nth-child(even) td{background:var(--soft)}

/* ---------- cronograma de reuniões ----------
   A sequência do primeiro ciclo, com as fases numa trilha à esquerda. A trilha
   é uma célula só por fase, com `rowspan`, e o rótulo deitado: são três
   palavras longas — Estruturação, Acompanhamento, Fechamento — e em pé elas
   roubariam uma coluna inteira da tabela para dizer o que é só a divisão.

   As datas são as únicas células que mudam de cliente para cliente, e por isso
   vêm dentro de uma cápsula: quem preenche vê onde escrever, e quem lê vê o que
   é combinado e o que é processo da casa. */
.crono{width:100%;border-collapse:collapse;font-size:8.4pt}
.crono thead th{background:var(--brand);color:#fff;text-align:left;font-weight:600;
  font-size:7pt;letter-spacing:.08em;text-transform:uppercase;padding:2.6mm 4mm}
.crono td{padding:2mm 4mm;border-bottom:1px solid var(--line);vertical-align:middle}
.crono tbody tr:nth-child(even) td{background:var(--soft)}
.crono .qual{font-weight:700;color:var(--brand);white-space:nowrap}
.crono .pauta{font-weight:600}
.crono .prazo{color:var(--ink-2);white-space:nowrap}
/* o objetivo estratégico é a coluna larga do plano do private: leva a frase
   inteira, e as outras três só o que precisam */
.crono .obj{color:var(--ink-2);width:100%}
.crono .quando{text-align:right;white-space:nowrap}
.crono .quando span{display:inline-block;padding:1.2mm 3.5mm;border:1px solid var(--line);
  border-radius:9mm;background:var(--paper);font-weight:700;font-size:8.2pt}
.crono td.fase{background:var(--brand);padding:0;width:9mm;border-bottom:1px solid var(--paper)}
.crono td.fase span{display:block;writing-mode:vertical-rl;transform:rotate(180deg);
  margin:0 auto;padding:4mm 0;color:var(--accent);font-size:6.8pt;font-weight:700;
  letter-spacing:.08em;text-transform:uppercase;white-space:nowrap}
.slide.dark .tb td{border-color:rgba(255,255,255,.16)}
.slide.dark .tb tbody tr:nth-child(even) td{background:rgba(255,255,255,.05)}
.tb .num,.tb th.num{text-align:right}
.tb tfoot td{font-weight:700;border-top:1.33px solid currentColor}

.cards{display:grid;grid-template-columns:repeat(var(--n,3),1fr);gap:6mm}
.card{border-left:1.33px solid var(--accent);padding-left:4mm}
.card h4{font-size:11pt;font-weight:700;margin:0 0 1.5mm}
.card p{font-size:9pt;color:var(--ink-2);margin:0;line-height:1.45}
.note{background:var(--soft);border-left:1.33px solid var(--brand);padding:4mm 5mm;font-size:9.5pt}
.note p:last-child{margin-bottom:0}
.tl{counter-reset:tl;list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:6mm 12mm}
.tl li{position:relative;padding-left:12mm;margin:0}
.tl li::before{counter-increment:tl;content:counter(tl,decimal-leading-zero);position:absolute;left:0;top:-1mm;
  font-size:16pt;font-weight:800;color:var(--accent);letter-spacing:-.02em}
.tl h4{font-size:10.5pt;font-weight:700;margin:0 0 1mm}
.tl p{font-size:9pt;color:var(--ink-2);margin:0;line-height:1.4}
.chart{border:1px dashed currentColor;background:repeating-linear-gradient(135deg,transparent 0 6px,rgba(0,0,0,.02) 6px 12px);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3mm;text-align:center;padding:6mm}
.slide.dark .chart{background:repeating-linear-gradient(135deg,transparent 0 6px,rgba(255,255,255,.045) 6px 12px)}
.chart .cl{font-size:7.6pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--brand)}
.chart.feito{border:0;background:none;padding:0;gap:2mm}
.slide.dark .chart .cl{color:#fff}
.chart .cd{font-size:9pt;color:var(--ink-2);max-width:150mm;line-height:1.45}
.slide.dark .chart .cd{color:rgba(255,255,255,.75)}
.sk-bars{display:flex;align-items:flex-end;gap:4mm;height:26mm;width:60%;opacity:.3}
.sk-bars i{flex:1;background:currentColor;border-radius:.6mm .6mm 0 0}
.sk-donut{width:32mm;height:32mm;border-radius:50%;opacity:.35;
  background:conic-gradient(var(--c1) 0 42%,var(--c2) 42% 63%,var(--c3) 63% 82%,var(--c4) 82% 100%);
  -webkit-mask:radial-gradient(circle,transparent 52%,#000 53%);mask:radial-gradient(circle,transparent 52%,#000 53%)}
.pill{display:inline-block;font-size:7.4pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  padding:1mm 3mm;border-radius:8mm;background:var(--soft);color:var(--brand);border:1px solid var(--line)}
.slide.dark .pill{background:rgba(255,255,255,.1);color:#fff;border-color:rgba(255,255,255,.24)}
.dl{display:grid;grid-template-columns:auto 1fr;gap:2mm 6mm;font-size:9.5pt;align-items:baseline}
.dl dt{color:var(--ink-2);text-transform:uppercase;font-size:7.4pt;letter-spacing:.08em;font-weight:600}
.slide.dark .dl dt{color:rgba(255,255,255,.7)}
.dl dd{margin:0;font-weight:600}
.qr{width:52mm;height:52mm;border:1px dashed currentColor;display:flex;align-items:center;justify-content:center;
  text-align:center;font-size:7.6pt;letter-spacing:.08em;text-transform:uppercase;font-weight:700;opacity:.85}
.imgbox{border:1px dashed currentColor;display:flex;flex-direction:column;align-items:center;justify-content:center;
  gap:2mm;text-align:center;padding:8mm;
  background:repeating-linear-gradient(135deg,transparent 0 7px,rgba(0,0,0,.022) 7px 14px)}
.slide.dark .imgbox{background:repeating-linear-gradient(135deg,transparent 0 7px,rgba(255,255,255,.05) 7px 14px)}
.imgbox .cl{font-size:7.6pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--brand)}
.slide.dark .imgbox .cl{color:#fff}
.imgbox .cd{font-size:9pt;max-width:90mm;line-height:1.45;color:var(--ink-2)}

/* A foto institucional é parte do desenho, e não escolha de quem preenche. Vai
   na proporção em que foi tirada: a sede é um prédio largo, e recortá-la para
   caber num retrato 3:4 cortava metade da fachada. A largura é a da coluna e a
   altura sai sozinha, que é o que `height:auto` faz — nenhuma caixa impõe
   formato a ela. */
.imgfixa{display:block;width:100%;height:auto;border-radius:1mm}
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
.cv-foot .cf{font-size:7.6pt;letter-spacing:.08em;text-transform:uppercase;opacity:.55}
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
.plan .tag{font-size:7.4pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2)}
.plan .pr{margin:3mm 0;padding:3mm 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.plan .pr b{display:block;font-size:14pt;font-weight:800;color:var(--brand);letter-spacing:-.02em}
.plan .pr span{font-size:8.4pt;color:var(--ink-2)}
.plan ul{list-style:none;padding:0;margin:0;font-size:8.6pt;line-height:1.4}
.plan li{position:relative;padding-left:4mm;margin-bottom:8px}
.plan li::before{content:"";position:absolute;left:0;top:7px;width:2.4mm;height:1.33px;background:var(--accent)}
.plan .ft{margin-top:auto;padding-top:4mm;font-size:8.2pt;color:var(--ink-2)}
.steps{display:grid;grid-template-columns:repeat(var(--n,4),1fr);gap:8mm;counter-reset:st;list-style:none;padding:0;margin:0}
.steps>li{min-width:0;position:relative;padding-top:10mm}
.steps>li::before{counter-increment:st;content:counter(st,decimal-leading-zero);position:absolute;left:0;top:0;
  font-size:18pt;font-weight:800;color:var(--accent);letter-spacing:-.02em}
.steps>li::after{content:"";position:absolute;left:0;top:9mm;width:100%;height:1px;background:var(--line)}
.steps h4{font-size:10.5pt;font-weight:700;margin:0 0 1.5mm}
.steps p{font-size:9pt;color:var(--ink-2);margin:0;line-height:1.45}
.slide.dark .steps>li::after{background:rgba(255,255,255,.25)}
.big{font-size:34pt;font-weight:800;line-height:1;letter-spacing:-.03em;color:var(--brand)}
.slide.dark .big{color:#fff}
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
.flow .tag{display:block;font-size:5.8pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  color:var(--ink-2);margin-bottom:1mm}
.flow h4{font-size:9pt;font-weight:700;margin:0 0 1mm}
.flow p{font-size:8pt;color:var(--ink-2);margin:0;line-height:1.45}

/* ---------- legenda de série, com a paleta do segmento ---------- */
/* ---------- gráfico desenhado a partir do dado ----------
   Entra no lugar da moldura vazia quando o consultor preenche a tabelinha na
   ferramenta. É SVG: sai vetor no PDF, na tipografia da casa e nas cores do
   segmento — `--c1`..`--c8`, as mesmas da legenda: a paleta categórica do
   design system (produtosauvp.github.io/central), em que a primeira cor é a da
   marca e as demais foram escolhidas para máximo contraste de matiz. Variação
   com sinal usa a divergente (`--g-pos`, `--g-neg`) e intensidade a sequencial
   (`--g-seq-1`..`--g-seq-5`). São tokens só dos gráficos: o resto do documento
   segue as cores do segmento. */
.g-svg{width:100%;height:auto;max-height:100%;display:block;flex:1 1 0;min-height:0}
/* O desenho não empurra a caixa: ele ocupa o que sobra dela. A moldura vazia e a
   preenchida medem o mesmo, e o gráfico nunca cresce por cima do que está ao lado. */
.g-guia{stroke:var(--line);stroke-width:1}
.g-eixo{fill:var(--ink-2);font-size:9px}
.g-mini{fill:var(--ink-2);font-size:9px;text-anchor:middle;letter-spacing:.04em}
.g-linha{fill:none;stroke:var(--c1);stroke-width:2.6;stroke-linejoin:round;stroke-linecap:round}
.g-area{fill:var(--c1);opacity:.10}
.g-ponto{fill:var(--paper);stroke:var(--c1);stroke-width:2}
.g-nota{font-size:7pt;color:var(--ink-2);text-align:center}
.slide.dark .g-eixo,.slide.dark .g-mini{fill:rgba(255,255,255,.75)}
.slide.dark .g-guia{stroke:rgba(255,255,255,.22)}


.legend{list-style:none;display:flex;flex-wrap:wrap;justify-content:center;gap:1.5mm 4mm;
  margin:3mm 0 0;padding:0;font-size:6.6pt;color:var(--ink-2)}
.legend li{display:flex;align-items:center;gap:1.5mm}
.legend i{width:2.4mm;height:2.4mm;border-radius:50%;flex:0 0 auto}
.g-zero{stroke:var(--ink-2);stroke-width:1}

"""

CSS_SLIDE += """
/* ---------- processo: nós numerados sobre um trilho contínuo ---------- */
.flow{list-style:none;margin:0;padding:0;counter-reset:fl;
  display:grid;grid-template-columns:repeat(var(--n,4),1fr);column-gap:8mm}
.flow>li{position:relative;min-width:0;padding-top:16mm}
.flow>li::after{content:"";position:absolute;left:0;right:calc(-1 * 8mm);top:6mm;height:1px;background:var(--line)}
.flow>li:last-child::after{right:0}
.flow .node{position:absolute;left:0;top:0;z-index:2;width:12mm;height:12mm;border-radius:50%;
  border:1px solid var(--brand);background:var(--paper);color:var(--brand);
  display:flex;align-items:center;justify-content:center;font-weight:800;font-size:11pt;letter-spacing:-.01em}
.flow .node::before{counter-increment:fl;content:counter(fl,decimal-leading-zero)}
.flow .tag{display:block;font-size:7pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  color:var(--ink-2);margin-bottom:1mm}
.flow h4{font-size:10.5pt;font-weight:700;margin:0 0 1mm}
.flow p{font-size:9pt;color:var(--ink-2);margin:0;line-height:1.45}

/* ---------- legenda de série, com a paleta do segmento ---------- */
/* ---------- gráfico desenhado a partir do dado ----------
   Entra no lugar da moldura vazia quando o consultor preenche a tabelinha na
   ferramenta. É SVG: sai vetor no PDF, na tipografia da casa e nas cores do
   segmento — `--c1`..`--c8`, as mesmas da legenda: a paleta categórica do
   design system (produtosauvp.github.io/central), em que a primeira cor é a da
   marca e as demais foram escolhidas para máximo contraste de matiz. Variação
   com sinal usa a divergente (`--g-pos`, `--g-neg`) e intensidade a sequencial
   (`--g-seq-1`..`--g-seq-5`). São tokens só dos gráficos: o resto do documento
   segue as cores do segmento. */
.g-svg{width:100%;height:auto;max-height:100%;display:block;flex:1 1 0;min-height:0}
/* O desenho não empurra a caixa: ele ocupa o que sobra dela. A moldura vazia e a
   preenchida medem o mesmo, e o gráfico nunca cresce por cima do que está ao lado. */
.g-guia{stroke:var(--line);stroke-width:1}
.g-eixo{fill:var(--ink-2);font-size:10px}
.g-mini{fill:var(--ink-2);font-size:10px;text-anchor:middle;letter-spacing:.04em}
.g-linha{fill:none;stroke:var(--c1);stroke-width:2.6;stroke-linejoin:round;stroke-linecap:round}
.g-area{fill:var(--c1);opacity:.10}
.g-ponto{fill:var(--paper);stroke:var(--c1);stroke-width:2}
.g-nota{font-size:7pt;color:var(--ink-2);text-align:center}
.slide.dark .g-eixo,.slide.dark .g-mini{fill:rgba(255,255,255,.75)}
.slide.dark .g-guia{stroke:rgba(255,255,255,.22)}


.legend{list-style:none;display:flex;flex-wrap:wrap;justify-content:center;gap:1.5mm 6mm;
  margin:4mm 0 0;padding:0;font-size:8pt;color:var(--ink-2)}
.legend li{display:flex;align-items:center;gap:1.5mm}
.legend i{width:3mm;height:3mm;border-radius:50%;flex:0 0 auto}

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
.stats{display:grid;grid-template-columns:repeat(var(--n,5),1fr);margin-top:6mm}
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
.lista{list-style:none;margin:0;padding:0;font-size:8.4pt;line-height:17px}
.lista li{position:relative;padding-left:5mm;margin-bottom:9px}
.lista li:last-child{margin-bottom:0}
.lista li::before{content:"";position:absolute;left:0;top:8px;width:2.6mm;height:1.33px;background:var(--accent)}
.lista.mut li{color:var(--ink-2)}
.chips{display:flex;flex-wrap:wrap;gap:1.5mm;margin-bottom:1mm}
.side h3{font-size:6.8pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  color:var(--ink-2);margin:5mm 0 2mm;padding-bottom:1mm;border-bottom:1px solid var(--line)}
.side h3:first-child{margin-top:0}
.side .lista{font-size:8pt;margin-bottom:0}
.side .dl{font-size:8pt}
"""

CSS_A4 += """
/* princípios em duas colunas: título embutido no parágrafo ocupa bem menos
   altura que cinco cards estreitos */
.principios{display:grid;grid-template-columns:1fr 1fr;gap:1.5mm 6mm}
.principios p{font-size:7.7pt;line-height:1.4;margin:0}
.principios strong{color:var(--brand)}
"""

CSS_A4 += """
/* ---------- retrato na coluna de apoio ---------- */
/* O retrato escrito, quando existe pessoa: mesma caixa e mesmo canto da
   moldura vazia, para a página não mudar de forma entre as duas. O corte sobe
   um pouco o enquadramento, que é onde o rosto costuma estar. */
.rt-img{display:block;width:100%;aspect-ratio:3/4;object-fit:cover;
  object-position:50% 26%;border-radius:3mm 0 0 0}
/* O espaço de imagem só existia nos slides, que são onde os `imgbox` estavam.
   A moldura vazia do retrato o traz para o A4, com a mesma escala do resto da
   página. */
.imgbox{border:1px dashed var(--line);display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:1.5mm;text-align:center;padding:5mm;
  background:repeating-linear-gradient(135deg,transparent 0 5px,rgba(0,0,0,.022) 5px 10px)}
.imgbox .cl{font-size:6.6pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  color:var(--brand)}
.imgbox .cd{font-size:7.4pt;max-width:70mm;line-height:1.4;color:var(--ink-2)}


/* A moldura vazia do retrato ocupa a mesma caixa e tem o mesmo canto, para a
   página não mudar de forma entre a versão escrita e a em branco. */
.rt-vaga{width:100%;aspect-ratio:3/4;flex:none;align-self:end;
  border-radius:3mm 0 0 0;padding:4mm 3mm}
.rt-vaga .cd{font-size:6.6pt;line-height:1.35}

/* ---------- respiro elástico entre faixas ----------
   Em página de altura fechada sobra espaço que varia de um documento para
   outro. Em vez de empurrar tudo para as bordas com um único vão enorme, o
   excedente é dividido entre as faixas: cada respiro cresce na mesma medida,
   entre um piso e um teto, e o que não couber fica na margem inferior. */
.esp{flex:1 1 0;min-height:4mm;max-height:11mm}

/* ---------- linha do tempo e etiquetas ----------
   Dois blocos que a folha do consultor usa ao lado do texto corrido. Nos
   marcos, o rótulo fica acima do texto e não numa coluna à esquerda: eles vão
   de "2016" a "Pandemia" e a "Há três anos", e coluna fixa não comporta os
   dois. */
.marcos{list-style:none;margin:0;padding:0}
.marcos li{position:relative;padding:0 0 10px 8mm}
.marcos li:last-child{padding-bottom:0}
.marcos li::before{content:"";position:absolute;left:1.15mm;top:4.2mm;bottom:-.4mm;
  width:1px;background:var(--line)}
.marcos li:last-child::before{display:none}
.marcos li::after{content:"";position:absolute;left:0;top:1.2mm;width:2.4mm;height:2.4mm;
  border-radius:50%;border:1px solid var(--brand);background:var(--paper)}
.marcos .q{display:block;font-size:6.6pt;font-weight:700;letter-spacing:.08em;
  text-transform:uppercase;color:var(--brand);margin-bottom:1mm}
.marcos p{margin:0;font-size:8.2pt;line-height:1.45;color:var(--ink-2)}

.tags{display:flex;flex-wrap:wrap;gap:1.4mm;margin:0}
.tags span{font-size:7.2pt;padding:.8mm 2.8mm;border:1px solid var(--line);
  border-radius:8mm;color:var(--ink-2)}


/* ---------- folha de uma página ----------
   A apresentação de uma página tem chrome próprio, como as capas: sem
   cabeçalho corrido e sem numeração, porque a página é uma só. As medidas vêm
   das proporções do modelo de referência, reescritas para A4. */
.page.folha{padding:0;display:block;position:relative}
.page.folha .fl-aneis,.page.folha .fl-foto,.page.folha .fl-nome,
.page.folha .fl-corpo,.page.folha .fl-pe{position:absolute}

/* Os anéis sangram pela esquerda; o traço fica fino em qualquer escala. A
   opacidade de cada um vem do gerador, que a calcula a partir do raio. */
.fl-aneis{fill:none;stroke:#fff;stroke-width:.75pt;
  vector-effect:non-scaling-stroke;overflow:visible}
.fl-aneis circle{vector-effect:non-scaling-stroke}

.fl-foto{border-radius:50%;overflow:hidden}
.fl-foto img{width:100%;height:100%;object-fit:cover;object-position:50% 26%;display:block}
/* A moldura vazia é o mesmo círculo, com a especificação dentro. */
.fl-foto.imgbox{border-color:rgba(255,255,255,.35);padding:6mm;gap:2mm;
  background:repeating-linear-gradient(135deg,transparent 0 6px,rgba(255,255,255,.04) 6px 12px)}
.fl-foto.imgbox .cl{color:rgba(255,255,255,.72)}
.fl-foto.imgbox .cd{font-size:6.6pt;line-height:1.35;color:rgba(255,255,255,.5)}

/* O bloco do nome se centra pelo centro do círculo do retrato, não pelo topo
   dele: é o eixo que os dois compartilham. */
.fl-nome{left:93mm;right:24mm;top:58.5mm;transform:translateY(-50%)}
.fl-nome h1{margin:0;font-size:32pt;font-weight:800;line-height:1.02;
  letter-spacing:-.02em;color:#fff}
.fl-nome p{margin:2mm 0 0;font-size:19pt;font-weight:300;line-height:1.15;
  color:rgba(255,255,255,.88)}

/* O texto corrido é justificado, como no original, e tem o corpo grande que
   aquela página usa: 2,1% da largura da folha. */
/* Texto e contatos ficam num bloco só, entre o retrato e o pé. O vão entre os
   dois é elástico com teto, como o `.esp` do resto do sistema: um consultor de
   texto curto não abre um buraco no meio da folha — a sobra vai para a margem
   de baixo, onde se lê como margem. */
.fl-corpo{left:24mm;right:24mm;top:112mm;bottom:34mm;
  display:flex;flex-direction:column}
.fl-bio{font-size:12.5pt;line-height:1.55;text-align:justify;color:rgba(255,255,255,.92)}
.fl-bio p{margin:0 0 6mm}
.fl-bio p:last-child{margin-bottom:0}
.fl-vao{flex:1 1 0;min-height:12mm;max-height:30mm}

.fl-contatos{display:grid;gap:7mm}
.fl-ct{display:grid;grid-template-columns:11mm 1fr;align-items:center;
  font-size:12.5pt;color:#fff}
.fl-ct .ic svg{width:8.5mm;height:8.5mm;display:block;fill:none;
  stroke:rgba(255,255,255,.85);stroke-width:1.3;
  stroke-linecap:round;stroke-linejoin:round}

.fl-pe{left:24mm;right:24mm;bottom:16mm;display:flex;align-items:center;gap:10mm}
.fl-pe .rule{flex:1 1 auto;height:1px;background:rgba(255,255,255,.45)}
.fl-pe .logo{flex:0 0 auto}

/* ---------- página invertida ----------
   A última página da apresentação do consultor roda no negativo. É o que a
   fecha sem acrescentar ornamento: mesma grelha, mesma tipografia, mesmos
   fios — só o fundo troca. */
.page.dark{color:#fff;background:linear-gradient(225deg,var(--brand) 0%,#000 100%)}
.page.dark .pg-head,.page.dark .pg-foot{border-color:rgba(255,255,255,.2)}
.page.dark .pg-head .sec,.page.dark .pg-head .dt{color:rgba(255,255,255,.78)}
.page.dark .pg-foot{color:rgba(255,255,255,.45)}
.page.dark .pg-foot .no{color:#fff}
.page.dark h2{border-color:rgba(255,255,255,.2)}
.page.dark .eyebrow{color:#fff}
.page.dark .lead,.page.dark .mut{color:rgba(255,255,255,.78)}
.page.dark .lista.mut li{color:rgba(255,255,255,.78)}
.page.dark .legal{color:rgba(255,255,255,.5)}
.page.dark .dl dt{color:rgba(255,255,255,.62)}
.page.dark .principios strong{color:#fff}
.page.dark .lista li::before,.page.dark .plan li::before{background:rgba(255,255,255,.55)}
.page.dark .card,.page.dark .plan.hl{border-color:rgba(255,255,255,.28)}
.page.dark .card .n,.page.dark .toc .n,.page.dark .plan .n{color:#fff}
.page.dark .ph{background:rgba(255,255,255,.16);color:#fff}
.page.dark .pill{background:rgba(255,255,255,.08);color:#fff;border-color:rgba(255,255,255,.24)}
.page.dark .note{background:rgba(255,255,255,.06);border-left-color:rgba(255,255,255,.4)}

"""


# ---------------------------------------------------------------- folha longa
# A apresentação do consultor não é um relatório: ela se lê de uma vez, do
# começo ao fim. Em oito páginas A4 isso virava oito quebras, oito cabeçalhos
# repetidos e um vão no pé de cada uma, porque o texto de cada pessoa tem um
# tamanho diferente. Numa folha só, alta, o texto corre e as faixas é que dão o
# ritmo — claro, escuro, claro — no lugar da quebra de página.
#
# A altura tem de estar escrita: `@page` não aceita altura automática, e é o
# `@page` que a ferramenta usa ao imprimir pelo navegador. O número abaixo é só
# o ponto de partida — quem o acerta é `npm run altura -- --ajustar`, que mede
# quanto o conteúdo de cada folha ocupa de fato e reescreve os dois números no
# arquivo gerado. Por isso cada documento sai com a altura do texto que ele tem,
# e não com a altura do consultor mais falante.
ALTURA_LONGA = 1420

CSS_LONGA = """
/* altura da folha — os dois números saem de `npm run altura -- --ajustar` */
@page{size:210mm %(h)dmm;margin:0}
.page.longa{height:%(h)dmm;padding:0;font-size:10pt}
@media print{.page.longa{break-after:auto}}

/* as faixas: a folha alterna fundo para marcar onde uma parte acaba e outra
   começa, que é o que a quebra de página fazia antes */
.lg-topo,.lg-pe{color:#fff;background:linear-gradient(225deg,var(--brand) 0%%,#000 100%%);
  position:relative;overflow:hidden;flex:0 0 auto}
.lg-corpo,.lg-faixa,.lg-topo,.lg-pe{padding:16mm 15.3mm}
.lg-faixa{background:var(--soft);flex:0 0 auto;display:flex;flex-direction:column}
.lg-corpo{flex:1 1 auto;display:flex;flex-direction:column;min-height:0}

/* o alto: retrato à esquerda, identificação à direita, declaração cruzando as
   duas colunas sob um fio — a mesma composição da abertura que existia antes.
   O plano, o nome e o cargo se centram pelo eixo do retrato, e não pelo pé
   dele: são dois blocos de altura diferente lado a lado, e alinhar pela base
   deixava o nome caído num canto da foto. */
.lg-topo{padding-top:20mm;padding-bottom:18mm}
.lg-topo .grain{position:absolute;inset:0;z-index:1}
.lg-topo>*{position:relative;z-index:2}
.lg-id{display:grid;grid-template-columns:44mm 1fr;gap:0 10mm;align-items:center}
.lg-id .rt-img,.lg-id .rt-vaga{margin:0;border-radius:4mm 0 0 0}
.lg-id .rt-vaga{border-color:rgba(255,255,255,.35);
  background:repeating-linear-gradient(135deg,transparent 0 6px,rgba(255,255,255,.05) 6px 12px)}
.lg-id .rt-vaga .cl{color:rgba(255,255,255,.72)}
.lg-id .rt-vaga .cd{color:rgba(255,255,255,.5)}
.lg-plano{display:block;font-size:7.2pt;font-weight:700;letter-spacing:.08em;
  text-transform:uppercase;color:rgba(255,255,255,.7);margin-bottom:3mm}
.lg-id h1{margin:0;font-size:30pt;font-weight:800;text-transform:uppercase;
  line-height:1.02;letter-spacing:-.02em}
.lg-id .papel{margin:3mm 0 0;font-size:11pt;font-weight:300;color:rgba(255,255,255,.85)}
/* a declaração fica na mesma coluna do nome, e não atravessando a folha: ela
   é sobre a pessoa, e lida ao lado do retrato diz de quem é. Em corpo pequeno,
   na escala das credenciais — é legenda do nome, não manchete. */
/* Sem teto de medida: o fio que abre a declaração termina onde termina a
   coluna, que é onde termina o fio da faixa de credenciais logo abaixo. Dois
   fios empilhados que parassem em pontos diferentes leriam como desalinho. */
.lg-frase{margin:5mm 0 0;padding-top:4mm;
  border-top:1px solid rgba(255,255,255,.3);
  font-size:9pt;line-height:1.6;font-weight:300;
  color:rgba(255,255,255,.88)}

/* a faixa de credenciais encosta no alto escuro, como legenda dele */
.lg-cred{margin-top:9mm;display:grid;grid-template-columns:repeat(var(--n,3),1fr);
  border-top:1px solid rgba(255,255,255,.3)}
.lg-cred>div{min-width:0;padding:5mm 7mm;border-left:1px solid rgba(255,255,255,.22)}
.lg-cred>div:first-child{padding-left:0;border-left:0}
.lg-cred>div:last-child{padding-right:0}
.lg-cred h3{margin:0 0 3mm;font-size:6.6pt;font-weight:700;letter-spacing:.08em;
  text-transform:uppercase;color:rgba(255,255,255,.62)}
/* dois blocos empilhados na mesma coluna precisam de ar entre eles */
.lg-cred h3:not(:first-child){margin-top:7mm}
.lg-cred .lista{font-size:8.4pt;margin:0;color:rgba(255,255,255,.9)}
.lg-cred .lista li{margin-bottom:5px}
.lg-cred .lista li::before{background:rgba(255,255,255,.55)}
.lg-cred .pill{background:rgba(255,255,255,.1);color:#fff;border-color:rgba(255,255,255,.28)}

/* cada assunto é uma seção com título; o corpo é o texto corrido do sistema */
.lg-sec{flex:0 0 auto}
.lg-sec h2{margin:0 0 5mm}
.longa .corrido{font-size:11pt;line-height:1.75;max-width:152mm}
.longa .corrido p{margin:0 0 5mm}
.longa .corrido p:last-child{margin-bottom:0}
.longa .cols2u .corrido,.longa .cols2 .corrido{max-width:none}
.longa .lista{font-size:9.4pt;line-height:20px}
.longa .lista li{padding-left:6mm;margin-bottom:14px}
.longa .lista li::before{top:9px;width:3.2mm}
.longa .principios{gap:7mm 12mm}
.longa .principios p{font-size:9.2pt;line-height:1.62}
.longa .lead{font-size:11.5pt;line-height:1.55;max-width:none;margin-bottom:0}

/* a nota de posição: onde este plano fica entre os três, fechando a faixa sob
   as duas colunas do que ele entrega. Caixa de papel sobre o fundo suave da
   faixa, com o fio da marca à esquerda — é a mesma ideia do `.note` do resto do
   sistema, que aqui não serve porque o fundo dele é justamente o da faixa.

   Por dentro a caixa se divide, porque à largura inteira a linha passaria de
   noventa caracteres: o parágrafo que situa o plano fica à esquerda, em corpo
   maior, e o que desdobra desce à direita — a mesma grelha das duas colunas de
   cima. Dividir por parágrafo, e não deixar o texto correr de uma coluna para a
   outra: correndo, as alturas fecham iguais, mas a frase quebra no meio do
   caminho e se lê pela metade antes de recomeçar do outro lado. */
.lg-posicao{margin-top:10mm;padding:8mm 9mm;background:var(--paper);
  border:1px solid var(--line);border-left:1.33px solid var(--brand);
  display:grid;grid-template-columns:1fr 1fr;gap:0 12mm}
.lg-posicao>*{min-width:0}
.lg-posicao p{margin:0;font-size:8.8pt;line-height:1.66;color:var(--ink-2)}
.lg-posicao p+p{margin-top:4mm}
.lg-posicao .abre{font-size:10.2pt;line-height:1.55;color:var(--ink)}

/* o respiro entre seções cresce com a sobra, entre um piso e um teto: é o que
   acomoda a diferença de tamanho entre um consultor e outro sem abrir um
   buraco único no meio da folha. O teto é alto porque a folha é alta: entre o
   consultor que escreve pouco e o que escreve muito há uns 20 cm de diferença,
   e é isso que se reparte aqui. */
.longa .esp{flex:1 1 0;min-height:10mm;max-height:60mm}

/* o pé: canais de um lado, contato do outro, régua e marca fechando */
.lg-pe{padding-top:16mm;padding-bottom:14mm}
.lg-pe .grain{position:absolute;inset:0;z-index:1}
.lg-pe>*{position:relative;z-index:2}
.lg-pe h2{margin:0 0 4mm;border-color:rgba(255,255,255,.3)}
.lg-pe .dl{font-size:9.4pt;gap:3mm 6mm}
.lg-pe .dl dt{color:rgba(255,255,255,.62)}
.lg-pe .mut{color:rgba(255,255,255,.72)}
.lg-pe .legal{color:rgba(255,255,255,.5)}
.lg-assina{margin-top:12mm;padding-top:6mm;border-top:1px solid rgba(255,255,255,.3);
  display:flex;align-items:center;justify-content:space-between;gap:10mm}
.lg-assina .data{font-size:8pt;letter-spacing:.08em;text-transform:uppercase;
  color:rgba(255,255,255,.72)}
""" % dict(h=ALTURA_LONGA)
