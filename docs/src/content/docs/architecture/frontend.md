---
title: Frontend
description: Páginas e componentes do frontend Next.js.
---

## Stack

- **Framework**: Next.js 14
- **QR Scanner**: `html5-qrcode` (importação dinâmica, sem SSR)
- **Hosting**: Vercel

## Páginas (`frontend/src/app/`)

| Rota | Descrição |
|------|-----------|
| `/` | Landing page com informações do projeto |
| `/scan` | Scanner de câmera QR (html5-qrcode, sem SSR) |
| `/results` | Busca e exibe `results.json` do CloudFront |

## Variáveis de Ambiente

Crie `.env.local` na pasta `frontend/`:

```bash
NEXT_PUBLIC_API_URL=https://<api-id>.execute-api.<region>.amazonaws.com/Prod
NEXT_PUBLIC_RESULTS_URL=https://<cloudfront-id>.cloudfront.net
```

## Comandos

```bash
cd frontend
npm install
npm run dev          # Servidor de desenvolvimento
npm run build        # Build de produção
npm run lint         # ESLint
npm run storybook    # Storybook em :6006

# Testes unitários (Vitest)
npx vitest run

# Testes E2E (Playwright)
npx playwright test
```
