# 📋 Mapeamento de Campos - SPED ICMS/IPI

## 📊 Bloco 0 - Abertura, Identificação e Referências

### Registro 0000 - Abertura do Arquivo Digital

| Campo | Descrição | Tipo |
|-------|-----------|------|
| REG | Texto fixo "0000" | C |
| COD_VER | Código da versão do leiaute | N |
| COD_FIN | Código da finalidade do arquivo | N |
| DT_INI | Data inicial das informações | N |
| DT_FIN | Data final das informações | N |
| NOME | Nome empresarial da entidade | C |
| CNPJ | CNPJ | N |
| CPF | CPF | N |
| UF | Sigla da UF da entidade | C |
| IE | Inscrição Estadual | C |
| COD_MUN | Código do município | N |
| IM | Inscrição Municipal | C |
| SUFRAMA | Inscrição SUFRAMA | C |
| IND_PERFIL | Perfil de apresentação | C |
| IND_ATIV | Indicador de tipo de atividade | N |

### Registro 0150 - Tabela de Cadastro de Participantes

| Campo | Descrição | Tipo |
|-------|-----------|------|
| REG | Texto fixo "0150" | C |
| COD_PART | Código de identificação do participante | C |
| NOME | Nome pessoal ou empresarial | C |
| COD_PAIS | Código do país | N |
| CNPJ | CNPJ | N |
| CPF | CPF | N |
| IE | Inscrição Estadual | C |
| COD_MUN | Código do município | N |
| SUFRAMA | Inscrição SUFRAMA | N |
| END | Logradouro | C |
| NUM | Número | C |
| COMPL | Complemento | C |
| BAIRRO | Bairro | C |

### Registro 0200 - Tabela de Identificação do Item

| Campo | Descrição | Tipo |
|-------|-----------|------|
| REG | Texto fixo "0200" | C |
| COD_ITEM | Código do item | C |
| DESCR_ITEM | Descrição do item | C |
| COD_BARRA | Código de barra | C |
| COD_ANT_ITEM | Código anterior do item | C |
| UNID_INV | Unidade de medida de estoque | C |
| TIPO_ITEM | Tipo do item | N |
| COD_NCM | Código NCM | C |
| EX_IPI | Exceção do IPI | C |
| COD_GEN | Código do gênero | N |
| COD_LST | Código de serviço | C |
| ALIQ_ICMS | Alíquota de ICMS | N |

## 📄 Bloco C - Documentos Fiscais I

### Registro C100 - Nota Fiscal

| Campo | Descrição | Tipo |
|-------|-----------|------|
| REG | Texto fixo "C100" | C |
| IND_OPER | Indicador do tipo de operação (0=Entrada, 1=Saída) | C |
| IND_EMIT | Indicador do emitente (0=Próprio, 1=Terceiros) | C |
| COD_PART | Código do participante | C |
| COD_MOD | Código do modelo do documento fiscal | C |
| COD_SIT | Código da situação do documento | N |
| SER | Série do documento | C |
| NUM_DOC | Número do documento | N |
| CHV_NFE | Chave da NF-e | N |
| DT_DOC | Data de emissão | N |
| DT_E_S | Data de entrada/saída | N |
| VL_DOC | Valor total do documento | N |
| IND_PGTO | Indicador do tipo de pagamento | C |
| VL_DESC | Valor total do desconto | N |
| VL_ABAT_NT | Abatimento não tributado | N |
| VL_MERC | Valor das mercadorias | N |
| IND_FRT | Indicador do tipo de frete | C |
| VL_FRT | Valor do frete | N |
| VL_SEG | Valor do seguro | N |
| VL_OUT_DA | Outras despesas acessórias | N |
| VL_BC_ICMS | Base de cálculo do ICMS | N |
| VL_ICMS | Valor do ICMS | N |
| VL_BC_ICMS_ST | Base de cálculo do ICMS ST | N |
| VL_ICMS_ST | Valor do ICMS ST | N |
| VL_IPI | Valor total do IPI | N |
| VL_PIS | Valor do PIS | N |
| VL_COFINS | Valor da COFINS | N |
| VL_PIS_ST | Valor do PIS retido por ST | N |
| VL_COFINS_ST | Valor da COFINS retido por ST | N |

### Registro C170 - Itens do Documento

