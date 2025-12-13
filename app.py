"""
Analisador de SPED ICMS/IPI
Sistema com múltiplas abas e upload global
"""

import streamlit as st
import pandas as pd
import zipfile
import io
from sped_parser import processar_multiplos_speds
from parser_registros_0 import processar_multiplos_speds_registros_0
from dashboards_bigfour import exibir_dashboard_executivo
from filtros_avancados import criar_painel_filtros, exibir_resumo_filtros
from acumuladores_cfop import exibir_acumulador_cfop

# Configuração da página
st.set_page_config(
    page_title="Analisador SPED ICMS/IPI",
    page_icon="📊",
    layout="wide"
)

# Título principal
st.title("📊 Analisador de SPED ICMS/IPI")
st.markdown("### Sistema Completo de Análise Fiscal - EFD ICMS/IPI")
st.markdown("---")

# ========================================================================
# UPLOAD GLOBAL (UMA VEZ SÓ)
# ========================================================================

st.subheader("📁 Upload de Arquivos SPED")
st.markdown("Faça upload de até 12 arquivos SPED (.txt ou .zip)")

uploaded_files = st.file_uploader(
    "Selecione os arquivos",
    type=['txt', 'zip'],
    accept_multiple_files=True,
    help="Arquivos SPED ICMS/IPI em formato .txt ou .zip"
)

# Inicializa variáveis de dados
dados_c = {}
dados_0 = {}

# ========================================================================
# PROCESSAMENTO (SE HOUVER UPLOAD)
# ========================================================================

