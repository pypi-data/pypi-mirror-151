
class Parameter(object):

    def __init__(self, name: str = None, title: str = None, description: str = "", value: object = None):
        self.__name = name
        self.__title = title
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


class FileInputParameter(Parameter):

    def __init__(self, name: str = None, title: str = None, description: str = "", value: str = None):
        super().__init__(name, title, description, value)

    def set_value(self, value: str):
        super(FileInputParameter, self).set_value(value)

    def value(self) -> str:
        return str(super(FileInputParameter, self).get_value())


class FileOutputParameter(Parameter):

    def __init__(self, name: str = None, title: str = None, description: str = "", value: str = None):
        super().__init__(name, title, description, value)

    def set_value(self, value: str):
        super(FileOutputParameter, self).set_value(value)

    def value(self) -> str:
        return str(super(FileOutputParameter, self).get_value())


class OuterFileInputParameter(Parameter):

    def __init__(self, name: str = None, title: str = None, description: str = "", value: str = None):
        super().__init__(name, title, description, value)

    def set_value(self, value: str):
        super(OuterFileInputParameter, self).set_value(value)

    def value(self) -> str:
        return str(super(OuterFileInputParameter, self).get_value())


class OuterFileOutputParameter(Parameter):

    def __init__(self, name: str = None, title: str = None, description: str = "", value: str = None):
        super().__init__(name, title, description, value)

    def set_value(self, value: str):
        super(OuterFileOutputParameter, self).set_value(value)

    def value(self) -> str:
        return str(super(OuterFileOutputParameter, self).get_value())


class StringParameter(Parameter):

    def __init__(self, name: str = None, title: str = None, description: str = "", value: str = None):
        super().__init__(name, title, description, value)

    def set_value(self, value: str):
        super(StringParameter, self).set_value(value)

    def value(self) -> str:
        return str(super(StringParameter, self).get_value())


class IntParameter(Parameter):

    def __init__(self, name: str = None, title: str = None, description: str = "", value: int = None):
        super().__init__(name, title, description, value)

    def set_value(self, value: int):
        super(IntParameter, self).set_value(value)

    def value(self) -> int:
        return int(str(super(IntParameter, self).get_value()))


class ListParameter(Parameter):

    def __init__(self, name: str = None, title: str = None, description: str = "", value: list = None):
        super().__init__(name, title, description, value)

    def set_value(self, value: list):
        super(ListParameter, self).set_value(value)

    def value(self) -> list:
        return super(ListParameter, self).get_value()



