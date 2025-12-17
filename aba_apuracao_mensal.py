"""
================================================================================
ABA: ICMS/IPI APURADO - ANÁLISE POR COMPETÊNCIA
================================================================================

Módulo para exibir apuração completa de ICMS com base nos registros E.
Suporta múltiplas competências (12 meses).

Baseado nos registros:
- E100: Período da Apuração
- E110: Apuração do ICMS (totais)
- E111: Ajustes da Apuração
- E116: Obrigações ICMS Recolhido/A Recolher (guias)

Data de Criação: 16/12/2025
Atualização: 17/12/2025 - Suporte a múltiplas competências

================================================================================
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Dict


def formatar_moeda_br(valor):
    """Formata valor para padrão brasileiro: R$ 1.234,56"""
    if pd.isna(valor) or valor == 0:
        return 'R$ 0,00'
    return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def extrair_competencia(data_str):
    """
    Extrai competência MM/AAAA de uma data DDMMAAAA.
    Exemplo: 01052025 → 05/2025
    """
    if not data_str or len(str(data_str)) < 8:
        return 'Indefinido'
    
    data_str = str(data_str)
    mm = data_str[2:4]
    aaaa = data_str[4:8]
    
    return f"{mm}/{aaaa}"


def formatar_data_br(data_str):
    """Formata data de DDMMAAAA para DD/MM/AAAA"""
    if not data_str or len(str(data_str)) < 8:
        return ''
    
    data_str = str(data_str)
    dd = data_str[0:2]
    mm = data_str[2:4]
    aaaa = data_str[4:8]
    
    return f"{dd}/{mm}/{aaaa}"


def mapear_codigo_obrigacao(cod_or):
    """Mapeia código de obrigação para descrição"""
    mapeamento = {
        '000': 'ICMS Normal',
        '001': 'ICMS ST',
        '002': 'ICMS Antecipado',
        '003': 'ICMS Diferencial de Alíquota',
        '006': 'FECP',
        '007': 'FECP ST',
    }
    return mapeamento.get(str(cod_or), f'Código {cod_or}')


def adicionar_competencia_aos_dados(dados_e: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """
    Adiciona coluna COMPETENCIA a todos os DataFrames baseado no E100.
    
    Retorna:
        dados_e atualizado com coluna COMPETENCIA
    """
    df_e100 = dados_e.get('E100', pd.DataFrame())
    
    if df_e100.empty:
        return dados_e
    
    # Adiciona competência ao E100
    df_e100['COMPETENCIA'] = df_e100['DT_INI'].apply(extrair_competencia)
    
    # Para E110, E111, E116: assumir que pertencem à mesma competência
    # (geralmente há 1 E100 seguido de seus E110, E111, E116)
    
    # Cria índice de competência baseado na ordem
    competencias = df_e100['COMPETENCIA'].tolist()
    
    # Adiciona competência aos outros registros
    for key in ['E110', 'E111', 'E116']:
        df = dados_e.get(key, pd.DataFrame())
        if not df.empty:
            # Se houver apenas 1 competência, aplica a todos
            if len(competencias) == 1:
                df['COMPETENCIA'] = competencias[0]
            else:
                # Se houver múltiplas, precisa mapear (assumir ordem sequencial)
                # Isso é uma simplificação - idealmente seria baseado em contexto
                if len(df) == len(competencias):
                    df['COMPETENCIA'] = competencias
                else:
                    # Distribui proporcionalmente
                    qtd_por_comp = len(df) // len(competencias)
                    comps = []
                    for comp in competencias:
                        comps.extend([comp] * qtd_por_comp)
                    # Preenche o resto com a última competência
                    while len(comps) < len(df):
                        comps.append(competencias[-1])
                    df['COMPETENCIA'] = comps[:len(df)]
            
            dados_e[key] = df
    
    dados_e['E100'] = df_e100
    
    return dados_e


def criar_tabela_consolidada(dados_e: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Cria tabela consolidada com uma linha por competência.
    
    Colunas:
    - COMPETENCIA
    - VL_TOT_DEBITOS
    - VL_TOT_CREDITOS
    - VL_ICMS_RECOLHER
    - QTD_AJUSTES
    - QTD_GUIAS
    """
    df_e100 = dados_e.get('E100', pd.DataFrame())
    df_e110 = dados_e.get('E110', pd.DataFrame())
    df_e111 = dados_e.get('E111', pd.DataFrame())
    df_e116 = dados_e.get('E116', pd.DataFrame())
    
    if df_e100.empty:
        return pd.DataFrame()
    
    # Agrupa E110 por competência
    if not df_e110.empty and 'COMPETENCIA' in df_e110.columns:
        df_consolidado = df_e110.groupby('COMPETENCIA').agg({
            'VL_TOT_DEBITOS': 'sum',
            'VL_TOT_CREDITOS': 'sum',
            'VL_ICMS_RECOLHER': 'sum'
        }).reset_index()
    else:
        df_consolidado = df_e100[['COMPETENCIA']].copy()
        df_consolidado['VL_TOT_DEBITOS'] = 0
        df_consolidado['VL_TOT_CREDITOS'] = 0
        df_consolidado['VL_ICMS_RECOLHER'] = 0
    
    # Conta ajustes por competência
    if not df_e111.empty and 'COMPETENCIA' in df_e111.columns:
        df_ajustes = df_e111.groupby('COMPETENCIA').size().reset_index(name='QTD_AJUSTES')
        df_consolidado = df_consolidado.merge(df_ajustes, on='COMPETENCIA', how='left')
    else:
        df_consolidado['QTD_AJUSTES'] = 0
    
    # Conta guias por competência
    if not df_e116.empty and 'COMPETENCIA' in df_e116.columns:
        df_guias = df_e116.groupby('COMPETENCIA').size().reset_index(name='QTD_GUIAS')
        df_consolidado = df_consolidado.merge(df_guias, on='COMPETENCIA', how='left')
    else:
        df_consolidado['QTD_GUIAS'] = 0
    
    # Preenche NaN com 0
    df_consolidado = df_consolidado.fillna(0)
    
    # Ordena por competência (MM/AAAA)
    df_consolidado['ORDEM'] = df_consolidado['COMPETENCIA'].apply(
        lambda x: f"{x.split('/')[1]}{x.split('/')[0]}" if '/' in str(x) else '999999'
    )
    df_consolidado = df_consolidado.sort_values('ORDEM').drop('ORDEM', axis=1)
    
    return df_consolidado


