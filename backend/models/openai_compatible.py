"""OpenAI-compatible chat-completions adapter using only the standard library."""

from __future__ import annotations

import asyncio
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from models.base import Model, ModelRequest, ModelResponse, ToolCall


class ModelProviderError(RuntimeError):
    """Safe provider error suitable for displaying to a user."""


class OpenAICompatibleModel(Model):
    def __init__(self, api_key: str, model: str, base_url: str = "https://api.openai.com/v1", timeout: int = 30):
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required")
        if not model:
            raise ValueError("OPENAI_MODEL is required")
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def generate(self, request: ModelRequest) -> ModelResponse:
        return await asyncio.to_thread(self._generate_sync, request)

    def _generate_sync(self, request: ModelRequest) -> ModelResponse:
        messages = [{"role": "system", "content": request.system_instruction}]
        messages.extend({"role": "user", "content": context} for context in request.context)
        messages.append({"role": "user", "content": request.prompt})
        payload = {"model": self.model, "messages": messages, "temperature": 0.2}
        if request.tools:
            payload["tools"] = list(request.tools)

        http_request = Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(http_request, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            detail = "rate limited" if error.code == 429 else f"provider returned HTTP {error.code}"
            raise ModelProviderError(f"Model request failed: {detail}.") from error
        except (URLError, TimeoutError) as error:
            raise ModelProviderError("Model request failed: network error or timeout.") from error
        except (json.JSONDecodeError, KeyError, IndexError, TypeError) as error:
            raise ModelProviderError("Model request failed: invalid provider response.") from error

        try:
            message = data["choices"][0]["message"]
            calls = tuple(
                ToolCall(
                    name=call["function"]["name"],
                    arguments=json.loads(call["function"].get("arguments") or "{}"),
                    id=call.get("id", ""),
                )
                for call in message.get("tool_calls", [])
            )
            return ModelResponse(
                text=message.get("content") or "",
                model_id=data.get("model", self.model),
                tool_calls=calls,
            )
        except (KeyError, TypeError, json.JSONDecodeError) as error:
            raise ModelProviderError("Model request failed: invalid tool response.") from error
