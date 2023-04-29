from infrastructure.services import InfrastructureService
from infrastructure.log_services import LogService

class Adapter(InfrastructureService):
    """
    Adapters are infrastructure interfaces
    that can make inbound and/or outbound data flows
    possible by implementing them.
    """

    def __init__(self,log_service:LogService,config):
        super(Adapter, self).__init__()
        self.config = config
        self.log_service = log_service
        self.service = None

    async def start(self):
        pass

    async def stop(self):
        pass

class 


