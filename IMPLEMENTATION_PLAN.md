# TrustOps RAG - Implementation Plan

Status: Draft v1.0  
Role: This document is the single source of truth for execution sequencing, technical backlog, phase-level Definition of Done, and incremental commit order. `ROADMAP.md` defines strategic milestones. This document defines how engineering work should be delivered.

## 1. Why this document exists

`ROADMAP.md` should stay strategic.

This file exists to answer four operational questions:

1. What should be built first.
2. How each phase breaks down into small technical tasks.
3. What “done” means before moving forward.
4. In what order the MVP should be committed without collapsing into one big batch.

## 2. Delivery principles

1. Deliver vertical slices, not disconnected code piles.
2. Prefer module completion over broad half-implementation.
3. No phase is done if it lacks tests, observability hooks, or failure behavior appropriate to that phase.
4. Every phase must leave the repository in a runnable state.
5. Each commit must move the system forward in a reviewable way.

## 3. MVP strategy

The MVP is not “the whole architecture with reduced quality”.

The MVP is:

- a narrow but real `/ask` flow
- citation-backed answers only
- deterministic escalation behavior
- basic auditability
- local reproducibility

Everything else should be layered onto that core in controlled increments.

## 4. Phase map

| Phase | Goal | Main outcome |
| --- | --- | --- |
| P0 | Workspace bootstrap | Runnable repo, Poetry, package layout, local study structure |
| P1 | Service foundation | Config, app boot, health, logging, base dependency wiring |
| P2 | Domain and persistence | Core entities, migrations, repositories, transaction boundaries |
| P3 | Ingestion baseline | Documents become versions, chunks, embeddings, and indexes |
| P4 | Retrieval baseline | Hybrid retrieval with version-aware evidence output |
| P5 | Generation and reliability | Structured answer generation plus evidence validation |
| P6 | Decisioning and API | `/ask` contract, policy control, fail-safe routing |
| P7 | Human review and async | Ticket lifecycle, workers, outbox, feedback hooks |
| P8 | Observability and evaluation | Metrics, traces, benchmark harness, release gates |
| P9 | Security and production hardening | ACL, auth, secrets, degraded mode, operational safety |

## 5. Technical backlog by phase

### P0. Workspace bootstrap

Backlog:

- create repository structure aligned to `ARCHITECTURE.md`
- initialize `pyproject.toml` and Poetry environment
- install core runtime and dev dependencies
- create package roots under `src/`
- create test directories
- create `.local` learning structure
- validate import path and package installation

Definition of Done:

- `poetry install` succeeds
- package imports cleanly
- directory structure matches architecture boundaries
- local study environment exists and is navigable

### P1. Service foundation

Backlog:

- create configuration model with environment loading
- create application settings separation for local vs production concerns
- create FastAPI app factory
- add `/health` route
- add request id middleware
- add structured logging bootstrap
- add basic dependency container or dependency module
- add initial test harness for app boot

Definition of Done:

- application boots with `poetry run`
- `/health` responds consistently
- request id is present in logs or response context
- config errors fail fast at startup
- tests cover app boot and config loading

### P2. Domain and persistence

Backlog:

- define core domain entities for documents, versions, queries, answers, tickets, audit events
- create base SQLAlchemy metadata and session management
- create initial Alembic migration
- implement repositories for documents and queries
- implement append-only audit event persistence contract
- add transaction boundary pattern
- define idempotency record model
- add persistence tests

Definition of Done:

- database schema is migration-driven
- core entities persist and reload correctly
- audit events are append-only by application behavior
- idempotency state can be stored and queried
- repository tests pass

### P3. Ingestion baseline

Backlog:

- create document loader abstraction
- implement Markdown parser path
- implement PDF parser path
- add normalization and cleanup stage
- add chunking stage with version linkage
- add embedding generation interface
- persist chunks and embeddings
- add lexical index bootstrap
- add ingestion worker entrypoint
- add ingestion integration test with sample docs

Definition of Done:

