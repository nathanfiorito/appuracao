---
title: Checklist de Segurança
description: Requisitos de segurança para deploy em produção.
---

## Base

- [ ] `.env` no `.gitignore`, `.env.example` apenas com valores placeholder
- [ ] HTTPS em todo o stack (API Gateway + CloudFront + Vercel)
- [ ] Todos os inputs validados com modelos Pydantic
- [ ] Dependências auditadas (`pip audit` + `npm audit`)

## AWS / Serverless

- [ ] IAM roles com least privilege por Lambda (cada Lambda acessa apenas o necessário)
- [ ] Bucket S3 de resultados: leitura pública via CloudFront OAC, escrita apenas pela Lambda de publicação
- [ ] Validação de request no API Gateway habilitada (JSON schema) antes do mapeamento VTL
- [ ] Throttling no API Gateway configurado (50 req/s sustentado, 100 burst)
- [ ] CloudTrail habilitado
- [ ] Sem credenciais hardcoded em nenhum lugar (usar env vars / Secrets Manager)

## Integridade dos Dados Eleitorais

- [ ] Nunca aceitar BU sem verificação de assinatura (flag `sig_verified`)
- [ ] Deduplicação por chave composta: `{PROC}#{PLEI}#{TURN}` + `{UNFE}#{MUNI}#{ZONA}#{SECA}`
- [ ] Duplicata com assinatura diferente → sinalizar para revisão manual
- [ ] Texto QR bruto armazenado para auditoria independente
- [ ] BUs imutáveis: insert-only (`ConditionExpression` no DynamoDB)
- [ ] Validação cruzada: `TOTC == NOMI + LEGC + BRAN + NULO`

## Frontend

- [ ] CORS restrito à origem Vercel apenas
- [ ] Sem dados sensíveis em código client-side ou localStorage
- [ ] Headers CSP via configuração Vercel

## Chave Pública TSE Conhecida (eleição 2024)

```
CF3AF898467A5B7A52D33D53BC037E2642A8DA996903FC252217E9C033E2F291
```

:::caution
Sempre busque as chaves mais recentes via `python scripts/fetch_tse_keys.py` antes de cada eleição.
:::
