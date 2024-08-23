import pandas
from openpyxl import load_workbook

from datetime import date


class Writer:

	def __init__(self) -> None:
		self.__BufferWb = {
					"Модель": [],
					"Название": [],
					"LinkWb": [],
					"Wb1": [],
					"Wb2": [],
					"Wb3": [], 
					"wb_code": []
				}
		self.__BufferOz = {
					"Модель": [],
					"Название": [],
					"LinkOz": [],
					"Oz1": [],
					"Oz2": [],
					"Oz3": [],
					"ozon_code": []
				}
		self.__BufferYa = {
					"Модель": [],
					"Название": [],
					"LinkYa": [],
					"Ya1": [],
					"Ya2": [],
					"Ya3": [],
					"yandex_code": []
				}	
	
	def WriteExcel(self, md, flags):
		today = date.today()
		today = today.strftime("%d.%m.%Y")
		
		for key in md:
			Model = key
			name = md[key]["name"]
			wildberries_link = md[key]["wildberries_link"]
			ozon_link = md[key]["ozon_link"]
			yandex_link = md[key]["yandex_link"]
			wb_code = md[key]["wb_code"]
			ozon_code = md[key]["ozon_code"]
			yandex_code = md[key]["yandex_code"]
			wildberries_price_main = md[key]["wildberries_price_main"]
			wildberries_price_secondary = md[key]["wildberries_price_secondary"]
			wildberries_price_discount = md[key]["wildberries_price_discount"]
			ozon_price_main = md[key]["ozon_price_main"]
			ozon_price_secondary = md[key]["ozon_price_secondary"]
			ozon_price_discount = md[key]["ozon_price_discount"]
			yandex_price_main = md[key]["yandex_price_main"]
			yandex_price_secondary = md[key]["yandex_price_secondary"]
			if md[key]["yandex_price_discount"]: yandex_price_discount = md[key]["yandex_price_discount"]
			else: yandex_price_discount = md[key]["yandex_price_main"]
			

			if wildberries_link: wildberries_link = f"=HYPERLINK(\"{wildberries_link}\", \"ссылка\")"
			if ozon_link: ozon_link = f"=HYPERLINK(\"{ozon_link}\", \"ссылка\")"
			if yandex_link: yandex_link = f"=HYPERLINK(\"{yandex_link}\", \"ссылка\")"

			if "wb" in flags:
				if wildberries_link:
					self.__BufferWb["Модель"].append(Model)
					self.__BufferWb["Название"].append(name)
					self.__BufferWb["LinkWb"].append(wildberries_link)
					self.__BufferWb["Wb1"].append(wildberries_price_discount)
					self.__BufferWb["Wb2"].append(wildberries_price_main)
					self.__BufferWb["Wb3"].append(wildberries_price_secondary)
					self.__BufferWb["wb_code"].append(wb_code)
				
				df = pandas.DataFrame.from_dict(self.__BufferWb)
				df.to_excel(f"Output/{"wb_"}{today}.xlsx", index= False)

			if "oz" in flags:
				if ozon_link:
					self.__BufferOz["Модель"].append(Model)
					self.__BufferOz["Название"].append(name)
					self.__BufferOz["LinkOz"].append(ozon_link)
					self.__BufferOz["Oz1"].append(ozon_price_discount)
					self.__BufferOz["Oz2"].append(ozon_price_main)
					self.__BufferOz["Oz3"].append(ozon_price_secondary)
					self.__BufferOz["ozon_code"].append(ozon_code)

				df = pandas.DataFrame.from_dict(self.__BufferOz)
				df.to_excel(f"Output/oz_{today}.xlsx", index= False)

			if "ya" in flags:
				if yandex_link: 
					self.__BufferYa["Модель"].append(Model)
					self.__BufferYa["Название"].append(name)
					self.__BufferYa["LinkYa"].append(yandex_link)
					self.__BufferYa["Ya1"].append(yandex_price_secondary)
					self.__BufferYa["Ya2"].append(yandex_price_main)
					self.__BufferYa["Ya3"].append(yandex_price_discount)
					self.__BufferYa["yandex_code"].append(yandex_code)
					
				df = pandas.DataFrame.from_dict(self.__BufferYa)
				df.to_excel(f"Output/ya_{today}.xlsx", index= False)