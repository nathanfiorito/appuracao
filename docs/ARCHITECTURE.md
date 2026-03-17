# Architecture

## Overview

Serverless parallel vote counting system based on QR Code data from Brazilian electronic ballot boxes (Boletim de Urna).

## Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Frontend | Next.js / Vercel | Camera access via `html5-qrcode`, SSR, free hosting |
| API Ingest | API Gateway REST + VTL | Zero Lambda on ingest path, direct Step Functions integration |
| Orchestration | Step Functions Express | Per-step retry, AWS console observability |
| Processing | Lambda (Python 3.11) | Individual functions: parse, assemble, verify, deduplicate, store, tally, publish |
| Database | DynamoDB | Serverless, permanent free tier (25GB), key-value ideal for BU lookup |
| Storage | S3 | Static JSON results |
| CDN | CloudFront | Public results serving |
| IaC | AWS SAM | Infra as code |
| Crypto | PyNaCl (libsodium) | Ed25519 signature verification |
| Hashing | hashlib (stdlib) | SHA-512 |

## Data Flow

```
[Mobile: camera scans QR Code]
    |
    v
[Browser: html5-qrcode decodes → raw alphanumeric text]
    |
    v
[POST /bulletins — sends raw QR text(s)]
    |
    v
[API Gateway REST]
    |  VTL Mapping: body → Step Functions input
    v
[Step Functions Express]
    ├─ Step 1: Parse      — tag:value → BulletinData struct
    ├─ Step 2: Assemble   — multi-QR reassembly (if needed)
    ├─ Step 3: Verify     — SHA-512 + Ed25519 signature
    ├─ Step 4: Deduplicate — check DynamoDB by PK/SK
    ├─ Step 5: Store      — write immutable BU to DynamoDB
    ├─ Step 6: Tally      — recompute full aggregation
    └─ Step 7: Publish    — write results.json → S3
    |
    v
[CloudFront serves results.json]
```

## DynamoDB Schema

### `bulletins` table
- **PK**: `{PROC}#{PLEI}#{TURN}` (election process key)
- **SK**: `{UNFE}#{MUNI}#{ZONA}#{SECA}` (section identifier)
- Attributes: `raw_text`, `eligible_voters`, `compared_voters`, `absent_voters`, `elections` (JSON), `hash_value`, `signature`, `sig_verified`, `created_at`

### `partial_qrcodes` table (multi-QR assembly buffer)
- **PK**: `session_id` (= API Gateway `requestId`)
- **SK**: `qr_index` (1-based)
- **TTL**: 1 hour
- Attributes: `total`, `raw_text`

## Security Model

- All BUs must pass SHA-512 hash + Ed25519 signature verification
- Deduplication by composite key prevents replay attacks
- BUs are immutable (DynamoDB `ConditionExpression: attribute_not_exists(pk)`)
- Raw QR text stored for independent audit
- S3 bucket write-only by publish Lambda; read via CloudFront OAC only
- API Gateway request validation (JSON schema) before VTL
- Throttling: 50 req/s sustained, 100 burst

## Cost (municipal scale, ~500 sections)

| Service | Cost |
|---------|------|
| Lambda (7 × 500 invocations) | Free tier |
| API Gateway (500 calls) | Free tier |
| Step Functions Express | ~$0.004 |
| DynamoDB | Free tier |
| S3 | Free tier |
| CloudFront | Free tier |
| **Total** | **~$0.004/election** |
