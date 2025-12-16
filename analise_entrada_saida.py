"""
================================================================================
MÓDULO: Análise de Entrada e Saída - SPED ICMS/IPI
================================================================================

OBJETIVO:
    Analisar notas fiscais de entrada e saída baseadas em C100 + C190

CONTEXTO:
    No EFD ICMS/IPI, as operações são detalhadas em:
    - C100: Cabeçalho da nota fiscal
    - C190: Consolidação por CFOP/CST (sem itens individuais)
    
CLASSIFICAÇÃO DE CFOP:
    - ENTRADA: CFOPs iniciados em 1, 2, 3
    - SAÍDA: CFOPs iniciados em 5, 6, 7

CAMPOS PRINCIPAIS:
    C100: VL_DOC, VL_ICMS, VL_IPI, DT_DOC
    C190: VL_OPR, VL_BC_ICMS, VL_ICMS, VL_IPI, CFOP, CST_ICMS

GATILHOS DE MANUTENÇÃO:
    1. Para adicionar novos campos: incluir em criar_resumo_entrada_saida()
    2. Para mudar classificação: ajustar classificar_tipo_operacao()
    3. Para novos gráficos: adicionar em criar_graficos_entrada_saida()

Data de Criação: 16/12/2025
Autor: Sistema Lavoratory
================================================================================
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from typing import Tuple, Dict


# ============================================================================
# FUNÇÕES DE CLASSIFICAÇÃO
# ============================================================================

def classificar_tipo_operacao(cfop: str) -> str:
    """
    Classifica o tipo de operação baseado no CFOP.
    
    GATILHO DE MANUTENÇÃO:
    - CFOPs 1,2,3 = ENTRADA
    - CFOPs 5,6,7 = SAÍDA
    - Outros = OUTROS
    """
    if not cfop or len(str(cfop)) == 0:
        return 'NÃO CLASSIFICADO'
    
    cfop_str = str(cfop).strip()
    if len(cfop_str) == 0:
        return 'NÃO CLASSIFICADO'
    
    primeiro_digito = cfop_str[0]
    
    if primeiro_digito in ['1', '2', '3']:
        return 'ENTRADA'
    elif primeiro_digito in ['5', '6', '7']:
        return 'SAÍDA'
    else:
        return 'OUTROS'


def adicionar_classificacao(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adiciona coluna TIPO_OPERACAO ao DataFrame.
    
    GATILHO DE MANUTENÇÃO:
    - Sempre aplicar antes de qualquer análise
    - Baseado na coluna CFOP
    """
    if df.empty:
        df['TIPO_OPERACAO'] = ''
        return df
    
    if 'CFOP' not in df.columns:
        df['TIPO_OPERACAO'] = 'NÃO CLASSIFICADO'
        return df
    
    df['TIPO_OPERACAO'] = df['CFOP'].apply(classificar_tipo_operacao)
    
    return df


# ============================================================================
# FUNÇÕES DE ANÁLISE
# ============================================================================

def criar_resumo_entrada_saida(df_c100: pd.DataFrame, df_c190: pd.DataFrame) -> pd.DataFrame:
    """
    Cria resumo consolidado de entrada e saída.
    
    IMPORTANTE:
    - Usa C100 para valores totais de documentos
    - Usa C190 para detalhamento por CFOP/CST
    
    GATILHO DE MANUTENÇÃO:
    - Para adicionar campos, incluir na agregação
    - Para mudar cálculo, ajustar lógica de soma
    """
    if df_c190.empty:
        return pd.DataFrame(columns=['TIPO', 'QUANTIDADE', 'VL_OPERACAO', 'VL_ICMS', 'VL_IPI', 'TOTAL'])
    
    # Adiciona classificação
    df_c190 = adicionar_classificacao(df_c190)
    
    # Agrupa por tipo de operação
    resumo_data = []
    
    for tipo in ['ENTRADA', 'SAÍDA']:
        df_tipo = df_c190[df_c190['TIPO_OPERACAO'] == tipo]
        
        if not df_tipo.empty:
            qtd = len(df_tipo)
            vl_opr = df_tipo['VL_OPR'].sum() if 'VL_OPR' in df_tipo.columns else 0
            vl_icms = df_tipo['VL_ICMS'].sum() if 'VL_ICMS' in df_tipo.columns else 0
            vl_ipi = df_tipo['VL_IPI'].sum() if 'VL_IPI' in df_tipo.columns else 0
            
            resumo_data.append({
                'TIPO': tipo,
                'QUANTIDADE': qtd,
                'VL_OPERACAO': vl_opr,
                'VL_ICMS': vl_icms,
                'VL_IPI': vl_ipi,
                'TOTAL': vl_icms + vl_ipi
            })
    
    df_resumo = pd.DataFrame(resumo_data)
    return df_resumo


