from app.schemas.contracts import AIRequest


def build_retrieval_queries(request: AIRequest) -> list[str]:
    """Build domain-knowledge queries from deterministic vehicle signals."""

    queries: list[str] = []

    for risk in request.risks:
        query = _build_risk_query(risk.category, risk.title, risk.explanation)
        if query and query not in queries:
            queries.append(query)

    if not queries:
        queries.extend(_build_evidence_queries(request))

    return queries


def _build_risk_query(
    category: str,
    title: str,
    explanation: str,
) -> str:
    parts = [
        category,
        title,
        explanation,
        "verification guidance",
    ]

    return " ".join(
        part.strip()
        for part in parts
        if part and part.strip()
    )


def _build_evidence_queries(request: AIRequest) -> list[str]:
    queries: list[str] = []

    for evidence in request.evidence:
        if evidence.status in {"conflicting", "partially_verified"}:
            query = " ".join(
                part.strip()
                for part in [
                    evidence.category,
                    evidence.title,
                    evidence.value,
                    "verification guidance",
                ]
                if part and part.strip()
            )

            if query and query not in queries:
                queries.append(query)

    return queries