- a raw document can become an active version with chunks
- every chunk belongs to one document version
- ingestion failures are surfaced clearly
- reprocessing the same document version is controlled and traceable
- at least one integration test covers end-to-end ingestion

### P4. Retrieval baseline

Backlog:

- implement dense retriever
- implement BM25 retriever
- implement metadata and version filters
- implement hybrid merge logic
- define evidence result schema
- add retrieval scoring fields
- add retrieval service orchestration
- add retrieval tests for active version filtering and basic ranking

Definition of Done:

- retrieval only uses active document versions
- evidence output is structured and testable
- dense-only and lexical-only fallback paths are explicit
- retrieval tests cover at least success, no-results, and version filtering cases

### P5. Generation and reliability

Backlog:

- create provider adapter interface
- add local provider adapter path
- define prompt builder contract
- define structured LLM output contract
- implement response parser
- implement evidence validator
- implement contradiction checker
- implement confidence scorer skeleton
- add reliability result model
- add tests for structured output parsing and validation paths

Definition of Done:

- generation returns structured output only
- unsupported or malformed output is rejected deterministically
- evidence validation produces machine-readable results
- confidence scoring is reproducible for the same inputs
- tests cover supported and unsupported answer paths

### P6. Decisioning and API

Backlog:

- implement policy rule model
- implement `policy_version` propagation
- implement closed `decision_reason` enum
- implement `system_state` handling
- implement decision router
- implement `/ask` request and response schemas
- add `Idempotency-Key` handling
- add request normalization for dedupe
- persist decision log and answer outcome
- add contract tests for every canonical response state

Definition of Done:

- `/ask` supports all canonical states from `SPEC.md`
- duplicate retried requests do not create duplicate business outcomes
- `policy_version`, `decision_reason`, and `system_state` are persisted and returned
- contract tests cover `answered`, `answered_with_warning`, `human_review_required`, `blocked`, and `failed_safe`

### P7. Human review and async

Backlog:

- create ticket model and repository
- implement ticket creation from escalation decision
- implement outbox or durable event handoff
- implement worker bootstrap
- implement ticket assignment rule skeleton
- implement reviewer action API
- implement feedback event persistence
- implement cache invalidation hook on human correction
- add integration tests for escalation and review flows

Definition of Done:

- escalated requests create tickets deterministically
- worker retries are idempotent by business key
- reviewer actions are auditable
- human correction emits feedback and invalidation hooks
- integration tests cover ticket creation and state transitions

### P8. Observability and evaluation

Backlog:

- add Prometheus metrics for request and worker paths
- add OpenTelemetry instrumentation for API and persistence
- define operational metric names
- define quality metric calculation path
- create evaluation dataset skeleton
- create baseline evaluation runner
- create TrustOps evaluation runner
- create release-gate report format
- add CI task hooks for lint, tests, and evaluation checks

Definition of Done:

- metrics and traces are emitted on the main path
- baseline and TrustOps evaluation can be run with the same dataset
- release-gate artifacts are generated consistently
- CI can fail on broken contracts or critical regressions

### P9. Security and production hardening

Backlog:

- add rate limiting
- add prompt injection detection path
- add PII analysis and redaction hooks
- add authn/authz wiring
- add document ACL enforcement in retrieval
- add secret-loading strategy for production
- add degraded-mode handling coverage
- add operational runbook skeleton
- add security tests for blocked and denied cases

Definition of Done:

- unauthorized or ACL-denied flows are blocked deterministically
- security-sensitive decisions are auditable
- degraded-mode behavior is explicit and tested
- production-facing config does not depend on repository secrets
- security tests cover at least abuse, ACL denial, and blocked prompt cases

## 6. Definition of Done by roadmap milestone

### M0. Reproducible baseline

Definition of Done:

- P0 through P5 are complete at MVP depth
- local environment boots end to end
- ingestion, retrieval, structured generation, and validation all work locally
- at least one narrow `/ask` slice works with citations

### M1. Internal pilot

Definition of Done:

