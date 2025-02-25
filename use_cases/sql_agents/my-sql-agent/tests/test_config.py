"""
Tests for LLM configuration.
"""
import pytest
from src.config.llm_config import (
    LLMConfig, 
    LLMProvider, 
    create_llm,
    OllamaSettings,
    OpenAISettings
)

def test_ollama_config():
    """Test creating Ollama configuration."""
    config = LLMConfig.ollama(model_name="mistral")
    assert config.provider == LLMProvider.OLLAMA
    assert isinstance(config.settings, OllamaSettings)
    assert config.settings.model_name == "mistral"
    assert config.settings.temperature == 0.0

def test_openai_config():
    """Test creating OpenAI configuration."""
    config = LLMConfig.openai(model_name="gpt-4", api_key="test-key")
    assert config.provider == LLMProvider.OPENAI
    assert isinstance(config.settings, OpenAISettings)
    assert config.settings.model_name == "gpt-4"
    assert config.settings.temperature == 0.0
    assert config.settings.api_key == "test-key"

def test_invalid_temperature():
    """Test temperature validation."""
    with pytest.raises(ValueError):
        LLMConfig.ollama(
            model_name="mistral",
            temperature=1.5
        )

def test_create_llm_ollama():
    """Test creating Ollama LLM instance."""
    config = LLMConfig.ollama(model_name="mistral")
    llm = create_llm(config)
    assert llm.model == "mistral"
    assert llm.temperature == 0.0

def test_create_llm_openai_missing_key():
    """Test error when OpenAI key is missing."""
    config = LLMConfig.openai(model_name="gpt-4")
    with pytest.raises(ValueError, match="OpenAI API key is required"):
        create_llm(config)

def test_create_llm_invalid_provider():
    """Test error with invalid provider."""
    with pytest.raises(ValueError):
        LLMConfig(
            provider="invalid",
            settings=OllamaSettings(model_name="test")
        ) 