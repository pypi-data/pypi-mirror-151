
class Args(object):
    pass


class Actor(object):

    def __init__(self, name=None, actor_id: str = None):
        self.__name = name
        self.__id = actor_id
        self.__output_ports = []
        self.__input_ports = []
        self.__parameters = {}
        self.__parameter_overrides = {}
        self.args = Args()
        self.__global_parameter = dict

    def begin(self):
        pass

    def end(self):
        pass

    def emit(self, data):
        for port in self.__output_ports:
            port.emit(data)

    def set_input_ports(self, input_ports: []):
        self.__input_ports = input_ports

    def set_output_ports(self, output_ports: []):
        self.__output_ports = output_ports

    def set_parameters(self, parameters: {}):
        self.__parameters = parameters

    def get_parameters(self):
        return self.__parameters

    def set_parameter_overrides(self, parameter_overrides: {}):
        self.__parameter_overrides = parameter_overrides

    def get_parameter_overrides(self):
        return self.__parameter_overrides

    def set_global_parameter(self, key: str, val: object):
        self.__global_parameter.update({key: val})

    def get_global_parameter(self, key: str):
        return self.__global_parameter.get(key)


class ComputeActor(Actor):

    def process(self, item: float, port=None):
        pass


class ParallelComputeActor(ComputeActor):

    def process(self, item, port=None):
        pass


class SinkActor(Actor):

    def write(self, data, port):
        pass


class SourceActor(Actor):

    def __iter__(self):
        pass

