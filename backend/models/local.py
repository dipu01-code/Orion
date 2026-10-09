"""A deterministic local model used until a real model adapter is configured."""

from models.base import Model, ModelRequest, ModelResponse


class LocalFallbackModel(Model):
    """Makes the first vertical slice usable without network access or API keys."""

    model_id = "local-fallback-v1"

    async def generate(self, request: ModelRequest) -> ModelResponse:
        return ModelResponse(
            text=(
                "I do not have a configured language model for that request yet. "
                "I can currently help with system information, arithmetic, "
                "folders, and launching applications."
            ),
            model_id=self.model_id,
            confidence=0.25,
        )
