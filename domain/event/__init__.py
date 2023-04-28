import copy
from abc import ABCMeta


class Event(metaclass=ABCMeta):
    """
    Base class for events
    """

    def __init__(self, name, version="1", date=None, sender=None, corr_ids=None):
        date = date if date is not None else arrow.utcnow()
        corr_ids = corr_ids if corr_ids is not None else []

        self.name = name
        self.version = version
        self.date = date
        self.sender = sender
        self.corr_ids = corr_ids