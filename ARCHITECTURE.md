# TrustOps RAG - Reference Architecture

Status: Draft v2.0  
Role: This document is the single source of truth for runtime architecture, data architecture, non-functional requirements, and operational controls. `SPEC.md` defines what the product must do. `STACK.md` defines which technologies are selected to implement this architecture.

## 1. Architectural thesis

TrustOps RAG is a production-oriented, risk-aware RAG platform for enterprise knowledge workflows. Its design priority is not maximum answer volume. Its priority is controlled behavior under uncertainty.

Core rule:

> The platform must prefer a safe refusal or human escalation over an unsupported answer.

## 2. Architecture principles

1. Evidence before fluency.
2. Fail safe before fail open.
3. Auditability is a first-class system requirement.
4. Security and tenant isolation are part of the request path, not an afterthought.
5. The system should start as a modular monolith with clear internal boundaries, not as premature microservices.
6. Local reproducibility is mandatory, but production topology must support enterprise controls.
7. Online behavior must be measurable and comparable against an offline evaluation baseline.

## 3. Operating modes

| Mode | Goal | Characteristics |
| --- | --- | --- |
| Local reproducible | Developer onboarding, demos, deterministic benchmarking | Single environment, local models, Docker Compose, reduced security integrations |
| Enterprise production | Internal pilot or multinational rollout | Managed identity, replicated services, centralized observability, stronger access control, operational SLOs |

The software architecture remains the same across both modes. Only deployment topology and provider integrations change.

## 4. System context

```txt
End User
  -> Web UI
  -> API Gateway / WAF
  -> TrustOps API

Reviewer
  -> Review Console
  -> API Gateway / WAF
  -> TrustOps API

Content Owner
  -> Document API
  -> Ingestion Workers

TrustOps API
  -> PostgreSQL / pgvector
  -> Redis
  -> Model Provider Adapter
  -> Audit / Metrics / Tracing

Ingestion Workers
  -> Object Storage
  -> PostgreSQL / pgvector
  -> Redis

Enterprise Integrations
  -> OIDC Identity Provider
  -> SIEM / Log Sink
  -> Backup / Key Management
```

## 5. Service model

The recommended implementation model is a modular monolith plus worker processes.

### Synchronous plane

- `api-service`: FastAPI application exposing external APIs
- `web-ui`: end-user interface
- `review-console`: reviewer interface

### Asynchronous plane

- `ingestion-worker`: parsing, chunking, embedding, indexing, version activation
- `review-worker`: ticket routing, SLA monitoring, notifications, feedback propagation
- `scheduler`: recurring evaluation jobs, cost projections, maintenance tasks

### Data and control plane

- relational system of record
- vector storage
- cache and broker
- object storage for raw artifacts
- metrics, tracing, and structured logs

This architecture deliberately avoids splitting business domains into separate network services until scale or ownership boundaries justify that complexity.

## 6. Internal domain boundaries

The codebase should enforce these boundaries even if deployed as one service:

- Edge and API: request validation, response serialization, auth context propagation
- Policy and security: rate limiting, prompt injection checks, PII handling, ACL enforcement
- Query understanding: intent, risk, complexity, rewriting
- Retrieval and ranking: dense search, BM25, metadata filters, reranking, evidence assembly
- Generation and reliability: prompt building, model routing, answer parsing, validation, confidence scoring
- Decisioning: policy rules, fail-safe routing, warning logic, ticket creation decisions
- Human review: ticket lifecycle, reviewer actions, assignment, SLA tracking
- Feedback and evaluation: failure taxonomy, correction analysis, benchmark execution
- Observability and governance: audit events, traces, metrics, cost accounting

### Policy control model

- `policy_version` is a first-class control-plane artifact, not a hidden config detail.
- It versions decision thresholds, warning behavior, `decision_reason` enum values, cache eligibility rules, and degraded-mode semantics.
- Any change that can alter request outcome must require a `policy_version` bump.
- Requests, answers, tickets, audit events, cache entries, and evaluation runs must persist the effective `policy_version`.

## 7. Synchronous request path

Canonical runtime flow for `POST /ask`:

