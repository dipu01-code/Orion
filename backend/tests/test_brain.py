import unittest

from brain.core import OrionBrain
from models.base import Model, ModelRequest, ModelResponse


class RecordingModel(Model):
    async def generate(self, request: ModelRequest) -> ModelResponse:
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
