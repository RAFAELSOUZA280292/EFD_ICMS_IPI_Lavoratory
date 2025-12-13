# 📊 Analisador de SPED ICMS e IPI

Sistema completo de análise fiscal para arquivos SPED ICMS e IPI (EFD ICMS/IPI).

## 🎯 Funcionalidades

- **Upload de Múltiplos Arquivos**: Suporte para até 12 arquivos SPED (.txt ou .zip)
- **Análise de Documentos Fiscais**: Processamento de registros C100, C170, C190
- **Análise de Participantes**: Cadastro de fornecedores e clientes (Registro 0150)
- **Análise de Produtos**: Cadastro de itens (Registro 0200)
- **Dashboards Executivos**: Visualizações interativas com gráficos
- **Filtros Avançados**: Filtros por período, CFOP, participante, produto
- **Acumuladores por CFOP**: Análise consolidada por código fiscal
- **Exportação**: Geração de relatórios em Excel e PDF

## 🚀 Tecnologias

- **Python 3.11+**
- **Streamlit**: Interface web interativa
- **Pandas**: Processamento de dados
- **Plotly**: Visualizações gráficas
- **OpenPyXL**: Exportação para Excel

## 📦 Instalação

```bash
# Clone o repositório
git clone https://github.com/RAFAELSOUZA280292/EFD_ICMS_IPI_Lavoratory.git
cd EFD_ICMS_IPI_Lavoratory

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt
```

## 🎮 Uso

```bash
# Execute a aplicação
streamlit run app.py
```

A aplicação estará disponível em `http://localhost:8501`

## 📋 Estrutura do Projeto

```
EFD_ICMS_IPI_Lavoratory/
├── app.py                      # Aplicação principal
├── sped_parser.py              # Parser de registros C (documentos)
├── parser_registros_0.py       # Parser de registros 0 (cadastros)
├── dashboards_bigfour.py       # Dashboards executivos
├── filtros_avancados.py        # Sistema de filtros
├── acumuladores_cfop.py        # Acumuladores por CFOP
├── exportar_pdf.py             # Exportação de relatórios
├── requirements.txt            # Dependências Python
└── README.md                   # Este arquivo
```

## 📊 Registros Suportados

### Bloco 0 - Abertura, Identificação e Referências
- **0000**: Abertura do arquivo digital
- **0001**: Abertura do bloco 0
- **0005**: Dados complementares da entidade
- **0100**: Dados do contabilista
- **0150**: Tabela de cadastro de participantes
- **0175**: Alteração da tabela de cadastro de participantes
- **0190**: Identificação das unidades de medida
- **0200**: Tabela de identificação do item (produto e serviços)
- **0205**: Alteração do item
- **0220**: Fatores de conversão de unidades

### Bloco C - Documentos Fiscais I
- **C100**: Nota fiscal (código 01), nota fiscal avulsa (código 1B), nota fiscal de produtor (código 04), NF-e (código 55) e NFC-e (código 65)
- **C110**: Informação complementar da nota fiscal (código 01, 1B, 04 e 55)
- **C113**: Documento fiscal referenciado
- **C170**: Itens do documento (código 01, 1B, 04, 55 e 65)
- **C190**: Registro analítico do documento (código 01, 1B, 04, 55 e 65)
- **C195**: Observações do lançamento fiscal (código 01, 1B, 04 e 55)
- **C197**: Outras obrigações tributárias, ajustes e informações de valores provenientes de documento fiscal

### Bloco E - Apuração do ICMS e do IPI
- **E116**: Obrigações do ICMS recolhido ou a recolher - Operações próprias

## 🔍 Análises Disponíveis

1. **Visão Geral**: Resumo executivo com principais indicadores
2. **Documentos Fiscais**: Análise detalhada de notas fiscais
3. **Análise por CFOP**: Consolidação por código fiscal
4. **Participantes**: Análise de fornecedores e clientes
5. **Produtos**: Análise de itens comercializados
6. **Apuração de Impostos**: Cálculo de ICMS e IPI

## 📝 Formato do Arquivo SPED

O arquivo SPED ICMS/IPI deve estar no formato texto (.txt) com a seguinte estrutura:

```
|0000|019|0|01062025|30062025|EMPRESA EXEMPLO LTDA|12345678000190||SP|12345678|1234567|||A|1|
|0001|0|
|0005|EMPRESA EXEMPLO|12345678|RUA EXEMPLO|123||CENTRO|SAO PAULO|1133334444|||
...
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 👨‍💻 Autor

Rafael Souza - [@RAFAELSOUZA280292](https://github.com/RAFAELSOUZA280292)

## 🙏 Agradecimentos

Baseado no projeto [EFDPis_Cofins_Lavoratory](https://github.com/RAFAELSOUZA280292/EFDPis_Cofins_Lavoratory)
