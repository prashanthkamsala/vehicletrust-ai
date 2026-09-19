from pathlib import Path

from app.retrieval.knowledge_retriever import KnowledgeRetriever
from app.retrieval.local import LocalKeywordRetriever
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


KNOWLEDGE_DIR = (
    Path(__file__).resolve().parents[1]
    / "knowledge"
    / "vehicle"
)


def build_request(
    *,
    risks: list[AIRiskItem],
    evidence: list[AIEvidenceItem],
) -> AIRequest:
    return AIRequest(
        vehicle=AIVehicleIdentity(
            make="Honda",
            model="City",
            year=2021,
            registration="MH 12 XY 9087",
        ),
        evidence=evidence,
        risks=risks,
        trust=AITrustAssessment(
            score=0,
            confidence="low",
            assessment="Very low trust",
        ),
        decision=AIDecisionAssessment(
            recommendation="avoid",
            confidence="high",
            rationale="High-severity risks require investigation.",
        ),
    )


def test_knowledge_retriever_finds_odometer_guidance() -> None:
    retriever = LocalKeywordRetriever(KNOWLEDGE_DIR)
    knowledge_retriever = KnowledgeRetriever(retriever)

    request = build_request(
        risks=[
            AIRiskItem(
                id="odometer-inconsistency",
                category="Mileage",
                title="Odometer inconsistency",
                severity="high",
                status="needs_review",
                confidence="high",
                explanation="The odometer history contains a decrease.",
                evidence_ids=["mileage-consistency"],
                recommended_action="Verify the mileage history.",
            ),
        ],
        evidence=[
            AIEvidenceItem(
                id="mileage-consistency",
                category="Mileage",
                title="Mileage consistency",
                value="Inconsistent: 67,300 km to 52,100 km",
                status="conflicting",
                confidence="high",
                explanation="The odometer history contains a decrease.",
                source=AIEvidenceSource(
                    id="mileage-records",
                    name="Mileage records",
                    type="vehicle_history",
                ),
                provenance=AIEvidenceProvenance(
                    observed_at="2026-09-10",
                ),
            ),
        ],
    )

    results = knowledge_retriever.retrieve(request)

    assert results
    assert results[0].document.id == "odometer"


def test_knowledge_retriever_finds_multiple_domains() -> None:
    retriever = LocalKeywordRetriever(KNOWLEDGE_DIR)
    knowledge_retriever = KnowledgeRetriever(retriever)

    request = build_request(
        risks=[
            AIRiskItem(
                id="expired-insurance",
                category="Insurance",
                title="Insurance has expired",
                severity="medium",
                status="needs_review",
                confidence="high",
                explanation="The insurance record is expired.",
                evidence_ids=["insurance-status"],
                recommended_action="Verify current insurance coverage.",
            ),
            AIRiskItem(
                id="expired-puc",
                category="Compliance",
                title="PUC certificate has expired",
                severity="medium",
                status="needs_review",
                confidence="high",
                explanation="The PUC record is expired.",
                evidence_ids=["puc-status"],
                recommended_action="Obtain a valid PUC certificate.",
            ),
        ],
        evidence=[],
    )

    results = knowledge_retriever.retrieve(request)

    document_ids = {result.document.id for result in results}

    assert "insurance" in document_ids
    assert "puc" in document_ids


def test_knowledge_retriever_deduplicates_documents() -> None:
    retriever = LocalKeywordRetriever(KNOWLEDGE_DIR)
    knowledge_retriever = KnowledgeRetriever(retriever)

    request = build_request(
        risks=[
            AIRiskItem(
                id="odometer-inconsistency",
                category="Mileage",
                title="Odometer inconsistency",
                severity="high",
                status="needs_review",
                confidence="high",
                explanation="The odometer history contains a decrease.",
                evidence_ids=["mileage-consistency"],
                recommended_action="Verify the mileage history.",
            ),
            AIRiskItem(
                id="mileage-review",
                category="Mileage",
                title="Mileage requires review",
                severity="medium",
                status="needs_review",
                confidence="high",
                explanation="Mileage records should be verified.",
                evidence_ids=["mileage-consistency"],
                recommended_action="Verify the mileage history.",
            ),
        ],
        evidence=[],
    )

    results = knowledge_retriever.retrieve(request)

    document_ids = [result.document.id for result in results]

    assert len(document_ids) == len(set(document_ids))

