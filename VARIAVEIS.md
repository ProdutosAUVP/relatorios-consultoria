# Dicionário de variáveis

Todo campo preenchível aparece nos modelos como `{{nome_da_variavel}}`, destacado em dourado. Substitua o token inteiro, chaves incluídas.

Os nomes são estáveis entre documentos: `{{patrimonio_total}}` significa a mesma coisa no relatório mensal e na versão em apresentação, o que permite preencher vários modelos com a mesma fonte de dados.

Arquivo gerado por `npm run vars`; não edite à mão.

## Convenções

| Padrão | Significado | Exemplo |
| --- | --- | --- |
| `nome_do_campo` | valor único | `{{nome_cliente}}` |
| `bloco_N_campo` | linha `N` de uma lista ou tabela | `{{mov_3_ativo}}` |
| `prefixo_chave_metrica` | célula de uma tabela de referência fixa | `{{alvo_rf_pos}}` |
| `texto_*`, `analise_*`, `comentario_*` | texto corrido escrito pelo responsável | `{{texto_desvio_alocacao}}` |

Linhas sobrando numa tabela (por exemplo, só houve 3 movimentações e o modelo traz 6 linhas) devem ser apagadas do HTML, não deixadas com o token à mostra.

## Campos institucionais e recorrentes

Estes se repetem na maior parte dos modelos. Vale manter um arquivo único com eles e aplicar em lote antes de partir para o conteúdo específico de cada documento.

| Variável | O que é | Em quantos modelos |
| --- | --- | --- |
| `razao_social` | Razão social da empresa emissora | 24 de 24 |
| `cnpj` | CNPJ da empresa emissora | 24 de 24 |
| `registro_cvm_empresa` | Registro da empresa na CVM | 4 de 24 |
| `canal_ouvidoria` | Telefone ou e-mail da ouvidoria | 20 de 24 |
| `disclaimer_regulatorio` | Texto legal aprovado pelo compliance, específico do segmento | 20 de 24 |
| `nome_cliente` | Nome do cliente destinatário | 20 de 24 |
| `nome_responsavel` | Consultor, assessor ou banker responsável | 20 de 24 |
| `registro_cvm_ou_ancord` | Registro do responsável (CVM 19 / Ancord) | 12 de 24 |
| `email_contato` | E-mail de contato exibido no documento | 20 de 24 |
| `whatsapp_contato` | WhatsApp direto do responsável | 8 de 24 |
| `canal_atendimento` | Canal e horário de atendimento | 12 de 24 |
| `link_agendamento` | URL de agendamento (a mesma do QR code) | 12 de 24 |
| `mes_referencia` | Mês de referência, ex.: Agosto de 2026 | 12 de 24 |
| `data_posicao` | Data da posição consolidada | 8 de 24 |
| `perfil_investidor` | Perfil de suitability do cliente | 8 de 24 |
| `patrimonio_total` | Patrimônio total sob acompanhamento | 8 de 24 |

## Apresentação geral

Arquivos: `modelos/apresentacao-geral-alta-renda.html`, `modelos/apresentacao-geral-assessoria.html`, `modelos/apresentacao-geral-consultoria.html`, `modelos/apresentacao-geral-private.html`

Segmentos: alta-renda, assessoria, consultoria, private &middot; 132 variáveis

<details><summary>Ver as 122 variáveis específicas deste documento</summary>

```
subtitulo_apresentacao            data_apresentacao                 historia_auvp
ano_fundacao                      modelo_remuneracao                custodiante
numero_1                          numero_1_legenda                  numero_2
numero_2_legenda                  numero_3                          numero_3_legenda
numero_4                          numero_4_legenda                  numero_5
numero_5_legenda                  numero_6                          numero_6_legenda
nota_fonte_numeros                metodo_1_detalhe                  metodo_2_detalhe
metodo_3_detalhe                  metodo_4_detalhe                  metodo_5_detalhe
prazo_implantacao                 entrega_1_nome                    entrega_1_freq
entrega_1_canal                   entrega_1_para                    entrega_2_nome
entrega_2_freq                    entrega_2_canal                   entrega_2_para
entrega_3_nome                    entrega_3_freq                    entrega_3_canal
entrega_3_para                    entrega_4_nome                    entrega_4_freq
entrega_4_canal                   entrega_4_para                    entrega_5_nome
entrega_5_freq                    entrega_5_canal                   entrega_5_para
alcada_1_decisao                  alcada_1_propoe                   alcada_1_aprova
alcada_2_decisao                  alcada_2_propoe                   alcada_2_aprova
alcada_3_decisao                  alcada_3_propoe                   alcada_3_aprova
alcada_4_decisao                  alcada_4_propoe                   alcada_4_aprova
cadencia_1_encontro               cadencia_1_freq                   cadencia_2_encontro
cadencia_2_freq                   cadencia_3_encontro               cadencia_3_freq
cadencia_4_encontro               cadencia_4_freq                   texto_sobre_responsavel
plano_1_tag                       plano_1_nome                      plano_1_taxa
plano_1_base_calculo              plano_1_item_1                    plano_1_item_2
plano_1_item_3                    plano_1_item_4                    plano_1_item_5
plano_1_item_6                    plano_1_para_quem                 plano_2_tag
plano_2_nome                      plano_2_taxa                      plano_2_base_calculo
plano_2_item_1                    plano_2_item_2                    plano_2_item_3
plano_2_item_4                    plano_2_item_5                    plano_2_item_6
plano_2_para_quem                 plano_3_tag                       plano_3_nome
plano_3_taxa                      plano_3_base_calculo              plano_3_item_1
plano_3_item_2                    plano_3_item_3                    plano_3_item_4
plano_3_item_5                    plano_3_item_6                    plano_3_para_quem
nota_taxas                        pessoa_1_nome                     pessoa_1_cargo
pessoa_1_bio                      pessoa_2_nome                     pessoa_2_cargo
pessoa_2_bio                      pessoa_3_nome                     pessoa_3_cargo
pessoa_3_bio                      passo_1_detalhe                   passo_2_detalhe
passo_3_detalhe                   passo_4_detalhe                   requisito_1_titulo
requisito_1_detalhe               requisito_2_titulo                requisito_2_detalhe
requisito_3_titulo                requisito_3_detalhe               chamada_final
site                              endereco_escritorio
```
</details>

