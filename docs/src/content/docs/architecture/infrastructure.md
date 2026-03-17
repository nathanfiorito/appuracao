---
title: Infraestrutura
description: AWS SAM, Step Functions e recursos de infraestrutura.
---

## Stack AWS

| Serviço | Uso |
|---------|-----|
| API Gateway REST | Recebe POST /bulletins, valida schema, mapeia via VTL direto para Step Functions |
| Step Functions Express | Orquestra os 7 passos com retry automático |
| Lambda (Python 3.11) | 7 funções isoladas, uma por etapa |
| DynamoDB (on-demand) | Armazenamento de BUs e buffer multi-QR |
| S3 | Armazena `results.json` |
| CloudFront + OAC | CDN pública para resultados |
| AWS SAM | IaC — `infrastructure/template.yaml` |

## Custo (escala municipal, ~500 seções)

| Serviço | Custo |
|---------|-------|
| Lambda (7 × 500 invocações) | Free tier |
| API Gateway (500 chamadas) | Free tier |
| Step Functions Express | ~$0.004 |
| DynamoDB | Free tier |
| S3 | Free tier |
| CloudFront | Free tier |
| **Total** | **~$0.004/eleição** |

## Deploy

```bash
cd infrastructure

# Buscar chaves públicas do TSE (pré-requisito)
python scripts/fetch_tse_keys.py

# Build e deploy
sam build
sam deploy --guided   # Primeira vez (salva parâmetros em samconfig.toml)
sam deploy            # Deploys subsequentes

# Testar Lambda localmente
sam local invoke ParseFunction --event events/parse_event.json
```

## Throttling API Gateway

- 50 req/s sustentado
- 100 burst

## State Machine

`statemachine/bulletin_processing.asl.json` define cada passo com retry individual.

## VTL Mapping

`vtl/` contém os templates de mapeamento do API Gateway que transformam o body do POST no input do Step Functions.
