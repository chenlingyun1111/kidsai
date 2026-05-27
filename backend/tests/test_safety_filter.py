from app.services.safety_filter import is_safe, sanitize_output


def test_safe_text():
    assert is_safe("I like cats and dogs") is True
    assert is_safe("Let's learn about animals") is True


def test_unsafe_text():
    assert is_safe("I want to kill the monster") is False


def test_sanitize_safe_text():
    text = "Great job! You said 'cat' perfectly!"
    assert sanitize_output(text) == text


def test_sanitize_unsafe_text():
    text = "Let me tell you about weapons"
    result = sanitize_output(text)
    assert result == "Let's talk about something fun instead!"