## Cronograma de reuniões

Arquivos: `modelos/cronograma-reunioes-alta-renda.html`, `modelos/cronograma-reunioes-assessoria.html`, `modelos/cronograma-reunioes-consultoria.html`, `modelos/cronograma-reunioes-private.html`

Segmentos: alta-renda, assessoria, consultoria, private &middot; 137 variáveis

<details><summary>Ver as 131 variáveis específicas deste documento</summary>

```
ano_vigencia                      data_emissao                      dur_1
fmt_1                             dur_2                             fmt_2
dur_3                             fmt_3                             dur_4
fmt_4                             time_principal_nome               time_principal_contato
time_principal_quando             time_backup_nome                  time_backup_contato
time_backup_quando                time_mesa_nome                    time_mesa_contato
time_mesa_quando                  time_ops_nome                     time_ops_contato
time_ops_quando                   antecedencia_pauta                prazo_resumo_pos_reuniao
antecedencia_confirmacao          cal_01_data                       cal_01_encontro
cal_01_pauta                      cal_01_entregavel                 cal_01_status
cal_02_data                       cal_02_encontro                   cal_02_pauta
cal_02_entregavel                 cal_02_status                     cal_03_data
cal_03_encontro                   cal_03_pauta                      cal_03_entregavel
cal_03_status                     cal_04_data                       cal_04_encontro
cal_04_pauta                      cal_04_entregavel                 cal_04_status
cal_05_data                       cal_05_encontro                   cal_05_pauta
cal_05_entregavel                 cal_05_status                     cal_06_data
cal_06_encontro                   cal_06_pauta                      cal_06_entregavel
cal_06_status                     cal_07_data                       cal_07_encontro
cal_07_pauta                      cal_07_entregavel                 cal_07_status
cal_08_data                       cal_08_encontro                   cal_08_pauta
cal_08_entregavel                 cal_08_status                     cal_09_data
cal_09_encontro                   cal_09_pauta                      cal_09_entregavel
cal_09_status                     cal_10_data                       cal_10_encontro
cal_10_pauta                      cal_10_entregavel                 cal_10_status
cal_11_data                       cal_11_encontro                   cal_11_pauta
cal_11_entregavel                 cal_11_status                     cal_12_data
cal_12_encontro                   cal_12_pauta                      cal_12_entregavel
cal_12_status                     prazo_inclusao_pauta              pauta_1
entrega_1                         pauta_2                           entrega_2
pauta_3                           entrega_3                         preparo_material
preparo_duvidas                   preparo_mudancas                  preparo_confirmacao
canal_whats_para                  canal_whats_horario               canal_whats_endereco
canal_email_para                  canal_email_horario               canal_email_endereco
canal_tel_para                    canal_tel_horario                 canal_tel_endereco
canal_portal_para                 canal_portal_horario              canal_portal_endereco
sla_1_tipo                        sla_1_resposta                    sla_1_execucao
sla_1_quem                        sla_2_tipo                        sla_2_resposta
sla_2_execucao                    sla_2_quem                        sla_3_tipo
sla_3_resposta                    sla_3_execucao                    sla_3_quem
sla_4_tipo                        sla_4_resposta                    sla_4_execucao
sla_4_quem                        procedimento_urgencia             texto_ouvidoria
antecedencia_remarcacao           regra_remarcacao_2                regra_remarcacao_3
texto_registro_decisoes           texto_revisao_cronograma
```
</details>

## Diagnóstico de carteira

Arquivos: `modelos/diagnostico-carteira-alta-renda.html`, `modelos/diagnostico-carteira-assessoria.html`, `modelos/diagnostico-carteira-consultoria.html`, `modelos/diagnostico-carteira-private.html`

Segmentos: alta-renda, assessoria, consultoria, private &middot; 319 variáveis

<details><summary>Ver as 309 variáveis específicas deste documento</summary>

