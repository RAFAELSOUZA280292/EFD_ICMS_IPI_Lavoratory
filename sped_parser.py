"""
Parser de Registros C (Documentos Fiscais) do SPED ICMS/IPI
Processa registros C100, C110, C113, C170, C190, C195, C197
"""

import pandas as pd
import io
import zipfile
from datetime import datetime


def parse_registro_c100(linha):
    """
    C100: Nota Fiscal (código 01), Nota Fiscal Avulsa (código 1B), 
    Nota Fiscal de Produtor (código 04), NF-e (código 55) e NFC-e (código 65)
    """
    campos = linha.split('|')
    
    try:
        return {
            'REG': campos[1],
            'IND_OPER': campos[2],  # 0=Entrada, 1=Saída
            'IND_EMIT': campos[3],  # 0=Emissão própria, 1=Terceiros
            'COD_PART': campos[4],
            'COD_MOD': campos[5],  # Código do modelo do documento fiscal
            'COD_SIT': campos[6],  # Situação do documento
            'SER': campos[7],  # Série do documento
            'NUM_DOC': campos[8],  # Número do documento
            'CHV_NFE': campos[9],  # Chave da NF-e
            'DT_DOC': campos[10],  # Data de emissão
            'DT_E_S': campos[11],  # Data de entrada/saída
            'VL_DOC': campos[12],  # Valor total do documento
            'IND_PGTO': campos[13],  # Indicador do tipo de pagamento
            'VL_DESC': campos[14],  # Valor total do desconto
            'VL_ABAT_NT': campos[15],  # Abatimento não tributado
            'VL_MERC': campos[16],  # Valor das mercadorias
            'IND_FRT': campos[17],  # Indicador do tipo de frete
            'VL_FRT': campos[18],  # Valor do frete
            'VL_SEG': campos[19],  # Valor do seguro
            'VL_OUT_DA': campos[20],  # Outras despesas acessórias
            'VL_BC_ICMS': campos[21],  # Base de cálculo do ICMS
            'VL_ICMS': campos[22],  # Valor do ICMS
            'VL_BC_ICMS_ST': campos[23],  # Base de cálculo do ICMS ST
            'VL_ICMS_ST': campos[24],  # Valor do ICMS ST
            'VL_IPI': campos[25],  # Valor total do IPI
            'VL_PIS': campos[26],  # Valor do PIS
            'VL_COFINS': campos[27],  # Valor da COFINS
            'VL_PIS_ST': campos[28],  # Valor do PIS retido por ST
            'VL_COFINS_ST': campos[29],  # Valor da COFINS retido por ST
        }
    except IndexError:
        return None


def parse_registro_c110(linha):
    """
    C110: Informação Complementar da Nota Fiscal
    """
    campos = linha.split('|')
    
    try:
        return {
            'REG': campos[1],
            'COD_INF': campos[2],  # Código da informação complementar
            'TXT_COMPL': campos[3],  # Texto complementar
        }
    except IndexError:
        return None


def parse_registro_c113(linha):
    """
    C113: Documento Fiscal Referenciado
    """
    campos = linha.split('|')
    
    try:
        return {
            'REG': campos[1],
            'IND_OPER': campos[2],
            'IND_EMIT': campos[3],
            'COD_PART': campos[4],
            'COD_MOD': campos[5],
            'SER': campos[6],
            'SUB': campos[7],
            'NUM_DOC': campos[8],
            'DT_DOC': campos[9],
            'CHV_DOCe': campos[10] if len(campos) > 10 else '',
        }
    except IndexError:
        return None


