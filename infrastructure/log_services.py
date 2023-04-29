from .services import InfrastructureService
from pydantic.dataclasses import dataclass
import logging
import copy
import sys
from enum import Enum

class LoggingTypes(Enum):
    API_BASED = 0
    FILE_BASED = 1
    DB_BASED = 2
    CONSOLE_BASED = 3

@dataclass
class LogConfig:
    """
    Config class of logging
    """

    def __init__(self,
                 type: LoggingTypes = None,
                 name:str = '',
                 **params
                 ):
        self.name = name
        self.type = type
        self.params = params

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name},type={self.type})"

    def get_config(self):
        """
        returns the config in a serialized form
        based on config type.
        :return:
        """



class LogService(InfrastructureService):
    """
    A log service for logging.
    third_party_logs_settings should be like this:
    {
    "modules" : ['azure','aiokafka']
    "level" : 'warning'
    }
    it will set those loggers to warning.
    """

    def __init__(
        self,
        config : LogConfig,
        third_party_logs_settings : dict = None,
        enabled=True,
    ):
        super().__init__(log_service="dummy")

        self.config = config
        self.enabled = enabled
        self.logger = None

        self.third_parties = third_party_logs_settings
        self._check_config()
        # Create the logger
        self._set_modules_logger_levels()
        self._create_logger()


    def _check_config(self):
        pass


    @classmethod
    def _do_log(
            cls,
            logger,
            level,
            message,
            extra,
            exc_info,
    ):
        """
        Helper to do the actual logging.
        Returns:
            Nothing if logging succeeds.
        Raises:
            Exception if logging fails.
        """
        e = None

        if extra is not None and extra != {}:
            e = {'extra': extra}

        getattr(logger, level)(
            message,
            extra=e,
            exc_info=exc_info,
        )

    def _set_modules_logger_levels(self):
        """
        Sets log level of used modules.
        Effectively remove/add unwanted/wanted logs of third-party packages
        from/to console output.
        """
        lvl = self.third_parties['level']
        for modl in self.third_parties['modules']:
            if lvl.lower() == 'warning':
                logging.getLogger(modl).setLevel(logging.WARNING)
            elif lvl.lower() == 'info' :
                logging.getLogger(modl).setLevel(logging.INFO)

            elif lvl.lower() == 'debug' :
                logging.getLogger(modl).setLevel(logging.DEBUG)

            elif lvl.lower() == 'error' :
                logging.getLogger(modl).setLevel(logging.ERROR)

    def info(self, message, extra=None, exc_info=False):
        """
        Log an info level message.
        """
        if self.enabled:
            LogService._do_log(
                logger=self.logger,
                level="info",
                message=message,
                extra=extra,
                exc_info=exc_info,
            )

    def warning(self, message, extra=None, exc_info=False):
        """
        Log an warning level message.
        """
        if self.enabled:
            LogService._do_log(
                logger=self.logger,
                level="warning",
                message=message,
                extra=extra,
                exc_info=exc_info,
            )

    def error(self, message, extra=None, exc_info=False):
        """
        Log an error level message.
        """
        if self.enabled:
            LogService._do_log(
                logger=self.logger,
                level="error",
                message=message,
                extra=extra,
                exc_info=exc_info,
            )

    def debug(self, message, extra=None, exc_info=False):
        """
        Log an debug level message.
        """
        if self.enabled:
            LogService._do_log(
                logger=self.logger,
                level="debug",
                message=message,
                extra=extra,
                exc_info=exc_info,
            )

    async def log_request(self, message, method, url, params):
        """
        Convenience method to log the request to an api.
        """
        if self.enabled:

            params = copy.deepcopy(params)

            if 'token' in params:
                params['token'] = "(hidden)"

            if 'password' in params:
                params['password'] = "(hidden)"

            self.debug(
                message,
                extra={
                    'method': method,
                    'url': url,
                    'params': params,
                }
            )

    async def log_response(self, message, method, url, params, response):
        """
        Convenience method to log the response of an api request.
        """
        if self.enabled:
            content = response.content
            params = copy.deepcopy(params)

            if response.headers.get('content-type') == 'application/json':
                content = json.loads(await response.content())
            else:
                content = await response.content()

            if 'token' in params:
                params['token'] = "(hidden)"

            if 'password' in params:
                params['password'] = "(hidden)"

            self.debug(
                message,
                extra={
                    'method': method,
                    'url': url,
                    'params': params,
                    'status_code': response.status_code,
                    'content_type': response.headers.get('content-type'),
                    'response': content,
                }
            )

    async def start(self):
        pass

    async def stop(self):
        pass

    def _create_logger(self):
        raise NotImplementedError()