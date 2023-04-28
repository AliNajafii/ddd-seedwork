
class DomainException(Exception):
    """
       A domain exception.
       """

    def __init__(self, errors):
        super(DomainException, self).__init__()
        self.errors = errors

    def __str__(self):
        return ",".join([e['message'] for e in self.errors])


class BusinessRuleValidationException(DomainException):
    def __init__(self, rule):
        self.rule = rule

    def __str__(self):
        return str(self.rule)


class EntityNotFoundException(Exception):
    def __init__(self, entity_id, repository):
        message = f"Entity {entity_id} not found"
        super().__init__(message)
        self.repository = repository
        self.entity_id = entity_id