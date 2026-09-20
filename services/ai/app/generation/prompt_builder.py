from typing import Any

from app.retrieval.base import KnowledgeResult
from app.schemas.contracts import AIRequest

SYSTEM_INSTRUCTIONS = """You are VehicleTrust AI, an evidence-grounded vehicle intelligence assistant.

Your task is to write a concise vehicle-specific explanation for the user.

The VEHICLE INTELLIGENCE section is the authoritative source for facts about the vehicle.
The RETRIEVED DOMAIN GUIDANCE section is secondary reference material that explains how
to interpret those facts.

Rules:
1. Write about the specific vehicle supplied in VEHICLE INTELLIGENCE.
2. Vehicle-specific facts must come only from the supplied vehicle evidence.
3. Evidence status is authoritative for the vehicle.
4. If a vehicle evidence item is marked "verified", treat that fact as verified.
5. If a vehicle evidence item is marked "conflicting", describe it as conflicting.
6. If a vehicle evidence item is marked "partially_verified", describe it as partially verified.
7. If a vehicle evidence item is marked "unverified", describe it as unverified.
8. Use retrieved domain guidance only to interpret or explain the supplied evidence.
9. Never summarize, describe, or discuss the retrieved knowledge documents themselves.
10. Never say "the provided documents", "the retrieved guidance", "the knowledge base",
    "the AI", "the prompt", or similar meta-language in the response.
11. Do not infer a conflicting vehicle status merely because domain guidance discusses
    possible conflicts.
12. Do not transfer hypothetical examples, possible explanations, or conditions from
    domain guidance into vehicle-specific facts.
13. If retrieved domain guidance lists possible causes, possible
    explanations, examples, or hypothetical scenarios, do not mention
    those causes or explanations in the vehicle response unless the
    supplied vehicle evidence explicitly establishes them.
14. For example, if domain guidance says an odometer inconsistency
    may be caused by data-entry error, instrument replacement,
    source-system issues, or tampering, and the vehicle evidence only
    establishes an odometer decrease, state only that the odometer
    history is conflicting and requires verification. Do not mention
    any possible cause.
15. Do not invent vehicle facts, events, measurements, dates, causes,
    or conditions.
16. The trust score, risks, and purchase decision are deterministic outputs.
17. Do not recalculate, modify, override, or contradict the trust score.
18. Do not recalculate, add, remove, or change risk severity.
19. Do not change the deterministic purchase decision.
20. Treat conflicting evidence as an evidence issue requiring verification.
21. If evidence is insufficient, explicitly say that additional verification is required.
22. Do not claim fraud, tampering, mechanical failure, structural damage, or other
    conclusions unless the supplied evidence explicitly establishes them.
23. The recommendation must explain the supplied deterministic decision rather than
    creating a new decision.
24. Keep the response concise and focused on the vehicle's actual evidence and risks.

Return a JSON object with exactly these fields:
{
  "summary": "string",
  "reasoning": "string",
  "recommendation": "string"
}

Do not return evidence IDs, knowledge references, or grounding metadata.
The application will construct those fields from the supplied evidence and retrieved knowledge.
"""

_GUIDANCE_SECTIONS = {
    "verification actions",
    "ai grounding rule",
}


def build_llm_prompt(
    request: AIRequest,
    knowledge: list[KnowledgeResult],
) -> str:
    return (
        f"{SYSTEM_INSTRUCTIONS}\n\n"
        f"VEHICLE INTELLIGENCE — AUTHORITATIVE VEHICLE FACTS:\n"
        f"{_format_vehicle_context(request)}\n\n"
        f"RETRIEVED DOMAIN GUIDANCE — SECONDARY INTERPRETATION ONLY:\n"
        f"{_format_knowledge(knowledge)}\n\n"
        "Write the explanation for the specific vehicle now. "
        "Do not summarize the domain guidance."
    )


def _format_vehicle_context(request: AIRequest) -> str:
    """Build a generation-focused projection of the vehicle intelligence.

    The API contract contains transport, provenance, and implementation
    metadata that is important to the application but is not required by
    the language model to produce a grounded explanation.
    """

    context: dict[str, Any] = {
        "vehicle": {
            "make": request.vehicle.make,
            "model": request.vehicle.model,
            "year": request.vehicle.year,
            "registration": request.vehicle.registration,
        },
        "evidence": [
            {
                "id": evidence.id,
                "category": evidence.category,
                "title": evidence.title,
                "value": evidence.value,
                "status": evidence.status,
                "confidence": evidence.confidence,
                "explanation": evidence.explanation,
            }
            for evidence in request.evidence
        ],
        "risks": [
            {
                "id": risk.id,
                "category": risk.category,
                "title": risk.title,
                "severity": risk.severity,
                "status": risk.status,
                "confidence": risk.confidence,
                "evidence_ids": risk.evidence_ids,
                "recommended_action": risk.recommended_action,
            }
            for risk in request.risks
        ],
        "trust": {
            "score": request.trust.score,
            "confidence": request.trust.confidence,
            "assessment": request.trust.assessment,
        },
        "decision": {
            "recommendation": request.decision.recommendation,
            "confidence": request.decision.confidence,
            "rationale": request.decision.rationale,
            "priority_risk_ids": request.decision.priority_risk_ids,
        },
    }

    import json

    return json.dumps(context, indent=2)


def _format_knowledge(knowledge: list[KnowledgeResult]) -> str:
    if not knowledge:
        return "No domain guidance was retrieved."

    sections: list[str] = []

    for result in knowledge:
        document = result.document
        content = _extract_relevant_guidance(document.content)

        sections.append(
            f"Knowledge ID: {document.id}\n"
            f"Title: {document.title}\n"
            f"Category: {document.category}\n"
            f"Relevance: {result.relevance}\n"
            f"Content:\n{content}"
        )

    return "\n\n---\n\n".join(sections)


def _extract_relevant_guidance(content: str) -> str:
    """Extract grounding and verification sections from structured Markdown.

    Short or unstructured knowledge content is returned unchanged so that
    compact test fixtures and future simple documents remain supported.
    """

    lines = content.splitlines()

    heading_indexes: list[tuple[int, str]] = []

    for index, line in enumerate(lines):
        if not line.startswith("## "):
            continue

        heading = line[3:].strip().lower()

        if heading in _GUIDANCE_SECTIONS:
            heading_indexes.append((index, heading))

    if not heading_indexes:
        return content

    extracted: list[str] = []

    for position, (start_index, _) in enumerate(heading_indexes):
        end_index = (
            heading_indexes[position + 1][0]
            if position + 1 < len(heading_indexes)
            else len(lines)
        )

        extracted.extend(lines[start_index:end_index])

    return "\n".join(extracted).strip()