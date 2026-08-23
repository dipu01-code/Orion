from brain.parser import parse_command
from brain.router import route_intent


class OrionBrain:

    def respond(self, command):
        original_command = command.strip()
        lowered_command = original_command.lower()

        if "hello" in lowered_command:
            return "Hello. I am ORION."

        elif "who are you" in lowered_command:
            return "I am ORION, your personal AI assistant."

        elif "status" in lowered_command:
            return "All systems are operational."

        elif "system information" in lowered_command or "system info" in lowered_command:
            return route_intent({"intent": "system_info"})

        else:
            return route_intent(parse_command(original_command))