```
patrimonio_analisado              data_diagnostico                  etapa_coleta
etapa_consolidacao                etapa_analise                     etapa_proposta
instituicoes_analisadas           data_corte                        documentos_base
ativos_fora_do_escopo             horizonte_principal               experiencia_investimentos
relacao_renda_despesa             reserva_emergencia                capacidade_aporte_mensal
liquidez_minima                   classes_vetadas                   situacao_tributaria
obrigacoes_futuras                outros_patrimonios                observacoes_perfil
obj_1_descricao                   obj_1_valor                       obj_1_prazo
obj_1_prioridade                  obj_1_situacao                    obj_2_descricao
obj_2_valor                       obj_2_prazo                       obj_2_prioridade
obj_2_situacao                    obj_3_descricao                   obj_3_valor
obj_3_prazo                       obj_3_prioridade                  obj_3_situacao
obj_4_descricao                   obj_4_valor                       obj_4_prazo
obj_4_prioridade                  obj_4_situacao                    qtd_ativos
qtd_instituicoes                  qtd_contas                        retorno_12m_atual
retorno_12m_pct_cdi               custo_total_anual                 custo_total_perc
at_1_classe                       at_1_instituicao                  at_1_valor
at_1_perc                         at_1_liquidez                     at_1_ret12m
at_1_custo                        at_2_classe                       at_2_instituicao
at_2_valor                        at_2_perc                         at_2_liquidez
at_2_ret12m                       at_2_custo                        at_3_classe
at_3_instituicao                  at_3_valor                        at_3_perc
at_3_liquidez                     at_3_ret12m                       at_3_custo
at_4_classe                       at_4_instituicao                  at_4_valor
at_4_perc                         at_4_liquidez                     at_4_ret12m
at_4_custo                        at_5_classe                       at_5_instituicao
at_5_valor                        at_5_perc                         at_5_liquidez
at_5_ret12m                       at_5_custo                        at_6_classe
at_6_instituicao                  at_6_valor                        at_6_perc
at_6_liquidez                     at_6_ret12m                       at_6_custo
at_7_classe                       at_7_instituicao                  at_7_valor
at_7_perc                         at_7_liquidez                     at_7_ret12m
at_7_custo                        forte_1_titulo                    forte_1_detalhe
forte_2_titulo                    forte_2_detalhe                   forte_3_titulo
forte_3_detalhe                   aten_1_gravidade                  aten_1_titulo
aten_1_motivo                     aten_1_impacto                    aten_1_acao
aten_2_gravidade                  aten_2_titulo                     aten_2_motivo
aten_2_impacto                    aten_2_acao                       aten_3_gravidade
aten_3_titulo                     aten_3_motivo                     aten_3_impacto
aten_3_acao                       aten_4_gravidade                  aten_4_titulo
aten_4_motivo                     aten_4_impacto                    aten_4_acao
aten_5_gravidade                  aten_5_titulo                     aten_5_motivo
aten_5_impacto                    aten_5_acao                       resumo_diagnostico
emis_1_nome                       emis_1_valor                      emis_1_perc
emis_1_rating                     emis_1_fgc                        emis_1_limite
emis_2_nome                       emis_2_valor                      emis_2_perc
emis_2_rating                     emis_2_fgc                        emis_2_limite
emis_3_nome                       emis_3_valor                      emis_3_perc
emis_3_rating                     emis_3_fgc                        emis_3_limite
emis_4_nome                       emis_4_valor                      emis_4_perc
emis_4_rating                     emis_4_fgc                        emis_4_limite
emis_5_nome                       emis_5_valor                      emis_5_perc
emis_5_rating                     emis_5_fgc                        emis_5_limite
prazo_1a_valor                    prazo_1a_perc                     prazo_3a_valor
prazo_3a_perc                     prazo_5a_valor                    prazo_5a_perc
prazo_5mais_valor                 prazo_5mais_perc                  moeda_brl_valor
moeda_brl_perc                    moeda_usd_valor                   moeda_usd_perc
moeda_eur_valor                   moeda_eur_perc                    moeda_out_valor
moeda_out_perc                    texto_cobertura_fgc               custo_1_origem
custo_1_onde                      custo_1_perc                      custo_1_reais
custo_1_contrapartida             custo_1_recuperavel               custo_2_origem
custo_2_onde                      custo_2_perc                      custo_2_reais
custo_2_contrapartida             custo_2_recuperavel               custo_3_origem
custo_3_onde                      custo_3_perc                      custo_3_reais
custo_3_contrapartida             custo_3_recuperavel               custo_4_origem
custo_4_onde                      custo_4_perc                      custo_4_reais
custo_4_contrapartida             custo_4_recuperavel               custo_5_origem
custo_5_onde                      custo_5_perc                      custo_5_reais
custo_5_contrapartida             custo_5_recuperavel               custo_recuperavel_total
trib_comecotas_diag               trib_comecotas_op                 trib_isentos_diag
trib_isentos_op                   trib_prejuizo_diag                trib_prejuizo_op
trib_prazo_diag                   trib_prazo_op                     custo_proposto_anual
custo_proposto_perc               economia_estimada_ano             economia_estimada_10a
prop_caixa_hoje                   prop_caixa_novo                   prop_caixa_var
prop_caixa_instrumento            prop_caixa_motivo                 prop_rfpos_hoje
prop_rfpos_novo                   prop_rfpos_var                    prop_rfpos_instrumento
prop_rfpos_motivo                 prop_rfipca_hoje                  prop_rfipca_novo
prop_rfipca_var                   prop_rfipca_instrumento           prop_rfipca_motivo
prop_rfpre_hoje                   prop_rfpre_novo                   prop_rfpre_var
prop_rfpre_instrumento            prop_rfpre_motivo                 prop_multi_hoje
prop_multi_novo                   prop_multi_var                    prop_multi_instrumento
prop_multi_motivo                 prop_rvbr_hoje                    prop_rvbr_novo
prop_rvbr_var                     prop_rvbr_instrumento             prop_rvbr_motivo
prop_intl_hoje                    prop_intl_novo                    prop_intl_var
prop_intl_instrumento             prop_intl_motivo                  prop_alt_hoje
prop_alt_novo                     prop_alt_var                      prop_alt_instrumento
prop_alt_motivo                   texto_o_que_muda                  retorno_esperado_proposta
risco_esperado_proposta           transicao_1_titulo                transicao_1_detalhe
transicao_2_titulo                transicao_2_detalhe               transicao_3_titulo
transicao_3_detalhe               transicao_4_titulo                transicao_4_detalhe
tr_1_quando                       tr_1_movimento                    tr_1_ativo
tr_1_valor                        tr_1_custo                        tr_1_destino
tr_2_quando                       tr_2_movimento                    tr_2_ativo
tr_2_valor                        tr_2_custo                        tr_2_destino
tr_3_quando                       tr_3_movimento                    tr_3_ativo
tr_3_valor                        tr_3_custo                        tr_3_destino
tr_4_quando                       tr_4_movimento                    tr_4_ativo
tr_4_valor                        tr_4_custo                        tr_4_destino
tr_5_quando                       tr_5_movimento                    tr_5_ativo
tr_5_valor                        tr_5_custo                        tr_5_destino
restricao_carencia                restricao_imposto                 restricao_marcacao
premissa_retornos                 premissa_risco                    premissa_macro
premissa_tributacao               premissa_custos                   limitacoes_diagnostico
```
</details>

