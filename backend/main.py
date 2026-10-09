from brain.core import OrionBrain
from config.settings import Settings
from memory import SQLiteMemoryStore
from models.router import ModelRouter


settings = Settings.from_environment()
brain = OrionBrain(
    memory=SQLiteMemoryStore(settings.database_path),
    model_router=ModelRouter.from_settings(settings),
    system_instruction=settings.system_instruction,
)


def listen_for_wake_word():

    while True:

        word = input("ORION sleeping... ")

        if word.lower().strip() == "orion":
            return


def conversation():

    print("ORION: Yes. How can I help you?")

    while True:

        command = input("You: ").strip()

        # Put ORION to sleep
        if command.lower() in ["sleep", "goodbye", "bye", "no", "nothing"]:
            print("ORION: Alright. Going to sleep.")
            return

        # Ignore empty input
        if not command:
            continue

        # Process command
        response = brain.respond(command)

        print("ORION:", response)

        # Ask for another request
        print("ORION: Can I help you with anything else?")


while True:

    listen_for_wake_word()
    conversation()
