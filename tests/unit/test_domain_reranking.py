from trustops_rag.domain.reranking import RerankInput, rerank_chunks
from trustops_rag.domain.retrieval import RetrievedChunk, ScoredRetrievedChunk


def test_rerank_chunks_prioritizes_full_question_match() -> None:
    rerank_input = RerankInput(
        normalized_question="vacation policy",
        max_results=2,
    )
    full_match_chunk = ScoredRetrievedChunk(
        chunk=RetrievedChunk(
            chunk_id="chunk-1",
            document_version_id="version-1",
            content="The vacation policy applies to all employees.",
            match_score=2,
            is_active=True,
        ),
        calculated_score=2,
    )
    partial_match_chunk = ScoredRetrievedChunk(
        chunk=RetrievedChunk(
            chunk_id="chunk-2",
            document_version_id="version-1",
            content="The policy covers travel reimbursement only.",
            match_score=3,
            is_active=True,
        ),
        calculated_score=3,
    )

    reranked_chunks = rerank_chunks(
        rerank_input,
        [partial_match_chunk, full_match_chunk],
    )

    assert len(reranked_chunks) == 2
    assert reranked_chunks[0].chunk_id == "chunk-1"
    assert reranked_chunks[0].contains_full_question is True
    assert reranked_chunks[0].rerank_reason == "full_question_match"


def test_rerank_chunks_rejects_empty_question() -> None:
    rerank_input = RerankInput(
        normalized_question="   ",
        max_results=2,
    )

    try:
        rerank_chunks(rerank_input, [])
    except ValueError as exc:
        assert str(exc) == "Normalized question cannot be empty."
    else:
        raise AssertionError("Expected ValueError for empty normalized question.")