1. Gateway authenticates caller, applies WAF and coarse rate limits.
2. API validates schema, resolves idempotency context, and assigns `request_id`.
3. Security layer checks tenant context, input policy, prompt injection heuristics, and PII policy.
4. Query understanding computes intent, risk level, and complexity.
5. Retrieval fetches candidate chunks using hybrid search over active document versions only.
6. Reranking orders candidates and removes weak evidence.
7. Context builder assembles an evidence pack with citations and budget-aware compression.
8. Model router selects provider and model according to risk, complexity, budget, and policy.
9. Generation produces structured output only.
10. Reliability layer validates claims, contradiction, evidence support, and confidence.
11. Decision engine returns `answered`, `answered_with_warning`, `human_review_required`, `blocked`, or `failed_safe`.
12. Audit, tracing, cost, and decision telemetry are persisted before request completion.

### Latency budget guidance

For non-escalated responses, the target p95 budget should be managed explicitly:

- edge and auth: `<= 150 ms`
- retrieval and reranking: `<= 1200 ms`
- generation: `<= 5000 ms`
- validation and decisioning: `<= 1500 ms`
- total p95: `<= 8000 ms`

## 8. Asynchronous pipelines

### 8.1 Ingestion pipeline

1. Document is uploaded or imported.
2. Raw artifact is stored immutably.
3. Parser extracts normalized text and metadata.
4. Cleaner and deduplicator remove noise.
5. Chunker produces version-scoped chunks.
6. Embedding generator creates vectors.
7. Indexers update dense and lexical retrieval structures.
8. Version is validated and then marked active.
9. Cache invalidation is triggered for impacted policies or document families.

### 8.2 Human review pipeline

1. Decision engine creates ticket in the same business transaction or outbox flow.
2. Assignment rules route by domain, jurisdiction, or team.
3. Reviewer action updates ticket state and may create corrected answer artifacts.
4. Feedback events are emitted for evaluation and retrieval improvement.
5. Cache entries related to corrected answers are invalidated.

### 8.3 Evaluation pipeline

1. Curated dataset is loaded.
2. Baseline pipeline is executed.
3. TrustOps pipeline is executed under the same dataset and pinned `policy_version`.
4. Comparative metrics and cost reports are published.

All asynchronous workflows must be idempotent, retry-safe, and observable.

## 9. Data architecture

### 9.1 Storage roles

| Store | Role | Rules |
| --- | --- | --- |
| PostgreSQL | System of record for business state | Authoritative source for documents, versions, queries, answers, tickets, and audit metadata |
| pgvector | Dense retrieval inside PostgreSQL | Version-aware and tenant-aware retrieval only |
| Redis | Cache and async broker | No authoritative business state stored only in Redis |
| Object storage | Raw document artifacts and large derived assets | Immutable versioned storage |
| Metrics and log backends | Telemetry | Must support tenant-safe redaction and retention policies |

### 9.2 Core logical entities

- `documents`
- `document_versions`
- `document_chunks`
- `queries`
- `retrieval_results`
- `answers`
- `model_calls`
- `reliability_reports`
- `decision_logs`
- `tickets`
- `human_reviews`
- `feedback_events`
- `evaluation_runs`
- `audit_events`
- `cache_entries`

### 9.3 Data governance rules

- Every chunk must belong to exactly one document version.
- Only active document versions may participate in online retrieval.
- Tenant identity and document ACL metadata must be attached before retrieval filtering.
- Audit events must be append-only from the application perspective.
- Idempotency keys must be unique per tenant and request scope for the configured replay window.
- `policy_version` must be queryable across requests, answers, tickets, and evaluation runs.

## 10. Security and compliance architecture

### Identity and access

- Production mode must integrate with enterprise OIDC or SAML-backed identity.
- API authorization must propagate tenant, role, and scope into the application layer.
- Retrieval must enforce document-level ACL filtering before reranking and before final citation selection.

### Data protection

- TLS in transit and encryption at rest are mandatory in production.
- Secrets must come from managed secret storage, not from repository files.
- PII minimization is applied before persistence when policy requires it.

### Threat controls

