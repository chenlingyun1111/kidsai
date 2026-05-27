from app.services.prompt_engine import PromptEngine


def test_build_system_prompt_includes_character_name(sample_character):
    engine = PromptEngine()
    prompt = engine.build_system_prompt(sample_character)
    assert "Spark" in prompt
    assert "Baby Dragon" in prompt
    assert "Letter Land" in prompt


def test_build_system_prompt_includes_safety_rules(sample_character):
    engine = PromptEngine()
    prompt = engine.build_system_prompt(sample_character)
    assert "violence" in prompt
    assert "Let's talk about something fun" in prompt


def test_build_system_prompt_includes_teaching_behavior(sample_character):
    engine = PromptEngine()
    prompt = engine.build_system_prompt(sample_character)
    assert "gentle_redirect" in prompt
    assert "rhyming" in prompt


def test_build_system_prompt_with_courseware_context(sample_character):
    engine = PromptEngine()
    prompt = engine.build_system_prompt(
        sample_character,
        courseware_context="Unit 3: Animals - cat, dog, bird",
    )
    assert "Unit 3: Animals" in prompt
    assert "cat, dog, bird" in prompt


def test_build_system_prompt_with_learning_state(sample_character):
    engine = PromptEngine()
    prompt = engine.build_system_prompt(
        sample_character,
        learning_state="Child has mastered: cat, dog. Needs practice: bird, fish.",
    )
    assert "mastered: cat, dog" in prompt
    assert "Needs practice" in prompt
