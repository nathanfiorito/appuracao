# Security Checklist

## Base
- [ ] `.env` in `.gitignore`, `.env.example` with placeholder values only
- [ ] HTTPS enforced everywhere (API Gateway + CloudFront + Vercel)
- [ ] All inputs validated with Pydantic models
- [ ] Dependencies audited (`pip audit` + `npm audit`)

## AWS / Serverless
- [ ] IAM roles with least privilege per Lambda (each Lambda only accesses what it needs)
- [ ] S3 results bucket: public read via CloudFront OAC only, write only by publish Lambda
- [ ] API Gateway request validation enabled (JSON schema) before VTL mapping
- [ ] API Gateway throttling configured (50 req/s sustained, 100 burst)
- [ ] CloudTrail enabled
- [ ] No hardcoded credentials anywhere (use env vars / Secrets Manager)

## Electoral data integrity
- [ ] Never accept BU without signature verification (sig_verified flag)
- [ ] Deduplication by composite key: `{PROC}#{PLEI}#{TURN}` + `{UNFE}#{MUNI}#{ZONA}#{SECA}`
- [ ] Duplicate with different signature → flagged for manual review
- [ ] Raw QR text stored for independent audit
- [ ] BUs are immutable: insert-only (DynamoDB ConditionExpression)
- [ ] Cross-validation: TOTC == NOMI + LEGC + BRAN + NULO

## Frontend
- [ ] CORS restricted to Vercel origin only
- [ ] No sensitive data in client-side code or localStorage
- [ ] CSP headers via Vercel config

## Known TSE public key (2024 election)
`CF3AF898467A5B7A52D33D53BC037E2642A8DA996903FC252217E9C033E2F291`
