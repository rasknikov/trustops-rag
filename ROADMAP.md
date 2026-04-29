# TrustOps RAG - Roadmap

Status: Draft v1.0  
Role: This document defines the product roadmap and implementation roadmap in one coordinated plan. The two tracks remain distinct in ownership and deliverables, but they stay in the same document to prevent dependency drift between product commitments and engineering reality.

Execution detail such as technical backlog, Definition of Done, and incremental commit order lives in `IMPLEMENTATION_PLAN.md`.

## 1. Roadmap decision

The roadmap should remain unified in one document with two synchronized tracks:

- Product track: defines business capability, adoption, governance, and release intent.
- Implementation track: defines architecture, engineering, platform, and delivery work required to make the product track credible.

This is the recommended structure because:

- the platform has strong coupling between policy, architecture, and operational controls
- a product milestone is not valid unless the implementation controls behind it are already in place
- separate roadmap files usually diverge on scope, dates, and release readiness

The correct separation is not document-level separation. It is section-level separation with shared release gates.

## 2. Planning model

This roadmap is milestone-based, not date-first. For a platform of this kind, false calendar precision is lower quality than explicit exit criteria.

Recommended planning cadence:

- strategy review: quarterly
- release planning: monthly
- execution review: weekly
- architecture checkpoint: at the end of every milestone

## 3. Milestone framework

Each milestone contains:

- product objective
- product deliverables
- implementation deliverables
- release gate
- primary risks

No milestone is considered complete if the product surface exists but the safety, audit, or operational controls are still missing.

## 4. Executive view

| Milestone | Strategic intent | Product outcome | Technical outcome |
| --- | --- | --- | --- |
| M0 | Prove the control model | Reproducible internal demo with trustworthy refusal behavior | End-to-end baseline with auditability and deterministic evaluation |
| M1 | Enable internal pilot | Usable RAG workflow for bounded internal domains | Hardened pipeline with tickets, validation, observability, and release gates |
| M2 | Make it enterprise-safe | Controlled rollout for higher-risk domains | Identity, ACLs, stronger governance, resilient async workflows |
| M3 | Make it operationally scalable | Multi-team adoption with measurable economics | Autoscaling, capacity planning, reliability drills, governance automation |
| M4 | Prepare for multinational production | Regional and organizational rollout readiness | Compliance-aligned controls, tenant isolation maturity, platform operating model |

## 5. Integrated roadmap

### M0 - Reproducible baseline

#### Product objective

Prove that TrustOps RAG can answer with citations, refuse safely, and benchmark itself against a simple baseline.

#### Product deliverables

- canonical `/ask` contract with the five response states from `SPEC.md`
- baseline question-answering flow over approved demo documents
- visible citations, confidence, status, and latency in the UI
- benchmark view comparing baseline RAG versus TrustOps RAG
- explicit limitations and non-goals documented for internal stakeholders

#### Implementation deliverables

- Docker Compose environment with API, worker, PostgreSQL, pgvector, Redis, Ollama, Prometheus, and Grafana
- modular monolith skeleton aligned with `ARCHITECTURE.md`
- ingestion pipeline for Markdown and PDF documents
- hybrid retrieval with version-aware filtering
- structured generation output and basic reliability validation
- initial `policy_version` propagation across responses, cache, audit, and evaluation
- closed `decision_reason` enum implemented in the contract and telemetry model
- audit event persistence, request tracing, and cost logging
- deterministic evaluation harness and release dataset bootstrap

#### Release gate

- `make dev` equivalent environment boots end to end
- every automatic answer returns at least one citation
- no unsupported automatic answer on the release-gate seed dataset
- baseline versus TrustOps comparison is reproducible locally

#### Primary risks

- overfitting evaluation to synthetic data
- insufficient document quality creating misleading trust signals
- premature feature expansion before the control path is stable

### M1 - Internal pilot

#### Product objective

Move from demo credibility to bounded internal usefulness in low- and medium-risk domains.

#### Product deliverables

- reviewer console with pending queue and action workflow
- `human_review_required` path operational for uncertain and high-risk requests
- warning-mode response for partial evidence in approved low- or medium-risk cases
- product metrics for escalation rate, citation coverage, and unsupported answer rate
- pilot documentation for supported domains, unsupported domains, and operating policy

#### Implementation deliverables

- ticket lifecycle APIs and worker-based assignment flow
- confidence scoring and contradiction checks wired into decisioning
- semantic cache with document-version invalidation and policy-version keying
- explicit `system_state` contract behavior for degraded-mode responses
- `Idempotency-Key` support for retriable clients and duplicate-prevention on ticket creation
- contract tests for `/ask` and reviewer actions
- integration tests for ingest, retrieval, decisioning, and ticketing
- initial SLO dashboards separated from broader operational metrics and alert thresholds

#### Release gate

- correct escalation rate meets pilot threshold on curated evaluation dataset
- ticket creation is deterministic and auditable
- degraded-mode behavior is tested for retrieval and model failure paths
- p95 latency for non-escalated requests stays within internal pilot budget

#### Primary risks

- reviewer workflow becomes a bottleneck before assignment logic matures
- confidence score looks precise without being calibrated enough
- cache invalidation defects create stale-but-plausible responses

### M2 - Enterprise control plane

#### Product objective

Make the platform safe enough for controlled rollout into higher-risk business workflows.

