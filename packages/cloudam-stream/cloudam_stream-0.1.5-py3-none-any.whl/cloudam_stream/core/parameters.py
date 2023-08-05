class Parameter(object):

    def __init__(self, name=None, value=None):
        self.value = value
        self.name = name

    def serialize(self):
        pass

    def deserialize(self):
        pass


class FileParameter(Parameter):
    pass


class StringParameter(Parameter):
    pass


class IntegerParameter(Parameter):
    pass
