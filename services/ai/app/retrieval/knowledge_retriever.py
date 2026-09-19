from app.retrieval.base import KnowledgeResult, Retriever
from app.retrieval.query_builder import build_retrieval_queries
from app.schemas.contracts import AIRequest


class KnowledgeRetriever:
    """Orchestrate retrieval of domain knowledge for an AI request."""

    CATEGORY_TO_DOMAIN = {
        "accident": "accident",
        "finance": "finance",
        "insurance": "insurance",
        "maintenance": "maintenance",
        "mileage": "odometer",
        "odometer": "odometer",
        "ownership": "ownership",
        "compliance": "puc",
        "puc": "puc",
    }

    def __init__(
        self,
        retriever: Retriever,
        *,
        results_per_query: int = 3,
    ) -> None:
        self.retriever = retriever
        self.results_per_query = results_per_query

    def retrieve(self, request: AIRequest) -> list[KnowledgeResult]:
        """Retrieve relevant domain knowledge for the supplied AI request."""

        queries = build_retrieval_queries(request)

        results: list[KnowledgeResult] = []
        seen_document_ids: set[str] = set()

        for query, domain in zip(
            queries,
            self._resolve_query_domains(request),
        ):
            query_results = self.retriever.search(
                query,
                limit=self.results_per_query,
            )

            for result in query_results:
                document_id = result.document.id

                if domain is not None and document_id != domain:
                    continue

                if document_id in seen_document_ids:
                    continue

                seen_document_ids.add(document_id)
                results.append(result)

        return results

    def _resolve_query_domains(
        self,
        request: AIRequest,
    ) -> list[str | None]:
        """Resolve the expected knowledge domain for each retrieval query."""

        domains: list[str | None] = []

        if request.risks:
            for risk in request.risks:
                domains.append(
                    self.CATEGORY_TO_DOMAIN.get(
                        risk.category.strip().lower()
                    )
                )

            return domains

        for evidence in request.evidence:
            if evidence.status in {"conflicting", "partially_verified"}:
                domains.append(
                    self.CATEGORY_TO_DOMAIN.get(
                        evidence.category.strip().lower()
                    )
                )

        return domains