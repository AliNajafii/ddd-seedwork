import copy
from abc import ABCMeta,abstractmethod
from utils.date.base_date_tools import now

class Event(metaclass=ABCMeta):
    """
    The event base class.
    """
    def __init__(self, name, version="1", date=None, sender=None, corr_ids=None):
        date = date if date is not None else now()
        corr_ids = corr_ids if corr_ids is not None else []

        self.name = name
        self.version = version
        self.date = date
        self.sender = sender
        self.corr_ids = corr_ids

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            a = copy.deepcopy(self.__dict__)
            b = copy.deepcopy(other.__dict__)
            a.pop('date')
            b.pop('date')
            return a == b
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @abstractmethod
    def get_serialized_payload(self):
        """
        Get the serialized payload (the event data).
        :rtype: dict
        """
        pass

    def serialize(self):
        obj = {
            'name': self.name,
            'version': self.version,
            'date': self.date.isoformat(),
            'sender': self.sender,
            'payload': self.get_serialized_payload(),
            'corr_ids': self.corr_ids,
        }
        return obj

