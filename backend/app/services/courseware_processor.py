"""Courseware processing pipeline.

Extracts structured content (vocabulary, dialogues, songs, grammar points)
from uploaded files and generates embeddings for RAG retrieval.
"""

from app.ai.embeddings import get_embedding_provider
from app.ai.llm import get_llm_provider

EXTRACTION_PROMPT = """Analyze this English learning material and extract structured content.
Return a JSON object with these keys:
- vocabulary: list of {"word": "...", "meaning": "...", "example": "..."}
- dialogues: list of {"speaker": "...", "line": "..."}
- songs: list of {"title": "...", "lyrics": "..."}
- grammar_points: list of {"rule": "...", "example": "..."}

Only include items that are actually present in the material.
Material:
"""


async def extract_content(raw_text: str) -> dict:
    llm = get_llm_provider()
    response = await llm.chat(
        system_prompt="You are a teaching material analyzer. Return valid JSON only.",
        messages=[{"role": "user", "content": EXTRACTION_PROMPT + raw_text}],
        temperature=0.1,
    )
    import json
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {"vocabulary": [], "dialogues": [], "songs": [], "grammar_points": []}


async def generate_chunks(content: dict) -> list[dict]:
    chunks = []

    for vocab in content.get("vocabulary", []):
        chunks.append({
            "chunk_type": "vocabulary",
            "content": f"{vocab['word']}: {vocab.get('meaning', '')}. Example: {vocab.get('example', '')}",
            "metadata": {"word": vocab["word"]},
        })

    for song in content.get("songs", []):
        chunks.append({
            "chunk_type": "song_lyrics",
            "content": f"Song: {song['title']}\n{song['lyrics']}",
            "metadata": {"title": song["title"]},
        })

    for dialogue in content.get("dialogues", []):
        chunks.append({
            "chunk_type": "dialogue",
            "content": f"{dialogue['speaker']}: {dialogue['line']}",
            "metadata": {},
        })

    for grammar in content.get("grammar_points", []):
        chunks.append({
            "chunk_type": "grammar_point",
            "content": f"Rule: {grammar['rule']}. Example: {grammar.get('example', '')}",
            "metadata": {},
        })

    return chunks


async def embed_chunks(chunks: list[dict]) -> list[dict]:
    if not chunks:
        return chunks

    embedder = get_embedding_provider()
    texts = [c["content"] for c in chunks]
    embeddings = await embedder.embed(texts)

    for chunk, emb in zip(chunks, embeddings):
        chunk["embedding"] = emb

    return chunks
