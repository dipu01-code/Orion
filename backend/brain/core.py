class OrionBrain:

    def respond(self, command):
        command = command.lower().strip()

        if "hello" in command:
            return "Hello. I am ORION."

        elif "who are you" in command:
            return "I am ORION, your personal AI assistant."

        elif "status" in command:
            return "All systems are operational."

        elif "time" in command:
            return "I can provide the current time once my time tool is connected."

        else:
            return "I don't understand that command yet."