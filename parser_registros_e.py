"""
================================================================================
PARSER: Registros E - Apuração do ICMS e do IPI
================================================================================

OBJETIVO:
    Extrair dados de apuração de ICMS e IPI dos registros E

REGISTROS IMPLEMENTADOS:
    - E100: Período da Apuração do ICMS
    - E110: Apuração do ICMS - Operações Próprias
    - E111: Ajuste/Benefício/Incentivo da Apuração do ICMS
    - E116: Obrigações do ICMS Recolhido ou a Recolher - Operações Próprias

ESTRUTURA DOS REGISTROS:
========================

E100: Período da Apuração
|E100|DT_INI|DT_FIN|

E110: Apuração do ICMS
|E110|VL_TOT_DEBITOS|VL_AJ_DEBITOS|VL_TOT_AJ_DEBITOS|VL_ESTORNOS_CRED|
     |VL_TOT_CREDITOS|VL_AJ_CREDITOS|VL_TOT_AJ_CREDITOS|VL_ESTORNOS_DEB|
     |VL_SLD_CREDOR_ANT|VL_SLD_APURADO|VL_TOT_DED|VL_ICMS_RECOLHER|
     |VL_SLD_CREDOR_TRANSPORTAR|DEB_ESP|

E111: Ajustes da Apuração
|E111|COD_AJ_APUR|DESCR_COMPL_AJ|VL_AJ_APUR|

E116: Obrigações ICMS Recolhido/A Recolher
|E116|COD_OR|VL_OR|DT_VCTO|COD_REC|NUM_PROC|IND_PROC|PROC|TXT_COMPL|MES_REF|

Data de Criação: 16/12/2025
Autor: Sistema Lavoratory
================================================================================
"""

import pandas as pd
from typing import Dict
import zipfile
import io


def parse_registro_e100(linha: str) -> dict:
    """
    Parse do registro E100 - Período da Apuração do ICMS.
    
    Formato: |E100|DT_INI|DT_FIN|
    
    GATILHO DE MANUTENÇÃO:
    - Campos na ordem: DT_INI, DT_FIN
    """
    campos = linha.split('|')
    
    return {
        'DT_INI': campos[2] if len(campos) > 2 else '',
        'DT_FIN': campos[3] if len(campos) > 3 else ''
    }


def parse_registro_e110(linha: str) -> dict:
    """
    Parse do registro E110 - Apuração do ICMS - Operações Próprias.
    
    Formato completo com 14 campos após E110.
    
    CAMPOS PRINCIPAIS:
    - VL_TOT_DEBITOS: Total de débitos
    - VL_TOT_CREDITOS: Total de créditos  
    - VL_SLD_APURADO: Saldo apurado
    - VL_ICMS_RECOLHER: ICMS a recolher
    
    GATILHO DE MANUTENÇÃO:
    - Campos na ordem conforme layout SPED
    """
    campos = linha.split('|')
    
    def to_float(valor):
        try:
            return float(valor.replace(',', '.')) if valor else 0.0
        except:
            return 0.0
    
    return {
        'VL_TOT_DEBITOS': to_float(campos[2]) if len(campos) > 2 else 0.0,
        'VL_AJ_DEBITOS': to_float(campos[3]) if len(campos) > 3 else 0.0,
        'VL_TOT_AJ_DEBITOS': to_float(campos[4]) if len(campos) > 4 else 0.0,
        'VL_ESTORNOS_CRED': to_float(campos[5]) if len(campos) > 5 else 0.0,
        'VL_TOT_CREDITOS': to_float(campos[6]) if len(campos) > 6 else 0.0,
        'VL_AJ_CREDITOS': to_float(campos[7]) if len(campos) > 7 else 0.0,
        'VL_TOT_AJ_CREDITOS': to_float(campos[8]) if len(campos) > 8 else 0.0,
        'VL_ESTORNOS_DEB': to_float(campos[9]) if len(campos) > 9 else 0.0,
        'VL_SLD_CREDOR_ANT': to_float(campos[10]) if len(campos) > 10 else 0.0,
        'VL_SLD_APURADO': to_float(campos[11]) if len(campos) > 11 else 0.0,
        'VL_TOT_DED': to_float(campos[12]) if len(campos) > 12 else 0.0,
        'VL_ICMS_RECOLHER': to_float(campos[13]) if len(campos) > 13 else 0.0,
        'VL_SLD_CREDOR_TRANSPORTAR': to_float(campos[14]) if len(campos) > 14 else 0.0,
        'DEB_ESP': campos[15] if len(campos) > 15 else ''
    }