def parse_registro_c170(linha):
    """
    C170: Itens do Documento (código 01, 1B, 04, 55 e 65)
    """
    campos = linha.split('|')
    
    try:
        return {
            'REG': campos[1],
            'NUM_ITEM': campos[2],  # Número sequencial do item
            'COD_ITEM': campos[3],  # Código do item
            'DESCR_COMPL': campos[4],  # Descrição complementar
            'QTD': campos[5],  # Quantidade
            'UNID': campos[6],  # Unidade
            'VL_ITEM': campos[7],  # Valor total do item
            'VL_DESC': campos[8],  # Valor do desconto
            'IND_MOV': campos[9],  # Movimentação física
            'CST_ICMS': campos[10],  # Código da Situação Tributária ICMS
            'CFOP': campos[11],  # Código Fiscal de Operação
            'COD_NAT': campos[12],  # Código da natureza da operação
            'VL_BC_ICMS': campos[13],  # Base de cálculo do ICMS
            'ALIQ_ICMS': campos[14],  # Alíquota do ICMS
            'VL_ICMS': campos[15],  # Valor do ICMS
            'VL_BC_ICMS_ST': campos[16],  # Base de cálculo do ICMS ST
            'ALIQ_ST': campos[17],  # Alíquota do ICMS ST
            'VL_ICMS_ST': campos[18],  # Valor do ICMS ST
            'IND_APUR': campos[19],  # Indicador de período de apuração
            'CST_IPI': campos[20],  # Código da Situação Tributária IPI
            'COD_ENQ': campos[21],  # Código de enquadramento legal IPI
            'VL_BC_IPI': campos[22],  # Base de cálculo do IPI
            'ALIQ_IPI': campos[23],  # Alíquota do IPI
            'VL_IPI': campos[24],  # Valor do IPI
            'CST_PIS': campos[25],  # Código da Situação Tributária PIS
            'VL_BC_PIS': campos[26],  # Base de cálculo do PIS
            'ALIQ_PIS': campos[27],  # Alíquota do PIS
            'QUANT_BC_PIS': campos[28],  # Quantidade BC PIS
            'ALIQ_PIS_QUANT': campos[29],  # Alíquota do PIS em reais
            'VL_PIS': campos[30],  # Valor do PIS
            'CST_COFINS': campos[31],  # Código da Situação Tributária COFINS
            'VL_BC_COFINS': campos[32],  # Base de cálculo da COFINS
            'ALIQ_COFINS': campos[33],  # Alíquota da COFINS
            'QUANT_BC_COFINS': campos[34],  # Quantidade BC COFINS
            'ALIQ_COFINS_QUANT': campos[35],  # Alíquota da COFINS em reais
            'VL_COFINS': campos[36],  # Valor da COFINS
            'COD_CTA': campos[37] if len(campos) > 37 else '',  # Código da conta analítica
        }
    except IndexError:
        return None


def parse_registro_c190(linha):
    """
    C190: Registro Analítico do Documento (código 01, 1B, 04, 55 e 65)
    """
    campos = linha.split('|')
    
    try:
        return {
            'REG': campos[1],
            'CST_ICMS': campos[2],  # Código da Situação Tributária ICMS
            'CFOP': campos[3],  # Código Fiscal de Operação
            'ALIQ_ICMS': campos[4],  # Alíquota do ICMS
            'VL_OPR': campos[5],  # Valor da operação
            'VL_BC_ICMS': campos[6],  # Base de cálculo do ICMS
            'VL_ICMS': campos[7],  # Valor do ICMS
            'VL_BC_ICMS_ST': campos[8],  # Base de cálculo do ICMS ST
            'VL_ICMS_ST': campos[9],  # Valor do ICMS ST
            'VL_RED_BC': campos[10],  # Valor não tributado
            'VL_IPI': campos[11],  # Valor do IPI
            'COD_OBS': campos[12] if len(campos) > 12 else '',  # Código da observação
        }
    except IndexError:
        return None


def parse_registro_c195(linha):
    """
    C195: Observações do Lançamento Fiscal
    """
    campos = linha.split('|')
    
    try:
        return {
            'REG': campos[1],
            'COD_OBS': campos[2],  # Código da observação
            'TXT_COMPL': campos[3],  # Descrição complementar
        }
    except IndexError:
        return None


