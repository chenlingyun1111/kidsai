"""Test WebSocket voice session with text messages."""

import asyncio
import json

import websockets


CHILD_ID = "303d5085-9795-4518-bf82-19c53c9b2763"
CHAR_ID = "b2a4a949-0784-49cf-b437-ecc4805296de"
WS_URL = f"ws://localhost:8000/api/v1/voice/session?child_id={CHILD_ID}&character_id={CHAR_ID}"

TEST_MESSAGES = [
    "Hi Spark! My name is Xiaoming!",
    "Can you teach me animal words?",
    "What sound does a cat make?",
]


async def main():
    print(f"Connecting to {WS_URL}\n")

    async with websockets.connect(WS_URL) as ws:
        audio_total = 0

        # Receive greeting
        print("--- Waiting for greeting ---")
        while True:
            msg = await ws.recv()
            if isinstance(msg, bytes):
                audio_total += len(msg)
            else:
                data = json.loads(msg)
                if data["type"] == "ai_text":
                    print(f"🐉 Spark: {data['text']}")
                elif data["type"] == "ai_turn_complete":
                    print(f"   [greeting audio: {audio_total:,} bytes]")
                    audio_total = 0
                    break

        # Send test messages
        for user_msg in TEST_MESSAGES:
            print(f"\n👦 Child: {user_msg}")
            await ws.send(json.dumps({"type": "text_message", "text": user_msg}))

            full_text = ""
            audio_total = 0

            while True:
                msg = await ws.recv()
                if isinstance(msg, bytes):
                    audio_total += len(msg)
                else:
                    data = json.loads(msg)
                    match data["type"]:
                        case "transcript_final":
                            pass
                        case "ai_text_partial":
                            full_text += data["text"]
                        case "ai_turn_complete":
                            final = data.get("text", full_text)
                            print(f"🐉 Spark: {final}")
                            print(f"   [audio: {audio_total:,} bytes]")
                            full_text = ""
                            audio_total = 0
                            break

        # End session
        await ws.send(json.dumps({"type": "session_end"}))
        print("\n--- Session ended ---")


if __name__ == "__main__":
    asyncio.run(main())
