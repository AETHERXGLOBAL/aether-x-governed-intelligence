# AX-AUTHORIZATION-INTEROP-RESEARCH-002

**Document ID:** `AX-AUTHORIZATION-INTEROP-RESEARCH-002`  
**Version:** `0.1`  
**Status:** `RESEARCH_CANDIDATE / NON-BINDING / NO_RUNTIME_CONTRACT`  
**Baseline:** `256594c364ca3e76eb7d6d95cd93d56e9773e36f`  
**Observed:** `2026-08-19`  
**Scope:** Bounded research only. No implementation, schema change, runtime/network integration, policy-engine selection, Gate/Release action, or production claim.

## Decision question

After controlled promotion of the offline in-toto/SLSA importer proof, what is the highest-value next interoperability gap that can reduce proprietary trust assumptions while preserving AETHER semantic authority boundaries?

## Preserved invariants

- `Evidence != Decision`
- `Decision != Authority`
- `Authority != Capability`
- `Signature Verified != Trusted Issuer`
- `External Verification != AETHER Verification`
- `Execution/Import != Verified Outcome`
- `Unknown != Pass`
- `Current Truth != Historical Truth`
- External identity or authorization claims do not self-create AETHER authority.

## Current baseline facts

The baseline already contains a controlled-promoted, independently verified offline in-toto/SLSA semantic importer proof. That path is preserved and is not a candidate for additional refactoring or feature expansion absent a new demonstrated gap.

The public authority model already distinguishes agent identity, action proposal, `authority_context`, `tool_use_grant`, invocation, and result. In particular, an AETHER authority context carries explicit permitted tools/actions, resource scope, parameter constraints, validity, revocation state, and evaluation time. Therefore the remaining authorization interoperability problem is not “build an authorization model”; it is how to admit external authorization decisions without collapsing them into AETHER authority.

## Primary-source observations

### OpenID AuthZEN Authorization API 1.0

**FACT.** Authorization API 1.0 is an OpenID Final Specification published in January 2026. It defines a vendor-neutral PDP-to-PEP API. The core request information model is `Subject / Resource / Action / Context`; the response is a `Decision` with a required boolean `decision` and optional response context.

**FACT.** A successful `decision=false` means the request is denied and must not proceed. `decision=true` means the request is permitted to go forward under the external PDP decision, but the PEP may still reject it when it cannot understand relevant response context.

**FACT.** Policy language, PDP architecture, and PDP state management are outside the AuthZEN specification. Authentication for the Authorization API is also outside the specification; OAuth 2.0 support is recommended rather than supplied by AuthZEN itself.

**IMPLICATION FOR AETHER.** AuthZEN can reduce proprietary coupling at the external PDP/PEP boundary without requiring AETHER to invent a generic policy language or select one authorization engine. However, an AuthZEN `decision=true` cannot be treated as an AETHER `authority_context` or `tool_use_grant`; it is an external authorization decision that must pass an AETHER admissibility boundary.

### Cedar

**FACT.** Cedar evaluates `principal / action / resource / context` requests and returns `Allow` or `Deny` under Cedar policy semantics.

**ASSESSMENT.** Cedar is a strong candidate external policy engine but is backend-specific. Integrating Cedar before defining the vendor-neutral external-decision boundary would create avoidable coupling. A future Cedar adapter can sit behind, or map consistently with, a standard decision-interoperability profile.

### OpenFGA

**FACT.** OpenFGA `Check` evaluates a user/relation/object request and can be pinned to an `authorization_model_id`; current documentation shows explicit model IDs in Check requests and responses of `allowed=true/false`.

**ASSESSMENT.** OpenFGA is valuable for ReBAC but remains a concrete backend. AETHER should preserve the model ID for point-in-time reproducibility if OpenFGA is ever integrated, while keeping `allowed=true != AETHER Authority`.

### SCITT RFC 9943

**FACT.** SCITT is an IETF Proposed Standard published June 2026 for signed-statement transparency, registration, receipts, and auditability.

**ASSESSMENT.** SCITT can strengthen transparency and third-party audit evidence, but it does not close the most immediate gap between AETHER's existing authority semantics and external authorization decisions. It is a later provenance/transparency interoperability candidate, not the next authorization boundary.

### WIMSE and agent authorization work

**FACT.** WIMSE workload identity/credential work remains active Internet-Draft work. Current workload-credentials revision observed is `draft-ietf-wimse-workload-creds-02` (July 2026).

**FACT.** `draft-klrc-aiagent-auth-02` is an individual active Internet-Draft that explicitly advocates composing existing identity/authorization standards rather than inventing new protocols, and states that an agent acting for a user/system requires delegated authority with that context preserved for authorization decisions and audit.

**ASSESSMENT.** This direction strongly matches AETHER's `Identity != Authority` and bounded delegation model, but draft maturity is not sufficient for a Core dependency. Continue to watch; do not implement a WIMSE/agent-auth dependency now.

### OAuth Transaction Tokens / agent extension

**FACT.** The current official OAuth WG Datatracker view observed during this research lists `draft-ietf-oauth-transaction-tokens-08` in WG Last Call. The active individual agent extension observed is `draft-araut-oauth-transaction-tokens-for-agents-02` (May 2026).

