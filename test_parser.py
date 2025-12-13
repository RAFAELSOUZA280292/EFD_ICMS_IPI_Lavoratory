"""
Script de teste para validar os parsers do SPED ICMS/IPI
"""

import sys
from sped_parser import processar_arquivo_sped
from parser_registros_0 import processar_arquivo_sped_registros_0

# Lê o arquivo de exemplo
with open('exemplo_sped.txt', 'rb') as f:
    conteudo = f.read()

print("=" * 80)
print("TESTANDO PARSER DE REGISTROS C (Documentos Fiscais)")
print("=" * 80)

dados_c = processar_arquivo_sped(conteudo)

for tipo, df in dados_c.items():
    if not df.empty:
        print(f"\n{tipo}: {len(df)} registros encontrados")
        print(f"Colunas: {list(df.columns)[:10]}...")  # Mostra primeiras 10 colunas
        if tipo == 'C100':
            print(f"Total VL_DOC: R$ {df['VL_DOC'].sum():,.2f}")
            print(f"Total VL_ICMS: R$ {df['VL_ICMS'].sum():,.2f}")
            print(f"Total VL_IPI: R$ {df['VL_IPI'].sum():,.2f}")

print("\n" + "=" * 80)
print("TESTANDO PARSER DE REGISTROS 0 (Cadastros)")
print("=" * 80)

dados_0 = processar_arquivo_sped_registros_0(conteudo)

for tipo, df in dados_0.items():
    if not df.empty:
        print(f"\n{tipo}: {len(df)} registros encontrados")
        print(f"Colunas: {list(df.columns)[:10]}...")  # Mostra primeiras 10 colunas

print("\n" + "=" * 80)
print("TESTE CONCLUÍDO COM SUCESSO!")
print("=" * 80)
