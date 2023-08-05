from cloudam_stream.core.actors import SinkActor
from cloudam_stream.core.constants import config

from cloudam_stream.core.ports.inputports import TextInputPort


class MySinkActor(SinkActor):
    title = "My sink actor"
    name = "Sink"
    intake = TextInputPort()

    def begin(self):
        print("------start sink actor")
        self.file = open(config.INPUT_FILE_DIRECTORY + "result.txt", "w+")

    def write(self, item, port):
        print("------running sink actor")
        self.file.write(item)

    def end(self):
        print("------stop sink actor")
        self.file.close()
