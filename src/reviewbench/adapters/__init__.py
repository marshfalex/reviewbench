from reviewbench.adapters.anthropic import AnthropicReviewer
from reviewbench.adapters.base import Finding, Reviewer, ReviewResult
from reviewbench.adapters.openai_compat import GroqReviewer, OllamaReviewer
from reviewbench.adapters.replay import ReplayReviewer

ADAPTERS: dict[str, type[Reviewer]] = {
    "groq": GroqReviewer,
    "anthropic": AnthropicReviewer,
    "ollama": OllamaReviewer,
    "replay": ReplayReviewer,
}


def get_adapter(provider: str, model: str | None = None) -> Reviewer:
    if provider not in ADAPTERS:
        raise ValueError(f"unknown provider {provider!r}; use one of {sorted(ADAPTERS)}")
    return ADAPTERS[provider](model)


__all__ = ["ADAPTERS", "Finding", "Reviewer", "ReviewResult", "get_adapter"]
