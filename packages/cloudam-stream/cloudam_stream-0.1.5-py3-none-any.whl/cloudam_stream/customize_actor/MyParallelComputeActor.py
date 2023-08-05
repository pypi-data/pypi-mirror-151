from cloudam_stream.core.actors import ParallelComputeActor
from cloudam_stream.core.ports.outputports import TextOutputPort

from cloudam_stream.core.ports.inputports import TextInputPort


class MyParallelComputeActor(ParallelComputeActor):
    title = "My Parallel Compute Actor"
    name = "Parallel"

    intake = TextInputPort()
    success = TextOutputPort()
    parameter_overrides = {
        "parallelism": 2,
    }

    def process(self, item, port):
        self.success.emit(item)
