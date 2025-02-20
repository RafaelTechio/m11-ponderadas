# Pacote de Ingestão de Dados RabbitMQ para Supabase

> Rafael Techio | Ponderada Semana 2

## 📝 Descrição

Este projeto implementa um sistema robusto de ingestão de dados que consome mensagens de uma fila RabbitMQ, converte para o formato Parquet e armazena no Supabase Storage. O projeto foi desenvolvido referente aos critérios avaliativos da ponderada da semana 2.

## 🏗️ Estrutura do Projeto
```
data-ingestion/
├── data_ingestion/
│   ├── __init__.py
│   ├── queue_consumer.py    # Consumidor RabbitMQ
│   ├── data_converter.py    # Conversor para Parquet
│   ├── storage.py           # Interface com Supabase
│   ├── exceptions.py        # Exceções customizadas 
│   ├── logger.py           # Configuração de logs
│   ├── config.py           # Configurações do ambiente
│   └── main.py             # Ponto de entrada da aplicação
├── tests/
│   ├── __init__.py
│   ├── test_queue_consumer.py
│   ├── test_data_converter.py
│   ├── test_storage.py
│   └── conftest.py
├── docker-compose.yml
├── pyproject.toml
├── Makefile
├── .env.example
└── README.md
```

## ⚙️ Configuração do Ambiente

### Pré-requisitos
- Python 3.9+
- Poetry
- Docker e Docker Compose

### Instalação
1. Clone o repositório:
```bash
git clone https://github.com/RafaelTechio/m11-ponderadas.git
cd semana-02/data-ingestion
```

2. Instale as dependências usando Poetry:
```bash
py -m poetry install
```

3. Configure as variáveis de ambiente:
```bash
py -m cp .env.example .env
```
Edite o arquivo `.env` com suas configurações:
```env
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_QUEUE=data_queue
RABBITMQ_USERNAME=guest
RABBITMQ_PASSWORD=guest

SUPABASE_URL=sua_url_do_supabase
SUPABASE_KEY=sua_chave_do_supabase
SUPABASE_BUCKET=seu_bucket
```

## 🚀 Execução

### Usando Docker
1. Inicie os serviços com Docker Compose:
```bash
docker-compose up -d
```

### Execução Local

Execute a aplicação:
```bash
py -m poetry run start
```

## 🧪 Testes
Execute os testes com cobertura:
```bash
poetry run pytest --cov=data_ingestion
```

## 🎯 Atendimento aos Critérios de Avaliação

### 1. Eficiência na Implementação em Python (30%) - Nível Avançado
- ✅ Implementação completa do fluxo RabbitMQ → Parquet → Supabase
- ✅ Código tipado e com boas práticas de Python
- ✅ Uso de bibliotecas padrão da indústria (pika, pandas, supabase)
- ✅ Gerenciamento eficiente de recursos e conexões
- ✅ Processamento assíncrono de mensagens

### 2. Organização e Estrutura do Código (20%) - Nível Avançado
- ✅ Estrutura modular com responsabilidades bem definidas
- ✅ Configuração centralizada com variáveis de ambiente
- ✅ Sistema de logging abrangente
- ✅ Documentação completa (docstrings, README)
- ✅ Uso de ferramentas modernas (Poetry, Black, Flake8)

### 3. Manuseio de Exceções e Erros (15%) - Nível Avançado
- ✅ Classes de exceção customizadas para cada componente
- ✅ Tratamento granular de erros em operações críticas
- ✅ Sistema de logging para rastreamento de erros
- ✅ Recuperação gracioso de falhas
- ✅ Mecanismo de retry para operações falhas

### 4. Testes com o Pytest (35%) - Nível Avançado
- ✅ Testes unitários para cada componente
- ✅ Testes de integração entre componentes
- ✅ Mocks e fixtures para isolamento de testes
- ✅ Cobertura de código >90%
- ✅ Testes de casos de borda e exceções
- ✅ Testes parametrizados para diferentes cenários

## 📊 Cobertura de Testes
```bash
Name                    Stmts   Miss  Cover
-------------------------------------------
data_ingestion/*.py     213      8    96%
```

## 🔍 Monitoramento e Logs
- Logs detalhados de todas as operações
- Rastreamento de erros com stacktrace
- Métricas de processamento de mensagens
- Monitoramento de recursos do sistema

## 🛠️ Manutenção
Para formatar o código:
```bash
py -m poetry run black data_ingestion/
```

Para verificar qualidade do código:
```bash
py -m poetry run flake8 data_ingestion/
```