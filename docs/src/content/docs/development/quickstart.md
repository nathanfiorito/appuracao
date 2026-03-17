---
title: Início Rápido
description: Como configurar o ambiente de desenvolvimento localmente.
---

## Pré-requisitos

- Python 3.11+
- Node.js 22+
- AWS CLI + SAM CLI
- Git

## 1. Clone o repositório

```bash
git clone https://github.com/nathanfiorito/appuracao.git
cd appuracao
```

## 2. Backend (Python)

```bash
# Instalar dependências (da raiz do repositório)
pip install -e ".[dev]"

# Verificar instalação
pytest tests/
```

## 3. Frontend (Next.js)

```bash
cd frontend
npm install

# Criar arquivo de variáveis de ambiente
cp .env.example .env.local
# Edite .env.local com suas URLs
```

```bash
npm run dev   # Inicia em http://localhost:3000
```

## 4. Infraestrutura AWS (opcional)

```bash
cd infrastructure

# Buscar chaves públicas do TSE
python scripts/fetch_tse_keys.py

# Primeiro deploy (interativo)
sam build
sam deploy --guided
```

## 5. Documentação (este site)

```bash
cd docs
npm install
npm run dev   # Inicia em http://localhost:4321
```

## Estrutura do Repositório

```
appuracao/
├── backend/          # Módulos Python (parser, verifier, etc.)
├── frontend/         # Next.js
├── infrastructure/   # AWS SAM template + Step Functions
│   ├── lambdas/      # 7 handlers Lambda
│   ├── statemachine/ # ASL do Step Functions
│   └── vtl/          # Mapeamentos VTL do API Gateway
├── docs/             # Esta documentação (Astro Starlight)
├── tests/            # Testes pytest do backend
└── keys/             # Chaves públicas do TSE
```
