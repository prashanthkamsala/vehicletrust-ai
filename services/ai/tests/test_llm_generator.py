import json

import pytest

from app.generation.llm import (
    LLMExplanation,
    LLMGenerationError,
    LLMGenerator,
)
from app.generation.providers.base import LLMClient
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


class FakeLLMClient(LLMClient):
    def __init__(self, response: str) -> None:
        self.response = response
        self.prompts: list[str] = []
        self.response_formats: list[dict | str | None] = []

    def generate(
        self,
        prompt: str,
        *,
        response_format: dict | str | None = None,
    ) -> str:
        self.prompts.append(prompt)
        self.response_formats.append(response_format)
        return self.response


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
                explanation=(
                    "A later observation is lower than an earlier observation."
                ),
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
                explanation=(
                    "Chronological odometer records contain a decrease."
                ),
                evidence_ids=["mileage-consistency"],
                recommended_action=(
                    "Verify the mileage history using additional records."
                ),
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
            rationale=(
                "Multiple high-severity risks require resolution before purchase."
            ),
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
                content=(
                    "A decrease between chronological odometer observations "
                    "requires investigation."
                ),
                keywords=["odometer", "mileage", "inconsistency"],
            ),
            relevance="Relevant to the identified odometer risk.",
        ),
    ]


def build_valid_response() -> str:
    return json.dumps(
        {
            "summary": (
                "The vehicle has an odometer inconsistency requiring "
                "verification."
            ),
            "reasoning": (
                "The mileage history contains a chronological decrease."
            ),
            "recommendation": (
                "The deterministic decision is avoid until the mileage "
                "history is verified."
            ),
        }
    )


def test_llm_generator_builds_prompt_and_parses_response():
    client = FakeLLMClient(build_valid_response())
    generator = LLMGenerator(client)

    result = generator.generate(
        build_test_request(),
        build_test_knowledge(),
    )

    assert result.summary == (
        "The vehicle has an odometer inconsistency requiring verification."
    )
    assert result.reasoning == (
        "The mileage history contains a chronological decrease."
    )
    assert result.recommendation == (
        "The deterministic decision is avoid until the mileage history "
        "is verified."
    )

    assert result.supporting_evidence_ids == ["mileage-consistency"]
    assert result.knowledge_references[0].id == "knowledge-odometer"
    assert result.grounding.status == "grounded"

    assert len(client.prompts) == 1
    assert client.response_formats == [LLMExplanation.model_json_schema()]
    assert "Honda" in client.prompts[0]
    assert "knowledge-odometer" in client.prompts[0]


def test_llm_generator_rejects_invalid_json():
    client = FakeLLMClient("This is not JSON.")
    generator = LLMGenerator(client)

    with pytest.raises(
        LLMGenerationError,
        match="not valid JSON",
    ):
        generator.generate(
            build_test_request(),
            build_test_knowledge(),
        )


def test_llm_generator_rejects_non_object_json():
    client = FakeLLMClient(json.dumps(["not", "an", "object"]))
    generator = LLMGenerator(client)

    with pytest.raises(
        LLMGenerationError,
        match="must be a JSON object",
    ):
        generator.generate(
            build_test_request(),
            build_test_knowledge(),
        )


def test_llm_generator_rejects_invalid_response_contract():
    invalid_response = json.dumps(
        {
            "summary": "Incomplete response",
            "reasoning": "Missing required fields.",
        }
    )

    client = FakeLLMClient(invalid_response)
    generator = LLMGenerator(client)

    with pytest.raises(
        LLMGenerationError,
        match="did not match the LLM explanation contract",
    ):
        generator.generate(
            build_test_request(),
            build_test_knowledge(),
        )


def test_llm_generator_builds_grounding_metadata_from_request_and_knowledge() -> None:
    llm_response = json.dumps(
        {
            "summary": "The vehicle has an odometer inconsistency.",
            "reasoning": (
                "The mileage history contains a chronological decrease."
            ),
            "recommendation": (
                "Verify the mileage history before purchase."
            ),
        }
    )

    client = FakeLLMClient(llm_response)
    generator = LLMGenerator(client)

    result = generator.generate(
        build_test_request(),
        build_test_knowledge(),
    )

    assert result.summary == "The vehicle has an odometer inconsistency."
    assert result.reasoning == (
        "The mileage history contains a chronological decrease."
    )
    assert result.recommendation == (
        "Verify the mileage history before purchase."
    )

    assert result.supporting_evidence_ids == ["mileage-consistency"]

    assert len(result.knowledge_references) == 1
    assert result.knowledge_references[0].id == "knowledge-odometer"

    assert result.grounding.status == "grounded"
    assert result.grounding.evidence_count == 1
    assert result.grounding.knowledge_count == 1