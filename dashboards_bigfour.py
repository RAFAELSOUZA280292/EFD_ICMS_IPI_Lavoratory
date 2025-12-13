"""
Dashboards Profissionais - Estilo Big Four
Módulo para criar visualizações executivas de alto nível para SPED ICMS/IPI
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st


# Paleta de cores profissional (estilo Big Four)
COLORS = {
    'primary': '#003366',      # Azul escuro corporativo
    'secondary': '#0066CC',    # Azul médio
    'accent': '#FF6B35',       # Laranja destaque
    'success': '#2ECC71',      # Verde sucesso
    'warning': '#F39C12',      # Amarelo alerta
    'danger': '#E74C3C',       # Vermelho perigo
    'neutral': '#95A5A6',      # Cinza neutro
    'background': '#F8F9FA'    # Fundo claro
}

# Paleta para gráficos de pizza (10 cores distintas)
PIZZA_COLORS = [
    '#003366', '#0066CC', '#3399FF', '#66B2FF',
    '#FF6B35', '#FFA07A', '#2ECC71', '#58D68D',
    '#F39C12', '#F8C471'
]


def formatar_valor_br(valor):
    """Formata valor no padrão brasileiro: R$ 1.234,56"""
    try:
        valor_str = f"{valor:,.2f}"
        valor_str = valor_str.replace(',', 'TEMP').replace('.', ',').replace('TEMP', '.')
        return f"R$ {valor_str}"
    except:
        return "R$ 0,00"


def criar_kpi_card(titulo, valor, subtitulo="", cor=COLORS['primary']):
    """Cria um card KPI profissional"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {cor} 0%, {cor}DD 100%);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: white;
        text-align: center;
    ">
        <div style="font-size: 14px; font-weight: 500; opacity: 0.9; margin-bottom: 8px;">
            {titulo}
        </div>
        <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">
            {valor}
        </div>
        <div style="font-size: 12px; opacity: 0.8;">
            {subtitulo}
        </div>
    </div>
    """, unsafe_allow_html=True)


def criar_grafico_pizza_top10_icms(df_c190):
    """
    Cria gráfico de pizza TOP 10 CFOP com maior ICMS
    """
    if df_c190.empty:
        return None
    
    # Agrupa por CFOP e soma ICMS
    top10 = df_c190.groupby('CFOP').agg({
        'VL_ICMS': 'sum'
    }).reset_index()
    
    # Ordena e pega TOP 10
    top10 = top10.sort_values('VL_ICMS', ascending=False).head(10)
    
    # Cria labels com CFOP e valor
    top10['label'] = top10.apply(
        lambda x: f"CFOP {x['CFOP']}<br>{formatar_valor_br(x['VL_ICMS'])}", 
        axis=1
    )
    
    fig = go.Figure(data=[go.Pie(
        labels=top10['label'],
        values=top10['VL_ICMS'],
        hole=0.4,
        marker=dict(colors=PIZZA_COLORS),
        textposition='auto',
        textinfo='percent',
        hovertemplate='<b>%{label}</b><br>Valor: %{value:,.2f}<br>Percentual: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title={
            'text': '🏆 TOP 10 CFOPs - Maior ICMS',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': COLORS['primary'], 'family': 'Arial Black'}
        },
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(size=10)
        ),
        height=500,
        margin=dict(l=20, r=150, t=80, b=20)
    )
    
    return fig


def criar_grafico_pizza_top10_ipi(df_c190):
    """
    Cria gráfico de pizza TOP 10 CFOP com maior IPI
    """
    if df_c190.empty:
        return None
    
    # Filtra apenas registros com IPI > 0
    df_ipi = df_c190[df_c190['VL_IPI'] > 0].copy()
    
    if df_ipi.empty:
        return None
    
    # Agrupa por CFOP e soma IPI
    top10 = df_ipi.groupby('CFOP').agg({
        'VL_IPI': 'sum'
    }).reset_index()
    
    # Ordena e pega TOP 10
    top10 = top10.sort_values('VL_IPI', ascending=False).head(10)
    
    # Cria labels com CFOP e valor
    top10['label'] = top10.apply(
        lambda x: f"CFOP {x['CFOP']}<br>{formatar_valor_br(x['VL_IPI'])}", 
        axis=1
    )
    
    fig = go.Figure(data=[go.Pie(
        labels=top10['label'],
        values=top10['VL_IPI'],
        hole=0.4,
        marker=dict(colors=PIZZA_COLORS),
        textposition='auto',
        textinfo='percent',
        hovertemplate='<b>%{label}</b><br>Valor: %{value:,.2f}<br>Percentual: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title={
            'text': '🏆 TOP 10 CFOPs - Maior IPI',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': COLORS['primary'], 'family': 'Arial Black'}
        },
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(size=10)
        ),
        height=500,
        margin=dict(l=20, r=150, t=80, b=20)
    )
    
    return fig


def criar_grafico_barras_entrada_saida(df_c100):
    """
    Cria gráfico de barras comparando Entrada vs Saída
    """
    if df_c100.empty:
        return None
    
    # Agrupa por tipo de operação
    resumo = df_c100.groupby('IND_OPER').agg({
        'VL_DOC': 'sum',
        'VL_ICMS': 'sum',
        'VL_IPI': 'sum'
    }).reset_index()
    
    # Mapeia indicador de operação
    resumo['OPERACAO'] = resumo['IND_OPER'].map({'0': 'Entrada', '1': 'Saída'})
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Valor Total',
        x=resumo['OPERACAO'],
        y=resumo['VL_DOC'],
        marker_color=COLORS['primary'],
        text=resumo['VL_DOC'].apply(formatar_valor_br),
        textposition='outside'
    ))
    
    fig.add_trace(go.Bar(
        name='ICMS',
        x=resumo['OPERACAO'],
        y=resumo['VL_ICMS'],
        marker_color=COLORS['success'],
        text=resumo['VL_ICMS'].apply(formatar_valor_br),
        textposition='outside'
    ))
    
    fig.add_trace(go.Bar(
        name='IPI',
        x=resumo['OPERACAO'],
        y=resumo['VL_IPI'],
        marker_color=COLORS['accent'],
        text=resumo['VL_IPI'].apply(formatar_valor_br),
        textposition='outside'
    ))
    
    fig.update_layout(
        title={
            'text': '📊 Comparativo: Entrada vs Saída',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': COLORS['primary'], 'family': 'Arial Black'}
        },
        barmode='group',
        xaxis_title='Tipo de Operação',
        yaxis_title='Valor (R$)',
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig


def criar_grafico_linha_temporal(df_c100):
    """
    Cria gráfico de linha temporal com valores por data
    """
    if df_c100.empty or 'DT_DOC' not in df_c100.columns:
        return None
    
    # Converte data
    df_temp = df_c100.copy()
    df_temp['DATA'] = pd.to_datetime(df_temp['DT_DOC'], format='%d%m%Y', errors='coerce')
    df_temp = df_temp.dropna(subset=['DATA'])
    
    if df_temp.empty:
        return None
    
    # Agrupa por data
    timeline = df_temp.groupby('DATA').agg({
        'VL_DOC': 'sum',
        'VL_ICMS': 'sum',
        'VL_IPI': 'sum'
    }).reset_index()
    
    timeline = timeline.sort_values('DATA')
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=timeline['DATA'],
        y=timeline['VL_DOC'],
        mode='lines+markers',
        name='Valor Total',
        line=dict(color=COLORS['primary'], width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=timeline['DATA'],
        y=timeline['VL_ICMS'],
        mode='lines+markers',
        name='ICMS',
        line=dict(color=COLORS['success'], width=2),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=timeline['DATA'],
        y=timeline['VL_IPI'],
        mode='lines+markers',
        name='IPI',
        line=dict(color=COLORS['accent'], width=2),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title={
            'text': '📈 Evolução Temporal dos Valores',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': COLORS['primary'], 'family': 'Arial Black'}
        },
        xaxis_title='Data',
        yaxis_title='Valor (R$)',
        height=500,
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig


def exibir_dashboard_executivo(df_c100, df_c190):
    """
    Exibe dashboard executivo completo
    """
    st.markdown("## 📊 Dashboard Executivo")
    st.markdown("---")
    
    # KPIs principais
    if not df_c100.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_docs = len(df_c100)
            criar_kpi_card(
                "Total de Documentos",
                f"{total_docs:,}".replace(',', '.'),
                "Notas Fiscais",
                COLORS['primary']
            )
        
        with col2:
            total_valor = df_c100['VL_DOC'].sum()
            criar_kpi_card(
                "Valor Total",
                formatar_valor_br(total_valor),
                "Soma de todas as NFs",
                COLORS['secondary']
            )
        
        with col3:
            total_icms = df_c100['VL_ICMS'].sum()
            criar_kpi_card(
                "Total ICMS",
                formatar_valor_br(total_icms),
                "Imposto sobre Circulação",
                COLORS['success']
            )
        
        with col4:
            total_ipi = df_c100['VL_IPI'].sum()
            criar_kpi_card(
                "Total IPI",
                formatar_valor_br(total_ipi),
                "Imposto sobre Produtos",
                COLORS['accent']
            )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gráficos principais
    col1, col2 = st.columns(2)
    
    with col1:
        if not df_c190.empty:
            fig_pizza_icms = criar_grafico_pizza_top10_icms(df_c190)
            if fig_pizza_icms:
                st.plotly_chart(fig_pizza_icms, use_container_width=True)
    
    with col2:
        if not df_c190.empty:
            fig_pizza_ipi = criar_grafico_pizza_top10_ipi(df_c190)
            if fig_pizza_ipi:
                st.plotly_chart(fig_pizza_ipi, use_container_width=True)
            else:
                st.info("ℹ️ Não há dados de IPI para exibir")
    
    # Gráfico de barras
    if not df_c100.empty:
        fig_barras = criar_grafico_barras_entrada_saida(df_c100)
        if fig_barras:
            st.plotly_chart(fig_barras, use_container_width=True)
    
    # Gráfico temporal
    if not df_c100.empty:
        fig_linha = criar_grafico_linha_temporal(df_c100)
        if fig_linha:
            st.plotly_chart(fig_linha, use_container_width=True)
