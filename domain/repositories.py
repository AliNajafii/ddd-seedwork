import abc
from .entity import Entity
from .value_objects import UUID

class GenericRepository(metaclass=abc.ABCMeta):
    """
    An interface for a generic repository
    """

    @abc.abstractmethod
    def add(self, entity: Entity):
        raise NotImplementedError()

    @abc.abstractmethod
    def remove(self, entity: Entity):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_id(id: UUID) -> Entity:
        raise NotImplementedError()

    def __getitem__(self, index) -> Entity:
        return self.get_by_id(index)

    @staticmethod
    def next_id() -> UUID:
        return UUID.v4()

class GenericListRepository(metaclass=abc.ABCMeta):
    """
    An Interface for managing list of entities repository
    """

    @abc.abstractmethod
    def get_by_ids(self,ids:list[UUID]) -> list[Entity]:
        raise NotImplementedError()

    @abc.abstractmethod
    def add(self, entities: list[Entity]):
        raise NotImplementedError()

    @abc.abstractmethod
    def remove(self,entities:list[Entity]):
        raise NotImplementedError()

    @staticmethod
    def next_id() -> UUID:
        return UUID.v4()


class AsyncGenericRepository(metaclass=abc.ABCMeta):
    """
    An interface for a generic repository with async manner
    """

    @abc.abstractmethod
    async def add(self, entity: Entity):
        raise NotImplementedError()

    @abc.abstractmethod
    async def remove(self, entity: Entity):
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_by_id(id: UUID) -> Entity:
        raise NotImplementedError()

    def __getitem__(self, index) -> Entity:
        return self.get_by_id(index)

    @staticmethod
    def next_id() -> UUID:
        return UUID.v4()

class AsyncGenericListRepository(metaclass=abc.ABCMeta):
    """
    An Interface for managing list
    of entities repository with async manner
    """

    @abc.abstractmethod
    async def get_by_ids(self,ids:list[UUID]) -> list[Entity]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def add(self, entities: list[Entity]):
        raise NotImplementedError()

    @abc.abstractmethod
    async def remove(self,entities:list[Entity]):
        raise NotImplementedError()

    @staticmethod
    def next_id() -> UUID:
        return UUID.v4()