## Relatório macroeconômico

Arquivos: `modelos/relatorio-macroeconomico-alta-renda.html`, `modelos/relatorio-macroeconomico-assessoria.html`, `modelos/relatorio-macroeconomico-consultoria.html`, `modelos/relatorio-macroeconomico-private.html`

Segmentos: alta-renda, assessoria, consultoria, private &middot; 306 variáveis

<details><summary>Ver as 300 variáveis específicas deste documento</summary>

```
nome_analista                     registro_analista                 tese_central
fato_1_titulo                     fato_1_detalhe                    fato_2_titulo
fato_2_detalhe                    fato_3_titulo                     fato_3_detalhe
fato_4_titulo                     fato_4_detalhe                    fato_5_titulo
fato_5_detalhe                    mudanca_de_visao                  resumo_internacional
analise_eua                       analise_europa                    analise_china
gi_fed_atual                      gi_fed_ant                        gi_fed_cons
gi_fed_leitura                    gi_cpi_atual                      gi_cpi_ant
gi_cpi_cons                       gi_cpi_leitura                    gi_payroll_atual
gi_payroll_ant                    gi_payroll_cons                   gi_payroll_leitura
gi_ust10_atual                    gi_ust10_ant                      gi_ust10_cons
gi_ust10_leitura                  gi_bce_atual                      gi_bce_ant
gi_bce_cons                       gi_bce_leitura                    gi_pibchina_atual
gi_pibchina_ant                   gi_pibchina_cons                  gi_pibchina_leitura
gi_brent_atual                    gi_brent_ant                      gi_brent_cons
gi_brent_leitura                  gi_dxy_atual                      gi_dxy_ant
gi_dxy_cons                       gi_dxy_leitura                    resumo_brasil_atividade
analise_atividade                 analise_trabalho                  analise_inflacao
bi_ipca_mes                       bi_ipca_12m                       bi_ipca_proj
bi_ipca_meta                      bi_nucleo_mes                     bi_nucleo_12m
bi_nucleo_proj                    bi_nucleo_meta                    bi_igpm_mes
bi_igpm_12m                       bi_igpm_proj                      bi_igpm_meta
bi_pib_mes                        bi_pib_12m                        bi_pib_proj
bi_pib_meta                       bi_desemp_mes                     bi_desemp_12m
bi_desemp_proj                    bi_desemp_meta                    bi_massa_mes
bi_massa_12m                      bi_massa_proj                     bi_massa_meta
analise_politica_monetaria        selic_atual                       decisao_copom
placar_copom                      data_proximo_copom                analise_curva_juros
analise_fiscal                    fi_primario_ult                   fi_primario_12m
fi_primario_proj                  fi_dbgg_ult                       fi_dbgg_12m
fi_dbgg_proj                      fi_cambio_ult                     fi_cambio_12m
fi_cambio_proj                    fi_cc_ult                         fi_cc_12m
fi_cc_proj                        analise_cambio                    fonte_dados_mercado
mk_cdi_mes                        mk_cdi_ano                        mk_cdi_12m
mk_cdi_24m                        mk_cdi_vol                        mk_imab_mes
mk_imab_ano                       mk_imab_12m                       mk_imab_24m
mk_imab_vol                       mk_irfm_mes                       mk_irfm_ano
mk_irfm_12m                       mk_irfm_24m                       mk_irfm_vol
mk_ibov_mes                       mk_ibov_ano                       mk_ibov_12m
mk_ibov_24m                       mk_ibov_vol                       mk_small_mes
mk_small_ano                      mk_small_12m                      mk_small_24m
mk_small_vol                      mk_ifix_mes                       mk_ifix_ano
mk_ifix_12m                       mk_ifix_24m                       mk_ifix_vol
mk_spx_mes                        mk_spx_ano                        mk_spx_12m
mk_spx_24m                        mk_spx_vol                        mk_ndx_mes
mk_ndx_ano                        mk_ndx_12m                        mk_ndx_24m
mk_ndx_vol                        mk_msciem_mes                     mk_msciem_ano
mk_msciem_12m                     mk_msciem_24m                     mk_msciem_vol
mk_usd_mes                        mk_usd_ano                        mk_usd_12m
mk_usd_24m                        mk_usd_vol                        mk_gold_mes
mk_gold_ano                       mk_gold_12m                       mk_gold_24m
mk_gold_vol                       mk_btc_mes                        mk_btc_ano
mk_btc_12m                        mk_btc_24m                        mk_btc_vol
destaques_positivos               destaques_negativos               ano_corrente
ano_seguinte                      pj_ipca_a1                        pj_ipca_a2
pj_ipca_c1                        pj_ipca_c2                        pj_selic_a1
pj_selic_a2                       pj_selic_c1                       pj_selic_c2
pj_pib_a1                         pj_pib_a2                         pj_pib_c1
pj_pib_c2                         pj_cambio_a1                      pj_cambio_a2
pj_cambio_c1                      pj_cambio_c2                      pj_primario_a1
pj_primario_a2                    pj_primario_c1                    pj_primario_c2
pg_fed_a1                         pg_fed_a2                         pg_fed_vies
pg_cpi_a1                         pg_cpi_a2                         pg_cpi_vies
pg_pibeua_a1                      pg_pibeua_a2                      pg_pibeua_vies
pg_pibchina_a1                    pg_pibchina_a2                    pg_pibchina_vies
divergencia_1_titulo              divergencia_1_racional            divergencia_2_titulo
divergencia_2_racional            divergencia_3_titulo              divergencia_3_racional
vis_rfpos_visao                   vis_rfpos_delta                   vis_rfpos_racional
vis_rfpos_como                    vis_rfipca_visao                  vis_rfipca_delta
vis_rfipca_racional               vis_rfipca_como                   vis_rfpre_visao
vis_rfpre_delta                   vis_rfpre_racional                vis_rfpre_como
vis_multi_visao                   vis_multi_delta                   vis_multi_racional
vis_multi_como                    vis_rvbr_visao                    vis_rvbr_delta
vis_rvbr_racional                 vis_rvbr_como                     vis_intl_visao
vis_intl_delta                    vis_intl_racional                 vis_intl_como
vis_fii_visao                     vis_fii_delta                     vis_fii_racional
vis_fii_como                      vis_alt_visao                     vis_alt_delta
vis_alt_racional                  vis_alt_como                      risco_1_nome
risco_1_prob                      risco_1_impacto                   risco_1_gatilho
risco_1_acao                      risco_2_nome                      risco_2_prob
risco_2_impacto                   risco_2_gatilho                   risco_2_acao
risco_3_nome                      risco_3_prob                      risco_3_impacto
risco_3_gatilho                   risco_3_acao                      sintese_posicionamento
mes_seguinte                      ag_1_data                         ag_1_evento
ag_1_pais                         ag_1_relevancia                   ag_1_motivo
ag_2_data                         ag_2_evento                       ag_2_pais
ag_2_relevancia                   ag_2_motivo                       ag_3_data
ag_3_evento                       ag_3_pais                         ag_3_relevancia
ag_3_motivo                       ag_4_data                         ag_4_evento
ag_4_pais                         ag_4_relevancia                   ag_4_motivo
ag_5_data                         ag_5_evento                       ag_5_pais
ag_5_relevancia                   ag_5_motivo                       ag_6_data
ag_6_evento                       ag_6_pais                         ag_6_relevancia
ag_6_motivo                       ag_7_data                         ag_7_evento
ag_7_pais                         ag_7_relevancia                   ag_7_motivo
ag_8_data                         ag_8_evento                       ag_8_pais
ag_8_relevancia                   ag_8_motivo                       observar_1_titulo
observar_1_detalhe                observar_2_titulo                 observar_2_detalhe
observar_3_titulo                 observar_3_detalhe                fonte_dados_macro
fonte_consenso                    data_fechamento                   declaracao_analista
```
</details>

