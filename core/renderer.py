from abc import abstractmethod, ABC


class Renderer(ABC):

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass
