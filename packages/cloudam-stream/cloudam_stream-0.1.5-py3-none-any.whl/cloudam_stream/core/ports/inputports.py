from cloudam_stream.core.ports.port import Port
from cloudam_stream.core.payload import Record
import json


class InputPort(Port):

    def parse(self, message):
        pass

    # 关联port
    def connect(self, upstream_actor_name, upstream_port_name):
        self.upstream_actor = upstream_actor_name
        self.upstream_port = upstream_port_name
        self.channel = upstream_actor_name.replace(' ', '_') + '&' + upstream_port_name.replace(' ', '_')


class BinaryInputPort(InputPort):

    def parse(self, message) -> bytes:
        return message


class TextInputPort(InputPort):

    def parse(self, message) -> str:
        return str(message)


class FloatInputPort(InputPort):

    def parse(self, message) -> float:
        return float(message)


class JsonInputPort(InputPort):

    def parse(self, message):
        return json.loads(message)


class RecordInputPort(InputPort):

    def parse(self, message) -> Record:
        return Record(message)