def criar_grafico_evolucao(df_consolidado: pd.DataFrame) -> go.Figure:
    """Cria gráfico de evolução mensal do ICMS a recolher"""
    if df_consolidado.empty:
        return None
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_consolidado['COMPETENCIA'],
        y=df_consolidado['VL_ICMS_RECOLHER'],
        mode='lines+markers',
        name='ICMS a Recolher',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=10),
        text=df_consolidado['VL_ICMS_RECOLHER'].apply(formatar_moeda_br),
        textposition='top center',
        hovertemplate='<b>%{x}</b><br>ICMS: %{text}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Evolução Mensal: ICMS a Recolher',
        xaxis_title='Competência',
        yaxis_title='Valor (R$)',
        template='plotly_white',
        height=400,
        hovermode='x unified'
    )
    
    fig.update_yaxes(tickformat=',.2f', tickprefix='R$ ')
    
    return fig


def exibir_aba_apuracao_mensal(dados_e: Dict[str, pd.DataFrame]):
    """
    Exibe a aba de ICMS/IPI Apurado com suporte a múltiplas competências.
    
    Parâmetros:
        dados_e: Dicionário com DataFrames dos registros E
    """
    st.header('💰 ICMS/IPI Apurado')
    st.markdown('**Apuração Completa de ICMS por Competência (Registros E100, E110, E111, E116)**')
    
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
    
    # Adiciona competência aos dados
    dados_e = adicionar_competencia_aos_dados(dados_e)
    
    # Cria tabela consolidada
    df_consolidado = criar_tabela_consolidada(dados_e)
    
    if df_consolidado.empty:
        st.warning('⚠️ Não foi possível consolidar os dados de apuração.')
        return
    
    # Exibe quantidade de competências
    qtd_competencias = len(df_consolidado)
    st.info(f'📅 **{qtd_competencias} competência(s) encontrada(s)**')
    st.markdown('---')
    
    # Gráfico de evolução
    st.subheader('📈 Evolução Mensal')
    fig = criar_grafico_evolucao(df_consolidado)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('---')
    
    # Tabela consolidada
    st.subheader('📋 Resumo por Competência')
    
    # Formata valores para exibição
    df_exibicao = df_consolidado.copy()
    df_exibicao['VL_TOT_DEBITOS'] = df_exibicao['VL_TOT_DEBITOS'].apply(formatar_moeda_br)
    df_exibicao['VL_TOT_CREDITOS'] = df_exibicao['VL_TOT_CREDITOS'].apply(formatar_moeda_br)
    df_exibicao['VL_ICMS_RECOLHER'] = df_exibicao['VL_ICMS_RECOLHER'].apply(formatar_moeda_br)
    df_exibicao['QTD_AJUSTES'] = df_exibicao['QTD_AJUSTES'].astype(int)
    df_exibicao['QTD_GUIAS'] = df_exibicao['QTD_GUIAS'].astype(int)
    
    # Renomeia colunas para exibição
    df_exibicao = df_exibicao.rename(columns={
        'COMPETENCIA': 'Competência',
        'VL_TOT_DEBITOS': 'Total Débitos',
        'VL_TOT_CREDITOS': 'Total Créditos',
        'VL_ICMS_RECOLHER': 'ICMS a Recolher',
        'QTD_AJUSTES': 'Ajustes',
        'QTD_GUIAS': 'Guias'
    })
    
    st.dataframe(df_exibicao, use_container_width=True, hide_index=True)
    
    # Download
    csv = df_consolidado.to_csv(index=False, encoding='utf-8-sig', sep=';', decimal=',')
    st.download_button(
        label='📥 Download CSV',
        data=csv,
        file_name='icms_ipi_apurado_por_competencia.csv',
        mime='text/csv'
    )
    
    st.markdown('---')
    
    # Detalhamento por competência (expansível)
    st.subheader('🔍 Detalhamento por Competência')
    
    competencias = df_consolidado['COMPETENCIA'].unique()
    
    for competencia in competencias:
        with st.expander(f"📅 Competência {competencia}"):
            # Filtra dados da competência
            df_e110_comp = df_e110[df_e110['COMPETENCIA'] == competencia] if 'COMPETENCIA' in df_e110.columns else pd.DataFrame()
            df_e111_comp = df_e111[df_e111['COMPETENCIA'] == competencia] if 'COMPETENCIA' in df_e111.columns else pd.DataFrame()
            df_e116_comp = df_e116[df_e116['COMPETENCIA'] == competencia] if 'COMPETENCIA' in df_e116.columns else pd.DataFrame()
            
            # Totais da apuração
            if not df_e110_comp.empty:
                st.markdown('**💰 Totais da Apuração**')
                apuracao = df_e110_comp.iloc[0]
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric('Total Débitos', formatar_moeda_br(apuracao.get('VL_TOT_DEBITOS', 0)))
                
                with col2:
                    st.metric('Total Créditos', formatar_moeda_br(apuracao.get('VL_TOT_CREDITOS', 0)))
                
                with col3:
                    st.metric('Saldo Apurado', formatar_moeda_br(apuracao.get('VL_SLD_APURADO', 0)))
                
                with col4:
                    st.metric('ICMS a Recolher', formatar_moeda_br(apuracao.get('VL_ICMS_RECOLHER', 0)))
            
            # Ajustes
            if not df_e111_comp.empty:
                st.markdown('**📝 Ajustes**')
                df_ajustes_exib = df_e111_comp[['COD_AJ_APUR', 'DESCR_COMPL_AJ', 'VL_AJ_APUR']].copy()
                df_ajustes_exib['VL_AJ_APUR'] = df_ajustes_exib['VL_AJ_APUR'].apply(formatar_moeda_br)
                df_ajustes_exib = df_ajustes_exib.rename(columns={
                    'COD_AJ_APUR': 'Código',
                    'DESCR_COMPL_AJ': 'Descrição',
                    'VL_AJ_APUR': 'Valor'
                })
                st.dataframe(df_ajustes_exib, use_container_width=True, hide_index=True)
            
            # Guias
            if not df_e116_comp.empty:
                st.markdown('**🧾 Guias de Recolhimento**')
                df_guias_exib = df_e116_comp.copy()
                df_guias_exib['TIPO'] = df_guias_exib['COD_OR'].apply(mapear_codigo_obrigacao)
                df_guias_exib['DT_VCTO_FMT'] = df_guias_exib['DT_VCTO'].apply(formatar_data_br)
                df_guias_exib['VL_OR_FMT'] = df_guias_exib['VL_OR'].apply(formatar_moeda_br)
                
                df_guias_exib = df_guias_exib[['TIPO', 'VL_OR_FMT', 'DT_VCTO_FMT', 'COD_REC', 'TXT_COMPL']]
                df_guias_exib = df_guias_exib.rename(columns={
                    'TIPO': 'Tipo',
                    'VL_OR_FMT': 'Valor',
                    'DT_VCTO_FMT': 'Vencimento',
                    'COD_REC': 'Cód. Receita',
                    'TXT_COMPL': 'Descrição'
                })
                st.dataframe(df_guias_exib, use_container_width=True, hide_index=True)
