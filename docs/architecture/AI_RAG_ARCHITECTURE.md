# VehicleTrust AI — AI / RAG Architecture

## 1. Purpose

The AI / RAG layer provides grounded, evidence-backed explanations for
VehicleTrust AI.

Its purpose is to help users understand:

- why a vehicle received its trust assessment
- why specific risks matter
- what additional information should be verified
- what domain knowledge is relevant to the identified risks
- how available evidence affects the purchase decision

The AI / RAG layer must not replace the deterministic vehicle intelligence
engines.

---

## 2. Architectural Principle

VehicleTrust AI separates deterministic vehicle intelligence from
probabilistic AI generation.

The deterministic intelligence layer is responsible for:

- vehicle data
- evidence
- risk detection
- trust calculation
- purchase decision

The AI / RAG layer is responsible for:

- retrieving relevant domain knowledge
- interpreting the supplied evidence
- explaining identified risks
- explaining the reasoning behind the deterministic assessment
- generating grounded user-facing explanations

The LLM must not independently calculate or override the VehicleTrust score,
risk severity, or purchase decision.

---

## 3. Target Architecture

```text
                         User
                           |
                           v
                       Next.js
                           |
                           v
                        FastAPI
                           |
                           v
               Vehicle Intelligence
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
       Evidence          Risks            Trust
          |                |                |
          +----------------+----------------+
                           |
                           v
                       Decision
                           |
                           v
                    AI / RAG Layer
                           |
             +-------------+-------------+
             |                           |
             v                           v
        Retrieval                    Generation
             |                           |
             v                           v
      Domain Knowledge  ----------->   LLM
             |                           |
             +-------------+-------------+
                           |
                           v
                   Grounded AI Response
                           |
                           v
                        FastAPI
                           |
                           v
                       Next.js