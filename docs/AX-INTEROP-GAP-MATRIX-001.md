# AETHER X — Interoperability Gap Matrix

**Document ID:** `AX-INTEROP-GAP-MATRIX-001`  
**Version:** `0.1`  
**Status:** `RESEARCH CANDIDATE / NON-BINDING / NO RUNTIME CONTRACT`  
**Baseline:** `59d6cec8c280d1032296a7fb771810633cdaafa7`  
**Observed:** `2026-08-19`

## Purpose

Compare external standards and authorization/provenance approaches against the AETHER X Semantic Trust Chain without promoting research into features, authority, release state, or runtime architecture.

`EVIDENCE → DECISION → AUTHORITY → EXECUTION → VERIFICATION → VERIFIED OUTCOME`

Preserve: `Evidence ≠ Decision`; `Decision ≠ Authority`; `Authority ≠ Capability`; `Execution ≠ Verified Outcome`; `Unknown ≠ Pass`; Point-in-Time Knowledge; immutable historical evidence; isolated public baseline.

## Matrix

| Standard | Class | What it solves | Missing capability | Candidate mapping | Loss-of-meaning risk | Boundary | Disposition |
|---|---|---|---|---|---|---|---|
| in-toto Attestation Framework | Relevant / P1 | Standard attestation envelope binding artifact subjects by name/digest to typed predicates and signatures. | No explicit generic import/export contract preserving AETHER semantic type boundaries. | `subject` → external artifact identity; predicate → standard provenance or bounded AETHER evidence payload/reference; signer → evidence source provenance. Imported attestation remains Evidence unless an explicit AETHER rule creates another typed record. | High if a signed attestation is interpreted as truth, decision, authority, or verified outcome merely because it is signed. | Signature authenticates an issuer statement; it does not grant AETHER authority or execution capability. | Integrate |
| SLSA 1.2 | Relevant / P1 | Supply-chain security levels plus build/source provenance and verification-summary attestation patterns. | No SLSA provenance/VSA consume-or-emit mapping into AETHER typed evidence and verification records. | Provenance → Evidence about source/build process; VSA → Evidence of external verifier assessment. AETHER Verification may validate relevance; Verified Outcome stays separate. | High if SLSA level/VSA becomes product correctness, security approval, or AETHER Verified Outcome. | SLSA provenance/levels do not create AETHER authority, release authority, or acceptance. | Integrate |
| PEP 740 / Python Index Hosted Attestations | Relevant / P1 | Index-hosted attestations with in-toto subject filename and SHA-256 binding. | No authorized-index attestation retrieval/verification evidence path; publication remains unauthorized. | Distribution filename+SHA-256 → external artifact identity; attestation verification → Evidence; signing identity → provenance source. | Medium-high if attestation availability is interpreted as publication approval, human evaluation, security approval, or verified outcome. | Attestation verification proves binding/signing properties; publication, release, and AETHER authority remain separate. | Integrate |
| OpenID AuthZEN Authorization API 1.0 | Relevant / P1 | Interoperable PDP↔PEP Subject/Resource/Action/Context request and boolean Decision. | No explicit mapping contract between AuthZEN information model and AETHER decision/authority records. | S/R/A/C → bounded external authorization evaluation context; AuthZEN Decision → external authorization decision record/evidence. It MUST NOT directly create an AETHER authority grant. | **Critical** if `decision=true` is promoted to AETHER Authority/capability. | PDP Decision ≠ AETHER Authority. Deny fails closed; allow remains insufficient without AETHER authority and capability. | Integrate |
| SCITT RFC 9943 | Relevant / P1-P2 | Signed Statements, transparency registration, Receipts, append-only/non-equivocating history, auditability. | No Signed Statement/Receipt mapping for AETHER evidence and verification records. | Signed Statement → Evidence envelope; `iss` → evidence issuer; `sub` → subject/artifact grouping; Receipt → Evidence of registration. AETHER Verification may verify receipt/signature. | **Critical** if receipt/inclusion becomes statement accuracy, AETHER Verification, Acceptance, or Authority. | Registration proves issuer statement registration/transparency properties; not truth and not AETHER authority. | Integrate |
| Cedar | Relevant / P2 | Policy evaluation over principal/action/resource/context with Allow/Deny. | No adapter contract for Cedar under AETHER authority constraints. | AETHER actor/action/resource/context → Cedar PARC; Cedar Allow/Deny → external authorization decision evidence. Authority/capability remain separately required. | High if Cedar Allow becomes authority or request context lacks point-in-time provenance. | Cedar decides under Cedar policy; AETHER separately determines admissibility and bounded authority/capability. | Integrate |
| OpenFGA | Relevant / P2 | Relationship-based authorization using models, tuples, contextual tuples, and Check decisions. | No adapter contract treating relationship/check data as external evidence without authority conflation. | Tuples + authorization-model ID → point-in-time external authorization evidence; Check → external decision evidence. Preserve model ID. | High if relation/`allowed=true` becomes AETHER Authority or model version is omitted. | OpenFGA relation/check ≠ AETHER authority grant. | Integrate |
| IETF WIMSE | Watch / P2 | Workload identity, credentials, proof-of-possession, trust-domain scoped workload identity. | No stable workload identity integration contract yet. | Future WIMSE identifier/credential → authenticated actor/workload identity Evidence; PoP → capability-to-present identity Evidence. | High if authenticated workload identity becomes authorization or agent authority. | Identity ≠ Authority; proof of possession ≠ execution permission. | Watch |
| OAuth Transaction Tokens | Watch / P2 | Short-lived transaction-scoped authorization context across workload call chains. | No stable token mapping for AETHER execution authority/context; still Internet-Draft. | Future token claims → external execution-context Evidence; AETHER authority IDs may be referenced but never synthesized from token scope/subject. | **Critical** if token possession becomes the AETHER authority record or scope expands silently. | Transaction context ≠ AETHER Authority. | Watch |
| Transaction Tokens for Agents | Watch / P2 | Agent context propagation using actor/principal semantics. | No stable standard mapping; no reason to replace AETHER Agent Authority. | Future `act`/`sub` → actor/principal identity Evidence only; Agent Authority remains AETHER-governed. | **Critical** if actor/principal identity is interpreted as delegation authorization. | Actor/principal identity context ≠ delegation grant/capability. | Watch |

