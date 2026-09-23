# -*- coding: utf-8 -*-
"""O documento em branco: capa, nada, e a página de avisos.

Existe para o construtor da ferramenta. Todo outro documento nasce com as
páginas que o gerador decidiu; este nasce com duas — a capa e o fecho — e o
que vai entre elas é montado com os blocos, página a página, por quem
precisa de um documento que ainda não existe: um estudo de caso, um material
de reunião fora do calendário, uma resposta escrita a uma pergunta grande.

Sai em dois formatos, e o formato é a capa: `build` dá o A4 com a capa de
relatório; `build_slide` dá o 16:9 com a capa de apresentação. A capa é a da
casa, na medida e no desenho de sempre; o que muda é o que está escrito nela,
e tudo o que está escrito é campo — os dois pares de título, as linhas de
identificação, a data. O campo já vem preenchido com um texto padrão, para a
capa nunca sair em branco por descuido, e se troca à vontade.

A página de fecho é a mesma dos relatórios: avisos legais e contato. Além de
fechar o documento, ela é o molde de que a ferramenta clona o cabeçalho, o
rodapé e a logo das páginas montadas — a capa não serve para isso, porque não
tem cabeçalho nem corpo.
"""
from layout import *

PAPEL = {"consultoria": "Consultor(a)", "alta-renda": "Consultor(a)",
         "private": "Banker", "assessoria": "Assessor(a)"}


def _identificacao(t, papel):
    return [com_rotulo(t, ph("nome_cliente")),
            papel + ": " + ph("nome_responsavel"),
            ph("capa_linha_livre", "Uma linha a mais na capa, se precisar; em branco, some"),
            ph("data_documento")]


def _avisos_campos():
    return dict(
        disc=ph("disclaimer_regulatorio", "Texto aprovado pelo compliance para este segmento"),
        cli=ph("nome_cliente"), resp=ph("nome_responsavel"), cert=ph("registro_cvm_ou_ancord"),
        canal=ph("canal_atendimento"), email=ph("email_contato"), ouv=ph("canal_ouvidoria"),
        razao=ph("razao_social"), cnpj=ph("cnpj"))


def build(t, seg):
    set_date_ph("data_documento")
    papel = PAPEL[seg]
    P = []
    P.append(cover_a4(
        t, ph("capa_titulo_1", "Primeira palavra do título, em peso leve", padrao="Documento"),
        ph("capa_titulo_2", "Segunda palavra do título, em negrito", padrao="Especial"),
        ph("capa_rodape_1", "Primeira palavra da linha de baixo, em peso leve", padrao="Sua"),
        ph("capa_rodape_2", "Segunda palavra da linha de baixo, em negrito", padrao="Carteira"),
        _identificacao(t, papel)))

    P.append(page_a4(t, "Avisos e contato", 2, """<h1 class="t">Avisos e contato</h1>
<h2>Avisos legais</h2>
<p class="legal">%(disc)s</p>
<p class="legal">Rentabilidade passada não representa garantia de rentabilidade futura. Os investimentos apresentados podem não ser adequados a todos os investidores e não contam, salvo quando expressamente indicado, com garantia do Fundo Garantidor de Créditos (FGC) nem de qualquer mecanismo de seguro. Antes de investir, leia atentamente os documentos de cada produto, incluindo regulamento, lâmina, prospecto e formulário de informações complementares.</p>
<p class="legal">Este material é destinado exclusivamente a %(cli)s, tem caráter informativo e não constitui oferta, recomendação pública, proposta de investimento ou solicitação de compra ou venda de qualquer ativo. É proibida a reprodução, redistribuição ou compartilhamento total ou parcial deste documento sem autorização prévia e por escrito.</p>
<h2>Contato e ouvidoria</h2>
<div class="dl">
  <dt>Responsável</dt><dd>%(resp)s, %(cert)s</dd>
  <dt>Atendimento</dt><dd>%(canal)s</dd>
  <dt>E-mail</dt><dd>%(email)s</dd>
  <dt>Ouvidoria</dt><dd>%(ouv)s</dd>
  <dt>Razão social</dt><dd>%(razao)s, CNPJ %(cnpj)s</dd>
</div>""" % _avisos_campos()))
    return P


def build_slide(t, seg):
    set_date_ph("data_documento")
    papel = PAPEL[seg]
    S = []
    S.append(cover_slide(
        t, ph("capa_titulo_1", "Primeira parte do título, em peso leve", padrao="Apresentação"),
        ph("capa_titulo_2", "Segunda parte do título, em negrito", padrao="Especial"),
        ph("capa_subtitulo", "Uma linha sob o título", padrao="O assunto desta apresentação"),
        _identificacao(t, papel)))

    S.append(slide(t, "Avisos", 2, """<h1 class="t">Notas e avisos</h1>
<p class="legal">%(disc)s</p>
<div class="cols2" style="margin-top:6mm">
  <div>
    <p class="legal">Rentabilidade passada não representa garantia de rentabilidade futura. Os investimentos apresentados podem não contar com garantia do Fundo Garantidor de Créditos (FGC). Antes de investir, leia os documentos oficiais de cada produto.</p>
  </div>
  <div>
    <p class="legal">Material destinado exclusivamente a %(cli)s. Não constitui oferta, recomendação pública ou solicitação de compra ou venda de ativos. É proibida a reprodução ou o compartilhamento total ou parcial sem autorização prévia e por escrito. %(razao)s, CNPJ %(cnpj)s. Ouvidoria: %(ouv)s.</p>
  </div>
</div>
<div class="dl" style="margin-top:6mm">
  <dt>Responsável</dt><dd>%(resp)s, %(cert)s</dd>
  <dt>E-mail</dt><dd>%(email)s</dd>
</div>""" % _avisos_campos()))
    return S
