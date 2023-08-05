
class Actor(object):

    def __init__(self, name=None, id=None):
        self.name = name
        self.id = id

    def begin(self):
        pass

    def end(self):
        pass

    def emit(self, data):
        for port in self.output_ports:
            port.emit(data)

    def input_ports(self):
        return self.input_ports

    def output_ports(self):
        return self.output_ports

    def parameters(self):
        return self.parameters

    def parameter_overrides(self):
        return self.parameter_overrides


class Args(object):
    pass


class ComputeActor(Actor):

    def process(self, item: float, port=None):
        pass


class ParallelComputeActor(ComputeActor):

    def process(self, item, port=None):
        pass

    def emit(self, data):
        for port_name, port in self.output_ports.items():
            port.emit(data)


class SinkActor(Actor):

    def write(self, data, port):
        pass


class SourceActor(Actor):

    def __iter__(self):
        pass