def top_cfops_por_tipo(df_c190: pd.DataFrame, tipo: str, top_n: int = 10) -> pd.DataFrame:
    """
    Retorna os top N CFOPs por tipo de operação.
    
    GATILHO DE MANUTENÇÃO:
    - Para mudar critério de ordenação, ajustar sort_values
    - Para adicionar campos, incluir no groupby.agg
    """
    if df_c190.empty:
        return pd.DataFrame()
    
    df_c190 = adicionar_classificacao(df_c190)
    df_tipo = df_c190[df_c190['TIPO_OPERACAO'] == tipo].copy()
    
    if df_tipo.empty:
        return pd.DataFrame()
    
    # Agrupa por CFOP
    df_agrupado = df_tipo.groupby('CFOP').agg({
        'VL_OPR': 'sum',
        'VL_ICMS': 'sum',
        'VL_IPI': 'sum'
    }).reset_index()
    
    df_agrupado['TOTAL'] = df_agrupado['VL_ICMS'] + df_agrupado['VL_IPI']
    df_agrupado = df_agrupado.sort_values('TOTAL', ascending=False).head(top_n)
    
    return df_agrupado


def extrair_mes_de_data(data_str: str) -> str:
    """
    Extrai o mês de uma data no formato DDMMAAAA.
    
    GATILHO DE MANUTENÇÃO:
    - Formato esperado: 06052025 (06/Maio/2025)
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
    
    # Extrai MM de DDMMAAAA (posições 2 e 3)
    mes_num = str(data_str)[2:4]
    return meses_dict.get(mes_num, 'Indefinido')


def evolucao_mensal_entrada_saida(df_c100: pd.DataFrame, df_c190: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula evolução mensal de entrada e saída.
    
    IMPORTANTE:
    - Usa DT_DOC do C100 para determinar o mês
    - Usa valores do C190 para ICMS/IPI
    
    GATILHO DE MANUTENÇÃO:
    - Para mudar formato de data, ajustar extrair_mes_de_data()
    - Para adicionar campos, incluir no merge
    """
    if df_c100.empty or df_c190.empty:
        return pd.DataFrame()
    
    # Adiciona mês ao C100
    df_c100 = df_c100.copy()
    df_c100['MES'] = df_c100['DT_DOC'].apply(extrair_mes_de_data)
    
    # Adiciona classificação ao C190
    df_c190 = adicionar_classificacao(df_c190)
    
    # Merge C100 com C190 (assumindo que há relação por NUM_DOC)
    if 'NUM_DOC' in df_c100.columns and 'NUM_DOC_PAI' in df_c190.columns:
        df_merged = df_c190.merge(
            df_c100[['NUM_DOC', 'MES']], 
            left_on='NUM_DOC_PAI', 
            right_on='NUM_DOC', 
            how='left'
        )
    else:
        # Se não houver relação, usa apenas C190
        return pd.DataFrame()
    
    # Agrupa por mês e tipo
    df_evolucao = df_merged.groupby(['MES', 'TIPO_OPERACAO']).agg({
        'VL_ICMS': 'sum',
        'VL_IPI': 'sum'
    }).reset_index()
    
    df_evolucao['TOTAL'] = df_evolucao['VL_ICMS'] + df_evolucao['VL_IPI']
    
    # Ordena por ordem alfabética dos meses
    ordem_meses = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ]
    df_evolucao['ORDEM'] = df_evolucao['MES'].apply(
        lambda x: ordem_meses.index(x) if x in ordem_meses else 99
    )
    df_evolucao = df_evolucao.sort_values('ORDEM').drop('ORDEM', axis=1)
    
    return df_evolucao