if uploaded_files:
    with st.spinner("🔄 Processando arquivos SPED..."):
        # Processa registros C (documentos fiscais)
        dados_c = processar_multiplos_speds(uploaded_files)
        
        # Reseta ponteiro dos arquivos para processar registros 0
        for file in uploaded_files:
            file.seek(0)
        
        # Processa registros 0 (cadastros)
        dados_0 = processar_multiplos_speds_registros_0(uploaded_files)
    
    st.success(f"✅ {len(uploaded_files)} arquivo(s) processado(s) com sucesso!")
    
    # ========================================================================
    # ABAS DE NAVEGAÇÃO
    # ========================================================================
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Dashboard",
        "📄 Documentos (C100)",
        "📦 Itens (C170)",
        "📈 Analítico (C190)",
        "👥 Participantes (0150)",
        "🏷️ Produtos (0200)",
        "🎯 Acumulador CFOP"
    ])
    
    # ========================================================================
    # ABA 1: DASHBOARD EXECUTIVO
    # ========================================================================
    
    with tab1:
        df_c100 = dados_c.get('C100', pd.DataFrame())
        df_c190 = dados_c.get('C190', pd.DataFrame())
        
        if not df_c100.empty or not df_c190.empty:
            exibir_dashboard_executivo(df_c100, df_c190)
        else:
            st.warning("⚠️ Não há dados para exibir o dashboard")
    
    # ========================================================================
    # ABA 2: DOCUMENTOS FISCAIS (C100)
    # ========================================================================
    
    with tab2:
        st.markdown("## 📄 Documentos Fiscais - Registro C100")
        st.markdown("Notas Fiscais (NF-e, NFC-e, Modelo 01, 04, etc.)")
        st.markdown("---")
        
        df_c100 = dados_c.get('C100', pd.DataFrame())
        
        if not df_c100.empty:
            # Aplica filtros
            df_filtrado, filtros = criar_painel_filtros(df_c100, key_prefix="c100")
            exibir_resumo_filtros(filtros)
            
            # Estatísticas
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total de Documentos", len(df_filtrado))
            
            with col2:
                total_valor = df_filtrado['VL_DOC'].sum()
                st.metric("Valor Total", f"R$ {total_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            
            with col3:
                total_icms = df_filtrado['VL_ICMS'].sum()
                st.metric("Total ICMS", f"R$ {total_icms:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            
            with col4:
                total_ipi = df_filtrado['VL_IPI'].sum()
                st.metric("Total IPI", f"R$ {total_ipi:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Tabela de dados
            st.dataframe(
                df_filtrado,
                use_container_width=True,
                hide_index=True
            )
            
            # Download
            csv = df_filtrado.to_csv(index=False, sep=';', decimal=',')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="documentos_c100.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ Não há registros C100 para exibir")
    
    # ========================================================================
    # ABA 3: ITENS DOS DOCUMENTOS (C170)
    # ========================================================================
    
    with tab3:
        st.markdown("## 📦 Itens dos Documentos - Registro C170")
        st.markdown("Detalhamento de produtos/serviços das notas fiscais")
        st.markdown("---")
        
        df_c170 = dados_c.get('C170', pd.DataFrame())
        
        if not df_c170.empty:
            # Aplica filtros
            df_filtrado, filtros = criar_painel_filtros(df_c170, key_prefix="c170")
            exibir_resumo_filtros(filtros)
            
            # Estatísticas
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total de Itens", len(df_filtrado))
            
            with col2:
                total_valor = df_filtrado['VL_ITEM'].sum()
                st.metric("Valor Total", f"R$ {total_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            
            with col3:
                total_icms = df_filtrado['VL_ICMS'].sum()
                st.metric("Total ICMS", f"R$ {total_icms:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            
            with col4:
                total_ipi = df_filtrado['VL_IPI'].sum()
                st.metric("Total IPI", f"R$ {total_ipi:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Tabela de dados
            st.dataframe(
                df_filtrado,
                use_container_width=True,
                hide_index=True
            )
            
            # Download
            csv = df_filtrado.to_csv(index=False, sep=';', decimal=',')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="itens_c170.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ Não há registros C170 para exibir")
    
    # ========================================================================
    # ABA 4: REGISTRO ANALÍTICO (C190)
    # ========================================================================
    
    with tab4:
        st.markdown("## 📈 Registro Analítico - C190")
        st.markdown("Consolidação por CST ICMS e CFOP")
        st.markdown("---")
        
        df_c190 = dados_c.get('C190', pd.DataFrame())
        
        if not df_c190.empty:
            # Aplica filtros
            df_filtrado, filtros = criar_painel_filtros(df_c190, key_prefix="c190")
            exibir_resumo_filtros(filtros)
            
            # Estatísticas
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total de Registros", len(df_filtrado))
            
            with col2:
                total_operacao = df_filtrado['VL_OPR'].sum()
                st.metric("Valor Operação", f"R$ {total_operacao:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            
            with col3:
                total_icms = df_filtrado['VL_ICMS'].sum()
                st.metric("Total ICMS", f"R$ {total_icms:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            
            with col4:
                total_ipi = df_filtrado['VL_IPI'].sum()
                st.metric("Total IPI", f"R$ {total_ipi:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Tabela de dados
            st.dataframe(
                df_filtrado,
                use_container_width=True,
                hide_index=True
            )
            
            # Download
            csv = df_filtrado.to_csv(index=False, sep=';', decimal=',')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="analitico_c190.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ Não há registros C190 para exibir")
    
    # ========================================================================
    # ABA 5: PARTICIPANTES (0150)
    # ========================================================================
    
    with tab5:
        st.markdown("## 👥 Cadastro de Participantes - Registro 0150")
        st.markdown("Fornecedores, clientes e outros participantes")
        st.markdown("---")
        
        df_0150 = dados_0.get('0150', pd.DataFrame())
        
        if not df_0150.empty:
            # Estatísticas
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total de Participantes", len(df_0150))
            
            with col2:
                com_cnpj = df_0150['CNPJ'].notna().sum()
                st.metric("Com CNPJ", com_cnpj)
            
            with col3:
                com_cpf = df_0150['CPF'].notna().sum()
                st.metric("Com CPF", com_cpf)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Busca por nome
            busca = st.text_input("🔍 Buscar por nome ou código", key="busca_participante")
            
            if busca:
                df_filtrado = df_0150[
                    df_0150['NOME'].str.contains(busca, case=False, na=False) |
                    df_0150['COD_PART'].astype(str).str.contains(busca, case=False, na=False)
                ]
            else:
                df_filtrado = df_0150
            
            # Tabela de dados
            st.dataframe(
                df_filtrado,
                use_container_width=True,
                hide_index=True
            )
            
            # Download
            csv = df_filtrado.to_csv(index=False, sep=';', decimal=',')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="participantes_0150.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ Não há registros 0150 para exibir")
    
    # ========================================================================
    # ABA 6: PRODUTOS (0200)
    # ========================================================================
    
    with tab6:
        st.markdown("## 🏷️ Cadastro de Produtos - Registro 0200")
        st.markdown("Itens comercializados (produtos e serviços)")
        st.markdown("---")
        
        df_0200 = dados_0.get('0200', pd.DataFrame())
        
        if not df_0200.empty:
            # Estatísticas
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total de Produtos", len(df_0200))
            
            with col2:
                com_ncm = df_0200['COD_NCM'].notna().sum()
                st.metric("Com NCM", com_ncm)
            
            with col3:
                tipos = df_0200['TIPO_ITEM'].nunique()
                st.metric("Tipos de Item", tipos)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Busca por descrição
            busca = st.text_input("🔍 Buscar por descrição ou código", key="busca_produto")
            
            if busca:
                df_filtrado = df_0200[
                    df_0200['DESCR_ITEM'].str.contains(busca, case=False, na=False) |
                    df_0200['COD_ITEM'].astype(str).str.contains(busca, case=False, na=False)
                ]
            else:
                df_filtrado = df_0200
            
            # Tabela de dados
            st.dataframe(
                df_filtrado,
                use_container_width=True,
                hide_index=True
            )
            
            # Download
            csv = df_filtrado.to_csv(index=False, sep=';', decimal=',')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="produtos_0200.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ Não há registros 0200 para exibir")
    
    # ========================================================================
    # ABA 7: ACUMULADOR POR CFOP
    # ========================================================================
    
    with tab7:
        df_c190 = dados_c.get('C190', pd.DataFrame())
        
        if not df_c190.empty:
            exibir_acumulador_cfop(df_c190)
        else:
            st.warning("⚠️ Não há dados C190 para exibir o acumulador")

else:
    # Mensagem inicial quando não há upload
    st.info("👆 Faça upload de um ou mais arquivos SPED ICMS/IPI para começar a análise")
    
    # Informações sobre o sistema
    with st.expander("ℹ️ Sobre o Sistema"):
        st.markdown("""
        ### 📊 Analisador de SPED ICMS/IPI
        
        Este sistema processa arquivos SPED EFD ICMS/IPI e oferece:
        
        **Registros Processados:**
        - **Bloco 0**: Cadastros (0000, 0005, 0100, 0150, 0200)
        - **Bloco C**: Documentos Fiscais (C100, C110, C113, C170, C190, C195, C197)
        
        **Funcionalidades:**
        - ✅ Upload de múltiplos arquivos (.txt ou .zip)
        - ✅ Dashboard executivo com gráficos interativos
        - ✅ Análise detalhada de documentos fiscais
        - ✅ Análise de itens e produtos
        - ✅ Cadastro de participantes
        - ✅ Acumuladores por CFOP e CST
        - ✅ Filtros avançados
        - ✅ Exportação para CSV
        
        **Desenvolvido com:**
        - Python 3.11+
        - Streamlit
        - Pandas
        - Plotly
        """)
    
    with st.expander("📖 Como Usar"):
        st.markdown("""
        ### Passo a Passo
        
        1. **Upload**: Clique no botão acima e selecione seus arquivos SPED
        2. **Aguarde**: O sistema processará automaticamente os arquivos
        3. **Navegue**: Use as abas para explorar diferentes análises
        4. **Filtre**: Use a barra lateral para aplicar filtros
        5. **Exporte**: Baixe os dados em formato CSV
        
        ### Formatos Aceitos
        - `.txt` - Arquivo SPED texto
        - `.zip` - Arquivo compactado contendo SPEDs
        
        ### Dicas
        - Você pode fazer upload de até 12 arquivos simultaneamente
        - Os filtros são aplicados em tempo real
        - Use o acumulador CFOP para análise consolidada
        """)

# ========================================================================
# RODAPÉ
# ========================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px;'>
    📊 Analisador SPED ICMS/IPI | Desenvolvido com Streamlit | 
    <a href='https://github.com/RAFAELSOUZA280292/EFD_ICMS_IPI_Lavoratory' target='_blank'>GitHub</a>
</div>
""", unsafe_allow_html=True)