def parse_registro_e111(linha: str) -> dict:
    """
    Parse do registro E111 - Ajuste/Benefício/Incentivo da Apuração do ICMS.
    
    Formato: |E111|COD_AJ_APUR|DESCR_COMPL_AJ|VL_AJ_APUR|
    
    IMPORTANTE:
    - COD_AJ_APUR: Código do ajuste (ex: RJ040010)
    - DESCR_COMPL_AJ: Descrição complementar
    - VL_AJ_APUR: Valor do ajuste
    
    GATILHO DE MANUTENÇÃO:
    - Campos na ordem: COD_AJ_APUR, DESCR_COMPL_AJ, VL_AJ_APUR
    """
    campos = linha.split('|')
    
    def to_float(valor):
        try:
            return float(valor.replace(',', '.')) if valor else 0.0
        except:
            return 0.0
    
    return {
        'COD_AJ_APUR': campos[2] if len(campos) > 2 else '',
        'DESCR_COMPL_AJ': campos[3] if len(campos) > 3 else '',
        'VL_AJ_APUR': to_float(campos[4]) if len(campos) > 4 else 0.0
    }


def parse_registro_e116(linha: str) -> dict:
    """
    Parse do registro E116 - Obrigações do ICMS Recolhido ou a Recolher.
    
    Formato: |E116|COD_OR|VL_OR|DT_VCTO|COD_REC|NUM_PROC|IND_PROC|PROC|TXT_COMPL|MES_REF|
    
    IMPORTANTE:
    - COD_OR: Código da obrigação (000=ICMS normal, 006=FECP, etc.)
    - VL_OR: Valor da obrigação
    - DT_VCTO: Data de vencimento
    - COD_REC: Código de receita
    - TXT_COMPL: Descrição complementar
    - MES_REF: Mês de referência (MMAAAA)
    
    GATILHO DE MANUTENÇÃO:
    - Campos na ordem conforme layout SPED
    """
    campos = linha.split('|')
    
    def to_float(valor):
        try:
            return float(valor.replace(',', '.')) if valor else 0.0
        except:
            return 0.0
    
    return {
        'COD_OR': campos[2] if len(campos) > 2 else '',
        'VL_OR': to_float(campos[3]) if len(campos) > 3 else 0.0,
        'DT_VCTO': campos[4] if len(campos) > 4 else '',
        'COD_REC': campos[5] if len(campos) > 5 else '',
        'NUM_PROC': campos[6] if len(campos) > 6 else '',
        'IND_PROC': campos[7] if len(campos) > 7 else '',
        'PROC': campos[8] if len(campos) > 8 else '',
        'TXT_COMPL': campos[9] if len(campos) > 9 else '',
        'MES_REF': campos[10] if len(campos) > 10 else ''
    }


