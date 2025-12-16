# 📊 Registros E - Apuração de ICMS

## 📋 Resumo

Implementação completa do parser e visualização dos registros E (Apuração de ICMS e IPI) no sistema SPED ICMS/IPI.

**Data de Implementação:** 16/12/2025

---

## 🎯 Objetivo

Extrair e exibir de forma clara e profissional a apuração de ICMS, incluindo:
- Totais de débitos e créditos
- Ajustes da apuração
- Guias de recolhimento (ICMS e FECP)

---

## 📂 Estrutura dos Registros E

### E100: Período da Apuração

Define o período de referência da apuração.

**Formato:**
```
|E100|DT_INI|DT_FIN|
```

**Campos:**
- `DT_INI`: Data inicial (DDMMAAAA)
- `DT_FIN`: Data final (DDMMAAAA)

**Exemplo:**
```
|E100|01052025|31052025|
```
→ Período: 01/05/2025 a 31/05/2025

---

### E110: Apuração do ICMS - Operações Próprias

Contém os totais da apuração de ICMS.

**Formato:**
```
|E110|VL_TOT_DEBITOS|VL_AJ_DEBITOS|VL_TOT_AJ_DEBITOS|VL_ESTORNOS_CRED|
     |VL_TOT_CREDITOS|VL_AJ_CREDITOS|VL_TOT_AJ_CREDITOS|VL_ESTORNOS_DEB|
     |VL_SLD_CREDOR_ANT|VL_SLD_APURADO|VL_TOT_DED|VL_ICMS_RECOLHER|
     |VL_SLD_CREDOR_TRANSPORTAR|DEB_ESP|
```

**Campos Principais:**

| Campo | Descrição | Tipo |
|-------|-----------|------|
| `VL_TOT_DEBITOS` | Total de débitos de ICMS | Decimal |
| `VL_AJ_DEBITOS` | Ajustes a débito | Decimal |
| `VL_TOT_CREDITOS` | Total de créditos de ICMS | Decimal |
| `VL_AJ_CREDITOS` | Ajustes a crédito | Decimal |
| `VL_SLD_CREDOR_ANT` | Saldo credor do período anterior | Decimal |
| `VL_SLD_APURADO` | Saldo apurado (débitos - créditos) | Decimal |
| `VL_TOT_DED` | Total de deduções | Decimal |
| `VL_ICMS_RECOLHER` | **ICMS a recolher** | Decimal |
| `VL_SLD_CREDOR_TRANSPORTAR` | Saldo credor a transportar | Decimal |

**Exemplo:**
```
|E110|23579,53|0|0|0|9871,31|0|0|0|0|13708,22|2020,91|11687,31|0|2020,91|
```

**Interpretação:**
- Débitos: R$ 23.579,53
- Créditos: R$ 9.871,31
- Saldo Apurado: R$ 13.708,22
- Deduções: R$ 2.020,91
- **ICMS a Recolher: R$ 11.687,31**

---

### E111: Ajustes/Benefícios/Incentivos da Apuração

Registra ajustes aplicados na apuração (podem ser vários).

**Formato:**
```
|E111|COD_AJ_APUR|DESCR_COMPL_AJ|VL_AJ_APUR|
```

**Campos:**

| Campo | Descrição | Tipo |
|-------|-----------|------|
| `COD_AJ_APUR` | Código do ajuste (varia por UF) | String |
| `DESCR_COMPL_AJ` | Descrição complementar | String |
| `VL_AJ_APUR` | Valor do ajuste | Decimal |

**Exemplo:**
```
|E111|RJ040010|ADICIONAL RELATIVO AO FECP|2020,91|
|E111|RJ050008|ADICIONAL RELATIVO AO FECP|2020,91|
```

**Interpretação:**
- 2 ajustes relacionados ao FECP (Fundo Estadual de Combate à Pobreza)
- Códigos específicos do Rio de Janeiro (RJ)
- Total de ajustes: R$ 4.041,82

---

### E116: Obrigações do ICMS Recolhido ou a Recolher

Registra as guias de recolhimento (podem ser várias).

**Formato:**
```
|E116|COD_OR|VL_OR|DT_VCTO|COD_REC|NUM_PROC|IND_PROC|PROC|TXT_COMPL|MES_REF|
```

**Campos:**

