---
title: Testes
description: Estratégia de testes do backend, frontend e E2E.
---

## Backend (pytest)

```bash
# Da raiz do repositório
pytest tests/

# Arquivo específico
pytest tests/test_parser.py

# Com cobertura
pytest --cov=backend tests/

# Lint
ruff check backend/
ruff format backend/
```

Usa **moto** para simular DynamoDB e S3 — cada handler Lambda é testável em isolamento.

## Frontend (Vitest)

```bash
cd frontend

# Rodar todos os testes unitários
npx vitest run

# Arquivo específico
npx vitest run src/components/QrScanner.test.tsx
```

## Testes E2E (Playwright)

```bash
cd frontend
npx playwright test
```

## Storybook

```bash
cd frontend
npm run storybook   # Inicia em http://localhost:6006
```

Stories ficam em `src/components/**/*.stories.tsx`.

## Estratégia

| Tipo | Ferramenta | Escopo |
|------|-----------|--------|
| Unitário backend | pytest + moto | Cada módulo e Lambda handler |
| Unitário frontend | Vitest | Componentes React |
| E2E | Playwright | Fluxos completos no browser |
| Componentes visuais | Storybook | UI isolado |
