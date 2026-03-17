# Apuração Paralela

Independent parallel vote counting via QR Code from Brazilian electronic ballot boxes (Boletim de Urna).

## How it works

1. After polls close, each polling section posts its official Boletim de Urna (BU) — a paper printout with QR codes
2. Any citizen scans the QR code with their phone camera
3. The app decodes the QR text in the browser and submits it to the API
4. The backend verifies the SHA-512 hash and Ed25519 signature (issued by TSE)
5. Valid BUs are stored and aggregated; results are published as public JSON via CloudFront

## Stack

- **Frontend**: Next.js (Vercel) + `html5-qrcode`
- **Backend**: Python 3.11 Lambdas + Step Functions + DynamoDB + S3 + CloudFront
- **IaC**: AWS SAM

## Getting started

### Backend

```bash
pip install -e ".[dev]"
pytest tests/
```

### Infrastructure

```bash
# Get TSE public key
python scripts/fetch_tse_keys.py --election-year 2024

# Build and deploy
cd infrastructure
sam build
sam deploy --guided
```

### Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local  # set NEXT_PUBLIC_API_URL and NEXT_PUBLIC_RESULTS_URL
npm run dev
```

## Docs

- [Architecture](docs/ARCHITECTURE.md)
- [Security Checklist](docs/SECURITY-CHECKLIST.md)
