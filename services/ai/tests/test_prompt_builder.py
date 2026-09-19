from app.generation.prompt_builder import build_llm_prompt
from app.retrieval.base import KnowledgeDocument, KnowledgeResult
from app.schemas.contracts import (
    AIDecisionAssessment,
    AIEvidenceItem,
    AIEvidenceProvenance,
    AIEvidenceSource,
    AIRiskItem,
    AIRequest,
    AITrustAssessment,
    AIVehicleIdentity,
)


def build_test_request() -> AIRequest:
    return AIRequest(
        vehicle=AIVehicleIdentity(
            make="Honda",
            model="City",
            year=2020,
            registration="MH 12 XY 9087",
        ),
        evidence=[
            AIEvidenceItem(
                id="mileage-consistency",
                category="odometer",
                title="Odometer history contains a decrease",
                value="42,100 km → 67,300 km → 52,100 km → 58,900 km",
                status="conflicting",
                confidence="high",
                explanation="A later observation is lower than an earlier observation.",
                source=AIEvidenceSource(
                    id="mock-history",
                    name="Mock Vehicle History",
                    type="synthetic",
                ),
                provenance=AIEvidenceProvenance(
                    observed_at="2025-08-01",
                    retrieved_at="2025-08-02",
                    reference_id="MOCK-ODO-001",
                ),
            ),
        ],
        risks=[
            AIRiskItem(
                id="odometer-inconsistency",
                category="odometer",
                title="Odometer inconsistency",
                severity="high",
                status="needs_review",
                confidence="high",
                explanation="Chronological odometer records contain a decrease.",
                evidence_ids=["mileage-consistency"],
                recommended_action="Verify the mileage history using additional records.",
            ),
        ],
        trust=AITrustAssessment(
            score=32,
            confidence="high",
            assessment="Very low trust due to multiple high-impact risks.",
            factors=[],
        ),
        decision=AIDecisionAssessment(
            recommendation="avoid",
            confidence="high",
            rationale="Multiple high-severity risks require resolution before purchase.",
            priority_risk_ids=["odometer-inconsistency"],
        ),
    )


def build_test_knowledge() -> list[KnowledgeResult]:
    return [
        KnowledgeResult(
            document=KnowledgeDocument(
                id="knowledge-odometer",
                title="Odometer Verification Guidance",
                category="odometer",
                content="A decrease between chronological odometer observations requires investigation.",
                keywords=["odometer", "mileage", "inconsistency"],
            ),
            relevance="Relevant to the identified odometer risk.",
        ),
        KnowledgeResult(
            document=KnowledgeDocument(
                id="knowledge-accident",
                title="Accident History Guidance",
                category="accident",
                content="Accident records should be reviewed against available supporting evidence.",
                keywords=["accident", "damage"],
            ),
            relevance="General guidance for accident-history verification.",
        ),
    ]


def test_prompt_contains_deterministic_vehicle_intelligence():
    prompt = build_llm_prompt(
        build_test_request(),
        build_test_knowledge(),
    )

    assert "Honda" in prompt
    assert "City" in prompt
    assert "MH 12 XY 9087" in prompt
    assert '"score": 32' in prompt
    assert '"recommendation": "avoid"' in prompt
    assert "odometer-inconsistency" in prompt
    assert "mileage-consistency" in prompt


def test_prompt_contains_retrieved_domain_guidance():
    prompt = build_llm_prompt(
        build_test_request(),
        build_test_knowledge(),
    )

    assert "knowledge-odometer" in prompt
    assert "Odometer Verification Guidance" in prompt
    assert "knowledge-accident" in prompt
    assert "Accident History Guidance" in prompt


def test_prompt_contains_grounding_rules():
    prompt = build_llm_prompt(
        build_test_request(),
        build_test_knowledge(),
    )

    assert "Do not invent vehicle facts" in prompt
    assert "Do not recalculate, modify, override, or contradict the trust score" in prompt
    assert "Do not recalculate, add, remove, or change risk severity" in prompt
    assert "Do not change the deterministic purchase decision" in prompt


def test_prompt_handles_empty_knowledge():
    prompt = build_llm_prompt(
        build_test_request(),
        [],
    )

    assert "No domain guidance was retrieved." in prompt


def test_prompt_requires_llm_to_return_only_explanation_fields():
    prompt = build_llm_prompt(
        build_test_request(),
        build_test_knowledge(),
    )

    assert (
        "Do not return evidence IDs, knowledge references, "
        "or grounding metadata."
    ) in prompt
    assert "The application will construct those fields" in prompt


def test_prompt_treats_evidence_status_as_authoritative():
    prompt = build_llm_prompt(
        build_test_request(),
        build_test_knowledge(),
    )

    assert "Evidence status is authoritative for the vehicle." in prompt
    assert (
        'If a vehicle evidence item is marked "verified", '
        "treat that fact as verified."
    ) in prompt
    assert (
        'If a vehicle evidence item is marked "conflicting", '
        "describe it as conflicting."
    ) in prompt


def test_prompt_prevents_knowledge_from_becoming_vehicle_specific_fact():
    prompt = build_llm_prompt(
        build_test_request(),
        build_test_knowledge(),
    )

    assert "Do not infer a conflicting vehicle status" in prompt
    assert "domain guidance" in prompt
    assert "possible conflicts" in prompt
    assert "hypothetical examples" in prompt
    assert "possible explanations" in prompt
    assert "vehicle-specific facts" in prompt