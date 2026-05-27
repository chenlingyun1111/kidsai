"""End-to-end test: DeepSeek character chat + Edge TTS voice synthesis.

Usage: python scripts/test_conversation.py
"""

import asyncio
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.prompt_engine import PromptEngine
from app.ai.llm.deepseek_provider import DeepSeekProvider
from app.ai.tts.edge_tts_provider import EdgeTTSProvider


SPARK_CHARACTER = {
    "name": "Spark",
    "catchphrases": ["Super sparkly!", "Roar-some job!"],
    "world_rules": {
        "character_meta": {
            "name": "Spark",
            "species": "Baby Dragon",
            "age_appearance": "young, same age as the child",
            "world": "Letter Land - a magical kingdom where letters come alive",
        },
        "personality": {
            "traits": ["cheerful", "curious", "slightly clumsy", "encouraging"],
            "interests": ["collecting shiny letters", "singing", "making up silly rhymes"],
        },
        "speaking_style": {
            "vocabulary_level": "simple, age-appropriate for 5-6 year olds",
            "sentence_length": "short, 5-10 words per sentence maximum",
            "tone": "warm, enthusiastic, patient",
            "forbidden_patterns": [
                "Never uses sarcasm",
                "Never says 'wrong' -- uses 'almost!' or 'close!'",
            ],
        },
        "teaching_behavior": {
            "correction_style": "gentle_redirect",
            "singing_enabled": True,
            "game_types": ["rhyming", "word_chain", "story_building"],
        },
        "safety_rules": {
            "never_discuss": ["violence", "scary topics", "adult themes"],
            "redirect_to": "Let's talk about something fun instead!",
        },
        "interaction_rules": [
            "Always wait for the child to respond",
            "Keep each response under 3 sentences unless singing",
            "Naturally incorporate vocabulary: cat, dog, bird, fish, rabbit",
        ],
    },
}

TEST_MESSAGES = [
    "Hello! What's your name?",
    "I like cats! Do you like cats?",
    "Can you sing a song about animals?",
]


async def test_llm(system_prompt: str):
    print("=" * 60)
    print("TEST 1: DeepSeek LLM - Character Chat")
    print("=" * 60)

    llm = DeepSeekProvider()
    messages = []

    for user_msg in TEST_MESSAGES:
        print(f"\n👦 Child: {user_msg}")
        messages.append({"role": "user", "content": user_msg})

        t0 = time.time()
        full_response = ""

        print(f"🐉 Spark: ", end="", flush=True)
        async for token in llm.chat_stream(system_prompt, messages):
            print(token, end="", flush=True)
            full_response += token

        elapsed = time.time() - t0
        print(f"\n   [{elapsed:.1f}s, {len(full_response)} chars]")

        messages.append({"role": "assistant", "content": full_response})

    return messages[-1]["content"]


async def test_tts(text: str):
    print("\n" + "=" * 60)
    print("TEST 2: Edge TTS - Voice Synthesis")
    print("=" * 60)

    tts = EdgeTTSProvider()

    output_dir = "/app/scripts" if os.path.exists("/app/scripts") else os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "test_output.mp3")

    t0 = time.time()
    audio_data = await tts.synthesize(text, "girl")
    elapsed = time.time() - t0

    with open(output_path, "wb") as f:
        f.write(audio_data)

    print(f"\n  Text: \"{text[:80]}...\"" if len(text) > 80 else f"\n  Text: \"{text}\"")
    print(f"  Voice: en-US-AnaNeural (girl)")
    print(f"  Audio size: {len(audio_data):,} bytes")
    print(f"  Time: {elapsed:.1f}s")
    print(f"  Saved to: {output_path}")


async def test_streaming_tts(text: str):
    print("\n" + "=" * 60)
    print("TEST 3: Edge TTS - Streaming Synthesis")
    print("=" * 60)

    tts = EdgeTTSProvider()

    t0 = time.time()
    chunk_count = 0
    total_bytes = 0

    async for chunk in tts.synthesize_stream(text, "girl"):
        chunk_count += 1
        total_bytes += len(chunk)
        if chunk_count == 1:
            first_chunk_time = time.time() - t0
            print(f"\n  First audio chunk received in {first_chunk_time:.2f}s")

    elapsed = time.time() - t0
    print(f"  Total chunks: {chunk_count}")
    print(f"  Total audio: {total_bytes:,} bytes")
    print(f"  Total time: {elapsed:.1f}s")


async def main():
    print("\nKidsAI End-to-End Conversation Test")
    print("DeepSeek + Edge TTS Pipeline\n")

    # Build system prompt
    engine = PromptEngine()
    system_prompt = engine.build_system_prompt(
        SPARK_CHARACTER,
        courseware_context="Unit 3: Animals. Vocabulary: cat, dog, bird, fish, rabbit. "
                          "Song: Old MacDonald had a farm.",
        learning_state="Child has practiced: cat (mastery 3/4), dog (mastery 2/4). "
                       "Needs practice: bird, fish, rabbit.",
    )

    print("System Prompt Preview:")
    print("-" * 40)
    print(system_prompt[:500] + "...\n")

    # Test LLM
    last_response = await test_llm(system_prompt)

    # Test TTS
    await test_tts(last_response)

    # Test streaming TTS
    await test_streaming_tts(last_response)

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