def parse_registro_c197(linha):
    """
    C197: Outras Obrigações Tributárias, Ajustes e Informações
    """
    campos = linha.split('|')
    
    try:
        return {
            'REG': campos[1],
            'COD_AJ': campos[2],  # Código do ajuste
            'DESCR_COMPL_AJ': campos[3],  # Descrição complementar
            'COD_ITEM': campos[4],  # Código do item
            'VL_BC_ICMS': campos[5],  # Base de cálculo do ICMS
            'ALIQ_ICMS': campos[6],  # Alíquota do ICMS
            'VL_ICMS': campos[7],  # Valor do ICMS
            'VL_OUTROS': campos[8],  # Outros valores
        }
    except IndexError:
        return None


def processar_arquivo_sped(conteudo):
    """
    Processa um arquivo SPED ICMS/IPI e retorna DataFrames
    """
    linhas = conteudo.decode('latin-1').split('\n')
    
    registros_c100 = []
    registros_c110 = []
    registros_c113 = []
    registros_c170 = []
    registros_c190 = []
    registros_c195 = []
    registros_c197 = []
    
    # Variáveis para controle de contexto
    ultimo_c100 = None
    
    for linha in linhas:
        if not linha.strip():
            continue
            
        campos = linha.split('|')
        if len(campos) < 2:
            continue
            
        tipo_registro = campos[1]
        
        if tipo_registro == 'C100':
            registro = parse_registro_c100(linha)
            if registro:
                registros_c100.append(registro)
                ultimo_c100 = registro
                
        elif tipo_registro == 'C110':
            registro = parse_registro_c110(linha)
            if registro and ultimo_c100:
                registro['NUM_DOC_PAI'] = ultimo_c100.get('NUM_DOC', '')
                registros_c110.append(registro)
                
        elif tipo_registro == 'C113':
            registro = parse_registro_c113(linha)
            if registro and ultimo_c100:
                registro['NUM_DOC_PAI'] = ultimo_c100.get('NUM_DOC', '')
                registros_c113.append(registro)
                
        elif tipo_registro == 'C170':
            registro = parse_registro_c170(linha)
            if registro and ultimo_c100:
                registro['NUM_DOC_PAI'] = ultimo_c100.get('NUM_DOC', '')
                registro['COD_PART_PAI'] = ultimo_c100.get('COD_PART', '')
                registro['DT_DOC_PAI'] = ultimo_c100.get('DT_DOC', '')
                registros_c170.append(registro)
                
        elif tipo_registro == 'C190':
            registro = parse_registro_c190(linha)
            if registro and ultimo_c100:
                registro['NUM_DOC_PAI'] = ultimo_c100.get('NUM_DOC', '')
                registro['COD_PART_PAI'] = ultimo_c100.get('COD_PART', '')
                registro['DT_DOC_PAI'] = ultimo_c100.get('DT_DOC', '')
                registros_c190.append(registro)
                
        elif tipo_registro == 'C195':
            registro = parse_registro_c195(linha)
            if registro and ultimo_c100:
                registro['NUM_DOC_PAI'] = ultimo_c100.get('NUM_DOC', '')
                registros_c195.append(registro)
                
        elif tipo_registro == 'C197':
            registro = parse_registro_c197(linha)
            if registro and ultimo_c100:
                registro['NUM_DOC_PAI'] = ultimo_c100.get('NUM_DOC', '')
                registros_c197.append(registro)
    
    # Criar DataFrames
    df_c100 = pd.DataFrame(registros_c100) if registros_c100 else pd.DataFrame()
    df_c110 = pd.DataFrame(registros_c110) if registros_c110 else pd.DataFrame()
    df_c113 = pd.DataFrame(registros_c113) if registros_c113 else pd.DataFrame()
    df_c170 = pd.DataFrame(registros_c170) if registros_c170 else pd.DataFrame()
    df_c190 = pd.DataFrame(registros_c190) if registros_c190 else pd.DataFrame()
    df_c195 = pd.DataFrame(registros_c195) if registros_c195 else pd.DataFrame()
    df_c197 = pd.DataFrame(registros_c197) if registros_c197 else pd.DataFrame()
    
    # Converter campos numéricos
    colunas_numericas_c100 = ['VL_DOC', 'VL_DESC', 'VL_ABAT_NT', 'VL_MERC', 'VL_FRT', 
                               'VL_SEG', 'VL_OUT_DA', 'VL_BC_ICMS', 'VL_ICMS', 
                               'VL_BC_ICMS_ST', 'VL_ICMS_ST', 'VL_IPI', 'VL_PIS', 
                               'VL_COFINS', 'VL_PIS_ST', 'VL_COFINS_ST']
    
    for col in colunas_numericas_c100:
        if col in df_c100.columns:
            df_c100[col] = pd.to_numeric(df_c100[col].str.replace(',', '.'), errors='coerce').fillna(0)
    
    colunas_numericas_c170 = ['QTD', 'VL_ITEM', 'VL_DESC', 'VL_BC_ICMS', 'ALIQ_ICMS', 
                               'VL_ICMS', 'VL_BC_ICMS_ST', 'ALIQ_ST', 'VL_ICMS_ST',
                               'VL_BC_IPI', 'ALIQ_IPI', 'VL_IPI', 'VL_BC_PIS', 
                               'ALIQ_PIS', 'VL_PIS', 'VL_BC_COFINS', 'ALIQ_COFINS', 'VL_COFINS']
    
    for col in colunas_numericas_c170:
        if col in df_c170.columns:
            df_c170[col] = pd.to_numeric(df_c170[col].str.replace(',', '.'), errors='coerce').fillna(0)
    
    colunas_numericas_c190 = ['ALIQ_ICMS', 'VL_OPR', 'VL_BC_ICMS', 'VL_ICMS', 
                               'VL_BC_ICMS_ST', 'VL_ICMS_ST', 'VL_RED_BC', 'VL_IPI']
    
    for col in colunas_numericas_c190:
        if col in df_c190.columns:
            df_c190[col] = pd.to_numeric(df_c190[col].str.replace(',', '.'), errors='coerce').fillna(0)
    
    return {
        'C100': df_c100,
        'C110': df_c110,
        'C113': df_c113,
        'C170': df_c170,
        'C190': df_c190,
        'C195': df_c195,
        'C197': df_c197
    }


