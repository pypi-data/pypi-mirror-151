from core.actors import ParallelComputeActor
from core.ports.inputports import TextInputPort
from core.ports.outputports import TextOutputPort


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
