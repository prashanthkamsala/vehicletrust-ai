from pathlib import Path

from app.retrieval.base import (
    KnowledgeDocument,
    KnowledgeResult,
    Retriever,
)


class LocalKeywordRetriever(Retriever):
    """Retrieve local knowledge documents using deterministic keyword matching."""

    def __init__(self, knowledge_dir: Path) -> None:
        self.knowledge_dir = knowledge_dir
        self.documents = self._load_documents()

    def search(
        self,
        query: str,
        *,
        limit: int = 5,
    ) -> list[KnowledgeResult]:
        """Return the most relevant local knowledge documents."""

        if limit <= 0:
            return []

        query_terms = self._tokenize(query)

        if not query_terms:
            return []

        scored_documents: list[tuple[int, KnowledgeDocument]] = []

        for document in self.documents:
            score = self._score_document(document, query_terms)

            if score > 0:
                scored_documents.append((score, document))

        scored_documents.sort(
            key=lambda item: (-item[0], item[1].id),
        )

        return [
            KnowledgeResult(
                document=document,
                relevance=f"Keyword relevance score: {score}",
            )
            for score, document in scored_documents[:limit]
        ]

    def _load_documents(self) -> list[KnowledgeDocument]:
        """Load Markdown knowledge documents from the configured directory."""

        if not self.knowledge_dir.exists():
            return []

        documents: list[KnowledgeDocument] = []

        for path in sorted(self.knowledge_dir.glob("*.md")):
            content = path.read_text(encoding="utf-8")

            documents.append(
                KnowledgeDocument(
                    id=path.stem,
                    title=self._extract_title(content, path.stem),
                    category=path.stem,
                    content=content,
                    keywords=self._extract_keywords(path.stem),
                )
            )

        return documents

    @staticmethod
    def _extract_title(content: str, fallback: str) -> str:
        for line in content.splitlines():
            if line.startswith("# "):
                return line[2:].strip()

        return fallback.replace("-", " ").title()

    @staticmethod
    def _extract_keywords(document_id: str) -> list[str]:
        keyword_map = {
            "accident": [
                "accident",
                "damage",
                "collision",
                "repair",
            ],
            "finance": [
                "finance",
                "financier",
                "loan",
                "lien",
            ],
            "insurance": [
                "insurance",
                "policy",
                "coverage",
                "expiry",
            ],
            "maintenance": [
                "maintenance",
                "service",
                "inspection",
                "invoice",
            ],
            "odometer": [
                "odometer",
                "mileage",
                "rollback",
                "inconsistency",
            ],
            "ownership": [
                "ownership",
                "owner",
                "transfer",
                "history",
            ],
            "puc": [
                "puc",
                "pollution",
                "emission",
                "certificate",
            ],
        }

        return keyword_map.get(document_id, [document_id])

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        return {
            token.strip(".,:;!?()[]{}\"'")
            for token in text.lower().split()
            if token.strip(".,:;!?()[]{}\"'")
        }

    def _score_document(
        self,
        document: KnowledgeDocument,
        query_terms: set[str],
    ) -> int:
        title_terms = self._tokenize(document.title)
        category_terms = self._tokenize(document.category)
        keyword_terms = set(document.keywords)
        content_terms = self._tokenize(document.content)

        score = 0

        score += len(query_terms & title_terms) * 5
        score += len(query_terms & category_terms) * 4
        score += len(query_terms & keyword_terms) * 3
        score += len(query_terms & content_terms)

        return score