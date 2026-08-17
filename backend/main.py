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

        if command.lower() in ["sleep", "goodbye", "bye"]:
            print("ORION: Going to sleep.")
            return

        response = brain.respond(command)

        print("ORION:", response)

        while True:

            answer = input(
                "ORION: Can I help you with anything else? "
            ).lower().strip()

            if answer in ["yes", "y", "yeah", "sure", "of course"]:
                print("ORION: Alright. I'm listening.")
                break

            elif answer in ["no", "n", "nope", "that's all", "nothing"]:
                print("ORION: Alright. Going to sleep.")
                return

            else:
                print("ORION: Please say yes or no.")


while True:

    listen_for_wake_word()
    conversation()