| Campo | Descrição | Tipo |
|-------|-----------|------|
| REG | Texto fixo "C170" | C |
| NUM_ITEM | Número sequencial do item | N |
| COD_ITEM | Código do item | C |
| DESCR_COMPL | Descrição complementar | C |
| QTD | Quantidade | N |
| UNID | Unidade | C |
| VL_ITEM | Valor total do item | N |
| VL_DESC | Valor do desconto | N |
| IND_MOV | Movimentação física (0=Sim, 1=Não) | C |
| CST_ICMS | Código da Situação Tributária ICMS | N |
| CFOP | Código Fiscal de Operação | N |
| COD_NAT | Código da natureza da operação | C |
| VL_BC_ICMS | Base de cálculo do ICMS | N |
| ALIQ_ICMS | Alíquota do ICMS | N |
| VL_ICMS | Valor do ICMS | N |
| VL_BC_ICMS_ST | Base de cálculo do ICMS ST | N |
| ALIQ_ST | Alíquota do ICMS ST | N |
| VL_ICMS_ST | Valor do ICMS ST | N |
| IND_APUR | Indicador de período de apuração | C |
| CST_IPI | Código da Situação Tributária IPI | C |
| COD_ENQ | Código de enquadramento legal IPI | C |
| VL_BC_IPI | Base de cálculo do IPI | N |
| ALIQ_IPI | Alíquota do IPI | N |
| VL_IPI | Valor do IPI | N |
| CST_PIS | Código da Situação Tributária PIS | N |
| VL_BC_PIS | Base de cálculo do PIS | N |
| ALIQ_PIS | Alíquota do PIS | N |
| VL_PIS | Valor do PIS | N |
| CST_COFINS | Código da Situação Tributária COFINS | N |
| VL_BC_COFINS | Base de cálculo da COFINS | N |
| ALIQ_COFINS | Alíquota da COFINS | N |
| VL_COFINS | Valor da COFINS | N |

### Registro C190 - Registro Analítico do Documento

| Campo | Descrição | Tipo |
|-------|-----------|------|
| REG | Texto fixo "C190" | C |
| CST_ICMS | Código da Situação Tributária ICMS | N |
| CFOP | Código Fiscal de Operação | N |
| ALIQ_ICMS | Alíquota do ICMS | N |
| VL_OPR | Valor da operação | N |
| VL_BC_ICMS | Base de cálculo do ICMS | N |
| VL_ICMS | Valor do ICMS | N |
| VL_BC_ICMS_ST | Base de cálculo do ICMS ST | N |
| VL_ICMS_ST | Valor do ICMS ST | N |
| VL_RED_BC | Valor não tributado | N |
| VL_IPI | Valor do IPI | N |
| COD_OBS | Código da observação | C |

## 🔍 Classificação de CFOPs

### Entradas (Crédito)
- **1.xxx**: Entradas ou aquisições de serviços do Estado
- **2.xxx**: Entradas ou aquisições de serviços de outros Estados
- **3.xxx**: Entradas ou aquisições de serviços do Exterior

### Saídas (Débito)
- **5.xxx**: Saídas ou prestações de serviços para o Estado
- **6.xxx**: Saídas ou prestações de serviços para outros Estados
- **7.xxx**: Saídas ou prestações de serviços para o Exterior

## 📝 Códigos de Situação Tributária (CST) - ICMS

| CST | Descrição |
|-----|-----------|
| 00 | Tributada integralmente |
| 10 | Tributada e com cobrança do ICMS por substituição tributária |
| 20 | Com redução de base de cálculo |
| 30 | Isenta ou não tributada e com cobrança do ICMS por ST |
| 40 | Isenta |
| 41 | Não tributada |
| 50 | Suspensão |
| 51 | Diferimento |
| 60 | ICMS cobrado anteriormente por ST |
| 70 | Com redução de BC e cobrança do ICMS por ST |
| 90 | Outras |

## 🎯 Indicadores Importantes

### IND_OPER (Tipo de Operação)
- **0**: Entrada
- **1**: Saída

### IND_EMIT (Emitente)
- **0**: Emissão própria
- **1**: Terceiros

### COD_MOD (Modelo do Documento)
- **01**: Nota Fiscal modelo 1
- **04**: Nota Fiscal de Produtor
- **55**: Nota Fiscal Eletrônica (NF-e)
- **65**: Nota Fiscal de Consumidor Eletrônica (NFC-e)

### TIPO_ITEM (Tipo do Item)
- **00**: Mercadoria para Revenda
- **01**: Matéria-Prima
- **02**: Embalagem
- **03**: Produto em Processo
- **04**: Produto Acabado
- **05**: Subproduto
- **06**: Produto Intermediário
- **07**: Material de Uso e Consumo
- **08**: Ativo Imobilizado
- **09**: Serviços
- **10**: Outros insumos
- **99**: Outras