#### Product deliverables

- tenant-aware access model
- document access controls enforced in the answer path
- domain-scoped rollout for legal, finance, compliance, or HR-sensitive use cases
- formal escalation policy by risk class
- operational reporting for cost by domain, model, and escalation path

#### Implementation deliverables

- OIDC-based authentication and role propagation
- document-level ACL filtering before reranking and citation selection
- outbox-based event handoff for tickets and feedback propagation
- stronger audit schema with reviewer and policy lineage
- secrets management, encryption, and production-grade configuration controls
- release-gate evaluation for unsupported answers, escalation correctness, and blocked prompt-injection cases

#### Release gate

- no bypass path around ACL enforcement
- audit trail can reconstruct request, evidence set, model, decision, and reviewer action
- security controls pass internal review for pilot production use
- fail-safe behavior covers model outage, retrieval degradation, and telemetry persistence failure

#### Primary risks

- security requirements arrive late and force redesign
- high-risk domain rollout expands faster than policy coverage
- event consistency gaps between synchronous decisions and asynchronous workers

### M3 - Scale and operations

#### Product objective

Enable adoption by multiple teams without losing cost control, reliability, or governance clarity.

#### Product deliverables

- multi-team tenant onboarding model
- service-level reporting by domain and tenant
- transparent budget and usage governance for business owners
- faster review turnaround through routing, queue visibility, and team metrics
- formal release notes and operational runbooks for platform stakeholders

#### Implementation deliverables

- horizontal scaling for API and worker pools
- queue depth monitoring, backpressure strategy, and capacity planning by risk class
- backup and restore validation, incident runbooks, and recovery exercises
- automated benchmark publication for every release candidate
- image scanning, dependency scanning, and stronger CI release gates
- platform dashboards for latency decomposition, failure taxonomy, and unit economics

#### Release gate

- production SLOs are met for availability and ticket creation latency
- recovery objectives are tested, not only documented
- benchmark regression checks block degraded releases
- cost trend and escalation volume are predictable enough for operational planning

#### Primary risks

- worker autoscaling without queue discipline creates unstable latency
- cost savings from routing are erased by poor prompt or context discipline
- observability exists technically but not in an operator-friendly form

### M4 - Multinational readiness

#### Product objective

Prepare the platform for broader organizational rollout across regions, policies, and operating teams.

#### Product deliverables

- regional operating model and supported jurisdiction matrix
- governance model for policy ownership, change approval, and document stewardship
- rollout playbook for new business units and new regulated domains
- executive reporting for risk posture, savings, review load, and policy gaps

#### Implementation deliverables

- regional tenancy design and data residency controls where required
- stronger policy versioning and change-management workflow
- SIEM integration and enterprise log retention alignment
- capacity and cost forecasting by region and business unit
- ADR and runbook library covering architecture, security, resilience, and operations

#### Release gate

- organizational ownership model is defined for product, platform, policy, and review operations
- region-specific compliance and data handling constraints are mapped to technical controls
- no critical operational process depends on tribal knowledge

#### Primary risks

- governance model lags behind platform capability
- regional requirements create hidden architecture branching
- document stewardship is underfunded relative to platform adoption

## 6. Cross-cutting workstreams

These workstreams run through every milestone and should be visible in planning, not buried in backlog noise.

### Policy and trust

- response policy versioning
- closed decision-reason taxonomy governance
- escalation rule tuning
- confidence calibration
- failure taxonomy maturity

### Data and document governance

- corpus quality standards
- document ownership and lifecycle
- version activation workflow
- ACL metadata hygiene

### Reliability engineering

- API idempotency and retry semantics
- degraded-mode testing
- dependency timeout strategy
- recovery exercises
- performance tuning under realistic load

### Security and compliance

- threat model updates
- identity integration
- audit retention
- secret rotation and access review

### Developer productivity

- local bootstrap speed
- fixture quality
- contract-test coverage
- CI feedback time

## 7. Release governance

Every release candidate should pass four gates:

1. Product gate: behavior matches `SPEC.md`.
2. Architecture gate: solution still conforms to `ARCHITECTURE.md`.
3. Technology gate: implementation does not violate `STACK.md` guardrails.
4. Operational gate: observability, security, and rollback paths are verified.

No milestone should be signed off by engineering alone. Minimum sign-off should include:

- product owner
- engineering lead
- architecture/platform owner
- security or governance representative for milestones M2 and above

## 8. Ownership model

### Product track ownership

- product scope and rollout sequencing
- supported domains and user promises
- review workflow policy
- stakeholder communication and adoption metrics

### Implementation track ownership

- system architecture and codebase evolution
- platform reliability and operational readiness
- security controls and data handling implementation
- performance, cost, and benchmark instrumentation

## 9. What not to do

- Do not commit to calendar dates before milestone exit criteria are credible.
- Do not ship higher-risk domains before ACL, audit, and escalation controls are live.
- Do not measure success by answer volume alone.
- Do not treat benchmark results as marketing if the release gate dataset is weak.
- Do not separate roadmap storytelling from operational readiness.

## 10. Immediate next planning moves

1. Approve this integrated roadmap model.
2. Break M0 and M1 into epics with owners, dependencies, and definition of done.
3. Create ADRs for the highest-risk implementation decisions before coding deep into M1.
4. Define the release-gate evaluation dataset that every milestone must satisfy.
