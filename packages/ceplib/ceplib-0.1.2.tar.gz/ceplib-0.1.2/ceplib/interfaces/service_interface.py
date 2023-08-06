from abc import ABC, abstractmethod
from ceplib.entities import Cep

class ServiceInterface(ABC):
    
    @abstractmethod
    def get(self, cep:str) -> Cep:
        raise NotImplementedError