## Relatório mensal

Arquivos: `modelos/relatorio-mensal-alta-renda.html`, `modelos/relatorio-mensal-assessoria.html`, `modelos/relatorio-mensal-consultoria.html`, `modelos/relatorio-mensal-private.html`

Segmentos: alta-renda, assessoria, consultoria, private &middot; 336 variáveis

<details><summary>Ver as 323 variáveis específicas deste documento</summary>

```
carta_paragrafo_1                 carta_paragrafo_2                 carta_paragrafo_3
telefone_contato                  rent_mes                          rent_mes_pct_cdi
rent_ano                          rent_ano_pct_cdi                  aporte_liquido_mes
resgates_mes                      rent_12m                          rent_24m
rent_inicio                       cdi_mes                           cdi_ano
cdi_12m                           cdi_24m                           cdi_inicio
ipca5_mes                         ipca5_ano                         ipca5_12m
ipca5_24m                         ipca5_inicio                      ibov_mes
ibov_ano                          ibov_12m                          ibov_24m
ibov_inicio                       vs_cdi_mes                        vs_cdi_ano
vs_cdi_12m                        vs_cdi_24m                        vs_cdi_inicio
alvo_rf_pos                       atual_rf_pos                      desvio_rf_pos
valor_rf_pos                      status_rf_pos                     alvo_rf_pre
atual_rf_pre                      desvio_rf_pre                     valor_rf_pre
status_rf_pre                     alvo_rf_ipca                      atual_rf_ipca
desvio_rf_ipca                    valor_rf_ipca                     status_rf_ipca
alvo_multi                        atual_multi                       desvio_multi
valor_multi                       status_multi                      alvo_rv_br
atual_rv_br                       desvio_rv_br                      valor_rv_br
status_rv_br                      alvo_intl                         atual_intl
desvio_intl                       valor_intl                        status_intl
alvo_fii                          atual_fii                         desvio_fii
valor_fii                         status_fii                        alvo_alt
atual_alt                         desvio_alt                        valor_alt
status_alt                        alvo_caixa                        atual_caixa
desvio_caixa                      valor_caixa                       status_caixa
texto_desvio_alocacao             texto_alocacao_em_linha           texto_alocacao_ajuste
d_rf_valor                        d_rf_peso                         d_rf_ret
d_rf_contrib                      d_rf_ret12m                       d_multi_valor
d_multi_peso                      d_multi_ret                       d_multi_contrib
d_multi_ret12m                    d_rvbr_valor                      d_rvbr_peso
d_rvbr_ret                        d_rvbr_contrib                    d_rvbr_ret12m
d_intl_valor                      d_intl_peso                       d_intl_ret
d_intl_contrib                    d_intl_ret12m                     d_fii_valor
d_fii_peso                        d_fii_ret                         d_fii_contrib
d_fii_ret12m                      d_alt_valor                       d_alt_peso
d_alt_ret                         d_alt_contrib                     d_alt_ret12m
d_caixa_valor                     d_caixa_peso                      d_caixa_ret
d_caixa_contrib                   d_caixa_ret12m                    top_1_ativo
top_1_ret                         top_1_contrib                     top_2_ativo
top_2_ret                         top_2_contrib                     top_3_ativo
top_3_ret                         top_3_contrib                     top_4_ativo
top_4_ret                         top_4_contrib                     bot_1_ativo
bot_1_ret                         bot_1_contrib                     bot_2_ativo
bot_2_ret                         bot_2_contrib                     bot_3_ativo
bot_3_ret                         bot_3_contrib                     bot_4_ativo
bot_4_ret                         bot_4_contrib                     data_inicio_periodo
data_fim_periodo                  mov_1_data                        mov_1_tipo
mov_1_ativo                       mov_1_classe                      mov_1_valor
mov_1_motivo                      mov_2_data                        mov_2_tipo
mov_2_ativo                       mov_2_classe                      mov_2_valor
mov_2_motivo                      mov_3_data                        mov_3_tipo
mov_3_ativo                       mov_3_classe                      mov_3_valor
mov_3_motivo                      mov_4_data                        mov_4_tipo
mov_4_ativo                       mov_4_classe                      mov_4_valor
mov_4_motivo                      mov_5_data                        mov_5_tipo
mov_5_ativo                       mov_5_classe                      mov_5_valor
mov_5_motivo                      mov_6_data                        mov_6_tipo
mov_6_ativo                       mov_6_classe                      mov_6_valor
mov_6_motivo                      prov_1_data                       prov_1_origem
prov_1_tipo                       prov_1_bruto                      prov_1_ir
prov_1_liquido                    prov_2_data                       prov_2_origem
prov_2_tipo                       prov_2_bruto                      prov_2_ir
prov_2_liquido                    prov_3_data                       prov_3_origem
prov_3_tipo                       prov_3_bruto                      prov_3_ir
prov_3_liquido                    total_aportes                     total_resgates
total_proventos                   total_custos                      custo_perc_patrimonio
oferta_1_nome                     oferta_1_classe                   oferta_1_emissor
oferta_1_taxa                     oferta_1_prazo                    oferta_1_ticket
oferta_1_janela                   oferta_2_nome                     oferta_2_classe
oferta_2_emissor                  oferta_2_taxa                     oferta_2_prazo
oferta_2_ticket                   oferta_2_janela                   oferta_3_nome
oferta_3_classe                   oferta_3_emissor                  oferta_3_taxa
oferta_3_prazo                    oferta_3_ticket                   oferta_3_janela
oferta_4_nome                     oferta_4_classe                   oferta_4_emissor
oferta_4_taxa                     oferta_4_prazo                    oferta_4_ticket
oferta_4_janela                   oportunidade_1_titulo             oportunidade_1_racional
oportunidade_2_titulo             oportunidade_2_racional           oportunidade_3_titulo
oportunidade_3_racional           texto_suitability_oferta          cenario_brasil
cenario_internacional             m_cdi_fech                        m_cdi_mes
m_cdi_ano                         m_cdi_12m                         m_ipca_fech
m_ipca_mes                        m_ipca_ano                        m_ipca_12m
m_selic_fech                      m_selic_mes                       m_selic_ano
m_selic_12m                       m_ibov_fech                       m_ibov_mes
m_ibov_ano                        m_ibov_12m                        m_spx_fech
m_spx_mes                         m_spx_ano                         m_spx_12m
m_usd_fech                        m_usd_mes                         m_usd_ano
m_usd_12m                         m_gold_fech                       m_gold_mes
m_gold_ano                        m_gold_12m                        m_ifix_fech
m_ifix_mes                        m_ifix_ano                        m_ifix_12m
m_imab_fech                       m_imab_mes                        m_imab_ano
m_imab_12m                        pos_rfpos_visao                   pos_rfpos_mov
pos_rfpos_racional                pos_rfipca_visao                  pos_rfipca_mov
pos_rfipca_racional               pos_rvbr_visao                    pos_rvbr_mov
pos_rvbr_racional                 pos_intl_visao                    pos_intl_mov
pos_intl_racional                 pos_alt_visao                     pos_alt_mov
pos_alt_racional                  acao_1_prioridade                 acao_1_descricao
acao_1_classe                     acao_1_valor                      acao_1_prazo
acao_2_prioridade                 acao_2_descricao                  acao_2_classe
acao_2_valor                      acao_2_prazo                      acao_3_prioridade
acao_3_descricao                  acao_3_classe                     acao_3_valor
acao_3_prazo                      acao_4_prioridade                 acao_4_descricao
acao_4_classe                     acao_4_valor                      acao_4_prazo
pendencia_1_titulo                pendencia_1_detalhe               pendencia_2_titulo
pendencia_2_detalhe               pendencia_3_titulo                pendencia_3_detalhe
data_proxima_reuniao              formato_reuniao                   pauta_proxima_reuniao
fonte_dados                       metodo_rentabilidade              metodo_fluxo_caixa
contas_consideradas               data_ptax
```
</details>

