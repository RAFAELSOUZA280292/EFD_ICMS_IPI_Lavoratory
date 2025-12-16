"""
Teste das novas funcionalidades: Entrada/Saída e Apuração Mensal
"""

import pandas as pd
from sped_parser import processar_sped
from analise_entrada_saida import (
    classificar_tipo_operacao,
    adicionar_classificacao,
    criar_resumo_entrada_saida
)

print("=" * 80)
print("TESTE: Novas Funcionalidades ICMS/IPI")
print("=" * 80)

# Processa arquivo SPED
print("\n1. Processando arquivo SPED...")
with open('exemplo_sped.txt', 'r', encoding='utf-8') as f:
    conteudo = f.read()

dados = processar_sped(conteudo)

df_c100 = dados.get('C100', pd.DataFrame())
df_c190 = dados.get('C190', pd.DataFrame())

print(f"   ✓ C100: {len(df_c100)} registros")
print(f"   ✓ C190: {len(df_c190)} registros")

# Teste de classificação de CFOP
print("\n2. Testando classificação de CFOP...")
cfops_teste = ['1102', '2102', '3102', '5102', '6102', '7102']
for cfop in cfops_teste:
    tipo = classificar_tipo_operacao(cfop)
    print(f"   CFOP {cfop} → {tipo}")

# Teste de resumo entrada/saída
print("\n3. Testando resumo entrada/saída...")
if not df_c190.empty:
    df_resumo = criar_resumo_entrada_saida(df_c100, df_c190)
    print(f"   ✓ Resumo criado com {len(df_resumo)} linhas")
    print("\n   Resumo:")
    for _, row in df_resumo.iterrows():
        print(f"   - {row['TIPO']}: {row['QUANTIDADE']} registros")
        print(f"     ICMS: R$ {row['VL_ICMS']:,.2f}")
        print(f"     IPI: R$ {row['VL_IPI']:,.2f}")
else:
    print("   ⚠ C190 vazio")

print("\n" + "=" * 80)
print("TESTE CONCLUÍDO!")
print("=" * 80)