- P6 through P8 are complete at pilot depth
- `/ask` contract is stable
- escalation and reviewer flow are operational
- core observability and benchmark gates exist

### M2. Enterprise control plane

Definition of Done:

- P9 is complete at control-plane depth
- auth, ACL, policy traceability, and stronger audit guarantees are in place
- no higher-risk pilot path bypasses governance controls

### M3. Scale and operations

Definition of Done:

- queue behavior, recovery procedures, and release gates are proven under load
- capacity planning and operational metrics are actionable
- benchmark and SLO regression checks inform release readiness

### M4. Multinational readiness

Definition of Done:

- regional rollout constraints are mapped to technical controls
- governance ownership is documented
- production operation no longer depends on undocumented knowledge

## 7. Incremental commit model

Use Conventional Commits with scope.

Recommended format:

```txt
type(scope): short summary
```

Allowed primary types:

- `feat`
- `fix`
- `refactor`
- `test`
- `docs`
- `chore`
- `build`
- `ci`
- `perf`
- `security`

Scope examples:

- `api`
- `domain`
- `infra`
- `ingestion`
- `retrieval`
- `reliability`
- `decision`
- `workers`
- `evals`
- `docs`
- `local`

Examples:

```txt
feat(api): add FastAPI app factory and health route
feat(domain): add document and document version entities
feat(ingestion): add markdown loader and chunking pipeline
feat(retrieval): add hybrid evidence retrieval service
feat(decision): implement canonical decision router
test(api): add contract coverage for ask response states
security(retrieval): enforce ACL filtering before reranking
docs(local): add module study templates and checkpoints
```

Commit rules:

1. One commit should represent one reviewable intention.
2. Do not mix refactor, feature, and unrelated formatting in the same commit.
3. Every commit should leave the branch in a buildable or at least structurally consistent state.
4. Test commits are allowed to follow feature commits immediately when the change is easier to review in two steps.

## 8. Recommended MVP commit order

This is the preferred initial delivery order.

1. `chore(infra): initialize poetry project and package layout`
2. `docs(local): add study roadmap and module structure`
3. `feat(api): add app factory, config bootstrap, and health route`
4. `feat(domain): add core entity definitions and repository contracts`
5. `build(db): add SQLAlchemy base, session management, and first migration`
6. `test(domain): add persistence tests for core entities`
7. `feat(ingestion): add document loader and markdown parsing path`
8. `feat(ingestion): add chunking and document version persistence`
9. `feat(retrieval): add dense and BM25 retriever interfaces`
10. `feat(retrieval): add hybrid retrieval orchestration and evidence schema`
11. `test(retrieval): add retrieval tests for active version filtering`
12. `feat(generation): add provider adapter and structured output contract`
13. `feat(reliability): add evidence validator and contradiction checker`
14. `feat(reliability): add confidence scoring skeleton`
15. `feat(decision): add policy version model and decision reason enum`
16. `feat(api): add ask schemas and canonical response envelope`
17. `feat(api): add idempotency key handling for ask flow`
18. `test(contract): add ask contract coverage for all response states`
19. `feat(workers): add ticket creation and worker bootstrap`
20. `feat(workers): add reviewer action flow and feedback hooks`
21. `feat(obs): add metrics, tracing, and audit persistence hooks`
22. `feat(evals): add baseline and TrustOps evaluation runners`
23. `security(api): add rate limiting and prompt injection guard path`
24. `security(retrieval): add ACL enforcement and auth integration hooks`
25. `ci(repo): add lint, test, and contract validation pipeline`

## 9. What not to do

- Do not create a single “initial MVP” commit containing half the platform.
- Do not start with UI-first delivery before the backend contract exists.
- Do not build retrieval, generation, and decisioning in one untestable step.
- Do not postpone observability until after the core logic is “done”.
- Do not treat human review as an afterthought if it already exists in the product contract.

## 10. Immediate next execution step

The next practical move after this document is:

1. start P1
2. open a branch for the service foundation slice
3. commit the app/config/health/logging baseline in small reviewable steps
