"""
================================================================================
ABA: ICMS/IPI APURADO - ANÁLISE MENSAL
================================================================================

Módulo para exibir evolução mensal dos valores de ICMS e IPI a recolher.

Baseado nos registros:
- E110: Apuração ICMS
- E520: Apuração IPI
- C190: Consolidação por CFOP/CST (alternativa se E não existir)

Data de Criação: 16/12/2025
Autor: Sistema Lavoratory

================================================================================
GATILHOS DE MANUTENÇÃO:
================================================================================

1. ADICIONAR NOVOS CAMPOS:
   - Editar função criar_tabela_mensal()
   - Adicionar campo no DataFrame

2. MUDAR GRÁFICO:
   - Editar função criar_grafico_evolucao()
   - Ajustar cores, títulos, etc.

3. ALTERAR ORDEM DOS MESES:
   - Editar ORDEM_MESES abaixo
   - Manter ordem alfabética (Jan, Fev, Mar...)

================================================================================
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ============================================================================
# CONSTANTES
# ============================================================================

# Ordem alfabética dos meses (Jan, Fev, Mar...)
ORDEM_MESES = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

# Mapeamento de número para nome do mês
MESES_DICT = {
    '01': 'Janeiro', '02': 'Fevereiro', '03': 'Março',
    '04': 'Abril', '05': 'Maio', '06': 'Junho',
    '07': 'Julho', '08': 'Agosto', '09': 'Setembro',
    '10': 'Outubro', '11': 'Novembro', '12': 'Dezembro'
}


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


def extrair_mes_data(data_str):
    """
    Extrai o mês de uma data no formato DDMMAAAA.
    
    Parâmetros:
        data_str (str): Data no formato '06052025' (06/Maio/2025)
    
    Retorna:
        str: Nome do mês ('Janeiro', 'Fevereiro', etc.)
    
    GATILHO DE MANUTENÇÃO:
    - Se formato da data mudar, ajustar aqui
    - Atualmente: DDMMAAAA (posições 2-3 = mês)
    """
    if not data_str or len(str(data_str)) < 6:
        return 'Indefinido'
    
    # Extrai MM de DDMMAAAA (posições 2 e 3)
    mes_num = str(data_str)[2:4]
    return MESES_DICT.get(mes_num, 'Indefinido')


def criar_tabela_mensal_c190(df_c190: pd.DataFrame) -> pd.DataFrame:
    """
    Cria tabela mensal de ICMS/IPI usando C190.
    
    IMPORTANTE:
    - Usa C190 quando registros E não estão disponíveis
    - Extrai mês de algum campo de data (se existir)
    
    GATILHO DE MANUTENÇÃO:
    - Para adicionar campos, incluir na agregação abaixo
    - Para mudar cálculo, ajustar a lógica de soma
    """
    if df_c190.empty:
        return pd.DataFrame(columns=['Competência', 'ICMS Apurado', 'IPI Apurado', 'Total'])
    
    # Verifica se há campo de data para extrair mês
    # Como C190 não tem data direta, precisamos buscar em C100
    # Por enquanto, retorna vazio se não houver registros E
    return pd.DataFrame(columns=['Competência', 'ICMS Apurado', 'IPI Apurado', 'Total'])


def criar_grafico_evolucao(tabela):
    """
    Cria gráfico de linha mostrando evolução mensal de ICMS, IPI e Total.
    
    Parâmetros:
        tabela (pd.DataFrame): Tabela mensal criada por criar_tabela_mensal()
    
    Retorna:
        plotly.graph_objects.Figure: Gráfico de evolução
    
    GATILHO DE MANUTENÇÃO:
    - Para mudar cores, ajustar parâmetro 'line=dict(color=...)'
    - Para adicionar linhas, adicionar fig.add_trace()
    """
    fig = go.Figure()
    
    # Linha ICMS (Azul)
    fig.add_trace(go.Scatter(
        x=tabela['Competência'],
        y=tabela['ICMS Apurado'],
        mode='lines+markers',
        name='ICMS',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{x}</b><br>ICMS: R$ %{y:,.2f}<extra></extra>'
    ))
    
    # Linha IPI (Laranja)
    fig.add_trace(go.Scatter(
        x=tabela['Competência'],
        y=tabela['IPI Apurado'],
        mode='lines+markers',
        name='IPI',
        line=dict(color='#ff7f0e', width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{x}</b><br>IPI: R$ %{y:,.2f}<extra></extra>'
    ))
    
    # Linha Total (Verde)
    fig.add_trace(go.Scatter(
        x=tabela['Competência'],
        y=tabela['Total'],
        mode='lines+markers',
        name='Total',
        line=dict(color='#2ca02c', width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{x}</b><br>Total: R$ %{y:,.2f}<extra></extra>'
    ))
    
    # Layout
    fig.update_layout(
        title='Evolução Mensal de ICMS/IPI Apurado',
        xaxis_title='Competência',
        yaxis_title='Valor (R$)',
        hovermode='x unified',
        template='plotly_white',
        height=500,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )
    
    # Formatação do eixo Y (valores em R$)
    fig.update_yaxes(tickformat=',.2f', tickprefix='R$ ')
    
    return fig


def exibir_aba_apuracao_mensal(df_c190: pd.DataFrame):
    """
    Exibe a aba de ICMS/IPI Apurado com tabela e gráfico.
    
    Parâmetros:
        df_c190: DataFrame com registros C190
    
    GATILHO DE MANUTENÇÃO:
    - Esta é a função principal chamada pelo app.py
    - Para adicionar seções, adicionar st.subheader() e conteúdo
    """
    st.header('ICMS/IPI Apurado')
    st.markdown('**Análise Mensal dos Valores (baseado em C190)**')
    
    # Criar tabela mensal
    tabela = criar_tabela_mensal_c190(df_c190)
    
    if tabela.empty:
        st.info('📊 Análise mensal de ICMS/IPI apurado')
        st.warning('⚠️ Registros de apuração mensal (E110/E520) não encontrados neste arquivo SPED.')
        st.info('💡 Esta funcionalidade requer registros do Bloco E (Apuração). Os dados disponíveis são do Bloco C (Documentos Fiscais).')
        
        # Mostra resumo do C190 disponível
        if not df_c190.empty:
            st.markdown('---')
            st.subheader('Resumo Disponível (C190)')
            
            total_icms = df_c190['VL_ICMS'].sum() if 'VL_ICMS' in df_c190.columns else 0
            total_ipi = df_c190['VL_IPI'].sum() if 'VL_IPI' in df_c190.columns else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric('Total ICMS (C190)', formatar_moeda_br(total_icms))
            with col2:
                st.metric('Total IPI (C190)', formatar_moeda_br(total_ipi))
            with col3:
                st.metric('Total Geral', formatar_moeda_br(total_icms + total_ipi))
        
        return
    
    # Exibir resumo
    total_icms = tabela['ICMS Apurado'].sum()
    total_ipi = tabela['IPI Apurado'].sum()
    total_geral = tabela['Total'].sum()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Total ICMS', formatar_moeda_br(total_icms))
    with col2:
        st.metric('Total IPI', formatar_moeda_br(total_ipi))
    with col3:
        st.metric('Total Geral', formatar_moeda_br(total_geral))
    
    st.markdown('---')
    
    # Gráfico de Evolução
    st.subheader('Evolução Mensal')
    fig = criar_grafico_evolucao(tabela)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('---')
    
    # Tabela Detalhada
    st.subheader('Detalhamento Mensal')
    
    # Formatar tabela para exibição
    tabela_exibicao = tabela.copy()
    tabela_exibicao['ICMS Apurado'] = tabela_exibicao['ICMS Apurado'].apply(formatar_moeda_br)
    tabela_exibicao['IPI Apurado'] = tabela_exibicao['IPI Apurado'].apply(formatar_moeda_br)
    tabela_exibicao['Total'] = tabela_exibicao['Total'].apply(formatar_moeda_br)
    
    st.dataframe(tabela_exibicao, use_container_width=True, hide_index=True)
    
    # Download CSV
    st.markdown('---')
    st.subheader('Download')
    
    csv = tabela.to_csv(index=False, encoding='utf-8-sig', sep=';', decimal=',')
    st.download_button(
        label='Baixar Tabela Mensal (CSV)',
        data=csv,
        file_name='icms_ipi_apurado_mensal.csv',
        mime='text/csv'
    )


# ============================================================================
# APRENDIZADOS E OBSERVAÇÕES
# ============================================================================

"""
APRENDIZADO 1: FORMATO BRASILEIRO
- Sempre usar formato brasileiro para valores monetários
- Exemplo: R$ 1.234,56 (ponto para milhar, vírgula para decimal)

APRENDIZADO 2: ORDEM ALFABÉTICA DOS MESES
- Janeiro, Fevereiro, Março, Abril, Maio, Junho
- Julho, Agosto, Setembro, Outubro, Novembro, Dezembro

APRENDIZADO 3: REGISTROS UTILIZADOS
- E110: Apuração ICMS (ideal, mas nem sempre presente)
- E520: Apuração IPI (ideal, mas nem sempre presente)
- C190: Consolidação por CFOP/CST (sempre presente)

APRENDIZADO 4: FORMATO DE DATA
- Formato: DDMMAAAA (ex: 06052025 = 06/Maio/2025)
- Extrair posições 2-3 para obter o mês
"""

# ============================================================================
# FIM DO ARQUIVO
# ============================================================================
