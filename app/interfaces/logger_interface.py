from abc import ABC, abstractmethod
from enum import Enum


class LogLevel(Enum):
    CRITICAL = "CRITICAL"
    FATAL = "FATAL" 
    ERROR = "ERROR" 
    WARNING = "WARNING" 
    WARN = "WARN" 
    INFO = "INFO" 
    DEBUG = "DEBUG" 

class ILogger(ABC):
	@abstractmethod
	def info(self, message: str | Exception):
		pass
	
	@abstractmethod
	def error(self, message: str | Exception):
		pass
	
	@abstractmethod
	def critical(self, message: str | Exception):
		pass
	
	@abstractmethod
	def setLogLevel(self, level: LogLevel):
		pass