from app.domain.vehicle_service import _build_vehicle_from_registration
from app.intelligence.ai.client import AIServiceClient
from app.intelligence.ai.request_builder import build_ai_request


def test_ai_service_client_calls_remote_service() -> None:
    vehicle = _build_vehicle_from_registration("MH 12 XY 9087")

    assert vehicle is not None

    request = build_ai_request(vehicle)

    client = AIServiceClient()

    result = client.interpret(request)

    assert result.summary
    assert result.reasoning
    assert result.recommendation

    assert result.supporting_evidence_ids
    assert 0 < result.grounding.evidence_count <= len(request.evidence)
    assert result.grounding.knowledge_count > 0