| Campo | Descrição | Tipo |
|-------|-----------|------|
| `COD_OR` | Código da obrigação | String |
| `VL_OR` | Valor da obrigação | Decimal |
| `DT_VCTO` | Data de vencimento (DDMMAAAA) | String |
| `COD_REC` | Código de receita | String |
| `TXT_COMPL` | Descrição complementar | String |
| `MES_REF` | Mês de referência (MMAAAA) | String |

**Códigos de Obrigação:**

| Código | Descrição |
|--------|-----------|
| `000` | ICMS Normal |
| `001` | ICMS ST (Substituição Tributária) |
| `002` | ICMS Antecipado |
| `003` | ICMS Diferencial de Alíquota |
| `006` | **FECP** (Fundo Estadual de Combate à Pobreza) |
| `007` | FECP ST |

**Exemplo:**
```
|E116|000|11687,31|10062025|0213||||ICMS NORMAL REF. 05/2025|052025|
|E116|006|2020,91|10062025|7501||||FECP NORMAL REF. 05/2025|052025|
```

**Interpretação:**
- Guia 1: ICMS Normal - R$ 11.687,31 - Venc: 10/06/2025
- Guia 2: FECP - R$ 2.020,91 - Venc: 10/06/2025
- **Total a Recolher: R$ 13.708,22**

---

## 🖥️ Visualização no Sistema

### 1. Totais da Apuração (E110)

Exibidos em **8 cards** organizados em 2 linhas:

**Linha 1:**
- Total de Débitos
- Ajustes a Débito
- Total de Créditos
- Ajustes a Crédito

**Linha 2:**
- Saldo Credor Anterior
- Saldo Apurado
- Deduções
- **ICMS a Recolher** (destaque)

### 2. Ajustes da Apuração (E111)

**Tabela com 3 colunas:**
- Código
- Descrição
- Valor

**Métricas:**
- Quantidade de Ajustes
- Total dos Ajustes

### 3. Guias de Recolhimento (E116)

**Tabela com 6 colunas:**
- Tipo (mapeado do código)
- Valor
- Vencimento
- Código de Receita
- Descrição
- Referência

**Métricas:**
- Quantidade de Guias
- Total a Recolher

**Funcionalidades:**
- Download CSV das guias

### 4. Resumo Final

**3 colunas:**
- Débitos
- Créditos
- ICMS a Recolher

---

## 🧪 Testes Realizados

### Dados de Teste

Arquivo: `teste_registros_e.txt`

```
|E100|01052025|31052025|
|E110|23579,53|0|0|0|9871,31|0|0|0|0|13708,22|2020,91|11687,31|0|2020,91|
|E111|RJ040010|ADICIONAL RELATIVO AO FECP|2020,91|
|E111|RJ050008|ADICIONAL RELATIVO AO FECP|2020,91|
|E116|000|11687,31|10062025|0213||||ICMS NORMAL REF. 05/2025|052025|
|E116|006|2020,91|10062025|7501||||FECP NORMAL REF. 05/2025|052025|
```

### Resultados

✅ **E100:** 1 registro processado  
✅ **E110:** 1 registro processado  
✅ **E111:** 2 registros processados  
✅ **E116:** 2 registros processados  

**Valores Validados:**
- Total Débitos: R$ 23.579,53 ✅
- Total Créditos: R$ 9.871,31 ✅
- Saldo Apurado: R$ 13.708,22 ✅
- ICMS a Recolher: R$ 11.687,31 ✅
- Total Guias: R$ 13.708,22 ✅

---

## 📝 Gatilhos de Manutenção

### Para adicionar novos campos E110:

**Arquivo:** `aba_apuracao_mensal.py`

```python
def exibir_totais_apuracao(df_e110: pd.DataFrame):
    # Adicionar nova métrica aqui
    with col_nova:
        st.metric(
            'Novo Campo',
            formatar_moeda_br(apuracao.get('NOVO_CAMPO', 0)),
            help='Descrição do novo campo'
        )
```

### Para adicionar novos códigos de obrigação:

**Arquivo:** `aba_apuracao_mensal.py`

```python
def mapear_codigo_obrigacao(cod_or):
    mapeamento = {
        '000': 'ICMS Normal',
        '006': 'FECP',
        '999': 'Novo Código'  # ← Adicionar aqui
    }
    return mapeamento.get(cod_or, f'Código {cod_or}')
```

