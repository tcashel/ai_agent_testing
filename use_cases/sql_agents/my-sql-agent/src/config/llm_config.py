"""
Configuration for Language Model providers and settings.
"""
from enum import Enum
from typing import Optional, Dict, Any, Union
from pathlib import Path
import os
import tomli
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMProvider(str, Enum):
    """Supported LLM providers."""
    OLLAMA = "ollama"
    OPENAI = "openai"

class ModelSettings(BaseModel):
    """Base settings for language models."""
    model_name: str
    temperature: float = Field(default=0.0, ge=0.0, le=1.0)
    additional_kwargs: Dict[str, Any] = Field(default_factory=dict)

class OllamaSettings(ModelSettings):
    """Ollama-specific settings."""
    pass

class OpenAISettings(ModelSettings):
    """OpenAI-specific settings."""
    api_key: Optional[str] = None

class LLMConfig(BaseModel):
    """Configuration for Language Model settings."""
    provider: LLMProvider
    settings: Union[OllamaSettings, OpenAISettings]

    @classmethod
    def ollama(cls, model_name: str = "mistral", temperature: float = 0.0) -> "LLMConfig":
        """Create Ollama configuration."""
        return cls(
            provider=LLMProvider.OLLAMA,
            settings=OllamaSettings(
                model_name=model_name,
                temperature=temperature
            )
        )
    
    @classmethod
    def openai(cls, 
               model_name: str = "gpt-4", 
               temperature: float = 0.0,
               api_key: Optional[str] = None) -> "LLMConfig":
        """Create OpenAI configuration."""
        return cls(
            provider=LLMProvider.OPENAI,
            settings=OpenAISettings(
                model_name=model_name,
                temperature=temperature,
                api_key=api_key
            )
        )

    @classmethod
    def from_env(cls) -> "LLMConfig":
        """Create configuration from environment and config files.
        
        Returns:
            LLMConfig: The configured LLM settings
            
        Raises:
            ValueError: If required settings are missing
        """
        # Load config.toml
        config_path = Path("config.toml")
        if not config_path.exists():
            raise FileNotFoundError("config.toml not found")
            
        with open(config_path, "rb") as f:
            config = tomli.load(f)
            
        # Get provider from environment or config
        provider = os.getenv("LLM_PROVIDER", config["llm"]["default_provider"])
        
        if provider == LLMProvider.OPENAI.value:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is required for OpenAI")
                
            return cls.openai(
                model_name=config["llm"]["openai"]["model_name"],
                temperature=config["llm"]["openai"]["temperature"],
                api_key=api_key
            )
            
        elif provider == LLMProvider.OLLAMA.value:
            return cls.ollama(
                model_name=config["llm"]["ollama"]["model_name"],
                temperature=config["llm"]["ollama"]["temperature"]
            )
            
        raise ValueError(f"Unsupported LLM provider: {provider}")

def create_llm(config: LLMConfig):
    """Create a LangChain LLM instance based on configuration.
    
    Args:
        config: LLM configuration
        
    Returns:
        A LangChain LLM instance
    
    Raises:
        ValueError: If provider is not supported
    """
    if config.provider == LLMProvider.OLLAMA:
        from langchain_ollama import OllamaLLM
        return OllamaLLM(
            model=config.settings.model_name,
            temperature=config.settings.temperature,
            **config.settings.additional_kwargs
        )
    
    elif config.provider == LLMProvider.OPENAI:
        from langchain_openai import ChatOpenAI
        settings = config.settings
        if not isinstance(settings, OpenAISettings) or not settings.api_key:
            raise ValueError("OpenAI API key is required")
            
        return ChatOpenAI(
            model_name=settings.model_name,
            temperature=settings.temperature,
            openai_api_key=settings.api_key,
            **settings.additional_kwargs
        )
    
    raise ValueError(f"Unsupported LLM provider: {config.provider}") 