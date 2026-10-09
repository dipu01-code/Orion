"""A deterministic local model used until a real model adapter is configured."""

from models.base import Model, ModelRequest, ModelResponse


class LocalFallbackModel(Model):
    """Makes the first vertical slice usable without network access or API keys."""

    model_id = "local-fallback-v1"

    async def generate(self, request: ModelRequest) -> ModelResponse:
        return ModelResponse(
            text=(
                "ORION's conversational model is not configured. Set "
                "ORION_MODEL_PROVIDER=openai, OPENAI_API_KEY, and OPENAI_MODEL "
                "to enable conversations. Built-in commands remain available."
            ),
            model_id=self.model_id,
            confidence=0.25,
        )
