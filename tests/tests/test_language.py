# tests/test_language.py

import pytest
from brains.c6_language import LanguageBrain

@pytest.fixture
def language_brain():
    # Nota: Estas pruebas pueden fallar si las APIs no están disponibles o sin clave.
    # Se pueden mockear para pruebas más robustas.
    return LanguageBrain()

def test_detect_spanish(language_brain):
    text = "Hola, cómo estás?"
    translated, detected = language_brain.detect_and_translate_to_english(text)
    assert detected == "es"
    assert "hello" in translated.lower()

def test_detect_english(language_brain):
    text = "Hello, how are you?"
    translated, detected = language_brain.detect_and_translate_to_english(text)
    assert detected == "en"
    assert translated == text # No debería cambiar

def test_translate_to_spanish(language_brain):
    text = "Where is the nearest hospital?"
    translated = language_brain.translate_from_english(text, "es")
    assert "hospital" in translated.lower()
