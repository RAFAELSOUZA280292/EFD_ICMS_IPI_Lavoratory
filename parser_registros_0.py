"""
Parser de Registros 0 (Abertura e Cadastros) do SPED ICMS/IPI
Processa registros 0000, 0001, 0005, 0100, 0150, 0175, 0190, 0200, 0205, 0220
"""

import pandas as pd
import io
import zipfile


def parse_registro_0000(linha):
    """
    0000: Abertura do Arquivo Digital e Identificação da Entidade
    """
    campos = linha.split('|')
    
    try:
        return {
            'REG': campos[1],
            'COD_VER': campos[2],  # Código da versão do leiaute
            'COD_FIN': campos[3],  # Código da finalidade do arquivo
            'DT_INI': campos[4],  # Data inicial das informações
            'DT_FIN': campos[5],  # Data final das informações
            'NOME': campos[6],  # Nome empresarial da entidade
            'CNPJ': campos[7],  # CNPJ
            'CPF': campos[8],  # CPF
            'UF': campos[9],  # Sigla da UF
            'IE': campos[10],  # Inscrição Estadual
            'COD_MUN': campos[11],  # Código do município
            'IM': campos[12],  # Inscrição Municipal
            'SUFRAMA': campos[13],  # Inscrição SUFRAMA
            'IND_PERFIL': campos[14],  # Perfil de apresentação
            'IND_ATIV': campos[15],  # Indicador de tipo de atividade
        }
    except IndexError:
        return None


def parse_registro_0005(linha):
    """
    0005: Dados Complementares da Entidade
    """
    campos = linha.split('|')
    
    try:
        return {
            'REG': campos[1],
            'FANTASIA': campos[2],  # Nome de fantasia
            'CEP': campos[3],  # CEP
            'END': campos[4],  # Logradouro
            'NUM': campos[5],  # Número
            'COMPL': campos[6],  # Complemento
            'BAIRRO': campos[7],  # Bairro
            'FONE': campos[8],  # Telefone
            'FAX': campos[9],  # Fax
            'EMAIL': campos[10],  # E-mail
        }
    except IndexError:
        return None


def parse_registro_0100(linha):
    """
    0100: Dados do Contabilista
    """
    campos = linha.split('|')
    
    try:
        return {
            'REG': campos[1],
            'NOME': campos[2],  # Nome do contabilista
            'CPF': campos[3],  # CPF do contabilista
            'CRC': campos[4],  # Registro no CRC
            'CNPJ': campos[5],  # CNPJ da empresa de contabilidade
            'CEP': campos[6],  # CEP
            'END': campos[7],  # Logradouro
            'NUM': campos[8],  # Número
            'COMPL': campos[9],  # Complemento
            'BAIRRO': campos[10],  # Bairro
            'FONE': campos[11],  # Telefone
            'FAX': campos[12],  # Fax
            'EMAIL': campos[13],  # E-mail
            'COD_MUN': campos[14],  # Código do município
        }
    except IndexError:
        return None


def parse_registro_0150(linha):
    """
    0150: Tabela de Cadastro de Participantes
    """
    campos = linha.split('|')
    
    try:
        return {
            'REG': campos[1],
            'COD_PART': campos[2],  # Código de identificação do participante
            'NOME': campos[3],  # Nome pessoal ou empresarial
            'COD_PAIS': campos[4],  # Código do país
            'CNPJ': campos[5],  # CNPJ
            'CPF': campos[6],  # CPF
            'IE': campos[7],  # Inscrição Estadual
            'COD_MUN': campos[8],  # Código do município
            'SUFRAMA': campos[9],  # Inscrição SUFRAMA
            'END': campos[10],  # Logradouro
            'NUM': campos[11],  # Número
            'COMPL': campos[12],  # Complemento
            'BAIRRO': campos[13],  # Bairro
        }
    except IndexError:
        return None


def parse_registro_0175(linha):
    """
    0175: Alteração da Tabela de Cadastro de Participantes
    """
    campos = linha.split('|')
    
    try:
        return {
            'REG': campos[1],
            'DT_ALT': campos[2],  # Data da alteração
            'NR_CAMPO': campos[3],  # Número do campo alterado
            'CONT_ANT': campos[4],  # Conteúdo anterior
        }
    except IndexError:
        return None


def parse_registro_0190(linha):
    """
    0190: Identificação das Unidades de Medida
    """
    campos = linha.split('|')
    
    try:
        return {
            'REG': campos[1],
            'UNID': campos[2],  # Código da unidade de medida
            'DESCR': campos[3],  # Descrição da unidade de medida
        }
    except IndexError:
        return None


def parse_registro_0200(linha):
    """
    0200: Tabela de Identificação do Item (Produto e Serviços)
    """
    campos = linha.split('|')
    
    try:
        return {
            'REG': campos[1],
            'COD_ITEM': campos[2],  # Código do item
            'DESCR_ITEM': campos[3],  # Descrição do item
            'COD_BARRA': campos[4],  # Código de barra
            'COD_ANT_ITEM': campos[5],  # Código anterior do item
            'UNID_INV': campos[6],  # Unidade de medida de estoque
            'TIPO_ITEM': campos[7],  # Tipo do item
            'COD_NCM': campos[8],  # Código NCM
            'EX_IPI': campos[9],  # Exceção do IPI
            'COD_GEN': campos[10],  # Código do gênero
            'COD_LST': campos[11],  # Código de serviço
            'ALIQ_ICMS': campos[12],  # Alíquota de ICMS
        }
    except IndexError:
        return None