## Research conclusion

- **Highest Candidate Gap:** A standard interoperability contract is absent for mapping external provenance/authorization/transparency facts into AETHER typed records without semantic promotion.
- **Smallest next integration candidate:** a read-only, offline in-toto/SLSA attestation mapping profile that imports artifact provenance as **Evidence only** and exports AETHER evidence references without creating Decision, Authority, or Verified Outcome.
- **Oversight boundary:** that mapping profile would be a proposed interoperability contract touching Core semantic boundaries and therefore requires independent review before runtime implementation or promotion.
- **Do not build now:** custom identity protocol, generic policy language, ReBAC engine, transparency ledger, production agent gateway, or cryptographic subsystem merely to avoid existing standards.

## Key semantic findings

- **in-toto / SLSA / PEP 740:** artifact provenance and attestation are valuable as external **Evidence**; signatures and supply-chain levels do not create AETHER authority or Verified Outcome.
- **AuthZEN:** `decision=true` is an external authorization decision, not an AETHER Authority grant. `false` remains fail-closed.
- **SCITT RFC 9943:** a Receipt proves registration/transparency properties, not statement accuracy; relying-party trust remains separate.
- **Cedar / OpenFGA:** suitable external PDP/enforcement backends; Allow/Check results remain external decision evidence and must not become authority automatically.
- **WIMSE / OAuth Transaction Tokens:** relevant to identity and bounded context propagation but still draft-based; track rather than couple the Core to them.

## Sources

- `SLSA-1.2` — Approved — https://slsa.dev/spec/v1.2/
- `SLSA-1.2-SOURCE` — Approved — https://slsa.dev/spec/v1.2/source-requirements
- `PYPA-INDEX-HOSTED-ATTESTATIONS` — Current specification — https://packaging.python.org/en/latest/specifications/index-hosted-attestations/
- `AUTHZEN-AUTHORIZATION-API-1.0` — Final — https://openid.net/specs/authorization-api-1_0.html
- `SCITT-RFC9943` — Proposed Standard — https://www.rfc-editor.org/rfc/rfc9943.html
- `CEDAR-AUTHORIZATION` — Current documentation — https://docs.cedarpolicy.com/auth/authorization.html
- `OPENFGA-CHECK` — Current documentation — https://openfga.dev/docs/getting-started/perform-check
- `OPENFGA-TUPLES-BEST-PRACTICES` — Current documentation — https://openfga.dev/docs/getting-started/tuples-api-best-practices
- `WIMSE-WORKLOAD-CREDS-02` — Active Internet-Draft — https://datatracker.ietf.org/doc/html/draft-ietf-wimse-workload-creds-02
- `OAUTH-TXN-TOKENS-11` — Active Internet-Draft / WG Last Call — https://datatracker.ietf.org/doc/draft-ietf-oauth-transaction-tokens/
- `TXN-TOKENS-AGENTS-02` — Individual Internet-Draft — https://datatracker.ietf.org/doc/draft-araut-oauth-transaction-tokens-for-agents/
