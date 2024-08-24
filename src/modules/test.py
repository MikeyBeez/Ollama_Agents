import textwrap
import shutil

class TextStreamer:
    def __init__(self, width):
        self.width = width
        self.current_line = ""

    def print_word(self, word):
        if len(self.current_line) + len(word) + 1 > self.width:
            print(self.current_line)
            self.current_line = word
        else:
            if self.current_line:
                self.current_line += " "
            self.current_line += word

    def flush(self):
        if self.current_line:
            print(self.current_line)

# Get the width of the window
width = shutil.get_terminal_size().columns

streamer = TextStreamer(width)

words = [
    "Lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
    "Sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et",
    "dolore", "magna", "aliqua", "Ut", "enim", "ad", "minim", "veniam",
    "quis", "nostrud", "exercitation", "ullamco", "laboris", "nisi", "ut",
    "aliquip", "ex", "ea", "commodo", "consequat", "Duis", "aute", "irure",
    "dolor", "in", "reprehenderit", "in", "voluptate", "velit", "esse",
    "cillum", "dolore", "eu", "fugiat", "nulla", "pariatur", "Excepteur",
    "sint", "occaecat", "cupidatat", "non", "proident", "sunt", "in",
    "culpa", "qui", "officia", "deserunt", "mollit", "anim", "id", "est",
    "laborum", "Lorem", "ipsum", "dolor", "sit", "amet", "consectetur",
    "adipiscing", "elit", "Sed", "do", "eiusmod", "tempor", "incididunt",
    "ut", "labore", "et", "dolore", "magna", "aliqua", "Ut", "enim", "ad",
    "minim", "veniam", "quis", "nostrud", "exercitation", "ullamco", "laboris",
    "nisi", "ut", "aliquip", "ex", "ea", "commodo", "consequat", "Duis",
    "aute", "irure", "dolor", "in", "reprehenderit", "in", "voluptate",
    "velit", "esse", "cillum", "dolore", "eu", "fugiat", "nulla", "pariatur",
    "Excepteur", "sint", "occaecat", "cupidatat", "non", "proident", "sunt",
    "in", "culpa", "qui", "officia", "deserunt", "mollit", "anim", "id",
    "est", "laborum", "Lorem", "ipsum", "dolor", "sit", "amet", "consectetur",
    "adipiscing", "elit", "Sed", "do", "eiusmod", "tempor", "incididunt",
    "ut", "labore", "et", "dolore", "magna", "aliqua", "Ut", "enim", "ad",
    "minim", "veniam", "quis", "nostrud", "exercitation", "ullamco", "laboris",
    "nisi", "ut", "aliquip", "ex", "ea", "commodo", "consequat", "Duis",
    "aute", "irure", "dolor", "in", "reprehenderit", "in", "voluptate",
    "velit", "esse", "cillum", "dolore", "eu", "fugiat", "nulla", "pariatur",
    "Excepteur", "sint", "occaecat", "cupidatat", "non", "proident", "sunt",
    "in", "culpa", "qui", "officia", "deserunt", "mollit", "anim", "id",
    "est", "laborum"
]

for word in words:
    streamer.print_word(word)

streamer.flush()
