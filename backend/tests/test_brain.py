import unittest

from brain.core import OrionBrain
from models.base import Model, ModelRequest, ModelResponse, ToolCall


class RecordingModel(Model):
    def __init__(self):
        self.requests = []

    async def generate(self, request: ModelRequest) -> ModelResponse:
        self.requests.append(request)
        return ModelResponse(text=f"model: {request.prompt}", model_id="test-model")


class OrionBrainTests(unittest.IsolatedAsyncioTestCase):
    async def test_unknown_input_reaches_model_through_contract(self):
        response = await OrionBrain(model=RecordingModel()).process("Explain quantum memory")
        self.assertEqual(response, "model: Explain quantum memory")

    async def test_calculation_uses_a_tool_and_returns_its_observation(self):
        response = await OrionBrain().process("calculate 6 * 7")
        self.assertEqual(response, "The answer is 42.")

    async def test_input_and_response_are_recorded_in_working_memory(self):
        brain = OrionBrain(model=RecordingModel())
        await brain.process("Remember this exchange")
        records = brain.memory.search("exchange")
        self.assertEqual(
            {record.content for record in records},
            {"Remember this exchange", "model: Remember this exchange"},
        )

    async def test_second_turn_receives_relevant_prior_context(self):
        model = RecordingModel()
        brain = OrionBrain(model=model)
        await brain.process("My project is named Atlas")
        await brain.process("What is my project named?")
        self.assertIn("My project is named Atlas", model.requests[1].context)

    async def test_model_tool_call_is_observed_before_final_response(self):
        class CalculatorModel(Model):
            def __init__(self):
                self.calls = 0

            async def generate(self, request):
                self.calls += 1
                if self.calls == 1:
                    return ModelResponse("", "test", tool_calls=(ToolCall("calculate", {"expression": "2 + 2"}),))
                return ModelResponse("The observed result is 4.", "test")

        response = await OrionBrain(model=CalculatorModel()).process("Please work this out")
        self.assertEqual(response, "The observed result is 4.")

    async def test_unconfigured_model_returns_configuration_guidance(self):
        response = await OrionBrain().process("Tell me a joke")
        self.assertIn("OPENAI_API_KEY", response)

    async def test_model_requested_caution_tool_requires_approval(self):
        class ApprovalModel(Model):
            def __init__(self):
                self.observation_prompt = ""
                self.calls = 0

            async def generate(self, request):
                self.calls += 1
                if self.calls == 1:
                    return ModelResponse("", "test", tool_calls=(ToolCall("create_folder", {"folder_name": "unsafe"}),))
                self.observation_prompt = request.prompt
                return ModelResponse("I need your approval before creating that folder.", "test")

        model = ApprovalModel()
        response = await OrionBrain(model=model).process("Create a folder")
        self.assertIn("approval", response.lower())
        self.assertIn("Approval is required", model.observation_prompt)