def processar_arquivo_sped_registros_e(conteudo: str) -> Dict[str, pd.DataFrame]:
    """
    Processa arquivo SPED e extrai registros E.
    
    RETORNA:
        Dicionário com DataFrames:
        - 'E100': Períodos de apuração
        - 'E110': Apurações de ICMS
        - 'E111': Ajustes de apuração
        - 'E116': Obrigações ICMS
    
    GATILHO DE MANUTENÇÃO:
    - Para adicionar novos registros E, criar parse_registro_eXXX() e adicionar aqui
    """
    linhas = conteudo.split('\n')
    
    registros_e100 = []
    registros_e110 = []
    registros_e111 = []
    registros_e116 = []
    
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
        
        if linha.startswith('|E100|'):
            registros_e100.append(parse_registro_e100(linha))
        elif linha.startswith('|E110|'):
            registros_e110.append(parse_registro_e110(linha))
        elif linha.startswith('|E111|'):
            registros_e111.append(parse_registro_e111(linha))
        elif linha.startswith('|E116|'):
            registros_e116.append(parse_registro_e116(linha))
    
    return {
        'E100': pd.DataFrame(registros_e100),
        'E110': pd.DataFrame(registros_e110),
        'E111': pd.DataFrame(registros_e111),
        'E116': pd.DataFrame(registros_e116)
    }


def processar_multiplos_speds_registros_e(uploaded_files) -> Dict[str, pd.DataFrame]:
    """
    Processa múltiplos arquivos SPED (txt ou zip) e consolida registros E.
    
    IMPORTANTE:
    - Suporta .txt e .zip
    - Consolida todos os arquivos em um único DataFrame por registro
    
    GATILHO DE MANUTENÇÃO:
    - Adicionar novos tipos de arquivo aqui se necessário
    """
    todos_dados = {
        'E100': [],
        'E110': [],
        'E111': [],
        'E116': []
    }
    
    for uploaded_file in uploaded_files:
        try:
            # Verifica se é ZIP
            if uploaded_file.name.endswith('.zip'):
                with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                    for file_name in zip_ref.namelist():
                        if file_name.endswith('.txt'):
                            with zip_ref.open(file_name) as file:
                                conteudo = file.read().decode('utf-8', errors='ignore')
                                dados = processar_arquivo_sped_registros_e(conteudo)
                                
                                for key in todos_dados.keys():
                                    if not dados[key].empty:
                                        todos_dados[key].append(dados[key])
            else:
                # Arquivo TXT direto
                conteudo = uploaded_file.read().decode('utf-8', errors='ignore')
                dados = processar_arquivo_sped_registros_e(conteudo)
                
                for key in todos_dados.keys():
                    if not dados[key].empty:
                        todos_dados[key].append(dados[key])
        
        except Exception as e:
            print(f"Erro ao processar {uploaded_file.name}: {e}")
            continue
    
    # Consolida DataFrames
    resultado = {}
    for key, lista_dfs in todos_dados.items():
        if lista_dfs:
            resultado[key] = pd.concat(lista_dfs, ignore_index=True)
        else:
            resultado[key] = pd.DataFrame()
    
    return resultado


# ============================================================================
# APRENDIZADOS E OBSERVAÇÕES
# ============================================================================

"""
APRENDIZADO 1: ESTRUTURA DA APURAÇÃO DE ICMS

E100: Define o período (data inicial e final)
E110: Contém os totais da apuração:
    - Débitos (saídas)
    - Créditos (entradas)
    - Ajustes
    - Saldo apurado
    - ICMS a recolher

E111: Ajustes da apuração (podem ser vários)
    - Código do ajuste (ex: RJ040010 para FECP)
    - Descrição
    - Valor

E116: Guias de recolhimento (podem ser várias)
    - Código da obrigação (000=ICMS, 006=FECP, etc.)
    - Valor
    - Data de vencimento
    - Código de receita
    - Descrição

APRENDIZADO 2: CÓDIGOS DE OBRIGAÇÃO (E116)

000 = ICMS Normal
006 = FECP (Fundo Estadual de Combate à Pobreza)
Outros códigos conforme tabela SPED

APRENDIZADO 3: AJUSTES (E111)

Podem ser positivos (aumentam débito) ou negativos (aumentam crédito)
Códigos variam por UF (ex: RJ040010, SP010203, etc.)
"""

# ============================================================================
# FIM DO ARQUIVO
# ============================================================================
