import pytest

from app.generation.llm import LLMExplanation, LLMGenerator
from app.generation.providers.base import LLMClient
from app.domain.ai_service import AIService
from app.domain.grounding import GroundingValidationError
from app.generation.base import AIGenerator
from app.retrieval.base import KnowledgeDocument, KnowledgeResult, Retriever
from app.retrieval.knowledge_retriever import KnowledgeRetriever
from app.schemas.contracts import (
    AIGrounding,
    AIRequest,
    AIResponse,
)


class FakeRetriever(Retriever):
    def __init__(self, results: list[KnowledgeResult]) -> None:
        self.results = results
        self.queries: list[str] = []

    def search(
        self,
        query: str,
        *,
        limit: int = 5,
    ) -> list[KnowledgeResult]:
        self.queries.append(query)
        return self.results[:limit]


class FakeGenerator(AIGenerator):
    def __init__(self, response: AIResponse) -> None:
        self.response = response
        self.request: AIRequest | None = None
        self.knowledge: list[KnowledgeResult] | None = None

    def generate(
        self,
        request: AIRequest,
        knowledge: list[KnowledgeResult],
    ) -> AIResponse:
        self.request = request
        self.knowledge = knowledge
        return self.response


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


def build_request() -> AIRequest:
    return AIRequest.model_validate(
        {
            "vehicle": {
                "make": "Honda",
                "model": "City",
                "year": 2020,
                "registration": "MH 12 XY 9087",
            },
            "evidence": [
                {
                    "id": "odometer-inconsistency",
                    "category": "mileage",
                    "title": "Odometer inconsistency",
                    "value": "67,300 km to 52,100 km",
                    "status": "conflicting",
                    "confidence": "high",
                    "explanation": "The recorded mileage decreases.",
                    "source": {
                        "id": "mock-provider",
                        "name": "Mock India Provider",
                        "type": "mock",
                    },
                    "provenance": {},
                }
            ],
            "risks": [],
            "trust": {
                "score": 42,
                "confidence": "medium",
                "assessment": "Low trust.",
                "factors": [],
            },
            "decision": {
                "recommendation": "avoid",
                "confidence": "high",
                "rationale": "Mileage evidence requires verification.",
                "priority_risk_ids": [],
            },
        }
    )


def build_knowledge_result() -> KnowledgeResult:
    return KnowledgeResult(
        document=KnowledgeDocument(
            id="odometer",
            title="Odometer Verification Guidance",
            category="odometer",
            content="Mileage decreases require investigation.",
            keywords=["odometer", "mileage"],
        ),
        relevance="Keyword relevance score: 8",
    )


def build_response(
    *,
    evidence_ids: list[str] | None = None,
    knowledge_ids: list[str] | None = None,
) -> AIResponse:
    evidence_ids = evidence_ids or []
    knowledge_ids = knowledge_ids or []

    return AIResponse(
        summary="Vehicle evidence requires verification.",
        reasoning="The available records contain an inconsistency.",
        recommendation="Review the vehicle evidence before purchase.",
        supporting_evidence_ids=evidence_ids,
        knowledge_references=[
            {
                "id": knowledge_id,
                "title": "Odometer Verification Guidance",
                "category": "odometer",
                "relevance": "Relevant guidance.",
            }
            for knowledge_id in knowledge_ids
        ],
        grounding=AIGrounding(
            status="grounded",
            evidence_count=len(evidence_ids),
            knowledge_count=len(knowledge_ids),
        ),
    )


def build_service(
    response: AIResponse,
) -> tuple[AIService, FakeRetriever, FakeGenerator]:
    knowledge_result = build_knowledge_result()

    fake_retriever = FakeRetriever(
        [knowledge_result],
    )
    fake_generator = FakeGenerator(response)

    knowledge_retriever = KnowledgeRetriever(
        fake_retriever,
    )

    service = AIService(
        retriever=knowledge_retriever,
        generator=fake_generator,
    )

    return service, fake_retriever, fake_generator


def test_ai_service_orchestrates_retrieval_and_generation() -> None:
    request = build_request()

    response = build_response(
        evidence_ids=["odometer-inconsistency"],
        knowledge_ids=["odometer"],
    )

    service, fake_retriever, fake_generator = build_service(response)

    result = service.interpret(request)

    assert result is response
    assert fake_retriever.queries
    assert fake_generator.request is request
    assert fake_generator.knowledge is not None
    assert len(fake_generator.knowledge) == 1
    assert fake_generator.knowledge[0].document.id == "odometer"


def test_ai_service_validates_generated_response() -> None:
    request = build_request()

    response = build_response(
        evidence_ids=["odometer-inconsistency"],
        knowledge_ids=["odometer"],
    )

    service, _, _ = build_service(response)

    result = service.interpret(request)

    assert result.grounding.status == "grounded"
    assert result.supporting_evidence_ids == [
        "odometer-inconsistency",
    ]


def test_ai_service_rejects_unknown_evidence_reference() -> None:
    request = build_request()

    response = build_response(
        evidence_ids=["unknown-evidence"],
        knowledge_ids=["odometer"],
    )

    service, _, _ = build_service(response)

    with pytest.raises(
        GroundingValidationError,
        match="unknown evidence IDs",
    ):
        service.interpret(request)


def test_ai_service_rejects_unknown_knowledge_reference() -> None:
    request = build_request()

    response = build_response(
        evidence_ids=["odometer-inconsistency"],
        knowledge_ids=["unknown-knowledge"],
    )

    service, _, _ = build_service(response)

    with pytest.raises(
        GroundingValidationError,
        match="unknown knowledge IDs",
    ):
        service.interpret(request)


def test_ai_service_passes_retrieved_knowledge_to_generator() -> None:
    request = build_request()

    response = build_response(
        evidence_ids=["odometer-inconsistency"],
        knowledge_ids=["odometer"],
    )

    service, _, fake_generator = build_service(response)

    service.interpret(request)

    assert fake_generator.knowledge is not None
    assert [
        result.document.id
        for result in fake_generator.knowledge
    ] == ["odometer"]


def test_ai_service_orchestrates_llm_generation_and_grounding() -> None:
    request = build_request()

    response = build_response(
        evidence_ids=["odometer-inconsistency"],
        knowledge_ids=["odometer"],
    )

    llm_client = FakeLLMClient(response.model_dump_json())
    llm_generator = LLMGenerator(llm_client)

    knowledge_result = build_knowledge_result()

    fake_retriever = FakeRetriever([knowledge_result])
    knowledge_retriever = KnowledgeRetriever(fake_retriever)

    service = AIService(
        retriever=knowledge_retriever,
        generator=llm_generator,
    )

    result = service.interpret(request)

    assert result.supporting_evidence_ids == [
        "odometer-inconsistency",
    ]
    assert result.knowledge_references[0].id == "odometer"
    assert result.grounding.status == "grounded"

    assert len(llm_client.prompts) == 1
    assert llm_client.response_formats == [
    LLMExplanation.model_json_schema()
    ]