def parse_registro_0205(linha):
    """
    0205: Alteração do Item
    """
    campos = linha.split('|')
    
    try:
        return {
            'REG': campos[1],
            'DESCR_ANT_ITEM': campos[2],  # Descrição anterior do item
            'DT_INI': campos[3],  # Data inicial de utilização
            'DT_FIM': campos[4],  # Data final de utilização
            'COD_ANT_ITEM': campos[5],  # Código anterior do item
        }
    except IndexError:
        return None


def parse_registro_0220(linha):
    """
    0220: Fatores de Conversão de Unidades
    """
    campos = linha.split('|')
    
    try:
        return {
            'REG': campos[1],
            'UNID_CONV': campos[2],  # Unidade comercial a ser convertida
            'FAT_CONV': campos[3],  # Fator de conversão
        }
    except IndexError:
        return None


def processar_arquivo_sped_registros_0(conteudo):
    """
    Processa registros 0 de um arquivo SPED ICMS/IPI
    """
    linhas = conteudo.decode('latin-1').split('\n')
    
    registros_0000 = []
    registros_0005 = []
    registros_0100 = []
    registros_0150 = []
    registros_0175 = []
    registros_0190 = []
    registros_0200 = []
    registros_0205 = []
    registros_0220 = []
    
    # Variável para controle de contexto
    ultimo_0150 = None
    ultimo_0200 = None
    
    for linha in linhas:
        if not linha.strip():
            continue
            
        campos = linha.split('|')
        if len(campos) < 2:
            continue
            
        tipo_registro = campos[1]
        
        if tipo_registro == '0000':
            registro = parse_registro_0000(linha)
            if registro:
                registros_0000.append(registro)
                
        elif tipo_registro == '0005':
            registro = parse_registro_0005(linha)
            if registro:
                registros_0005.append(registro)
                
        elif tipo_registro == '0100':
            registro = parse_registro_0100(linha)
            if registro:
                registros_0100.append(registro)
                
        elif tipo_registro == '0150':
            registro = parse_registro_0150(linha)
            if registro:
                registros_0150.append(registro)
                ultimo_0150 = registro
                
        elif tipo_registro == '0175':
            registro = parse_registro_0175(linha)
            if registro and ultimo_0150:
                registro['COD_PART_PAI'] = ultimo_0150.get('COD_PART', '')
                registros_0175.append(registro)
                
        elif tipo_registro == '0190':
            registro = parse_registro_0190(linha)
            if registro:
                registros_0190.append(registro)
                
        elif tipo_registro == '0200':
            registro = parse_registro_0200(linha)
            if registro:
                registros_0200.append(registro)
                ultimo_0200 = registro
                
        elif tipo_registro == '0205':
            registro = parse_registro_0205(linha)
            if registro and ultimo_0200:
                registro['COD_ITEM_PAI'] = ultimo_0200.get('COD_ITEM', '')
                registros_0205.append(registro)
                
        elif tipo_registro == '0220':
            registro = parse_registro_0220(linha)
            if registro and ultimo_0200:
                registro['COD_ITEM_PAI'] = ultimo_0200.get('COD_ITEM', '')
                registros_0220.append(registro)
    
    # Criar DataFrames
    df_0000 = pd.DataFrame(registros_0000) if registros_0000 else pd.DataFrame()
    df_0005 = pd.DataFrame(registros_0005) if registros_0005 else pd.DataFrame()
    df_0100 = pd.DataFrame(registros_0100) if registros_0100 else pd.DataFrame()
    df_0150 = pd.DataFrame(registros_0150) if registros_0150 else pd.DataFrame()
    df_0175 = pd.DataFrame(registros_0175) if registros_0175 else pd.DataFrame()
    df_0190 = pd.DataFrame(registros_0190) if registros_0190 else pd.DataFrame()
    df_0200 = pd.DataFrame(registros_0200) if registros_0200 else pd.DataFrame()
    df_0205 = pd.DataFrame(registros_0205) if registros_0205 else pd.DataFrame()
    df_0220 = pd.DataFrame(registros_0220) if registros_0220 else pd.DataFrame()
    
    return {
        '0000': df_0000,
        '0005': df_0005,
        '0100': df_0100,
        '0150': df_0150,
        '0175': df_0175,
        '0190': df_0190,
        '0200': df_0200,
        '0205': df_0205,
        '0220': df_0220
    }


def processar_multiplos_speds_registros_0(uploaded_files):
    """
    Processa múltiplos arquivos SPED e consolida registros 0
    """
    dfs_consolidados = {
        '0000': [],
        '0005': [],
        '0100': [],
        '0150': [],
        '0175': [],
        '0190': [],
        '0200': [],
        '0205': [],
        '0220': []
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
                                resultado = processar_arquivo_sped_registros_0(conteudo)
                                
                                for tipo, df in resultado.items():
                                    if not df.empty:
                                        df['ARQUIVO_ORIGEM'] = uploaded_file.name
                                        dfs_consolidados[tipo].append(df)
            else:
                # Processar arquivo TXT
                conteudo = uploaded_file.read()
                resultado = processar_arquivo_sped_registros_0(conteudo)
                
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
