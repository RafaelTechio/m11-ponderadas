# Pacote de Ingestão de Dados RabbitMQ para Supabase

> Rafael Techio | Ponderada Semana 2

## 📝 Descrição

Este projeto implementa um sistema robusto de ingestão de dados que consome mensagens de uma fila RabbitMQ, converte para o formato Parquet e armazena no Supabase Storage. O projeto foi desenvolvido referente aos critérios avaliativos da ponderada da semana 2.

## 🏗️ Estrutura do Projeto
```
data-ingestion/
├── data_ingestion/
│   ├── __init__.py
│   ├── app.py                 # Aplicação principal
│   ├── config.py              # Configurações do ambiente
│   ├── data_processor.py      # Processador de dados
│   ├── dlq_handler.py         # Tratamento de Dead Letter Queue
│   ├── exceptions.py          # Exceções customizadas
│   ├── logger.py              # Configuração de logs
│   ├── main.py                # Ponto de entrada da aplicação
│   ├── parquet_converter.py   # Conversor para Parquet
│   ├── queue_consumer.py      # Consumidor RabbitMQ
│   └── storage.py             # Interface com Supabase
├── tests/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── test_app.py
│   ├── test_config.py
│   ├── test_data_processor.py
│   ├── test_dlq_handler.py
│   ├── test_main.py
│   ├── test_parquet_converter.py
│   ├── test_queue_consumer.py
│   └── test_storage.py
├── .pytest_cache/
├── .coverage
├── .env
├── .env.example
├── .gitignore
├── poetry.lock
├── pyproject.toml
├── docker-compose.yml
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

![image](https://github.com/user-attachments/assets/e3d79ba8-dd55-4b84-984c-9f312bceeaf4)


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

## Evidências de Funcionamento

Para evidenciar o funcionamento da aplicação, separei um uma amostra do dataset **InteliFalhas** e converti seus dados para JSON:

```json
[
 {
   "ID": "2024-3712154",
   "DATA DETECCAO": "2010-01-29-02.25.25.000000",
   "PONTO": "RODAGEM",
   "LOC_ID": 5559,
   "LOC": "Tampa traseira",
   "POS_ID": -2,
   "POS": "",
   "TYPE_ID": 70,
   "TYPE_TEXT": "070 - Ruído",
   "VIEW_ID": null,
   "COLUNA": "",
   "LINHA": null
 },
 {
   "ID": "2024-3722068",
   "DATA DETECCAO": "2010-01-29-02.38.57.000000",
   "PONTO": "RODAGEM",
   "LOC_ID": 5559,
   "LOC": "Tampa traseira",
   "POS_ID": -2,
   "POS": "",
   "TYPE_ID": 70,
   "TYPE_TEXT": "070 - Ruído",
   "VIEW_ID": null,
   "COLUNA": "",
   "LINHA": null
 },
 {
   "ID": "2024-3732080",
   "DATA DETECCAO": "2010-01-29-02.44.54.000000",
   "PONTO": "RODAGEM",
   "LOC_ID": 7057,
   "LOC": "Revestimento coluna A",
   "POS_ID": 5,
   "POS": "direita",
   "TYPE_ID": 70,
   "TYPE_TEXT": "070 - Ruído",
   "VIEW_ID": null,
   "COLUNA": "",
   "LINHA": null
 },
 {
   "ID": "2024-3732079",
   "DATA DETECCAO": "2010-01-29-02.53.28.000000",
   "PONTO": "RODAGEM",
   "LOC_ID": 5851,
   "LOC": "Porta traseira",
   "POS_ID": 5,
   "POS": "direita",
   "TYPE_ID": 70,
   "TYPE_TEXT": "070 - Ruído",
   "VIEW_ID": null,
   "COLUNA": "",
   "LINHA": null
 },
 {
   "ID": "2024-3711076",
   "DATA DETECCAO": "2010-01-29-02.54.22.000000",
   "PONTO": "RODAGEM",
   "LOC_ID": 4661,
   "LOC": "Alavanca do freio manual",
   "POS_ID": -2,
   "POS": "",
   "TYPE_ID": 5,
   "TYPE_TEXT": "005 - Baixo (a)",
   "VIEW_ID": null,
   "COLUNA": "",
   "LINHA": null
 },
 {
   "ID": "2024-3732094",
   "DATA DETECCAO": "2010-01-29-04.04.56.000000",
   "PONTO": "RODAGEM",
   "LOC_ID": 98761528,
   "LOC": "Regulador de altura cinto de segurança",
   "POS_ID": 3,
   "POS": "esquerda",
   "TYPE_ID": 31,
   "TYPE_TEXT": "031 - Parcialmente sem fun\\u00e7\\u00e3o",
   "VIEW_ID": null,
   "COLUNA": "",
   "LINHA": null
 },
 {
   "ID": "2024-3732158",
   "DATA DETECCAO": "2010-01-29-04.07.53.000000",
   "PONTO": "RODAGEM",
   "LOC_ID": 51371,
   "LOC": "Coluna A",
   "POS_ID": 3,
   "POS": "esquerda",
   "TYPE_ID": 70,
   "TYPE_TEXT": "070 - Ruído",
   "VIEW_ID": null,
   "COLUNA": "",
   "LINHA": null
 },
 {
   "ID": "2024-3721002",
   "DATA DETECCAO": "2010-01-29-04.34.44.000000",
   "PONTO": "RODAGEM",
   "LOC_ID": 5851,
   "LOC": "Porta traseira",
   "POS_ID": 5,
   "POS": "direita",
   "TYPE_ID": 70,
   "TYPE_TEXT": "070 - Ruído",
   "VIEW_ID": null,
   "COLUNA": "",
   "LINHA": null
 },
 {
   "ID": "2024-3732118",
   "DATA DETECCAO": "2010-01-29-04.35.35.000000",
   "PONTO": "RODAGEM",
   "LOC_ID": 7018,
   "LOC": "Painel de instrumentos",
   "POS_ID": 4,
   "POS": "centralizado",
   "TYPE_ID": 70,
   "TYPE_TEXT": "070 - Ruído",
   "VIEW_ID": null,
   "COLUNA": "",
   "LINHA": null
 },
 {
   "ID": "2024-3711332",
   "DATA DETECCAO": "2010-01-29-05.18.43.000000",
   "PONTO": "RODAGEM",
   "LOC_ID": 4200,
   "LOC": "Suspensão traseira",
   "POS_ID": 3,
   "POS": "esquerda",
   "TYPE_ID": 70,
   "TYPE_TEXT": "070 - Ruído",
   "VIEW_ID": null,
   "COLUNA": "",
   "LINHA": null
 },
 {
   "ID": "2024-1712444",
   "DATA DETECCAO": "2024-02-23-22.30.59.000000",
   "PONTO": "ZP5",
   "LOC_ID": 53002,
   "LOC": "Canal de escoamento de água",
   "POS_ID": 10,
   "POS": "direito externo",
   "TYPE_ID": 89,
   "TYPE_TEXT": "089 - Res\\u00edduo de soldagem",
   "VIEW_ID": 691,
   "COLUNA": "G",
   "LINHA": 2
 },
 {
   "ID": "2024-1712444",
   "DATA DETECCAO": "2024-02-23-22.31.10.000000",
   "PONTO": "ZP5",
   "LOC_ID": 51371,
   "LOC": "Coluna A",
   "POS_ID": 10,
   "POS": "direito externo",
   "TYPE_ID": 4,
   "TYPE_TEXT": "004 - Amassado",
   "VIEW_ID": 748,
   "COLUNA": "D",
   "LINHA": 2
 },
 {
   "ID": "2024-3022168",
   "DATA DETECCAO": "2024-03-05-11.12.35.000000",
   "PONTO": "ZP5",
   "LOC_ID": 5355,
   "LOC": "Painel lateral",
   "POS_ID": 10,
   "POS": "direito externo",
   "TYPE_ID": 4,
   "TYPE_TEXT": "004 - Amassado",
   "VIEW_ID": 764,
   "COLUNA": "E",
   "LINHA": 6
 },
 {
   "ID": "2024-1742108",
   "DATA DETECCAO": "2024-03-07-11.56.22.000000",
   "PONTO": "ZP5",
   "LOC_ID": 5355,
   "LOC": "Painel lateral",
   "POS_ID": 17,
   "POS": "esquerdo externo",
   "TYPE_ID": 185,
   "TYPE_TEXT": "185 - Falta Rebite",
   "VIEW_ID": 744,
   "COLUNA": "C",
   "LINHA": 2
 },
 {
   "ID": "2024-1742108",
   "DATA DETECCAO": "2024-03-07-11.56.28.000000",
   "PONTO": "ZP5",
   "LOC_ID": 53002,
   "LOC": "Canal de escoamento de água",
   "POS_ID": 10,
   "POS": "direito externo",
   "TYPE_ID": 89,
   "TYPE_TEXT": "089 - Res\\u00edduo de soldagem",
   "VIEW_ID": 691,
   "COLUNA": "G",
   "LINHA": 2
 },
 {
   "ID": "2024-2121169",
   "DATA DETECCAO": "2024-03-08-07.57.45.000000",
   "PONTO": "ZP5A",
   "LOC_ID": 5751,
   "LOC": "Porta dianteira",
   "POS_ID": 10,
   "POS": "direito externo",
   "TYPE_ID": 109,
   "TYPE_TEXT": "109 - Fervido",
   "VIEW_ID": 715,
   "COLUNA": "E",
   "LINHA": 4
 },
 {
   "ID": "2024-2121169",
   "DATA DETECCAO": "2024-03-08-07.57.54.000000",
   "PONTO": "ZP5A",
   "LOC_ID": 5851,
   "LOC": "Porta traseira",
   "POS_ID": 10,
   "POS": "direito externo",
   "TYPE_ID": 109,
   "TYPE_TEXT": "109 - Fervido",
   "VIEW_ID": 723,
   "COLUNA": "E",
   "LINHA": 4
 },
 {
   "ID": "2024-2121169",
   "DATA DETECCAO": "2024-03-08-07.58.11.000000",
   "PONTO": "ZP5A",
   "LOC_ID": 5355,
   "LOC": "Painel lateral",
   "POS_ID": 10,
   "POS": "direito externo",
   "TYPE_ID": 9,
   "TYPE_TEXT": "009 - Escorrido, gotas (coladura)",
   "VIEW_ID": 764,
   "COLUNA": "D",
   "LINHA": 5
 },
 {
   "ID": "2024-2121169",
   "DATA DETECCAO": "2024-03-08-07.58.22.000000",
   "PONTO": "ZP5A",
   "LOC_ID": 5355,
   "LOC": "Painel lateral",
   "POS_ID": 17,
   "POS": "esquerdo externo",
   "TYPE_ID": 9,
   "TYPE_TEXT": "009 - Escorrido, gotas (coladura)",
   "VIEW_ID": 744,
   "COLUNA": "F",
   "LINHA": 4
 },
 {
   "ID": "2024-2121169",
   "DATA DETECCAO": "2024-03-08-07.58.45.000000",
   "PONTO": "ZP5A",
   "LOC_ID": 5851,
   "LOC": "Porta traseira",
   "POS_ID": 17,
   "POS": "esquerdo externo",
   "TYPE_ID": 109,
   "TYPE_TEXT": "109 - Fervido",
   "VIEW_ID": 707,
   "COLUNA": "E",
   "LINHA": 4
 },
 {
   "ID": "2024-2121169",
   "DATA DETECCAO": "2024-03-08-07.58.55.000000",
   "PONTO": "ZP5A",
   "LOC_ID": 5751,
   "LOC": "Porta dianteira",
   "POS_ID": 17,
   "POS": "esquerdo externo",
   "TYPE_ID": 109,
   "TYPE_TEXT": "109 - Fervido",
   "VIEW_ID": 699,
   "COLUNA": "D",
   "LINHA": 4
 },
 {
   "ID": "2024-2121169",
   "DATA DETECCAO": "2024-03-08-07.59.11.000000",
   "PONTO": "ZP5A",
   "LOC_ID": 5559,
   "LOC": "Tampa traseira",
   "POS_ID": 1,
   "POS": "externo",
   "TYPE_ID": 9,
   "TYPE_TEXT": "009 - Escorrido, gotas (coladura)",
   "VIEW_ID": 673,
   "COLUNA": "D",
   "LINHA": 5
 },
 {
   "ID": "2024-1342087",
   "DATA DETECCAO": "2024-03-12-16.31.02.000000",
   "PONTO": "ZP5",
   "LOC_ID": 5055,
   "LOC": "Pára-lama dianteiro",
   "POS_ID": 17,
   "POS": "esquerdo externo",
   "TYPE_ID": 30,
   "TYPE_TEXT": "030 - Folga fechada / pequena",
   "VIEW_ID": 677,
   "COLUNA": "G",
   "LINHA": 3
 },
 {
   "ID": "2024-1342087",
   "DATA DETECCAO": "2024-03-12-16.31.09.000000",
   "PONTO": "ZP5",
   "LOC_ID": 5305,
   "LOC": "Paínel traseiro",
   "POS_ID": 1,
   "POS": "externo",
   "TYPE_ID": 19,
   "TYPE_TEXT": "019 - Deslocado",
   "VIEW_ID": 687,
   "COLUNA": "B",
   "LINHA": 4
 },
 {
   "ID": "2024-1731050",
   "DATA DETECCAO": "2024-03-14-11.22.52.000000",
   "PONTO": "ZP5A",
   "LOC_ID": 5751,
   "LOC": "Porta dianteira",
   "POS_ID": 17,
   "POS": "esquerdo externo",
   "TYPE_ID": 126,
   "TYPE_TEXT": "126 - Sujeiras, contamina\\u00e7\\u00f5es",
   "VIEW_ID": 699,
   "COLUNA": "C",
   "LINHA": 4
 },
 {
   "ID": "2024-1441247",
   "DATA DETECCAO": "2024-03-14-13.27.40.000000",
   "PONTO": "ZP5",
   "LOC_ID": 5103,
   "LOC": "Teto",
   "POS_ID": 1,
   "POS": "externo",
   "TYPE_ID": 4,
   "TYPE_TEXT": "004 - Amassado",
   "VIEW_ID": 665,
   "COLUNA": "D",
   "LINHA": 4
 },
 {
   "ID": "2024-1441247",
   "DATA DETECCAO": "2024-03-14-13.27.42.000000",
   "PONTO": "ZP5",
   "LOC_ID": 5103,
   "LOC": "Teto",
   "POS_ID": 1,
   "POS": "externo",
   "TYPE_ID": 4,
   "TYPE_TEXT": "004 - Amassado",
   "VIEW_ID": 665,
   "COLUNA": "D",
   "LINHA": 3
 },
 {
   "ID": "2024-1441247",
   "DATA DETECCAO": "2024-03-15-15.35.41.000000",
   "PONTO": "ZP5A",
   "LOC_ID": 5103,
   "LOC": "Teto",
   "POS_ID": 1,
   "POS": "externo",
   "TYPE_ID": 4,
   "TYPE_TEXT": "004 - Amassado",
   "VIEW_ID": 665,
   "COLUNA": "D",
   "LINHA": 4
 },
 {
   "ID": "2024-1441247",
   "DATA DETECCAO": "2024-03-15-15.35.55.000000",
   "PONTO": "ZP5A",
   "LOC_ID": 5103,
   "LOC": "Teto",
   "POS_ID": 1,
   "POS": "externo",
   "TYPE_ID": 4,
   "TYPE_TEXT": "004 - Amassado",
   "VIEW_ID": 665,
   "COLUNA": "D",
   "LINHA": 2
 },
 {
   "ID": "2024-1442137",
   "DATA DETECCAO": "2024-03-15-16.07.18.000000",
   "PONTO": "ZP5",
   "LOC_ID": 5141,
   "LOC": "Coluna B",
   "POS_ID": 17,
   "POS": "esquerdo externo",
   "TYPE_ID": 4,
   "TYPE_TEXT": "004 - Amassado",
   "VIEW_ID": 736,
   "COLUNA": "D",
   "LINHA": 4
 },
 {
   "ID": "2024-1442137",
   "DATA DETECCAO": "2024-03-15-16.07.18.000000",
   "PONTO": "ZP5",
   "LOC_ID": 51371,
   "LOC": "Coluna A",
   "POS_ID": 17,
   "POS": "esquerdo externo",
   "TYPE_ID": 4,
   "TYPE_TEXT": "004 - Amassado",
   "VIEW_ID": 732,
   "COLUNA": "C",
   "LINHA": 5
 },
 {
   "ID": "2024-1442137",
   "DATA DETECCAO": "2024-03-15-16.07.19.000000",
   "PONTO": "ZP5",
   "LOC_ID": 51371,
   "LOC": "Coluna A",
   "POS_ID": 17,
   "POS": "esquerdo externo",
   "TYPE_ID": 4,
   "TYPE_TEXT": "004 - Amassado",
   "VIEW_ID": 732,
   "COLUNA": "C",
   "LINHA": 3
 },
 {
   "ID": "2024-1731050",
   "DATA DETECCAO": "2024-03-15-17.37.38.000000",
   "PONTO": "ZP5A",
   "LOC_ID": 5522,
   "LOC": "Tampa dianteira",
   "POS_ID": 1,
   "POS": "externo",
   "TYPE_ID": 126,
   "TYPE_TEXT": "126 - Sujeiras, contamina\\u00e7\\u00f5es",
   "VIEW_ID": 661,
   "COLUNA": "C",
   "LINHA": 4
 }
]
```

E inseri na fila rabbitMq:


![image](https://github.com/user-attachments/assets/83548c3f-b1b1-480d-a196-184fe922f907)


Dessa forma, a mensagem foi consumida pelo pacote python, convertida para um arquivo parquet e salva no storage do supabase:

![image](https://github.com/user-attachments/assets/e67dccaa-6abc-4096-ac31-88a0d64aa5a8)

Storage:

![image](https://github.com/user-attachments/assets/b3a6bc2f-6053-42a4-9072-093d773e65e1)

Conteúdo do parquet:

![image](https://github.com/user-attachments/assets/a72f218c-c377-45a1-a79f-241313c4a09b)

