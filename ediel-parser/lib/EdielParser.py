from pydifact.message import Message

class EdielParser():
    def __init__(self, segments):
        self.msg = Message.from_str(segments)

    def parse(self):
        for s in self.msg.segments:
            print(s, end='\n\n')

