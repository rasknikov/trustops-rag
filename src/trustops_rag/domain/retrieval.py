from dataclasses import dataclass

@dataclass
class RetrievalInput:
    normalized_question: str
    max_results: int

@dataclass
class RetrievedChunk:
    chunk_id: str
    document_version_id: str
    content: str
    match_score: int
    is_active: bool

@dataclass
class ScoredRetrievedChunk:
    chunk: RetrievedChunk
    calculated_score: int

def validate_retrieval_input(retrieval_input: RetrievalInput) -> None:
    if not retrieval_input.normalized_question.strip():
        raise ValueError("Normalized question cannot be empty.")
    
    if retrieval_input.max_results <= 0:
        raise ValueError("max_results must be greater than zero.")
    
def extract_query_terms(normalized_question: str) -> list[str]:
    question_words = normalized_question.split()
    return question_words

def chunk_matches_query(query_terms: list[str], chunk: RetrievedChunk) -> bool:
    for i in query_terms:
        if i in chunk.content:
            return True
    return False

def calculate_match_score(query_terms: list[str], chunk: RetrievedChunk) -> int:
    score = 0

    for word in query_terms:
        if word in chunk.content:
            score += 1
    return score 

def score_retrieved_chunk(query_terms: list[str], chunk: RetrievedChunk) -> ScoredRetrievedChunk:
    score = calculate_match_score(query_terms, chunk)
    return ScoredRetrievedChunk(
        chunk=chunk,
        calculated_score=score
    )

def rank_scored_chunks(scored_chunks: list[ScoredRetrievedChunk]) -> list[ScoredRetrievedChunk]:
    return sorted(scored_chunks, key=lambda scored_chunks: scored_chunks.calculated_score, reverse=True)
                
def retrieve_scored_chunks(retrieval_input: RetrievalInput, available_chunks: list[RetrievedChunk]) -> list[ScoredRetrievedChunk]:
    results = []

    validate_retrieval_input(retrieval_input)

    question_words = extract_query_terms(retrieval_input.normalized_question)

    for chunk in available_chunks:
        if not chunk.is_active:
            continue

        if chunk_matches_query(question_words, chunk):
            results.append(score_retrieved_chunk(question_words, chunk))

    ranked_results = rank_scored_chunks(results)

    return ranked_results[:retrieval_input.max_results]

def retrieve_chunks(retrieval_input: RetrievalInput, available_chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
    results = []

    validate_retrieval_input(retrieval_input)

    question_words = extract_query_terms(retrieval_input.normalized_question)
    
    
    for chunk in available_chunks:
        if not chunk.is_active:
            continue

        if chunk_matches_query(question_words, chunk):
            results.append(chunk)

    return results[:retrieval_input.max_results]