Campos exclusivos da variante **assessoria** (45):

```
rf_1_indexador                    rf_1_perc                         rf_1_prazo
rf_1_taxa                         rf_1_valor                        rf_2_indexador
rf_2_perc                         rf_2_prazo                        rf_2_taxa
rf_2_valor                        rf_3_indexador                    rf_3_perc
rf_3_prazo                        rf_3_taxa                         rf_3_valor
rf_4_indexador                    rf_4_perc                         rf_4_prazo
rf_4_taxa                         rf_4_valor                        texto_concentracao_fgc
venc_1_ativo                      venc_1_data                       venc_1_destino
venc_1_emissor                    venc_1_indexador                  venc_1_valor
venc_2_ativo                      venc_2_data                       venc_2_destino
venc_2_emissor                    venc_2_indexador                  venc_2_valor
venc_3_ativo                      venc_3_data                       venc_3_destino
venc_3_emissor                    venc_3_indexador                  venc_3_valor
venc_4_ativo                      venc_4_data                       venc_4_destino
venc_4_emissor                    venc_4_indexador                  venc_4_valor
```

Campos exclusivos da variante **consultoria** (45):

```
rf_1_indexador                    rf_1_perc                         rf_1_prazo
rf_1_taxa                         rf_1_valor                        rf_2_indexador
rf_2_perc                         rf_2_prazo                        rf_2_taxa
rf_2_valor                        rf_3_indexador                    rf_3_perc
rf_3_prazo                        rf_3_taxa                         rf_3_valor
rf_4_indexador                    rf_4_perc                         rf_4_prazo
rf_4_taxa                         rf_4_valor                        texto_concentracao_fgc
venc_1_ativo                      venc_1_data                       venc_1_destino
venc_1_emissor                    venc_1_indexador                  venc_1_valor
venc_2_ativo                      venc_2_data                       venc_2_destino
venc_2_emissor                    venc_2_indexador                  venc_2_valor
venc_3_ativo                      venc_3_data                       venc_3_destino
venc_3_emissor                    venc_3_indexador                  venc_3_valor
venc_4_ativo                      venc_4_data                       venc_4_destino
venc_4_emissor                    venc_4_indexador                  venc_4_valor
```

