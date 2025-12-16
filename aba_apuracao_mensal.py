"""
================================================================================
ABA: ICMS/IPI APURADO - ANÁLISE COMPLETA
================================================================================

Módulo para exibir apuração completa de ICMS com base nos registros E.

Baseado nos registros:
- E100: Período da Apuração
- E110: Apuração do ICMS (totais)
- E111: Ajustes da Apuração
- E116: Obrigações ICMS Recolhido/A Recolher (guias)

Data de Criação: 16/12/2025
Atualização: 16/12/2025 - Implementação completa com registros E

================================================================================
GATILHOS DE MANUTENÇÃO:
================================================================================

1. ADICIONAR NOVOS CAMPOS E110:
   - Editar função exibir_totais_apuracao()
   - Adicionar métrica

2. ADICIONAR NOVOS TIPOS DE AJUSTE:
   - Editar função exibir_ajustes()
   - Adicionar filtro ou classificação

3. ADICIONAR NOVOS CÓDIGOS DE OBRIGAÇÃO:
   - Editar função exibir_guias_recolhimento()
   - Adicionar mapeamento de código

================================================================================
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Dict


def formatar_moeda_br(valor):
    """
    Formata valor para padrão brasileiro: R$ 1.234,56
    
    GATILHO DE MANUTENÇÃO:
    - Sempre usar este formato em todo o sistema
    - Ponto para milhar, vírgula para decimal
    """
    if pd.isna(valor) or valor == 0:
        return 'R$ 0,00'
    return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def formatar_data_br(data_str):
    """
    Formata data de DDMMAAAA para DD/MM/AAAA
    
    GATILHO DE MANUTENÇÃO:
    - Formato entrada: DDMMAAAA (ex: 01052025)
    - Formato saída: DD/MM/AAAA (ex: 01/05/2025)
    """
    if not data_str or len(str(data_str)) < 8:
        return ''
    
    data_str = str(data_str)
    dd = data_str[0:2]
    mm = data_str[2:4]
    aaaa = data_str[4:8]
    
    return f"{dd}/{mm}/{aaaa}"


def extrair_mes_de_data(data_str):
    """
    Extrai nome do mês de uma data DDMMAAAA.
    
    GATILHO DE MANUTENÇÃO:
    - Formato: DDMMAAAA (ex: 01052025 = 01/Maio/2025)
    - Posições 2-3 contêm o mês
    """
    if not data_str or len(str(data_str)) < 6:
        return 'Indefinido'
    
    meses_dict = {
        '01': 'Janeiro', '02': 'Fevereiro', '03': 'Março',
        '04': 'Abril', '05': 'Maio', '06': 'Junho',
        '07': 'Julho', '08': 'Agosto', '09': 'Setembro',
        '10': 'Outubro', '11': 'Novembro', '12': 'Dezembro'
    }
    
    # Extrai MM de DDMMAAAA (posições 2-3)
    mes_num = str(data_str)[2:4]
    return meses_dict.get(mes_num, 'Indefinido')


def mapear_codigo_obrigacao(cod_or):
    """
    Mapeia código de obrigação para descrição.
    
    GATILHO DE MANUTENÇÃO:
    - Adicionar novos códigos conforme necessário
    """
    mapeamento = {
        '000': 'ICMS Normal',
        '001': 'ICMS ST',
        '002': 'ICMS Antecipado',
        '003': 'ICMS Diferencial de Alíquota',
        '004': 'ICMS Substituição Tributária',
        '005': 'ICMS Importação',
        '006': 'FECP (Fundo Estadual de Combate à Pobreza)',
        '007': 'FECP ST',
        '008': 'ICMS Complementar',
        '009': 'ICMS Outros'
    }
    
    return mapeamento.get(cod_or, f'Código {cod_or}')


def exibir_totais_apuracao(df_e110: pd.DataFrame):
    """
    Exibe totais da apuração de ICMS (E110).
    
    GATILHO DE MANUTENÇÃO:
    - Para adicionar campos, incluir nova métrica
    """
    if df_e110.empty:
        st.info('Nenhum registro E110 (Apuração de ICMS) encontrado.')
        return
    
    st.subheader('📊 Totais da Apuração de ICMS')
    
    # Pega primeira linha (geralmente há apenas uma por período)
    apuracao = df_e110.iloc[0]
    
    # Linha 1: Débitos e Créditos
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            'Total de Débitos',
            formatar_moeda_br(apuracao.get('VL_TOT_DEBITOS', 0)),
            help='Valor total dos débitos de ICMS'
        )
    
    with col2:
        st.metric(
            'Ajustes a Débito',
            formatar_moeda_br(apuracao.get('VL_AJ_DEBITOS', 0)),
            help='Ajustes que aumentam o débito'
        )
    
    with col3:
        st.metric(
            'Total de Créditos',
            formatar_moeda_br(apuracao.get('VL_TOT_CREDITOS', 0)),
            help='Valor total dos créditos de ICMS'
        )
    
    with col4:
        st.metric(
            'Ajustes a Crédito',
            formatar_moeda_br(apuracao.get('VL_AJ_CREDITOS', 0)),
            help='Ajustes que aumentam o crédito'
        )
    
    st.markdown('<br>', unsafe_allow_html=True)
    
    # Linha 2: Saldos e Valores a Recolher
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            'Saldo Credor Anterior',
            formatar_moeda_br(apuracao.get('VL_SLD_CREDOR_ANT', 0)),
            help='Saldo credor do período anterior'
        )
    
    with col2:
        st.metric(
            'Saldo Apurado',
            formatar_moeda_br(apuracao.get('VL_SLD_APURADO', 0)),
            help='Saldo apurado no período (débitos - créditos)'
        )
    
    with col3:
        st.metric(
            'Deduções',
            formatar_moeda_br(apuracao.get('VL_TOT_DED', 0)),
            help='Total de deduções'
        )
    
    with col4:
        st.metric(
            '💰 ICMS a Recolher',
            formatar_moeda_br(apuracao.get('VL_ICMS_RECOLHER', 0)),
            help='Valor do ICMS a recolher',
            delta_color='inverse'
        )
    
    st.markdown('---')


def exibir_ajustes(df_e111: pd.DataFrame):
    """
    Exibe ajustes da apuração (E111).
    
    GATILHO DE MANUTENÇÃO:
    - Para adicionar filtros, incluir selectbox ou multiselect
    """
    if df_e111.empty:
        return
    
    st.subheader('⚙️ Ajustes da Apuração')
    
    # Estatísticas dos ajustes
    total_ajustes = df_e111['VL_AJ_APUR'].sum()
    qtd_ajustes = len(df_e111)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Quantidade de Ajustes', qtd_ajustes)
    with col2:
        st.metric('Total dos Ajustes', formatar_moeda_br(total_ajustes))
    
    st.markdown('<br>', unsafe_allow_html=True)
    
    # Tabela de ajustes
    df_exibicao = df_e111.copy()
    df_exibicao['Código'] = df_exibicao['COD_AJ_APUR']
    df_exibicao['Descrição'] = df_exibicao['DESCR_COMPL_AJ']
    df_exibicao['Valor'] = df_exibicao['VL_AJ_APUR'].apply(formatar_moeda_br)
    
    st.dataframe(
        df_exibicao[['Código', 'Descrição', 'Valor']],
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown('---')


def exibir_guias_recolhimento(df_e116: pd.DataFrame):
    """
    Exibe guias de recolhimento (E116).
    
    GATILHO DE MANUTENÇÃO:
    - Para adicionar colunas, incluir no DataFrame de exibição
    """
    if df_e116.empty:
        return
    
    st.subheader('📄 Guias de Recolhimento (ICMS Recolhido/A Recolher)')
    
    # Estatísticas das guias
    total_guias = df_e116['VL_OR'].sum()
    qtd_guias = len(df_e116)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Quantidade de Guias', qtd_guias)
    with col2:
        st.metric('Total a Recolher', formatar_moeda_br(total_guias))
    
    st.markdown('<br>', unsafe_allow_html=True)
    
    # Tabela de guias
    df_exibicao = df_e116.copy()
    df_exibicao['Tipo'] = df_exibicao['COD_OR'].apply(mapear_codigo_obrigacao)
    df_exibicao['Valor'] = df_exibicao['VL_OR'].apply(formatar_moeda_br)
    df_exibicao['Vencimento'] = df_exibicao['DT_VCTO'].apply(formatar_data_br)
    df_exibicao['Cód. Receita'] = df_exibicao['COD_REC']
    df_exibicao['Descrição'] = df_exibicao['TXT_COMPL']
    df_exibicao['Referência'] = df_exibicao['MES_REF']
    
    st.dataframe(
        df_exibicao[['Tipo', 'Valor', 'Vencimento', 'Cód. Receita', 'Descrição', 'Referência']],
        use_container_width=True,
        hide_index=True
    )
    
    # Download CSV
    csv = df_e116.to_csv(index=False, encoding='utf-8-sig', sep=';', decimal=',')
    st.download_button(
        label='📥 Baixar Guias (CSV)',
        data=csv,
        file_name='guias_icms_e116.csv',
        mime='text/csv'
    )
    
    st.markdown('---')


def exibir_aba_apuracao_mensal(dados_e: Dict[str, pd.DataFrame]):
    """
    Exibe a aba de ICMS/IPI Apurado com dados completos.
    
    Parâmetros:
        dados_e: Dicionário com DataFrames dos registros E
    
    GATILHO DE MANUTENÇÃO:
    - Esta é a função principal chamada pelo app.py
    - Para adicionar seções, adicionar st.subheader() e conteúdo
    """
    st.header('💰 ICMS/IPI Apurado')
    st.markdown('**Apuração Completa de ICMS (Registros E100, E110, E111, E116)**')
    
    # Extrai DataFrames
    df_e100 = dados_e.get('E100', pd.DataFrame())
    df_e110 = dados_e.get('E110', pd.DataFrame())
    df_e111 = dados_e.get('E111', pd.DataFrame())
    df_e116 = dados_e.get('E116', pd.DataFrame())
    
    # Verifica se há dados
    if df_e110.empty and df_e116.empty:
        st.info('📊 Análise de ICMS/IPI Apurado')
        st.warning('⚠️ Registros de apuração (E110, E116) não encontrados neste arquivo SPED.')
        st.info('💡 Esta funcionalidade requer registros do Bloco E (Apuração de ICMS).')
        return
    
    # Exibe período da apuração (E100)
    if not df_e100.empty:
        periodo = df_e100.iloc[0]
        dt_ini = formatar_data_br(periodo.get('DT_INI', ''))
        dt_fin = formatar_data_br(periodo.get('DT_FIN', ''))
        
        st.info(f'📅 **Período de Apuração:** {dt_ini} a {dt_fin}')
        st.markdown('---')
    
    # Exibe totais da apuração (E110)
    if not df_e110.empty:
        exibir_totais_apuracao(df_e110)
    
    # Exibe ajustes (E111)
    if not df_e111.empty:
        exibir_ajustes(df_e111)
    
    # Exibe guias de recolhimento (E116)
    if not df_e116.empty:
        exibir_guias_recolhimento(df_e116)
    
    # Resumo final
    if not df_e110.empty:
        st.markdown('---')
        st.subheader('📋 Resumo da Apuração')
        
        apuracao = df_e110.iloc[0]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('**Débitos:**')
            st.write(formatar_moeda_br(apuracao.get('VL_TOT_DEBITOS', 0)))
        
        with col2:
            st.markdown('**Créditos:**')
            st.write(formatar_moeda_br(apuracao.get('VL_TOT_CREDITOS', 0)))
        
        with col3:
            st.markdown('**ICMS a Recolher:**')
            st.write(formatar_moeda_br(apuracao.get('VL_ICMS_RECOLHER', 0)))


# ============================================================================
# APRENDIZADOS E OBSERVAÇÕES
# ============================================================================

"""
APRENDIZADO 1: ESTRUTURA DA APURAÇÃO DE ICMS

E100: Período da apuração (data inicial e final)
E110: Totais da apuração (débitos, créditos, saldo)
E111: Ajustes (podem ser vários)
E116: Guias de recolhimento (podem ser várias)

APRENDIZADO 2: CÓDIGOS DE OBRIGAÇÃO (E116)

000 = ICMS Normal
006 = FECP (Fundo Estadual de Combate à Pobreza)
001 = ICMS ST
Outros conforme tabela SPED

APRENDIZADO 3: AJUSTES (E111)

Códigos variam por UF (ex: RJ040010, SP010203)
Podem aumentar débito ou crédito
Descrição complementar explica o motivo

APRENDIZADO 4: FORMATO DE DATA

DT_INI, DT_FIN, DT_VCTO: DDMMAAAA (ex: 01052025 = 01/05/2025)
"""

# ============================================================================
# FIM DO ARQUIVO
# ============================================================================
