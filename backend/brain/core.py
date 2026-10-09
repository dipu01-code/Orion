from brain.parser import parse_command
from brain.router import route_intent
from memory import InMemoryStore, MemoryRecord, MemoryStore
from models import LocalFallbackModel, Model, ModelProviderError
from models.router import ModelRouter
from tools.registry import TOOLS, model_tool_definitions, run_tool


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
        system_instruction: str = "You are ORION, a helpful and safety-conscious desktop assistant.",
        max_agent_iterations: int = 3,
    ):
        self.model_router = model_router or ModelRouter(model or LocalFallbackModel())
        self.memory = memory or InMemoryStore()
        self.system_instruction = system_instruction
        self.max_agent_iterations = max_agent_iterations

    async def process(self, user_input: str) -> str:
        """Process one request through the initial observable cognitive loop."""
        command = user_input.strip()
        if not command:
            return "Please tell me what you would like help with."

        relevant_memory = self.memory.search(command)
        self.memory.write(MemoryRecord(content=command, kind="working", source="user"))

        response = self._handle_builtin(command) or await self._run_agent(command, relevant_memory)

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
    def _model_request(command, memories, *, tools=(), system_instruction=""):
        from models import ModelRequest

        return ModelRequest(
            prompt=command,
            context=tuple(record.content for record in memories),
            metadata={"task_type": "general"},
            tools=tools,
            system_instruction=system_instruction or "You are ORION.",
        )

    async def _run_agent(self, command, relevant_memory):
        """Bounded observe-and-respond loop for model-selected registered tools."""
        model = self.model_router.select(task_type="general")
        try:
            response = await model.generate(self._model_request(
                command, relevant_memory, tools=model_tool_definitions(),
                system_instruction=self.system_instruction,
            ))
        except ModelProviderError as error:
            return str(error)
        except Exception:
            return "ORION could not reach the configured model safely. Please try again."

        for _ in range(self.max_agent_iterations):
            if not response.tool_calls:
                return response.text or "The model returned no response."
            observations = [self._execute_requested_tool(call.name, call.arguments) for call in response.tool_calls]
            try:
                response = await model.generate(self._model_request(
                    "Use these observed tool results to answer the user's request: " + repr(observations),
                    relevant_memory, system_instruction=self.system_instruction,
                ))
            except ModelProviderError as error:
                return f"Tool observations: {observations}\n{error}"
        return "ORION stopped this task after reaching its safe action limit."

    @staticmethod
    def _execute_requested_tool(tool_name, arguments):
        tool = TOOLS.get(tool_name)
        if tool is None:
            return {"success": False, "message": f"The requested tool is not registered: {tool_name}."}
        if tool["safety"] != "safe":
            return {
                "success": False,
                "approval_required": True,
                "message": f"Approval is required before ORION can run {tool_name}.",
            }
        try:
            result = run_tool(tool_name, **dict(arguments))
            return result if isinstance(result, dict) else {"success": True, "result": result}
        except (TypeError, ValueError, OSError) as error:
            return {"success": False, "message": f"Tool {tool_name} failed: {error}"}
