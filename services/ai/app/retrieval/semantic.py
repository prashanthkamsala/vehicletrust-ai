from sentence_transformers import SentenceTransformer

from app.retrieval.base import (
    KnowledgeDocument,
    KnowledgeResult,
    Retriever,
)


class SemanticRetriever(Retriever):
    """Retrieve local knowledge using semantic similarity."""

    def __init__(
        self,
        documents: list[KnowledgeDocument],
        *,
        model_name: str = "all-MiniLM-L6-v2",
    ) -> None:
        self.documents = documents
        self.model = SentenceTransformer(model_name)

        self.document_texts = [
            self._build_document_text(document)
            for document in documents
        ]

        self.document_embeddings = self.model.encode(
            self.document_texts,
            normalize_embeddings=True,
        )

    def search(
        self,
        query: str,
        *,
        limit: int = 5,
    ) -> list[KnowledgeResult]:
        if limit <= 0 or not query.strip() or not self.documents:
            return []

        query_embedding = self.model.encode(
            query,
            normalize_embeddings=True,
        )

        scores = self.document_embeddings @ query_embedding

        ranked_indexes = sorted(
            range(len(scores)),
            key=lambda index: float(scores[index]),
            reverse=True,
        )

        results: list[KnowledgeResult] = []

        for index in ranked_indexes[:limit]:
            score = float(scores[index])

            results.append(
                KnowledgeResult(
                    document=self.documents[index],
                    relevance=f"Semantic similarity score: {score:.4f}",
                )
            )

        return results

    @staticmethod
    def _build_document_text(document: KnowledgeDocument) -> str:
        return " ".join(
            part
            for part in [
                document.title,
                document.category,
                " ".join(document.keywords),
                document.content,
            ]
            if part
        )
