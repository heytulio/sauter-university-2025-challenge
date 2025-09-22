# Usar imagem oficial do Python
FROM python:3.11-slim

# Variáveis de ambiente
ENV POETRY_VERSION=1.8.2 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Instalar poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Adicionar Poetry ao PATH
ENV PATH="/root/.local/bin:$PATH"

# Criar diretório da aplicação
WORKDIR /app

# Copiar arquivos de configuração primeiro (para cache de dependências)
COPY pyproject.toml poetry.lock* /app/

# --- CORREÇÃO 1: Usar a sintaxe moderna do Poetry ---
# Instalar dependências de produção (apenas do grupo 'main')
RUN poetry install --only main --no-root

# Copiar código do projeto
COPY . /app

# Expor porta do FastAPI
EXPOSE 8080

# --- CORREÇÃO 2: Apontar para o caminho correto do seu app ---
# Comando para rodar a API (src.main:app em vez de main:app)
CMD ["sh", "-c", "poetry run uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