# ============================================================================
# FUNÇÕES DE VISUALIZAÇÃO
# ============================================================================

def formatar_moeda_br(valor):
    """Formata valor no padrão brasileiro: R$ 1.234,56"""
    if pd.isna(valor) or valor == 0:
        return 'R$ 0,00'
    return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def criar_grafico_comparativo(df_resumo: pd.DataFrame) -> go.Figure:
    """
    Cria gráfico de barras comparando Entrada vs Saída.
    
    GATILHO DE MANUTENÇÃO:
    - Para mudar cores, ajustar marker_color
    - Para adicionar barras, adicionar fig.add_trace
    """
    if df_resumo.empty:
        return None
    
    fig = go.Figure()
    
    # Barras de ICMS
    fig.add_trace(go.Bar(
        name='ICMS',
        x=df_resumo['TIPO'],
        y=df_resumo['VL_ICMS'],
        marker_color='#1f77b4',
        text=df_resumo['VL_ICMS'].apply(formatar_moeda_br),
        textposition='outside'
    ))
    
    # Barras de IPI
    fig.add_trace(go.Bar(
        name='IPI',
        x=df_resumo['TIPO'],
        y=df_resumo['VL_IPI'],
        marker_color='#ff7f0e',
        text=df_resumo['VL_IPI'].apply(formatar_moeda_br),
        textposition='outside'
    ))
    
    fig.update_layout(
        title='Comparativo: Entrada vs Saída',
        xaxis_title='Tipo de Operação',
        yaxis_title='Valor (R$)',
        barmode='group',
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
    
    fig.update_yaxes(tickformat=',.2f', tickprefix='R$ ')
    
    return fig


def criar_grafico_evolucao_mensal(df_evolucao: pd.DataFrame) -> go.Figure:
    """
    Cria gráfico de linha mostrando evolução mensal.
    
    GATILHO DE MANUTENÇÃO:
    - Para mudar cores, ajustar line=dict(color=...)
    - Para adicionar linhas, adicionar fig.add_trace
    """
    if df_evolucao.empty:
        return None
    
    fig = go.Figure()
    
    # Linha para ENTRADA
    df_entrada = df_evolucao[df_evolucao['TIPO_OPERACAO'] == 'ENTRADA']
    if not df_entrada.empty:
        fig.add_trace(go.Scatter(
            x=df_entrada['MES'],
            y=df_entrada['TOTAL'],
            mode='lines+markers',
            name='Entrada',
            line=dict(color='#2ca02c', width=3),
            marker=dict(size=8),
            hovertemplate='<b>%{x}</b><br>Entrada: R$ %{y:,.2f}<extra></extra>'
        ))
    
    # Linha para SAÍDA
    df_saida = df_evolucao[df_evolucao['TIPO_OPERACAO'] == 'SAÍDA']
    if not df_saida.empty:
        fig.add_trace(go.Scatter(
            x=df_saida['MES'],
            y=df_saida['TOTAL'],
            mode='lines+markers',
            name='Saída',
            line=dict(color='#d62728', width=3),
            marker=dict(size=8),
            hovertemplate='<b>%{x}</b><br>Saída: R$ %{y:,.2f}<extra></extra>'
        ))
    
    fig.update_layout(
        title='Evolução Mensal: ICMS + IPI',
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
    
    fig.update_yaxes(tickformat=',.2f', tickprefix='R$ ')
    
    return fig


# ============================================================================
# FUNÇÃO PRINCIPAL DE EXIBIÇÃO
# ============================================================================

def exibir_analise_entrada_saida(df_c100: pd.DataFrame, df_c190: pd.DataFrame):
    """
    Exibe análise completa de entrada e saída.
    
    GATILHO DE MANUTENÇÃO:
    - Esta é a função principal chamada pelo app.py
    - Para adicionar seções, adicionar st.subheader() e conteúdo
    """
    st.header('Análise de Entrada e Saída')
    st.markdown('**Baseado em C100 (Documentos) + C190 (Consolidação por CFOP/CST)**')
    
    # Cria resumo
    df_resumo = criar_resumo_entrada_saida(df_c100, df_c190)
    
    if df_resumo.empty:
        st.warning('Nenhum dado de entrada/saída encontrado.')
        return
    
    # Exibir métricas resumidas
    col1, col2, col3, col4 = st.columns(4)
    
    entrada = df_resumo[df_resumo['TIPO'] == 'ENTRADA']
    saida = df_resumo[df_resumo['TIPO'] == 'SAÍDA']
    
    with col1:
        qtd_entrada = entrada['QUANTIDADE'].sum() if not entrada.empty else 0
        st.metric('Registros Entrada', f"{qtd_entrada:,}".replace(',', '.'))
    
    with col2:
        icms_entrada = entrada['VL_ICMS'].sum() if not entrada.empty else 0
        st.metric('ICMS Entrada', formatar_moeda_br(icms_entrada))
    
    with col3:
        qtd_saida = saida['QUANTIDADE'].sum() if not saida.empty else 0
        st.metric('Registros Saída', f"{qtd_saida:,}".replace(',', '.'))
    
    with col4:
        icms_saida = saida['VL_ICMS'].sum() if not saida.empty else 0
        st.metric('ICMS Saída', formatar_moeda_br(icms_saida))
    
    st.markdown('---')
    
    # Gráfico comparativo
    st.subheader('Comparativo Entrada vs Saída')
    fig_comp = criar_grafico_comparativo(df_resumo)
    if fig_comp:
        st.plotly_chart(fig_comp, use_container_width=True)
    
    st.markdown('---')
    
    # Evolução mensal
    st.subheader('Evolução Mensal')
    df_evolucao = evolucao_mensal_entrada_saida(df_c100, df_c190)
    if not df_evolucao.empty:
        fig_evol = criar_grafico_evolucao_mensal(df_evolucao)
        if fig_evol:
            st.plotly_chart(fig_evol, use_container_width=True)
    else:
        st.info('Dados insuficientes para gerar evolução mensal.')
    
    st.markdown('---')
    
    # Tabela resumida
    st.subheader('Resumo Detalhado')
    df_exibicao = df_resumo.copy()
    df_exibicao['VL_OPERACAO'] = df_exibicao['VL_OPERACAO'].apply(formatar_moeda_br)
    df_exibicao['VL_ICMS'] = df_exibicao['VL_ICMS'].apply(formatar_moeda_br)
    df_exibicao['VL_IPI'] = df_exibicao['VL_IPI'].apply(formatar_moeda_br)
    df_exibicao['TOTAL'] = df_exibicao['TOTAL'].apply(formatar_moeda_br)
    
    st.dataframe(df_exibicao, use_container_width=True, hide_index=True)
    
    # Download
    csv = df_resumo.to_csv(index=False, encoding='utf-8-sig', sep=';', decimal=',')
    st.download_button(
        label='Baixar Resumo (CSV)',
        data=csv,
        file_name='entrada_saida_icms_ipi.csv',
        mime='text/csv'
    )


# ============================================================================
# APRENDIZADOS E OBSERVAÇÕES
# ============================================================================

"""
APRENDIZADO 1: ESTRUTURA C100 + C190
- C100 contém o cabeçalho da nota fiscal
- C190 contém a consolidação por CFOP/CST (sem itens individuais)
- Esta é a principal diferença em relação ao PIS/COFINS

APRENDIZADO 2: CLASSIFICAÇÃO DE CFOP
- 1,2,3 = ENTRADA (crédito)
- 5,6,7 = SAÍDA (débito)

APRENDIZADO 3: FORMATO DE DATA
- DT_DOC no formato DDMMAAAA (ex: 06052025 = 06/Maio/2025)
- Posições 2-3 contêm o mês

APRENDIZADO 4: ORDEM ALFABÉTICA DOS MESES
- Janeiro, Fevereiro, Março, Abril, Maio, Junho
- Julho, Agosto, Setembro, Outubro, Novembro, Dezembro
"""

# ============================================================================
# FIM DO ARQUIVO
# ============================================================================
