from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from dublib.Methods.JSON import ReadJSON
import os
import sys

class Parser:

	@property
	def browser(self):
		return self.__browser

	def close(self):
		try:
			self.__browser.close()

		except: pass

	def __ClickButton(self, class_name: str, one_try: bool = False):
		"""
		Нажимает на кнопку.
			class_name – название класса кнопки.
		"""

		# Состояние: выполнено ли нажатие.
		IsSuccess = False

		# Пока кнопка не нажата.
		while not IsSuccess:

			try:
				# Выжидание интервала.
				sleep(1)
				# Переключение статуса.
				if one_try: IsSuccess = True
				# Поиск и нажатие кнопки.
				self.__browser.find_element(By.CLASS_NAME, class_name).click()

			except Exception as ExceptionData: pass

			else: IsSuccess = True

	def __ExecuteJavaScript(self, script: str) -> any:
		"""
		Выполняет JavaScript.
			script – исполняемый код.
		"""

		# Состояние: выполнен ли переход.
		IsSuccess = False
		# Результат выполнения.
		Result = None

		# Пока переход не выполнен.
		while not IsSuccess:

			try:
				# Обновление страницы.
				Result = self.__browser.execute_script(script)

			except: pass

			else: IsSuccess = True

		return Result

	def __Get(self, url: str):
		"""
		Обрабатывает переход браузера по URL.
			url – ссылка для перехода.
		"""

		# Состояние: выполнен ли переход.
		IsSuccess = False

		# Пока переход не выполнен.
		while not IsSuccess:

			try:
				# Переход по ссылке.
				self.__browser.get(url)
				# Остановка цикла.
				IsSuccess = True

			except Exception as ExceptionData: pass

	def __Refresh(self):
		"""Обновляет текущую страницу."""

		# Состояние: выполнен ли переход.
		IsSuccess = False

		# Пока переход не выполнен.
		while not IsSuccess:

			try:
				# Обновление страницы.
				self.__browser.refresh()
				# Остановка цикла.
				IsSuccess = True

			except Exception as ExceptionData: pass
	 
	def __init__(self, use_vpn: bool = True) -> None:

		# Чтение настроек.
		self.__Setings = ReadJSON("Settings.json")
		chrome_options = Options()
		if "linux" in sys.platform: chrome_options.add_argument(r'user-data-dir=./User')
		if "win32" in sys.platform: chrome_options.add_argument('user-data-dir=' + os.path.dirname(__file__) + "\\User")
		chrome_options.add_argument('--allow-profiles-outside-user-dir')
		chrome_options.add_argument('--enable-profile-shortcut-manager')
		chrome_options.add_argument('--profile-directory=Profile 1')

		chrome_options.add_argument("--disable-gpu")
		chrome_options.add_argument("--no-sandbox")
		chrome_options.add_argument("--disable-software-rasterizer")

		#chrome_options.binary_location = "./Chrome/chrome"
		self.__browser = webdriver.Chrome(options=chrome_options)
		self.__browser.set_window_size(1920, 1080)

		if use_vpn and self.__Setings["vpn_extension_identificator"]:
			VPN_Name = self.__Setings["vpn_extension_identificator"]
			self.__Get(f"chrome-extension://{VPN_Name}/popup.html")
			sleep(1)
			self.__Refresh()
			self.__Refresh()
			self.__ClickButton("analytics__button", True)
			self.__ClickButton("connect-button")
			sleep(3)
		
	def __GetBody(self):
		html = self.__ExecuteJavaScript("return document.body.outerHTML;")
		soup = BeautifulSoup(html, "html.parser")

		return soup
	
	def LogInWildberries(self):
		"""Открывает страницу входа в Wildberries."""

		self.__browser.get("https://www.wildberries.ru/")
		input("Нажмите ENTER после выполнения входа...")

	def LogInYandexMarket(self):
		"""Открывает страницу входа в Яндекс Маркет."""

		self.__browser.get("https://market.yandex.ru/")
		input("Нажмите ENTER после выполнения входа...")

	def ParseWb(self, md: dict):
		for key in md:
			wildberries_price_discount = None
			wildberries_price_main = None
			wildberries_price_secondary = None
			name = md[key]["name"]
			Query = md[key]["wildberries_link"]

			if Query:
				self.__Get(Query)
				sleep(3)
				if name == None: 
					nametag = self.__GetBody().find("h1",{ "class":"product-page__title"})
					if nametag == None: self.__GetBody().find("h1",{ "class":"product-page__title product-page__title--long"})
					if nametag:

						nametag = nametag.get_text()
						name = nametag.strip()
					
					else:
						try:
							sleep(7)

							name = self.__GetBody().find("h1",{ "class":"product-page__title"}).get_text()
							if name == None: self.__GetBody().find("h1",{ "class":"product-page__title product-page__title--long"}).get_text()
							name = name.strip()
			
						except:
							name = None

				wildberries_price_discounttag = self.__GetBody().find("span",{ "class":"price-block__wallet-price"})
				wildberries_price_maintag = self.__GetBody().find("ins")
				wildberries_price_secondarytag = self.__GetBody().find("del",{ "class":"price-block__old-price"})
				
				if wildberries_price_maintag:

					if wildberries_price_discounttag: wildberries_price_discounttag = wildberries_price_discounttag.get_text()
					wildberries_price_maintag = wildberries_price_maintag.get_text()
					if wildberries_price_secondarytag: wildberries_price_secondarytag = wildberries_price_secondarytag.get_text()
			
					if wildberries_price_discounttag: wildberries_price_discount = wildberries_price_discounttag.strip().replace("₽","")
					wildberries_price_main = wildberries_price_maintag.strip().replace("\xa0", "").replace("₽","")
					if wildberries_price_secondarytag: wildberries_price_secondary = wildberries_price_secondarytag.strip().replace("\xa0", "").replace("₽","")
					
				else:
					try:
						sleep(7)
						wildberries_price_discount = self.__GetBody().find("span",{ "class":"price-block__wallet-price"})
						if wildberries_price_discount: wildberries_price_discount = wildberries_price_discount.get_text().strip().replace("₽","")
						wildberries_price_main = self.__GetBody().find("ins").get_text()
						wildberries_price_main = wildberries_price_main.strip().replace("\xa0", "").replace("₽","")
						wildberries_price_secondary = self.__GetBody().find("del",{ "class":"price-block__old-price"}).get_text()
						wildberries_price_secondary = wildberries_price_secondary.strip().replace("\xa0", "").replace("₽","")
					except:
						wildberries_price_discount = None
						wildberries_price_main = None
						wildberries_price_secondary = None
				
				md[key]["name"] = name	
				md[key]["wildberries_price_discount"] = wildberries_price_discount	
				md[key]["wildberries_price_main"] = wildberries_price_main
				md[key]["wildberries_price_secondary"] = wildberries_price_secondary

		return md

	def ParseOz(self, md):
		isFirst = True
		for key in md:
			ozon_price_discount = None
			ozon_price_main = None
			ozon_price_secondary = None
			name = md[key]["name"]
			Query = md[key]["ozon_link"]
			if Query:
				self.__Get(Query)

				if isFirst:
					self.__Refresh()
					isFirst = False 

				sleep(3)

				if not self.__GetBody().find("h2", {"class": "c2"}):

					if name == None: 
						nametag = self.__GetBody().find("div",{ "data-widget":"webProductHeading"})
						if nametag:

							nametag = nametag.get_text()
							name = nametag.strip()
					
					else:
						try:
							sleep(7)

							name = self.__GetBody().find("div",{ "data-widget":"webProductHeading"}).get_text()
							name = name.strip()
			
						except:
							name = None

					
					PageBody = self.__GetBody()
					PricesWidget = PageBody.find("div", {"data-widget": "webPrice"})
					
					if PricesWidget:
						Prices = PricesWidget.get_text().replace("c Ozon Картой", "").replace("без Ozon Карты", "").replace(" ", "").replace("\u2009", "")
						Prices = Prices.split("₽")

						for Index in range(len(Prices)):
							if Index == 0 and Prices[Index].isdigit(): ozon_price_discount = int(Prices[Index])
							if Index == 1 and Prices[Index].isdigit(): ozon_price_main = int(Prices[Index])
							if Index == 2 and Prices[Index].isdigit(): ozon_price_secondary = int(Prices[Index])

					if not PricesWidget:
						try:
							sleep(7)
							PageBody = self.__GetBody()
							PricesWidget = PageBody.find("div", {"data-widget": "webPrice"})
							
							if PricesWidget:
								Prices = PricesWidget.get_text().replace("c Ozon Картой", "").replace("без Ozon Карты", "").replace(" ", "").replace("\u2009", "")
								Prices = Prices.split("₽")

								for Index in range(len(Prices)):
									if Index == 0 and Prices[Index].isdigit(): ozon_price_discount = int(Prices[Index])
									if Index == 1 and Prices[Index].isdigit(): ozon_price_main = int(Prices[Index])
									if Index == 2 and Prices[Index].isdigit(): ozon_price_secondary = int(Prices[Index])
						except: pass
				
				md[key]["name"] = name	
				md[key]["ozon_price_discount"] = ozon_price_discount
				md[key]["ozon_price_main"] = ozon_price_main
				md[key]["ozon_price_secondary"] = ozon_price_secondary
		return md
				
	def ParseYa(self, data: dict):

		# Для каждой модели.
		for Model in data.keys():
			# Получение ссылки.
			Link = data[Model]["yandex_link"]
			# Типы цен и название товара.
			PriceMain = None
			PriceSecondary = None
			PriceDiscount = None
			PriceThird = None
			Name = data[Model]["name"]
			
			# Если для модели имеется ссылка на страницу товара.
			if Link:
				# Загрузка страницы.
				self.__Get(Link)
				# Выжидание интервала.
				sleep(5)
				# Получение кода страницы.
				PageBody = self.__GetBody()
				# Пойск контейнеров цен.
				PriceMainTag = PageBody.find("span", {"data-auto": "snippet-price-old"})
				PriceSecondaryTag = PageBody.find("h3", {"data-auto": "snippet-price-current"})
				PriceDiscountTag = PageBody.find("div", {"data-zone-name": "blackOfferLink"})

				# Получение главной цены.
				if PriceMainTag:
					PriceMainOld = PriceMainTag.find("s")

					if PriceMainOld: 
						PriceThird = PriceMainOld.get_text()
						PriceThird = PriceThird.replace("\u2009", "").strip()
						PriceMainOld.decompose()

					PriceMain = PriceMainTag.get_text()
					PriceMain = PriceMain.replace("без:", "").replace("Вместо:", "").replace(" ", "").replace("₽", "").replace("\u2009", "").strip()
					
				# Получение вторичной цены.
				if PriceSecondaryTag:
					PriceSecondary = PriceSecondaryTag.get_text()
					PriceSecondary = PriceSecondary.replace("Цена с картой Яндекс Пэй:", "").replace(" ", "").replace("₽", "").replace("\u2009", "").strip()

				# Получение цены для юридических лиц.
				if PriceDiscountTag:
					PriceDiscount = PriceDiscountTag.get_text()
					PriceDiscount = PriceDiscount.replace("НДС", "").replace(" ", "").replace("₽", "").replace("\u2009", "").strip()
					
				# Если не задано наименование.
				if not Name:
					# Поиск тега наименования.
					NameTag = PageBody.find("h1", {"data-additional-zone": "title"})

					# Получение наименования.
					if NameTag:
						Name = NameTag.get_text().strip()

				# Запись данных.
				data[Model]["name"] = Name
				data[Model]["yandex_price_main"] = PriceMain
				data[Model]["yandex_price_secondary"] = PriceSecondary
				data[Model]["yandex_price_discount"] = PriceThird
				
		return data
	
