from typing import Any


class PromptEngine:
    """Assembles the system prompt from character world rules, courseware context,
    learning state, and parent overrides."""

    def build_system_prompt(
        self,
        character: dict[str, Any],
        courseware_context: str = "",
        learning_state: str = "",
        parent_overrides: str = "",
    ) -> str:
        world_rules = character.get("world_rules", {})
        meta = world_rules.get("character_meta", {})
        personality = world_rules.get("personality", {})
        style = world_rules.get("speaking_style", {})
        teaching = world_rules.get("teaching_behavior", {})
        safety = world_rules.get("safety_rules", {})
        interaction = world_rules.get("interaction_rules", [])

        sections = []

        sections.append(
            f"You are {meta.get('name', character['name'])}, "
            f"a {meta.get('species', 'character')} from {meta.get('world', 'a magical world')}. "
            f"You are having a voice conversation with a young child who is learning English."
        )

        if personality:
            traits = ", ".join(personality.get("traits", []))
            sections.append(f"\n[CHARACTER PERSONALITY]\nYour traits: {traits}.")
            catchphrases = character.get("catchphrases", [])
            if catchphrases:
                sections.append(f"Your catchphrases: {', '.join(f'"{c}"' for c in catchphrases)}.")

        if style:
            parts = []
            if style.get("vocabulary_level"):
                parts.append(f"Vocabulary level: {style['vocabulary_level']}.")
            if style.get("sentence_length"):
                parts.append(f"Sentence length: {style['sentence_length']}.")
            if style.get("tone"):
                parts.append(f"Tone: {style['tone']}.")
            forbidden = style.get("forbidden_patterns", [])
            if forbidden:
                parts.append("NEVER: " + "; ".join(forbidden) + ".")
            sections.append("\n[SPEAKING STYLE]\n" + " ".join(parts))

        if courseware_context:
            sections.append(f"\n[CURRENT LESSON CONTEXT]\n{courseware_context}")

        if learning_state:
            sections.append(f"\n[LEARNING STATE]\n{learning_state}")

        if parent_overrides:
            sections.append(f"\n[PARENT NOTES]\n{parent_overrides}")

        if teaching:
            parts = []
            if teaching.get("correction_style"):
                parts.append(f"Correction style: {teaching['correction_style']}.")
            if teaching.get("game_types"):
                parts.append(f"You can play: {', '.join(teaching['game_types'])}.")
            if teaching.get("singing_enabled"):
                parts.append("You can sing songs with the child.")
            sections.append("\n[TEACHING BEHAVIOR]\n" + " ".join(parts))

        if safety:
            never = safety.get("never_discuss", [])
            if never:
                sections.append(f"\n[SAFETY]\nNever discuss: {', '.join(never)}.")
            if safety.get("redirect_to"):
                sections.append(f"If asked about unsafe topics, say: \"{safety['redirect_to']}\"")

        if interaction:
            sections.append("\n[INTERACTION RULES]\n" + "\n".join(f"- {r}" for r in interaction))

        sections.append(
            "\n[RESPONSE FORMAT]\n"
            "- Respond in 1-3 short sentences unless singing.\n"
            "- Plain text only, no emojis, no markdown.\n"
            "- Stay in character at all times."
        )

        return "\n".join(sections)
