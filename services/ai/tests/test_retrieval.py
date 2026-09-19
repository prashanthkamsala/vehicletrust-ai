from app.retrieval.base import (
    KnowledgeDocument,
    KnowledgeResult,
)


def test_knowledge_document_contains_domain_knowledge() -> None:
    document = KnowledgeDocument(
        id="puc-compliance",
        title="PUC compliance guidance",
        category="puc",
        content="A valid PUC certificate provides evidence of current emission compliance.",
        keywords=["puc", "pollution", "emission", "certificate"],
    )

    assert document.id == "puc-compliance"
    assert document.category == "puc"
    assert "emission" in document.content
    assert "puc" in document.keywords


def test_knowledge_result_wraps_document() -> None:
    document = KnowledgeDocument(
        id="maintenance-basics",
        title="Vehicle maintenance basics",
        category="maintenance",
        content="Regular maintenance helps identify wear and maintenance gaps.",
        keywords=["maintenance", "service"],
    )

    result = KnowledgeResult(
        document=document,
        relevance="Matches the maintenance risk.",
    )

    assert result.document.id == "maintenance-basics"
    assert result.relevance == "Matches the maintenance risk."