- WAF and API gateway for coarse filtering
- request validation and rate limiting
- prompt injection and prompt exfiltration detection
- structured audit trail for abusive or blocked requests
- log redaction to prevent sensitive content leakage

### Compliance posture

The platform should be designed so that audit evidence can answer:

- who asked
- which documents were considered
- which model responded
- why the system answered, warned, escalated, or blocked
- which human changed the outcome, if any

## 11. Reliability and fail-safe design

### Mandatory behavior

- No automatic answer without citations.
- No answer from inactive or superseded document versions.
- No high-risk cache replay.
- No final response if the system cannot persist the audit-critical outcome.

### Degraded modes

- reranker unavailable: fall back to hybrid retrieval ranking and mark contract `system_state=degraded`
- BM25 unavailable: continue with dense retrieval if evidence remains sufficient
- dense retrieval unavailable: continue with BM25 only for low or medium risk, otherwise escalate
- primary model unavailable: use approved fallback model
- validation failure: escalate or fail safe, never auto-answer
- cost threshold breach: route to cheaper approved model or escalate

### Consistency patterns

- Request writes that create answer state, decision logs, and ticket state should use transactional boundaries.
- Cross-component side effects should use an outbox pattern or equivalent durable event handoff.
- Worker retries must be idempotent by business key, not only by transport message id.

## 12. Service level objectives

### Baseline target for internal pilot

- `POST /ask` availability: `99.5%`
- non-escalated p95 latency: `<= 8 s`
- audit completeness: `100%`
- automatic answer citation coverage: `100%`
- correct escalation rate on release dataset: `>= 95%`

### Production target for broader rollout

- `POST /ask` availability: `99.9%`
- ticket creation latency after escalation decision: `<= 60 s`
- recovery point objective: `<= 15 min`
- recovery time objective: `<= 60 min`
- no unsupported automatic answers in release-gate evaluation suite

## 13. Operational metrics

### Platform metrics

- request rate by endpoint, tenant, and risk class
- p50, p95, and p99 latency
- ticket creation latency
- error rate and timeout rate
- audit completeness rate

### Quality metrics

- automatic answer citation coverage
- unsupported automatic answer rate
- contradiction rate
- correct escalation rate
- confidence distribution by risk class

### Economic metrics

- cost per query
- cost per model
- cost per domain
- cache hit rate
- routing savings estimate

### Governance metrics

- blocked request rate
- review queue depth
- average review turnaround time
- top failure taxonomy categories
- policy-version adoption across evaluation and production traffic

## 14. Deployment topology

### Local reproducible topology

- Docker Compose
- single API container
- worker container
- PostgreSQL with pgvector
- Redis
- Ollama
- Prometheus and Grafana
- simple web UI and review console

### Enterprise production topology

- WAF and ingress layer
- multiple API replicas behind load balancing
- separate worker autoscaling pool
- managed PostgreSQL and Redis
- managed object storage
- centralized identity provider
- centralized telemetry export and SIEM integration
- backup, restore, and key management controls

Multi-region active-active deployment is explicitly out of scope for the first production milestone and should only be introduced when legal or latency requirements justify the added complexity.

## 15. Recommended repository structure

The repo should reflect domain boundaries, not implementation trivia.

```txt
trustops-rag/
  docs/
    SPEC.md
    ARCHITECTURE.md
    STACK.md
    adr/
  src/trustops_rag/
    api/
    application/
    domain/
    infrastructure/
    workers/
    evals/
  frontend/
    user-portal/
    review-console/
  tests/
    unit/
    integration/
    contract/
    security/
    evaluation/
  infra/
    docker/
    compose/
    observability/
```

## 16. Architecture maturity roadmap

### Stage 1: Reproducible baseline

- local end-to-end flow
- ingestion
- hybrid retrieval
- structured answer and validation

### Stage 2: Pilot hardening

- OIDC integration
- stronger audit model
- worker reliability and SLA monitoring
- release-gate evaluation suite

### Stage 3: Enterprise controls

- document ACL enforcement
- secret management
- SIEM export
- backup and restore drills

### Stage 4: Scale and governance

- autoscaling workers
- capacity planning by risk class
- regional tenancy controls
- formal ADR lifecycle and operational runbooks
