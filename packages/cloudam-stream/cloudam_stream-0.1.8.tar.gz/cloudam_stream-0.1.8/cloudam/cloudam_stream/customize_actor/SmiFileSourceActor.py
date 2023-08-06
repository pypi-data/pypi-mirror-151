from core.actors import SourceActor
from core.ports.outputports import TextOutputPort

from core.parameters import FileParameter
from core.constants import config
import pickle


class SmiFileSourceActor(SourceActor):
    title = "Smi File Source Actor"
    # 必填，用来定位ports
    name = "Source"
    success = TextOutputPort()
    input_file = FileParameter()

    def __iter__(self):
        source_file = config.INPUT_FILE_DIRECTORY + self.args.input_file.value
        print("------source file"+source_file)
        with open(source_file) as f:
            while True:
                line = f.readline()
                if not line:
                    break
                yield line