Campos exclusivos da variante **private** (36):

```
estrutura_1_finalidade            estrutura_1_nome                  estrutura_1_revisao
estrutura_1_status                estrutura_1_tipo                  estrutura_2_finalidade
estrutura_2_nome                  estrutura_2_revisao               estrutura_2_status
estrutura_2_tipo                  estrutura_3_finalidade            estrutura_3_nome
estrutura_3_revisao               estrutura_3_status                estrutura_3_tipo
intl_1_jurisdicao                 intl_1_moeda                      intl_1_perc
intl_1_ret12m                     intl_1_saldo                      intl_1_veiculo
intl_2_jurisdicao                 intl_2_moeda                      intl_2_perc
intl_2_ret12m                     intl_2_saldo                      intl_2_veiculo
intl_3_jurisdicao                 intl_3_moeda                      intl_3_perc
intl_3_ret12m                     intl_3_saldo                      intl_3_veiculo
nota_holding                      nota_seguros                      nota_sucessao
```

## Relatório mensal em formato de apresentação

Arquivos: `modelos/relatorio-mensal-apresentacao-alta-renda.html`, `modelos/relatorio-mensal-apresentacao-assessoria.html`, `modelos/relatorio-mensal-apresentacao-consultoria.html`, `modelos/relatorio-mensal-apresentacao-private.html`

