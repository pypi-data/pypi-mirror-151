import sys
import time
class SLogger(object):
	def __init__(self, app_name):
		self.app_name = app_name.lower()
		self.info("logger created!")
		self.info("app runned!")
	def info(self, text):
		self._print("info", text)
	def _print(self, method, text):
		print("["+self.app_name+"]", "["+time.strftime("%H:%M:%S")+"]","["+method.upper()+"]", text)
	def error(self, text):
		self._print("error", text)
	def warning(self, text):
		self._print("warning", text)

