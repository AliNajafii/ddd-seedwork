from pydantic.dataclasses import dataclass
import uuid
UUID = uuid.UUID
UUID.v4 = uuid.uuid4

@dataclass
class ValueObject:
    """
        Represents Value Objects in the domain
        Value objects are NOT self-descriptive
        Entities like money , datetime or ...
    """
