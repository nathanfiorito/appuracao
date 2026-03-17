---
title: Backend
description: Módulos Python do backend e suas responsabilidades.
---

## Stack

- **Runtime**: Python 3.11
- **Framework**: AWS Lambda + Step Functions Express
- **Validação**: Pydantic
- **Criptografia**: PyNaCl (libsodium) para Ed25519, `hashlib` stdlib para SHA-512

## Módulos (`backend/`)

| Módulo | Responsabilidade |
|--------|-----------------|
| `qrcode/parser.py` | Parseia o formato tag:value do TSE em `BulletinData`; trata multi-QR com cabeçalho `QRBU:index:total` |
| `qrcode/assembler.py` | Remonta QRs multi-parte a partir do buffer no DynamoDB |
| `qrcode/models.py` | Modelos Pydantic: `BulletinData`, `ElectionResult`, `CandidateVotes`, `QRCodePart`, `IngestRequest` |
| `crypto/verifier.py` | Verificação de assinatura Ed25519 (PyNaCl) |
| `crypto/hasher.py` | Verificação de hash SHA-512 |
| `crypto/keys.py` | Carrega chaves públicas do TSE do diretório `keys/` |
| `storage/dynamodb.py` | Tabelas `bulletins` (store/dedup) e `partial_qrcodes` (buffer de montagem) |
| `storage/s3.py` | Publica `results.json` |
| `tallying/aggregator.py` | Scan da tabela bulletins e agregação de votos por processo→cargo→candidato |
| `lambdas/` | 7 handlers; cada um importa apenas os módulos que precisa |

## Lambdas

Cada Lambda é responsável por uma única etapa do Step Functions:

1. **ParseFunction** — `lambdas/parse_handler.py`
2. **AssembleFunction** — `lambdas/assemble_handler.py`
3. **VerifyFunction** — `lambdas/verify_handler.py`
4. **DeduplicateFunction** — `lambdas/deduplicate_handler.py`
5. **StoreFunction** — `lambdas/store_handler.py`
6. **TallyFunction** — `lambdas/tally_handler.py`
7. **PublishFunction** — `lambdas/publish_handler.py`

## Retry Policy

Configurado no Step Functions (`statemachine/bulletin_processing.asl.json`):
- Intervalo: 2 segundos
- Tentativas: 3
- Backoff: 2×