**EVIDENCE-METADATA NOTE.** `AX-INTEROP-GAP-MATRIX-001` currently records the base Transaction Tokens draft as `-11`. That version was not reproduced from the current official Datatracker state in this research session. This is a research-metadata freshness discrepancy only; it does not affect the candidate selection below. No historical artifact is rewritten here.

**ASSESSMENT.** Transaction-scoped context propagation is strategically relevant to future controlled execution, but both the base and agent-specific work remain drafts. Keep `Watch`; no Core dependency.

## Comparative value assessment

| Candidate | Standards maturity | Direct value to current AETHER | Proprietary-assumption reduction | Core semantic risk | Disposition now |
|---|---:|---:|---:|---:|---|
| **AuthZEN 1.0** | High / Final | **High** | **High** | High if Allow is promoted to Authority | **Research next / candidate design boundary** |
| SCITT RFC 9943 | High / Proposed Standard | Medium | High for transparency | Medium-high | Defer after authorization boundary |
| Cedar | Mature implementation model | Medium | Medium | High if Allow becomes Authority | Backend candidate only |
| OpenFGA | Mature implementation model | Medium | Medium | High if Check becomes Authority or model ID omitted | Backend candidate only |
| WIMSE | Draft | High long-term | High | High | Watch |
| OAuth Transaction Tokens | Draft / WG Last Call | High long-term | High | Critical if token becomes Authority | Watch |
| Agent authorization drafts | Individual drafts | High long-term | High | Critical | Watch |
| in-toto / SLSA | Already promoted bounded proof | Gap currently closed for this layer | Already realized | Preserve | Do not expand without new gap |

## Highest Candidate Gap

**Candidate Gap:** AETHER has no vendor-neutral, point-in-time **external authorization decision admissibility contract** that can preserve an external PDP request/response as attributable evidence/decision context while preventing `ALLOW` from implicitly creating AETHER Authority or execution capability.

This gap is higher-value than selecting Cedar or OpenFGA now because AuthZEN defines a stable interoperability boundary independent of the PDP's internal policy language or storage model. It also complements the existing AETHER authority envelope instead of replacing it.

## Smallest coherent candidate after research

If separately authorized after review of this research conclusion, the smallest coherent design candidate would be an **offline AuthZEN Decision Admissibility Profile** with no network client and no policy engine. It would define only:

1. preservation of the exact external request and decision source identity;
2. point-in-time observation and external PDP/policy identity references when supplied;
3. mapping of `Subject / Resource / Action / Context / Decision` into an external authorization decision record/evidence boundary;
4. `decision=false` as fail-closed input that cannot be overridden by the adapter;
5. `decision=true` as insufficient to create `authority_context`, `tool_use_grant`, capability, invocation permission, AETHER Verification, or Verified Outcome;
6. unknown/unrecognized decision context as non-promoting and fail-closed where enforcement meaning is required;
7. no interpretation of unprofiled AuthZEN response context as AETHER obligations, approvals, delegation, or authority.

That proposed design would touch the Core `Decision != Authority` trust boundary and therefore is an **Independent Technical Oversight trigger before any runtime implementation or promotion**.

## Explicit non-goals

- no AuthZEN network client;
- no PDP implementation;
- no Cedar/OpenFGA adapter;
- no custom policy language;
- no identity protocol;
- no OAuth/WIMSE runtime dependency;
- no transaction-token support;
- no SCITT service or ledger;
- no schema or SDK change;
- no Gate, Release, Production, or risk-acceptance action.

## Research conclusion

**RECOMMENDATION:** Continue research/design attention on the AuthZEN external-decision admissibility boundary as the next highest-value interoperability candidate. Do not treat this recommendation as implementation authorization.

**Confidence:** High for candidate prioritization; medium for the eventual exact mapping shape until AETHER decision-record semantics and external PDP trust/provenance requirements are independently reviewed together.

**What would change the recommendation:** a newly stabilized agent-authorization standard that directly provides a stronger vendor-neutral decision/delegation boundary compatible with AETHER semantics; a concrete product requirement that makes transparency receipts materially more urgent than authorization interoperability; or evidence that AuthZEN cannot preserve the required point-in-time/trust provenance without proprietary extensions.

## Primary sources

- OpenID AuthZEN Authorization API 1.0 Final Specification: https://openid.net/specs/authorization-api-1_0.html
- OpenID Foundation final-specification approval notice: https://openid.net/authorization-api-1-0-final-specification-approved/
- Cedar authorization model: https://docs.cedarpolicy.com/auth/authorization.html
- OpenFGA Check documentation: https://openfga.dev/docs/getting-started/perform-check
- SCITT RFC 9943: https://www.rfc-editor.org/rfc/rfc9943.html
- IETF WIMSE WG: https://datatracker.ietf.org/wg/wimse/
- WIMSE Workload Credentials: https://datatracker.ietf.org/doc/draft-ietf-wimse-workload-creds/
- AI Agent Authentication and Authorization: https://datatracker.ietf.org/doc/draft-klrc-aiagent-auth/
- OAuth Transaction Tokens: https://datatracker.ietf.org/doc/draft-ietf-oauth-transaction-tokens/
- Transaction Tokens for Agents: https://datatracker.ietf.org/doc/draft-araut-oauth-transaction-tokens-for-agents/
