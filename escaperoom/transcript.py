class Transcript:

    def __init__(self, filename):
        self.filename = filename

        # Create an empty transcript file
        with open(self.filename, "w", encoding="utf-8") as file:
            pass

    def write(self, text):

        # Print to terminal
        print(text)

        # Write to run.txt
        with open(self.filename, "a", encoding="utf-8") as file:
            file.write(text + "\n")