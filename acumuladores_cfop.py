"""
================================================================================
MÓDULO: Acumuladores por CFOP - SPED ICMS/IPI
================================================================================

OBJETIVO:
    Criar totalizadores agrupados por CFOP para análise fiscal de ICMS e IPI

CONTEXTO:
    - CFOP = Código Fiscal de Operações e Prestações
    - Usado em Notas Fiscais brasileiras
    - Identifica o tipo de operação fiscal

CLASSIFICAÇÃO:
    - ENTRADA: CFOP iniciados em 1, 2, 3 (ex: 1102, 2102, 3102)
    - SAÍDA: CFOP iniciados em 5, 6, 7 (ex: 5102, 6102, 7102)

CAMPOS ACUMULADOS:
    - VL_OPR: Valor da Operação
    - VL_BC_ICMS: Base de Cálculo do ICMS
    - VL_ICMS: Valor do ICMS
    - VL_BC_ICMS_ST: Base de Cálculo do ICMS ST
    - VL_ICMS_ST: Valor do ICMS ST
    - VL_IPI: Valor do IPI

FORMATO DE VALORES:
    - Padrão brasileiro: R$ 1.234,56
    - Ponto para milhar, vírgula para decimal

AUTOR: Manus AI Assistant
================================================================================
"""

import pandas as pd
import streamlit as st


# ============================================================================
# CONSTANTES E CONFIGURAÇÕES
# ============================================================================

# Campos que serão somados no acumulador
CAMPOS_ACUMULAVEIS = ['VL_OPR', 'VL_BC_ICMS', 'VL_ICMS', 'VL_BC_ICMS_ST', 'VL_ICMS_ST', 'VL_IPI']

# Mapeamento de nomes para exibição
NOMES_COLUNAS = {
    'CFOP': 'CFOP',
    'CST_ICMS': 'CST ICMS',
    'QTD_REGISTROS': 'Qtd. Registros',
    'VL_OPR': 'Valor Operação',
    'VL_BC_ICMS': 'Base ICMS',
    'VL_ICMS': 'Valor ICMS',
    'VL_BC_ICMS_ST': 'Base ICMS ST',
    'VL_ICMS_ST': 'Valor ICMS ST',
    'VL_IPI': 'Valor IPI',
    'TOTAL_IMPOSTOS': 'Total Impostos'
}


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def formatar_valor_br(valor):
    """
    Formata valor monetário no padrão brasileiro.
    """
    try:
        valor_str = f"{valor:,.2f}"
        valor_str = valor_str.replace(',', 'TEMP').replace('.', ',').replace('TEMP', '.')
        return f"R$ {valor_str}"
    except:
        return "R$ 0,00"


def classificar_cfop(cfop):
    """
    Classifica CFOP como ENTRADA ou SAÍDA.
    """
    try:
        primeiro_digito = str(cfop)[0]
        if primeiro_digito in ['1', '2', '3']:
            return 'ENTRADA'
        elif primeiro_digito in ['5', '6', '7']:
            return 'SAÍDA'
        else:
            return 'OUTROS'
    except:
        return 'INDEFINIDO'


# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def criar_acumulador_cfop(df):
    """
    Cria DataFrame acumulado por CFOP e CST ICMS.
    
    Args:
        df: DataFrame com registros C190
        
    Returns:
        DataFrame acumulado
    """
    if df.empty:
        return pd.DataFrame()
    
    # Verifica se as colunas necessárias existem
    colunas_necessarias = ['CFOP', 'CST_ICMS'] + CAMPOS_ACUMULAVEIS
    colunas_disponiveis = [col for col in colunas_necessarias if col in df.columns]
    
    if 'CFOP' not in colunas_disponiveis or 'CST_ICMS' not in colunas_disponiveis:
        return pd.DataFrame()
    
    # Campos para agrupar
    campos_grupo = ['CFOP', 'CST_ICMS']
    
    # Campos para somar (apenas os que existem)
    campos_soma = [col for col in CAMPOS_ACUMULAVEIS if col in df.columns]
    
    # Agrupa e soma
    agg_dict = {campo: 'sum' for campo in campos_soma}
    df_acumulado = df.groupby(campos_grupo).agg(agg_dict).reset_index()
    
    # Adiciona contagem de registros
    df_contagem = df.groupby(campos_grupo).size().reset_index(name='QTD_REGISTROS')
    df_acumulado = df_acumulado.merge(df_contagem, on=campos_grupo, how='left')
    
    # Adiciona coluna de classificação
    df_acumulado['TIPO'] = df_acumulado['CFOP'].apply(classificar_cfop)
    
    # Calcula total de impostos
    df_acumulado['TOTAL_IMPOSTOS'] = (
        df_acumulado.get('VL_ICMS', 0) + 
        df_acumulado.get('VL_ICMS_ST', 0) + 
        df_acumulado.get('VL_IPI', 0)
    )
    
    # Ordena por valor total (maior para menor)
    df_acumulado = df_acumulado.sort_values('TOTAL_IMPOSTOS', ascending=False)
    
    # Reordena colunas
    colunas_ordem = ['TIPO', 'CFOP', 'CST_ICMS', 'QTD_REGISTROS'] + campos_soma + ['TOTAL_IMPOSTOS']
    colunas_ordem = [col for col in colunas_ordem if col in df_acumulado.columns]
    df_acumulado = df_acumulado[colunas_ordem]
    
    return df_acumulado


