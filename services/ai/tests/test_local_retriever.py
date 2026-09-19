from pathlib import Path

from app.retrieval.local import LocalKeywordRetriever


KNOWLEDGE_DIR = (
    Path(__file__).resolve().parents[1]
    / "knowledge"
    / "vehicle"
)


def test_retriever_loads_local_knowledge_documents() -> None:
    retriever = LocalKeywordRetriever(KNOWLEDGE_DIR)

    assert len(retriever.documents) == 7
    assert {document.id for document in retriever.documents} == {
        "accident",
        "finance",
        "insurance",
        "maintenance",
        "odometer",
        "ownership",
        "puc",
    }


def test_retriever_finds_odometer_guidance() -> None:
    retriever = LocalKeywordRetriever(KNOWLEDGE_DIR)

    results = retriever.search(
        "odometer mileage inconsistency",
        limit=3,
    )

    assert results
    assert results[0].document.id == "odometer"


def test_retriever_finds_puc_guidance() -> None:
    retriever = LocalKeywordRetriever(KNOWLEDGE_DIR)

    results = retriever.search(
        "PUC pollution emission certificate",
        limit=3,
    )

    assert results
    assert results[0].document.id == "puc"


def test_retriever_respects_limit() -> None:
    retriever = LocalKeywordRetriever(KNOWLEDGE_DIR)

    results = retriever.search(
        "vehicle history",
        limit=2,
    )

    assert len(results) <= 2


def test_retriever_returns_empty_for_unknown_query() -> None:
    retriever = LocalKeywordRetriever(KNOWLEDGE_DIR)

    results = retriever.search(
        "quantum telescope moonlight",
        limit=5,
    )

    assert results == []


def test_retriever_returns_empty_for_invalid_limit() -> None:
    retriever = LocalKeywordRetriever(KNOWLEDGE_DIR)

    assert retriever.search("odometer", limit=0) == []
    assert retriever.search("odometer", limit=-1) == []