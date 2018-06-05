from abc import ABC


class MqClient(ABC):
    def pop(self, parameter_list):
        raise NotImplementedError

    def push(self, parameter_list):
        raise NotImplementedError