def formatar_dataframe_para_exibicao(df):
    """
    Formata DataFrame para exibição com valores em R$.
    """
    if df.empty:
        return df
    
    df_formatado = df.copy()
    
    # Formata colunas numéricas
    colunas_numericas = ['VL_OPR', 'VL_BC_ICMS', 'VL_ICMS', 'VL_BC_ICMS_ST', 'VL_ICMS_ST', 'VL_IPI', 'TOTAL_IMPOSTOS']
    
    for col in colunas_numericas:
        if col in df_formatado.columns:
            df_formatado[col] = df_formatado[col].apply(formatar_valor_br)
    
    # Renomeia colunas para nomes amigáveis
    df_formatado.rename(columns=NOMES_COLUNAS, inplace=True)
    
    return df_formatado


# ============================================================================
# FUNÇÃO DE EXIBIÇÃO
# ============================================================================

def exibir_acumulador_cfop(df):
    """
    Exibe acumulador de CFOP na interface Streamlit.
    """
    st.markdown("## 📊 Acumulador por CFOP e CST ICMS")
    st.markdown("Totalizadores agrupados por CFOP e Código de Situação Tributária do ICMS")
    st.markdown("---")
    
    # Cria acumulador
    df_acumulado = criar_acumulador_cfop(df)
    
    if df_acumulado.empty:
        st.warning("⚠️ Não há dados para exibir o acumulador")
        return
    
    # Estatísticas gerais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_cfops = df_acumulado['CFOP'].nunique()
        st.metric("Total de CFOPs", total_cfops)
    
    with col2:
        total_registros = df_acumulado['QTD_REGISTROS'].sum()
        st.metric("Total de Registros", f"{total_registros:,}".replace(',', '.'))
    
    with col3:
        total_icms = df_acumulado['VL_ICMS'].sum() if 'VL_ICMS' in df_acumulado.columns else 0
        st.metric("Total ICMS", formatar_valor_br(total_icms))
    
    with col4:
        total_ipi = df_acumulado['VL_IPI'].sum() if 'VL_IPI' in df_acumulado.columns else 0
        st.metric("Total IPI", formatar_valor_br(total_ipi))
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Abas por tipo de operação
    tipos = df_acumulado['TIPO'].unique()
    
    if len(tipos) > 1:
        tabs = st.tabs([f"📥 {tipo}" for tipo in sorted(tipos)])
        
        for i, tipo in enumerate(sorted(tipos)):
            with tabs[i]:
                df_tipo = df_acumulado[df_acumulado['TIPO'] == tipo].copy()
                df_tipo = df_tipo.drop(columns=['TIPO'])
                
                # Formata para exibição
                df_exibicao = formatar_dataframe_para_exibicao(df_tipo)
                
                st.dataframe(
                    df_exibicao,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Botão de download
                csv = df_tipo.to_csv(index=False, sep=';', decimal=',')
                st.download_button(
                    label=f"📥 Download CSV - {tipo}",
                    data=csv,
                    file_name=f"acumulador_cfop_{tipo.lower()}.csv",
                    mime="text/csv"
                )
    else:
        # Se houver apenas um tipo, exibe direto
        df_exibicao = formatar_dataframe_para_exibicao(df_acumulado.drop(columns=['TIPO']))
        
        st.dataframe(
            df_exibicao,
            use_container_width=True,
            hide_index=True
        )
        
        # Botão de download
        csv = df_acumulado.to_csv(index=False, sep=';', decimal=',')
        st.download_button(
            label="📥 Download CSV Completo",
            data=csv,
            file_name="acumulador_cfop_completo.csv",
            mime="text/csv"
        )
