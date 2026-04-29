# TrustOps RAG - Technology Decisions

Status: Draft v2.0  
Role: This document records the selected technology stack, the rationale behind each choice, and the conditions under which a choice may be revisited. It does not define product behavior or architecture rules.

## 1. Selection principles

1. Prefer explicit control flow over framework magic.
2. Prefer technologies that work locally and in production with the same conceptual model.
3. Keep the online request path observable and debuggable.
4. Avoid premature distributed-system complexity.
5. Use abstractions at provider boundaries, not at every internal call site.

## 2. Primary stack

| Domain | Selected technology | Why this is the default choice | Notes |
| --- | --- | --- | --- |
| Backend language | Python 3.12 | Mature ecosystem for retrieval, ML, and service code | Python 3.11 is acceptable if platform constraints require it |
| API framework | FastAPI + Pydantic v2 | Strong typing, OpenAPI generation, good async support | Good fit for contract-first service boundaries |
| ASGI runtime | Uvicorn for local, Gunicorn + Uvicorn workers for production | Simple local dev and stable multi-worker production model | Tune worker count by latency and model mix |
| Relational store | PostgreSQL 16 | Strong transactional guarantees and operational maturity | System of record for business state |
| Vector search | pgvector | Keeps retrieval close to transactional metadata and simplifies local reproducibility | Revisit only if scale or recall profile outgrows PostgreSQL |
| Cache and broker | Redis 7 | Fast cache, simple queue backend, broad operational familiarity | Do not store authoritative business state only in Redis |
| Object storage | S3-compatible storage, MinIO locally | Required for raw document artifacts and reproducible document versions | Cloud-managed object storage in enterprise mode |
| Async jobs | Celery with Redis broker for baseline | Widely understood pattern for ingestion and review workflows | Broker abstraction should allow future migration if needed |
| PDF parsing | PyMuPDF | Good performance and extraction quality for enterprise PDFs | Add OCR path only when document corpus requires it |
| Markdown parsing | `markdown-it-py` | Predictable parsing for Markdown knowledge assets | Lightweight and easy to test |
| Embeddings | `sentence-transformers` | Local baseline, low friction, reproducible benchmarks | Provider adapter can support remote embeddings later |
| Lexical retrieval | `rank-bm25` | Lightweight baseline BM25 implementation | Move to search engine only if scale or features demand it |
| Reranking | `sentence-transformers` CrossEncoder | Good quality-to-complexity ratio for first production milestone | Keep reranker optional in degraded mode |
| Numeric and analysis tooling | `numpy`, `pandas`, `scikit-learn` | Evaluation, scoring, reporting, and dataset tooling | Not all of these belong in the request path |
| Local model serving | Ollama | Reproducible local mode without external API keys | Default local provider only |
| Hosted model providers | OpenAI SDK and Azure OpenAI adapter | Gives production path for stronger hosted models | Must be accessed through provider interface, not directly from business modules |
| Security controls | `slowapi`, Presidio, OIDC/JWKS validation helpers | Covers rate limiting, PII handling, and enterprise identity integration | `python-dotenv` is local-only convenience, not production secret management |
| Structured logging | `structlog` | Better long-term operability than ad hoc logging | Prefer JSON logs end to end |
| Metrics | Prometheus | Standard metrics scraping for service and worker telemetry | Combine with RED and USE dashboards |
| Tracing | OpenTelemetry | Vendor-neutral tracing model across API and workers | Required for latency decomposition |
| Dashboards | Grafana | Strong fit with Prometheus and OTEL exports | Dashboard definitions should be versioned |
| Frontend | React + Vite + TypeScript | Strong tooling and maintainability | Keep UI thin; business rules stay in backend |
| Testing | `pytest`, `pytest-asyncio`, `httpx`, `locust`, `mypy`, `ruff` | Balanced local speed and production-oriented coverage | Type checks and lint should block merges |
| Contract testing | Schemathesis or equivalent OpenAPI contract tests | Protects the API contract as the platform evolves | Strongly recommended before any external pilot |
| CI/CD | GitHub Actions | Sufficient for baseline automation and release gates | Add image scanning and dependency scanning |
| Local orchestration | Docker Compose | Required for reproducible local mode | Must bring up API, workers, data stores, and observability |
| Production orchestration | Kubernetes or managed container platform | Enterprise deployment target, not local requirement | Final choice depends on hosting standards of the organization |

## 3. Technology guardrails

- Do not use LangChain or similar orchestration frameworks as the core control plane.
- Provider calls must go through internal interfaces so model routing and audit remain centralized.
- Redis may accelerate the system, but PostgreSQL remains the source of truth.
- Evaluation libraries such as Ragas or DeepEval are optional helpers, not the primary truth model.
- Frontend code must not reimplement backend decision logic.

## 4. Deferred or conditional choices

These technologies are intentionally deferred until there is measured need:

| Deferred choice | Why it is deferred | Trigger to revisit |
| --- | --- | --- |
| OpenSearch or Elasticsearch | Adds operational complexity beyond current needs | Retrieval corpus size, advanced filtering, or recall profile exceeds pgvector + BM25 baseline |
| Kafka or RabbitMQ | Not required for first milestone if async volume is moderate | Worker throughput, ordering, or cross-team eventing complexity grows |
| Dedicated workflow engine | Ticket lifecycle is initially simple enough for application-driven orchestration | Approval process becomes multi-step, regulated, or highly parallel |
| OCR pipeline by default | Not every corpus needs it and it increases ingestion complexity | Document corpus contains scanned PDFs at meaningful volume |
| Multi-region active-active | High operational cost and hard consistency tradeoffs | Jurisdictional requirements or latency targets require it |

## 5. Engineering standards attached to the stack

- Typed Python is mandatory for application boundaries and core domain logic.
- Linting, type checking, unit tests, integration tests, and security checks must run in CI.
- Dependency and container image scanning should be part of the delivery pipeline.
- OpenAPI output is a release artifact and should be version-controlled or snapshotted.
- Contract artifacts such as `Idempotency-Key`, `policy_version`, and closed response enums must be preserved consistently across API, workers, UI, and tests.
- Observability instrumentation is not optional for new request-path components.

## 6. Review cadence

This stack should be reviewed when one of the following happens:

- production latency or cost targets are consistently missed
- tenant isolation or compliance requirements tighten
- corpus scale changes retrieval economics materially
- hosted provider strategy changes at the organization level
- benchmark results show the current stack is the limiting factor