### Para adicionar filtros em ajustes:

**Arquivo:** `aba_apuracao_mensal.py`

```python
def exibir_ajustes(df_e111: pd.DataFrame):
    # Adicionar filtro aqui
    filtro = st.multiselect('Filtrar por código', df_e111['COD_AJ_APUR'].unique())
    if filtro:
        df_e111 = df_e111[df_e111['COD_AJ_APUR'].isin(filtro)]
```

---

## 🔄 Fluxo de Processamento

```
1. Upload do SPED
   ↓
2. Parser de Registros E (parser_registros_e.py)
   ↓
3. Extração de E100, E110, E111, E116
   ↓
4. Criação de DataFrames
   ↓
5. Passagem para aba_apuracao_mensal.py
   ↓
6. Exibição na aba "ICMS/IPI Apurado"
```

---

## 📚 Aprendizados

### 1. Estrutura Hierárquica

```
E100 (Período)
  └── E110 (Apuração)
       ├── E111 (Ajustes) - podem ser vários
       └── E116 (Guias) - podem ser várias
```

### 2. Códigos Específicos por UF

Os códigos de ajuste (E111) variam por Unidade Federativa:
- **RJ:** RJ040010, RJ050008
- **SP:** SP010203, SP020304
- **MG:** MG010101, MG020202

### 3. FECP (Fundo Estadual de Combate à Pobreza)

- Adicional ao ICMS
- Código 006 no E116
- Alíquota varia por UF (geralmente 1% ou 2%)
- Destinado a programas sociais

### 4. Formato de Data

**Padrão:** DDMMAAAA

| Exemplo | Interpretação |
|---------|---------------|
| 01052025 | 01/05/2025 |
| 10062025 | 10/06/2025 |
| 31122025 | 31/12/2025 |

---

## 🎯 Casos de Uso

### 1. Conferência de Apuração

Usuário pode verificar se os valores apurados estão corretos comparando:
- Débitos x Créditos
- Saldo Apurado x ICMS a Recolher
- Total Guias x ICMS a Recolher

### 2. Identificação de Ajustes

Usuário pode identificar quais ajustes foram aplicados e seus valores.

### 3. Controle de Guias

Usuário pode visualizar todas as guias a recolher com:
- Valores
- Vencimentos
- Códigos de receita

### 4. Exportação de Dados

Usuário pode baixar CSV das guias para:
- Importação em sistemas de pagamento
- Controle em planilhas
- Auditoria

---

## ✅ Checklist de Implementação

- [x] Criar parser E100
- [x] Criar parser E110
- [x] Criar parser E111
- [x] Criar parser E116
- [x] Implementar exibição de totais
- [x] Implementar exibição de ajustes
- [x] Implementar exibição de guias
- [x] Implementar resumo final
- [x] Adicionar formatação brasileira
- [x] Adicionar mapeamento de códigos
- [x] Adicionar download CSV
- [x] Testar com dados reais
- [x] Documentar código
- [x] Fazer commit

---

## 🚀 Próximos Passos

### Melhorias Futuras:

1. **Gráfico de Evolução Mensal**
   - Comparar apurações de múltiplos períodos
   - Visualizar tendência de ICMS a recolher

2. **Filtros Avançados**
   - Filtrar ajustes por código
   - Filtrar guias por tipo

3. **Alertas Automáticos**
   - Guias próximas do vencimento
   - Valores atípicos na apuração

4. **Exportação PDF**
   - Relatório completo da apuração
   - Formatação profissional

---

## 📦 Arquivos Relacionados

| Arquivo | Descrição | Linhas |
|---------|-----------|--------|
| `parser_registros_e.py` | Parser dos registros E | 412 |
| `aba_apuracao_mensal.py` | Visualização da apuração | 415 |
| `app.py` | Integração no app principal | +10 |

**Total:** 837 linhas de código

---

## 🔗 Referências

- [Guia Prático EFD-ICMS/IPI - Versão 3.1.7](http://sped.rfb.gov.br/arquivo/show/7119)
- [Tabela de Códigos de Ajuste - SPED](http://sped.rfb.gov.br/pasta/show/1644)
- Documentação interna do projeto

---

**Versão:** 1.0.0  
**Data:** 16/12/2025  
**Status:** ✅ Implementado e Testado
