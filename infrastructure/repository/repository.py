import abc
from domain.entity import Entity
from domain.aggregate import Aggregate
from domain.value_objects import UUID
from infrastructure.exceptions import InfrastructureException

class Repository(metaclass=abc.ABCMeta):
    """
    Abstract class of repositories.
    note that repositories are made
    that manipulate data without
    concerning implementation and any
    back-end dilemma.
    """

    @abc.abstractmethod
    def persist(self,entity:Entity):
        raise NotImplementedError()

    @abc.abstractmethod
    def persist_aggregate(self,aggregate:Aggregate):
        raise NotImplementedError()


class ReadOnlyRepository(metaclass=abc.ABCMeta):
    """
    Abstract class of read-only repositories.
    As we know the differences between queries and commands
    in application layer. it's a best practice to split
    read and write abstractions
    """

    @abc.abstractmethod
    def get_by_id(self,id:UUID) -> Entity|Aggregate:
        raise NotImplementedError()

    def __getitem__(self, item):
        return self.get_by_id(item)

    def __setitem__(self, key, value):
        raise InfrastructureException('ReadOnlyRepository can not write')


class WriteOnlyRepository(metaclass=abc.ABCMeta):
    """
    Abstract class for write-only repositories.
    As we know the differences between queries and commands
    in application layer. it's a best practice to split
    read and write abstractions
    """

    @abc.abstractmethod
    def remove_by_id(self,id:UUID):
        raise NotImplementedError()

    def create(self,entity:Entity):
        raise  NotImplementedError()

    def update(self,id:UUID,**kwargs):
        raise NotImplementedError()

    def __getitem__(self, item):
        raise InfrastructureException('WriteOnlyRepository can not read')

    def __delitem__(self, key):
        return self.remove_by_id(key)



