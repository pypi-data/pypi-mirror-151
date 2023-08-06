import asyncio
import typing

from pathlib import Path

from ceplib.loader import Loader


class Cep:
    def __init__(self, *, loader=Loader) -> None:
        self.__loader = loader       
        self.__base_path = Path(__file__)
    
    def get(self, cep: typing.Union[str, int], *, get_all=False):
        cep = self.__apply_transforms(cep)
        tasks: typing.Set[typing.Awaitable] = set()
        loop = asyncio.get_event_loop()
        for service in self.__loader(self.__base_path.parent / "services").load():
            future = loop.run_in_executor(None, service().get, cep)
            tasks.add(future)
        
        async def exec_tasks(tasks=tasks, get_all=get_all):
            ended, working = await asyncio.wait(
                tasks, 
                return_when=asyncio.FIRST_COMPLETED if not get_all\
                     else asyncio.ALL_COMPLETED
            )

            if list(ended)[0].exception():
                if working:
                    return await exec_tasks(working)

                def make_result():
                    def result(self,):
                        return {'response':'Cep não encontrado'}
                    obj = type('Result', (object,), {})
                    obj.result = result
                    return obj()
                return {make_result()}
            return ended

        
        response = list(loop.run_until_complete(exec_tasks()))
        
        if not get_all:
            return response[0].result()

        return [res.result() for res in response]
    
    def __apply_transforms(self, cep: typing.Union[str, int]) -> str:
        for transform in self.__loader(self.__base_path.parent / "transforms").load():
            cep = transform.transform(cep)
        return str(cep)

    def __call__(self, cep, get_all=False):
        return self.get(cep, get_all=get_all)