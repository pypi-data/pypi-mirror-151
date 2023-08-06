# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ceplib',
 'ceplib.entities',
 'ceplib.errors',
 'ceplib.interfaces',
 'ceplib.loader',
 'ceplib.services',
 'ceplib.services.awesomeapi',
 'ceplib.services.cepla',
 'ceplib.services.correios',
 'ceplib.services.viacep',
 'ceplib.transforms',
 'ceplib.validations']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0']

setup_kwargs = {
    'name': 'ceplib',
    'version': '0.1.2',
    'description': 'An easy way to fetch Brazil Zip code using several services',
    'long_description': "# CepLib\nUma lib feita em python para consultar cep em diversos serviços\n\n# Instalando a Lib\n```\npip install ceplib\npoetry add ceplib\n```\n\n## Serviços disponíveis\n- AwesomeApi\n- Cep.la\n- Correios\n- ViaCep\n- Widenet\n\n## Como utilizar\nNo mesmo diretório onde está o example.py execute o código abaixo:\n\n```\nfrom ceplib import Cep\n\ncep = Cep()\nprint(cep(21351050))\n```\n\n### Quando o cep é encontrado\n```\n# {'cep': '21351050', 'state': 'RJ', 'city': 'Rio de Janeiro', 'district': 'Madureira', \n# 'address': 'Estrada do Portela - até 279 - lado ímpar', 'provider': 'CorreiosService'}\n```\n### Consultando todos os serviços\n```\nfrom ceplib import Cep\n\ncep = Cep()\nprint(cep(21351050, get_all=True))\n```\n\n```\n#[{'cep': '01513000', 'state': 'SP', 'city': 'São Paulo', 'district': 'Liberdade', 'address': 'Rua São Paulo', \n#'provider': 'CepLaService'}, {'cep': '01513000', #'state': 'SP', 'city': 'São Paulo', 'district': 'Liberdade', \n#'address': 'Rua São Paulo', 'provider': 'AwesomeApiService'}, {'cep': '01513000', 'state': 'SP', #'city': 'São Paulo', \n#'district': 'Liberdade', 'address': 'Rua São Paulo', 'provider': 'ViaCEPService'}, {'cep': '01513000', 'state': 'SP', \n#'city': 'São Paulo', #'district': 'Liberdade', 'address': 'Rua São Paulo', 'provider': 'WideNetService'}, \n#{'cep': '01513000', 'state': 'SP', 'city': 'São Paulo', 'district': #'Liberdade', 'address': 'Rua São Paulo', \n#'provider': 'CorreiosService'}]\n```\n\n### Quando o cep não é encontrado\n```\n# {'response': 'Cep não encontrado'}\n```\n",
    'author': 'Erick Duarte',
    'author_email': 'erickod@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/erickod/CepLib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
