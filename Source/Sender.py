from ftplib import FTP

import os

class Sender:
	"""Обработчик выгрузки файла по FTP."""

	def __init__(self, server: str, login: str, password: str):
		"""Обработчик выгрузки файла по FTP."""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# FTP-клиент.
		self.__Client = None

		# Инициализация клиента.
		self.__Client = FTP(server)
		self.__Client.login(login, password)

	def cd(self, directory: str):
		"""
		Указывает директорию для перехода.
			directory – директория для вохда.
		"""

		# Переход в директорию.
		self.__Client.cwd(directory)

	def upload(self, filename: str, autoremove: bool = True):
		"""
		Выгружает файл на FTP сервер.
			filename – название локального файла.
		"""

		# Открытие потока чтения.
		with open(f"Output/{filename}", "rb") as FileReader:
			# Выгрузка файла.
			self.__Client.storbinary(f"STOR {filename}", FileReader)

		# Удаление локального файла.
		if autoremove: os.remove(filename)
