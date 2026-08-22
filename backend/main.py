from brain.core import OrionBrain


brain = OrionBrain()


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