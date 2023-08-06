from ceplib.errors import CepLengthError
from ceplib.interfaces import ValidationInterface


class CepLengthValidation(ValidationInterface):
    '''
    Throw an error if len != 8
    '''
    loader_flag = True
    
    @classmethod
    def validate(cls, cep_model):
        if not len(cep_model) == 8:
            raise CepLengthError