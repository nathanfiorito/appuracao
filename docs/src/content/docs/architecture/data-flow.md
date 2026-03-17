---
title: Fluxo de Dados
description: Fluxo completo desde o scan do QR Code até a publicação dos resultados.
---

## Visão Geral

```
Browser (html5-qrcode)
  → POST /bulletins [array de strings QR brutas]
  → API Gateway (VTL mapeia para input do Step Functions)
  → Step Functions Express
      1. Parse      — formato tag:value do TSE → BulletinData (Pydantic)
      2. Assemble   — agrupa partes de QR multi-parte no DynamoDB (TTL 1h)
      3. Verify     — hash SHA-512 + assinatura Ed25519 (chave pública TSE)
      4. Deduplicate — consulta DynamoDB por chave composta; rejeita replay
      5. Store      — escrita condicional no DynamoDB (imutável, QR bruto armazenado)
      6. Tally      — scan completo da tabela → resultados agregados por cargo/candidato
      7. Publish    — grava results.json no S3 (servido via CloudFront OAC)
```

## Identificadores de Dados

### Chave de Processo (PK de deduplicação)
```
{PROC}#{PLEI}#{TURN}
```
Processo eleitoral, pleito e turno.

### Chave de Seção (SK de deduplicação)
```
{UNFE}#{MUNI}#{ZONA}#{SECA}
```
UF, município, zona eleitoral e seção.

### Sessões Multi-QR
O `requestId` do API Gateway agrupa as partes na tabela `partial_qrcodes`.

## Esquema DynamoDB

### Tabela `bulletins`

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `pk` | String (PK) | `{PROC}#{PLEI}#{TURN}` |
| `sk` | String (SK) | `{UNFE}#{MUNI}#{ZONA}#{SECA}` |
| `raw_text` | String | QR bruto para auditoria independente |
| `eligible_voters` | Number | Eleitores aptos |
| `compared_voters` | Number | Comparecimento |
| `absent_voters` | Number | Abstenções |
| `elections` | JSON | Votos por cargo e candidato |
| `hash_value` | String | Hash SHA-512 |
| `signature` | String | Assinatura Ed25519 |
| `sig_verified` | Boolean | Resultado da verificação |
| `created_at` | String | ISO 8601 |

### Tabela `partial_qrcodes` (buffer de montagem)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `session_id` | String (PK) | `requestId` do API Gateway |
| `qr_index` | Number (SK) | Índice base 1 |
| `total` | Number | Total de partes esperadas |
| `raw_text` | String | Texto da parte |
| TTL | Number | Expira em 1 hora |
