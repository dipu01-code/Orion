from brain.parser import parse_command
from brain.router import route_intent
from memory import InMemoryStore, MemoryRecord, MemoryStore
from models import LocalFallbackModel, Model
from models.router import ModelRouter


class OrionBrain:
    """Central coordinator for input, memory, tools, and model responses.

    Provider code belongs behind ``Model``.  This class only knows the model
    contract, making it safe to replace the local fallback with a real adapter.
    """

    def __init__(
        self,
        model: Model | None = None,
        memory: MemoryStore | None = None,
        model_router: ModelRouter | None = None,
    ):
        self.model_router = model_router or ModelRouter(model or LocalFallbackModel())
        self.memory = memory or InMemoryStore()

    async def process(self, user_input: str) -> str:
        """Process one request through the initial observable cognitive loop."""
        command = user_input.strip()
        if not command:
            return "Please tell me what you would like help with."

        relevant_memory = self.memory.search(command)
        self.memory.write(MemoryRecord(content=command, kind="working", source="user"))

        response = self._handle_builtin(command)
        if response is None:
            model = self.model_router.select(task_type="general")
            model_response = await model.generate(
                request=self._model_request(command, relevant_memory)
            )
            response = model_response.text

        self.memory.write(MemoryRecord(content=response, kind="working", source="orion"))
        return response

    def respond(self, command):
        """Synchronous compatibility API for the existing command-line client."""
        import asyncio

        return asyncio.run(self.process(command))

    def _handle_builtin(self, command):
        original_command = command.strip()
        lowered_command = original_command.lower()

        if "hello" in lowered_command:
            return "Hello. I am ORION."

        if "who are you" in lowered_command:
            return "I am ORION, your personal AI assistant."

        if "status" in lowered_command:
            return "All systems are operational."

        if "system information" in lowered_command or "system info" in lowered_command:
            return route_intent({"intent": "system_info"})

        intent = parse_command(original_command)
        if intent["intent"] != "unknown":
            return route_intent(intent)
        return None

    @staticmethod
    def _model_request(command, memories):
        from models import ModelRequest

        return ModelRequest(
            prompt=command,
            context=tuple(record.content for record in memories),
            metadata={"task_type": "general"},
        )
