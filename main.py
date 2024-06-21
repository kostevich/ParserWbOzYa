from dublib.Terminalyzer import Command, Terminalyzer
from dublib.Methods import ReadJSON, MakeRootDirectories
from Source.Reader import Reader
from Source.Parser import Parser
from Source.Writer import Writer
from Source.Sender import Sender

import os

MakeRootDirectories(["Output", "Input"])

#==========================================================================================#
# >>>>> НАСТРОЙКА ОБРАБОТЧИКА КОМАНД <<<<< #
#==========================================================================================#

# Список описаний обрабатываемых команд.
CommandsList = list()

# Создание команды: setup.
Com = Command("setup")
CommandsList.append(Com)

# Создание команды: login.
Com = Command("login")
Com.add_flag_position(["wb"])
Com.add_flag_position(["oz"])
Com.add_flag_position(["ya"])
CommandsList.append(Com)

# Создание команды: parse.
Com = Command("parse")
Com.add_flag_position(["wb"])
Com.add_flag_position(["oz"])
Com.add_flag_position(["ya"])
CommandsList.append(Com)

# Инициализация обработчика консольных аргументов.
CAC = Terminalyzer()

# Получение информации о проверке команд. 
CommandDataStruct = CAC.check_commands(CommandsList)

#==========================================================================================#
# >>>>> ОБРАБОТКА КОММАНД <<<<< #
#==========================================================================================#

# Обработка команды: setup.
if "setup" == CommandDataStruct.name:
	parser = Parser(False)
	parser.browser.get("https://chromewebstore.google.com/detail/%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9-vpn-%D0%B4%D0%BB%D1%8F-chrome/adlpodnneegcnbophopdmhedicjbcgco")
	if not CommandDataStruct.flags: input("Нажмите ENTER после установки расширения в браузер...")
	parser.close()

# Обработка команды: login.
if "login" == CommandDataStruct.name:
	parser = Parser(False)
	
	if "wb" in CommandDataStruct.flags: parser.LogInWildberries()

	if "oz" in CommandDataStruct.flags: print("Вход не требуется.")

	if "ya" in CommandDataStruct.flags: parser.LogInYandexMarket()

	parser.close()

# Обработка команды: parse.
if "parse" == CommandDataStruct.name:
	if not CommandDataStruct.flags: raise Exception("Не выбран ни один источник для парсинга.")
	reader = Reader()
	parser = Parser()
	writer = Writer()
	
	md = reader.GetMegaDict(CommandDataStruct.flags)
	
	if "wb" in CommandDataStruct.flags: md = parser.ParseWb(md)
		
	if "oz" in CommandDataStruct.flags: md = parser.ParseOz(md)
	
	if "ya" in CommandDataStruct.flags: md = parser.ParseYa(md)

	writer.WriteExcel(md, CommandDataStruct.flags)

	Settings = ReadJSON("Settings.json")

	if Settings["ftp_server"]:

		SenderObject = Sender(Settings["ftp_server"], Settings["ftp_login"], Settings["ftp_password"])
		SenderObject.cd("httpdocs/parser")

		for File in os.listdir("Output"):

			if "wb" in CommandDataStruct.flags and File.startswith("wb"): SenderObject.upload(File, False)
			if "oz" in CommandDataStruct.flags and File.startswith("oz"): SenderObject.upload(File, False)
			if "ya" in CommandDataStruct.flags and File.startswith("ya"): SenderObject.upload(File, False)
