from cloudam_stream.core.ports.port import Port
from cloudam_stream.core.payload import Message, Record
from cloudam_stream.core.streams import RedisProducer
import json


class OutputPort(Port):
    def __init__(self, producer: RedisProducer = None, name=None, actor_name=None):
        if name and actor_name:
            self.channel = actor_name.replace(' ', '_') + '&' + name.replace(' ', '_')
        self.producer = producer
        super().__init__(name, actor_name)

    def encode(self, data):
        pass

    def emit(self, data):
        pass

    def _emit(self, payload: object):
        message_object = Message(payload, "0", type(self).__name__)
        # 转二进制
        msg = message_object.serialize()
        stream_name = self.channel
        self.producer.produce(stream_name, msg)


class TextOutputPort(OutputPort):

    def emit(self, data: str):
        super(TextOutputPort, self)._emit(data)


class BinaryOutputPort(OutputPort):

    def emit(self, data: bytes):
        super(BinaryOutputPort, self)._emit(data)


class IntOutputPort(OutputPort):

    def emit(self, data: int):
        super(IntOutputPort, self)._emit(data)


class FloatOutputPort(OutputPort):

    def emit(self, data: float):
        super(FloatOutputPort, self)._emit(data)


class JsonOutputPort(OutputPort):

    def emit(self, data: json):
        super(JsonOutputPort, self)._emit(data)


class RecordOutputPort(OutputPort):

    def emit(self, data: Record):
        super(RecordOutputPort, self)._emit(data)

