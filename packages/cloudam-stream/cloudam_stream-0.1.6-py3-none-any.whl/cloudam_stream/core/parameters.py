class Parameter(object):

    def __init__(self, name: str = None, description: str = "", value: object = None):
        self.__name = name
        self.__description = description
        self.__value = value

    def set_name(self, name: str):
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def set_description(self, description: str = ""):
        self.__description = description

    def get_description(self) -> str:
        return self.__description

    def set_value(self, value: object):
        self.__value = value

    def get_value(self) -> object:
        return self.__value

    def serialize(self):
        pass

    def deserialize(self):
        pass


class FileParameter(Parameter):

    def __init__(self, name: str = None, description: str = "", value: str = None):
        super().__init__(name, description, value)

    def set_value(self, value: str):
        super(FileParameter, self).set_value(value)

    def get_value(self) -> str:
        return str(super(FileParameter, self).get_value())


class StringParameter(Parameter):

    def __init__(self, name: str = None, description: str = "", value: str = None):
        super().__init__(name, description, value)

    def set_value(self, value: str):
        super(StringParameter, self).set_value(value)

    def get_value(self) -> str:
        return str(super(StringParameter, self).get_value())


class IntegerParameter(Parameter):

    def __init__(self, name: str = None, description: str = "", value: int = None):
        super().__init__(name, description, value)

    def set_value(self, value: int):
        super(IntegerParameter, self).set_value(value)

    def get_value(self) -> int:
        return int(str(super(IntegerParameter, self).get_value()))

