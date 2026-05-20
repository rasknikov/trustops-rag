from dataclasses import dataclass

from trustops_rag.domain.retrieval import ScoredRetrievedChunk


@dataclass
class RerankInput:
    normalized_question: str
    max_results: int


@dataclass
class RerankedChunk:
    chunk_id: str
    document_version_id: str
    content: str
    retrieval_score: int
    rerank_score: int
    matched_term_count: int
    contains_full_question: bool
    rerank_reason: str


def validate_rerank_input(rerank_input: RerankInput) -> None:
    if not rerank_input.normalized_question.strip():
        raise ValueError("Normalized question cannot be empty.")

    if rerank_input.max_results <= 0:
        raise ValueError("max_results must be greater than zero.")


def extract_rerank_terms(normalized_question: str) -> list[str]:
    return normalized_question.split()


def count_term_matches(query_terms: list[str], chunk_content: str) -> int:
    normalized_content = chunk_content.lower()
    score = 0

    for word in query_terms:
        if word in normalized_content:
            score += 1

    return score


def chunk_contains_full_question(normalized_question: str, chunk_content: str) -> bool:
    return normalized_question in chunk_content.lower()


def calculate_rerank_score(
    normalized_question: str,
    query_terms: list[str],
    scored_chunk: ScoredRetrievedChunk,
) -> int:
    matched_term_count = count_term_matches(query_terms, scored_chunk.chunk.content)
    rerank_score = scored_chunk.calculated_score + matched_term_count

    if chunk_contains_full_question(normalized_question, scored_chunk.chunk.content):
        rerank_score += 3

    return rerank_score


def build_reranked_chunk(
    normalized_question: str,
    query_terms: list[str],
    scored_chunk: ScoredRetrievedChunk,
) -> RerankedChunk:
    matched_term_count = count_term_matches(query_terms, scored_chunk.chunk.content)
    contains_full_question = chunk_contains_full_question(
        normalized_question,
        scored_chunk.chunk.content,
    )
    rerank_score = calculate_rerank_score(
        normalized_question,
        query_terms,
        scored_chunk,
    )

    if contains_full_question:
        rerank_reason = "full_question_match"
    else:
        rerank_reason = "term_match_reordered"

    return RerankedChunk(
        chunk_id=scored_chunk.chunk.chunk_id,
        document_version_id=scored_chunk.chunk.document_version_id,
        content=scored_chunk.chunk.content,
        retrieval_score=scored_chunk.calculated_score,
        rerank_score=rerank_score,
        matched_term_count=matched_term_count,
        contains_full_question=contains_full_question,
        rerank_reason=rerank_reason,
    )


def rank_reranked_chunks(reranked_chunks: list[RerankedChunk]) -> list[RerankedChunk]:
    return sorted(
        reranked_chunks,
        key=lambda chunk: (
            chunk.contains_full_question,
            chunk.rerank_score,
            chunk.matched_term_count,
            chunk.retrieval_score,
        ),
        reverse=True,
    )


def rerank_chunks(
    rerank_input: RerankInput,
    available_chunks: list[ScoredRetrievedChunk],
) -> list[RerankedChunk]:
    validate_rerank_input(rerank_input)

    query_terms = extract_rerank_terms(rerank_input.normalized_question)
    reranked_chunks: list[RerankedChunk] = []

    for scored_chunk in available_chunks:
        reranked_chunk = build_reranked_chunk(
            rerank_input.normalized_question,
            query_terms,
            scored_chunk,
        )

        if reranked_chunk.matched_term_count <= 0:
            continue

        reranked_chunks.append(reranked_chunk)

    ranked_results = rank_reranked_chunks(reranked_chunks)

    return ranked_results[:rerank_input.max_results]
