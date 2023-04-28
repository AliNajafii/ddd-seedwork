from pydantic import BaseModel

class BusinessRule(BaseModel):
    """This is a base class for implementing domain rules"""

    # for showing when a rule is broken
    _message:str = ""

    def get_message(self) -> str:
        return self._message

    def is_broken(self) -> bool:
        pass

    def __str__(self):
        return f"{self.__class__.__name__} {super().__str__()}"