def test_knowledge_retriever_covers_all_vehicle_domains() -> None:
    retriever = LocalKeywordRetriever(KNOWLEDGE_DIR)
    knowledge_retriever = KnowledgeRetriever(retriever)

    request = build_request(
        risks=[
            AIRiskItem(
                id="accident-risk",
                category="Accident",
                title="Major accident history",
                severity="high",
                status="needs_review",
                confidence="high",
                explanation="The vehicle has a reported major accident.",
                evidence_ids=["accident-history"],
                recommended_action="Review accident and repair records.",
            ),
            AIRiskItem(
                id="finance-risk",
                category="Finance",
                title="Active finance",
                severity="medium",
                status="identified",
                confidence="high",
                explanation="The vehicle has an active finance record.",
                evidence_ids=["finance-status"],
                recommended_action="Verify finance closure status.",
            ),
            AIRiskItem(
                id="insurance-risk",
                category="Insurance",
                title="Expired insurance",
                severity="medium",
                status="needs_review",
                confidence="high",
                explanation="The insurance record has expired.",
                evidence_ids=["insurance-status"],
                recommended_action="Verify current insurance coverage.",
            ),
            AIRiskItem(
                id="maintenance-risk",
                category="Maintenance",
                title="Maintenance history requires review",
                severity="medium",
                status="needs_review",
                confidence="medium",
                explanation="The available maintenance history has gaps.",
                evidence_ids=["service-history"],
                recommended_action="Review available service records.",
            ),
            AIRiskItem(
                id="odometer-risk",
                category="Mileage",
                title="Odometer inconsistency",
                severity="high",
                status="needs_review",
                confidence="high",
                explanation="The odometer history contains a decrease.",
                evidence_ids=["mileage-consistency"],
                recommended_action="Verify the mileage history.",
            ),
            AIRiskItem(
                id="ownership-risk",
                category="Ownership",
                title="Multiple ownership history",
                severity="low",
                status="identified",
                confidence="high",
                explanation="The vehicle has multiple recorded owners.",
                evidence_ids=["ownership-history"],
                recommended_action="Review ownership history.",
            ),
            AIRiskItem(
                id="puc-risk",
                category="Compliance",
                title="PUC certificate has expired",
                severity="medium",
                status="needs_review",
                confidence="high",
                explanation="The PUC record is expired.",
                evidence_ids=["puc-status"],
                recommended_action="Verify current PUC status.",
            ),
        ],
        evidence=[],
    )

    results = knowledge_retriever.retrieve(request)

    document_ids = {
        result.document.id
        for result in results
    }

    assert document_ids == {
        "accident",
        "finance",
        "insurance",
        "maintenance",
        "odometer",
        "ownership",
        "puc",
    }


def test_knowledge_retriever_scopes_single_risk_to_its_domain() -> None:
    retriever = LocalKeywordRetriever(KNOWLEDGE_DIR)
    knowledge_retriever = KnowledgeRetriever(retriever)

    request = build_request(
        risks=[
            AIRiskItem(
                id="odometer-inconsistency",
                category="Mileage",
                title="Odometer inconsistency",
                severity="high",
                status="needs_review",
                confidence="high",
                explanation="The odometer history contains a decrease.",
                evidence_ids=["mileage-consistency"],
                recommended_action="Verify the mileage history.",
            ),
        ],
        evidence=[],
    )

    results = knowledge_retriever.retrieve(request)

    document_ids = [result.document.id for result in results]

    assert document_ids == ["odometer"]