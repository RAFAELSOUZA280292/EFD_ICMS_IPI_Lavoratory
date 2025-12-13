"""
Filtros Avançados - Módulo para filtrar dados SPED ICMS/IPI
Permite filtrar por múltiplos campos com operadores: =, ≠, <, >
"""

import pandas as pd
import streamlit as st


def aplicar_filtro_numerico(df, coluna, operador, valor):
    """
    Aplica filtro numérico em uma coluna
    """
    try:
        valor_float = float(valor)
        
        if operador == '=':
            return df[df[coluna] == valor_float]
        elif operador == '≠':
            return df[df[coluna] != valor_float]
        elif operador == '<':
            return df[df[coluna] < valor_float]
        elif operador == '>':
            return df[df[coluna] > valor_float]
        else:
            return df
    except:
        return df


def aplicar_filtro_texto(df, coluna, operador, valor):
    """
    Aplica filtro de texto em uma coluna
    """
    try:
        if operador == '=':
            return df[df[coluna].astype(str) == str(valor)]
        elif operador == '≠':
            return df[df[coluna].astype(str) != str(valor)]
        else:
            return df
    except:
        return df


def criar_painel_filtros(df, key_prefix=""):
    """
    Cria painel de filtros avançados na sidebar
    
    Args:
        df: DataFrame a ser filtrado
        key_prefix: Prefixo único para as keys dos widgets (evita IDs duplicados)
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 🔍 Filtros Avançados")
    
    df_filtrado = df.copy()
    filtros_aplicados = []
    
    # Filtro por CFOP
    with st.sidebar.expander("📋 Filtrar por CFOP"):
        if 'CFOP' in df.columns:
            cfops_disponiveis = sorted(df['CFOP'].dropna().unique())
            cfop_selecionado = st.multiselect(
                "Selecione CFOPs",
                options=cfops_disponiveis,
                key=f"{key_prefix}_filtro_cfop"
            )
            
            if cfop_selecionado:
                df_filtrado = df_filtrado[df_filtrado['CFOP'].isin(cfop_selecionado)]
                filtros_aplicados.append(f"CFOP: {', '.join(map(str, cfop_selecionado))}")
    
    # Filtro por Participante
    with st.sidebar.expander("👥 Filtrar por Participante"):
        if 'COD_PART' in df.columns:
            participantes = sorted(df['COD_PART'].dropna().unique())
            part_selecionado = st.multiselect(
                "Selecione Participantes",
                options=participantes,
                key=f"{key_prefix}_filtro_participante"
            )
            
            if part_selecionado:
                df_filtrado = df_filtrado[df_filtrado['COD_PART'].isin(part_selecionado)]
                filtros_aplicados.append(f"Participante: {', '.join(map(str, part_selecionado))}")
    
    # Filtro por CST ICMS
    with st.sidebar.expander("🏷️ Filtrar por CST ICMS"):
        if 'CST_ICMS' in df.columns:
            csts = sorted(df['CST_ICMS'].dropna().unique())
            cst_selecionado = st.multiselect(
                "Selecione CST ICMS",
                options=csts,
                key=f"{key_prefix}_filtro_cst_icms"
            )
            
            if cst_selecionado:
                df_filtrado = df_filtrado[df_filtrado['CST_ICMS'].isin(cst_selecionado)]
                filtros_aplicados.append(f"CST ICMS: {', '.join(map(str, cst_selecionado))}")
    
    # Filtro por Valor do Documento
    with st.sidebar.expander("💰 Filtrar por Valor"):
        if 'VL_DOC' in df.columns:
            col1, col2 = st.columns(2)
            with col1:
                operador_valor = st.selectbox(
                    "Operador",
                    options=['=', '≠', '<', '>'],
                    key=f"{key_prefix}_op_valor"
                )
            with col2:
                valor_filtro = st.number_input(
                    "Valor",
                    min_value=0.0,
                    value=0.0,
                    step=100.0,
                    key=f"{key_prefix}_valor_filtro"
                )
            
            aplicar_filtro_valor = st.button("Aplicar Filtro Valor", key=f"{key_prefix}_btn_valor")
            
            if aplicar_filtro_valor and valor_filtro > 0:
                df_filtrado = aplicar_filtro_numerico(df_filtrado, 'VL_DOC', operador_valor, valor_filtro)
                filtros_aplicados.append(f"Valor {operador_valor} R$ {valor_filtro:,.2f}")
    
    # Filtro por Data
    with st.sidebar.expander("📅 Filtrar por Data"):
        if 'DT_DOC' in df.columns:
            df_temp = df_filtrado.copy()
            df_temp['DATA_CONV'] = pd.to_datetime(df_temp['DT_DOC'], format='%d%m%Y', errors='coerce')
            
            if not df_temp['DATA_CONV'].isna().all():
                data_min = df_temp['DATA_CONV'].min()
                data_max = df_temp['DATA_CONV'].max()
                
                col1, col2 = st.columns(2)
                with col1:
                    data_inicio = st.date_input(
                        "Data Início",
                        value=data_min,
                        min_value=data_min,
                        max_value=data_max,
                        key=f"{key_prefix}_data_inicio"
                    )
                
                with col2:
                    data_fim = st.date_input(
                        "Data Fim",
                        value=data_max,
                        min_value=data_min,
                        max_value=data_max,
                        key=f"{key_prefix}_data_fim"
                    )
                
                aplicar_filtro_data = st.button("Aplicar Filtro Data", key=f"{key_prefix}_btn_data")
                
                if aplicar_filtro_data:
                    df_filtrado = df_temp[
                        (df_temp['DATA_CONV'] >= pd.to_datetime(data_inicio)) &
                        (df_temp['DATA_CONV'] <= pd.to_datetime(data_fim))
                    ].drop(columns=['DATA_CONV'])
                    filtros_aplicados.append(f"Data: {data_inicio} a {data_fim}")
    
    # Botão para limpar filtros
    if st.sidebar.button("🔄 Limpar Todos os Filtros", key=f"{key_prefix}_btn_limpar"):
        st.rerun()
    
    return df_filtrado, filtros_aplicados


def exibir_resumo_filtros(filtros_aplicados):
    """
    Exibe resumo dos filtros aplicados
    """
    if filtros_aplicados:
        st.info(f"🔍 **Filtros Ativos:** {' | '.join(filtros_aplicados)}")
    else:
        st.success("✅ Nenhum filtro aplicado - Exibindo todos os dados")
