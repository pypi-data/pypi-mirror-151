import contextlib
import json
import re
import httpx

from ceplib.interfaces import ServiceInterface
from ceplib.entities import Cep
from ceplib.services.awesomeapi.awesomeapi_config import config


class AwesomeApiService(ServiceInterface):
    __config = config
    __cep_model = Cep
    loader_flag = True
    
    @classmethod
    def get(cls, cep:str) -> Cep:
        model:Cep = cls.__cep_model(cep)
        url = f"{cls.__config['URL']}/{model.number}"
        response = httpx.get(url).json()
        return  cls.__fit_to_cep_model(response, model)
    
    @classmethod
    def __fit_to_cep_model(cls, response, cep) -> Cep:
        with contextlib.suppress(KeyError):
            cep['state'] = response['state']
            cep['city'] = response['city']
            cep['address'] = response['address']
            cep['district'] = response['district']
            cep['provider'] = cls.__name__
            return cep
        return response