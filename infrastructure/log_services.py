import abc

from .services import InfrastructureService
from pydantic.dataclasses import dataclass
import inspect
from .exceptions import InfrastructureException
import logging
import copy
import sys
import abc
from enum import Enum

class LoggingType(Enum):
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
                 type: LoggingType = None,
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

class LogBackend(InfrastructureService):
    """
    it is the back-end and implementation of log service
    for ex : ap based service or console based and so on.
    """

    async def start(self):
        pass

    async def stop(self):
        pass

    def __init__(self,config:LogConfig):
        self.config = config
        super(LogBackend, self).__init__()

    def check_config(self):
        raise NotImplementedError()

    def _create_logger(self):
        raise NotImplementedError()

    def get_logger(self) -> "LogBackend":
        self.check_config()
        return self._create_logger()

    @abc.abstractmethod
    def log(self, message, level, extra=None, exec_info=None):
        raise NotImplementedError()

    @abc.abstractmethod
    def info(self, message, extra=None, exec_info=None):
        raise NotImplementedError()

    @abc.abstractmethod
    def debug(self, message, extra=None, exec_info=None):
        raise NotImplementedError()

    @abc.abstractmethod
    def warning(self, message, extra=None, exec_info=None):
        raise NotImplementedError()

    @abc.abstractmethod
    def error(self, message, extra=None, exec_info=None):
        raise NotImplementedError()

    @abc.abstractmethod
    def critical(self, message, extra=None, exec_info=None):
        raise NotImplementedError()


class LogService(InfrastructureService):
    """
    A log service for logging.
    it is an Abstract class wich represents
    a logging service conceptual functionalities
    """

    def __init__(
        self,
        config : LogConfig,
        log_backend : LogBackend,
        enabled=True,
    ):
        super().__init__(log_service="dummy")

        self.config = config
        self.enabled = enabled
        self.logger = None
        self.log_backend = log_backend

        #cheking
        self._check_params()

        # Create the logger
        self._create_logger()

    def _check_params(self):
        if not inspect.isclass(self.log_backend):
            raise InfrastructureException(f"log backend should be a class not object")

        if not isinstance(self.log_backend,LogBackend):
            raise InfrastructureException(
                f"log backend should be LogBackend class not {self.log_backend}")
        if not isinstance(self.config,LogConfig):
            raise InfrastructureException(
                f'logger config should be instance of LogConfig class not {self.config.__class__}')

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
        raise NotImplementedError()

    async def log_response(self, message, method, url, params, response):
        """
        Convenience method to log the response of an api request.
        """
        raise NotImplementedError()

    async def start(self):
        pass

    async def stop(self):
        pass

    def _create_logger(self):
        return self.log_backend(self.config).get_logger()