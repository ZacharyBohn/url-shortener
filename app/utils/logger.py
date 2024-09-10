from app.interfaces.logger_interface import LogLevel
from app.interfaces.logger_interface import ILogger
import logging

class Logger(ILogger):
	def __init__(self, name: str) -> None:
		self.name = name
		return

	def info(self, message: str | Exception):
		logging.info(message)
		return
	
	def error(self, message: str | Exception):
		logging.error(message)
		return
	
	def critical(self, message: str | Exception):
		logging.critical(message)
		return
	
	def setLogLevel(self, level: LogLevel):
		logging.basicConfig(format="%(levelname)s: %(message)s")
		logging.getLogger(self.name).setLevel(level.value)
		return