Segmentos: alta-renda, assessoria, consultoria, private &middot; 193 variáveis

<details><summary>Ver as 180 variáveis específicas deste documento</summary>

```
duracao_reuniao                   rent_mes                          rent_mes_pct_cdi
rent_ano                          rent_ano_pct_cdi                  aporte_liquido_mes
resgates_mes                      resumo_do_mes                     ponto_de_atencao_mes
rent_12m                          rent_24m                          cdi_mes
cdi_ano                           cdi_12m                           cdi_24m
ipca5_mes                         ipca5_ano                         ipca5_12m
ipca5_24m                         ibov_mes                          ibov_ano
ibov_12m                          ibov_24m                          vs_cdi_mes
vs_cdi_ano                        vs_cdi_12m                        vs_cdi_24m
alvo_rf_pos                       atual_rf_pos                      desvio_rf_pos
alvo_rf_ipca                      atual_rf_ipca                     desvio_rf_ipca
alvo_rf_pre                       atual_rf_pre                      desvio_rf_pre
alvo_multi                        atual_multi                       desvio_multi
alvo_rv_br                        atual_rv_br                       desvio_rv_br
alvo_intl                         atual_intl                        desvio_intl
alvo_fii                          atual_fii                         desvio_fii
alvo_alt                          atual_alt                         desvio_alt
alvo_caixa                        atual_caixa                       desvio_caixa
texto_rebalanceamento             top_1_ativo                       top_1_ret
top_1_contrib                     top_2_ativo                       top_2_ret
top_2_contrib                     top_3_ativo                       top_3_ret
top_3_contrib                     top_4_ativo                       top_4_ret
top_4_contrib                     comentario_destaques              bot_1_ativo
bot_1_ret                         bot_1_contrib                     bot_2_ativo
bot_2_ret                         bot_2_contrib                     bot_3_ativo
bot_3_ret                         bot_3_contrib                     bot_4_ativo
bot_4_ret                         bot_4_contrib                     comentario_detratores
mov_1_data                        mov_1_tipo                        mov_1_ativo
mov_1_classe                      mov_1_valor                       mov_1_motivo
mov_2_data                        mov_2_tipo                        mov_2_ativo
mov_2_classe                      mov_2_valor                       mov_2_motivo
mov_3_data                        mov_3_tipo                        mov_3_ativo
mov_3_classe                      mov_3_valor                       mov_3_motivo
mov_4_data                        mov_4_tipo                        mov_4_ativo
mov_4_classe                      mov_4_valor                       mov_4_motivo
mov_5_data                        mov_5_tipo                        mov_5_ativo
mov_5_classe                      mov_5_valor                       mov_5_motivo
total_aportes                     total_resgates                    total_proventos
total_custos                      custo_perc_patrimonio             seg_1_item
seg_1_detalhe                     seg_1_valor                       seg_1_perc
seg_1_obs                         seg_2_item                        seg_2_detalhe
seg_2_valor                       seg_2_perc                        seg_2_obs
seg_3_item                        seg_3_detalhe                     seg_3_valor
seg_3_perc                        seg_3_obs                         seg_4_item
seg_4_detalhe                     seg_4_valor                       seg_4_perc
seg_4_obs                         seg_5_item                        seg_5_detalhe
seg_5_valor                       seg_5_perc                        seg_5_obs
cenario_brasil                    cenario_internacional             pos_rfpos_visao
pos_rfpos_mov                     pos_rfpos_racional                pos_rfipca_visao
pos_rfipca_mov                    pos_rfipca_racional               pos_rvbr_visao
pos_rvbr_mov                      pos_rvbr_racional                 pos_intl_visao
pos_intl_mov                      pos_intl_racional                 pos_alt_visao
pos_alt_mov                       pos_alt_racional                  acao_1_prioridade
acao_1_descricao                  acao_1_prazo                      acao_2_prioridade
acao_2_descricao                  acao_2_prazo                      acao_3_prioridade
acao_3_descricao                  acao_3_prazo                      acao_4_prioridade
acao_4_descricao                  acao_4_prazo                      pendencia_1_titulo
pendencia_1_detalhe               pendencia_2_titulo                pendencia_2_detalhe
data_proxima_reuniao              formato_reuniao                   mensagem_encerramento
fonte_dados                       metodo_rentabilidade              contas_consideradas
```
</details>

