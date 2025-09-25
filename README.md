# sauter-university-2025-challenge

## ONS Data Ingestion Pipeline

Este projeto implementa um pipeline de ingestão de dados que busca arquivos no formato Parquet do portal de Dados Abertos do Operador Nacional do Sistema Elétrico (ONS), processa-os e os armazena no Google Cloud Storage (GCS).

A aplicação é construída em Python utilizando o framework FastAPI para expor uma API RESTful, que permite acionar o pipeline de forma programática. A arquitetura é projetada para ser modular e extensível, facilitando a manutenção e a adição de novas funcionalidades.

---

## 🛠 Tecnologias Utilizadas
- **Python 3.11**
- **FastAPI** — framework para APIs
- **Google BigQuery**
- **Google Cloud Storage**
- **Docker**
- **Pydantic** — validação de dados
- **Poetry** — gerenciamento de dependências
---

---

## Exemplo de arquivo .env:
```bash
GOOGLE_APPLICATION_CREDENTIALS=/caminho/para/seu/arquivo-de-credenciais.json
PROJECT_ID=seu-id-de-projeto-gcp
BASEURL_ONS=https://dados.ons.org.br/api/3/action
PACKAGE_ID=id-do-pacote-de-dados
BUCKET_PATH=raw/ons
GCP_DATASET_NAME=nome-do-seu-dataset-bigquery
GCP_TABLE_NAME=nome-da-sua-tabela-bigquery
GCP_BUCKET_NAME=seu-nome-de-bucket-aqui
```
---

## 🏗 Arquitetura
A API foi construída seguindo o padrão **Adapters**, garantindo:
- **Desacoplamento** entre módulos.
- **Flexibilidade** para troca de implementações.
- **Organização** clara da estrutura de pastas.
- **Facilidade de manutenção**.

**Diagrama Simplificado**:
Client → API Endpoints → Services → Adapters → Data Sources (BigQuery, GCS)

---

## ⚙️ Instalação
Clone o repositório:
```bash
git clone https://github.com/heytulio/sauter-university-2025-challenge.git
cd sauter-university-2025-challenge
```

Crie um ambiente virtual linux:
```bash
python -m venv env
source env/bin/activate
```

crie um ambiente virtual windows:
```bash
python -m venv env
.\env\Scripts\activate
```

Instale o Poetry: Siga este 
[instalacao_do_poetry_simples](https://python-poetry.org/docs/#installing-with-the-official-installer)

Instale as dependências:
```bash
poetry install
```

Uso local:
```bash
poetry run uvicorn src.main:app --reload
```

Uso Docker:
```bash
docker build -t sauter-api .
docker run --name sauter-api -p 8081:8000 sauter-api
```

Acesse o Swagger:

Aqui: http://127.0.0.1:8000/docs

---

Endpoints:

- **GET** `/bq` - Busca dados do BigQuery.
    - params:
        - `page`: int
        - `page_size`: int
        - `date`: str

- **POST** `/bucket` - Cria a pipeline de processamento dos dados no Google Cloud Storage. 
    - body:
        - `start_year`: int
        - `end_year`: int

---
*Resposta de Sucesso:*

json
{
  "status": "Pipeline executado com sucesso.",
  "ingested_files": true,
  "bucket": "seu-nome-de-bucket-aqui",
  "runtime": "15.234"
}


*Resposta de Falha:*

json
{
  "status": "Pipeline falhou.",
  "error": "Descrição do erro."
}

---