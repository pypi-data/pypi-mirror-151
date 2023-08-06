from abc import ABC, abstractmethod

from tonclient.types import ParamsOfQueryCollection, ResultOfQueryCollection

from tvmbase.client import Client


class BaseTvm(ABC):

    def __init__(self, idx: str):
        self.idx = idx

    @classmethod
    async def from_idx(cls, client: Client, idx: str) -> 'BaseTvm':
        query = cls.gql_query(idx)
        result = await client.net.query_collection(params=query)
        return await cls.from_query_result(client, idx, result)

    @staticmethod
    @abstractmethod
    def gql_query(idx: str) -> ParamsOfQueryCollection:
        pass

    @classmethod
    async def from_query_result(cls, client: Client, idx: str, result: ResultOfQueryCollection) -> 'BaseTvm':
        boc = result.result[0]['boc']
        return await cls.from_boc(client, boc)

    @classmethod
    @abstractmethod
    async def from_boc(cls, client: Client, boc: str, **kwargs) -> 'BaseTvm':
        pass

    def __str__(self) -> str:
        return f'{self.__class__.__name__}<{self.idx}>'

    __repr__ = __str__