def processar_multiplos_speds(uploaded_files):
    """
    Processa múltiplos arquivos SPED e consolida em um único DataFrame
    """
    dfs_consolidados = {
        'C100': [],
        'C110': [],
        'C113': [],
        'C170': [],
        'C190': [],
        'C195': [],
        'C197': []
    }
    
    for uploaded_file in uploaded_files:
        try:
            if uploaded_file.name.endswith('.zip'):
                # Processar arquivo ZIP
                with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                    for file_name in zip_ref.namelist():
                        if file_name.endswith('.txt'):
                            with zip_ref.open(file_name) as file:
                                conteudo = file.read()
                                resultado = processar_arquivo_sped(conteudo)
                                
                                for tipo, df in resultado.items():
                                    if not df.empty:
                                        df['ARQUIVO_ORIGEM'] = uploaded_file.name
                                        dfs_consolidados[tipo].append(df)
            else:
                # Processar arquivo TXT
                conteudo = uploaded_file.read()
                resultado = processar_arquivo_sped(conteudo)
                
                for tipo, df in resultado.items():
                    if not df.empty:
                        df['ARQUIVO_ORIGEM'] = uploaded_file.name
                        dfs_consolidados[tipo].append(df)
                        
        except Exception as e:
            print(f"Erro ao processar {uploaded_file.name}: {str(e)}")
            continue
    
    # Consolidar DataFrames
    resultado_final = {}
    for tipo, lista_dfs in dfs_consolidados.items():
        if lista_dfs:
            resultado_final[tipo] = pd.concat(lista_dfs, ignore_index=True)
        else:
            resultado_final[tipo] = pd.DataFrame()
    
    return resultado_final
