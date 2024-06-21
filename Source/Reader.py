import pandas

class Reader:

	def __init__(self) -> None:
		self.__wb = self.__ReadExcel("Wb")
		self.__ozon = self.__ReadExcel("Ozon")
		self.__yandex = self.__ReadExcel("Yandex")
	 
	def __ReadExcel(self, Market):
		exceldata = pandas.read_excel(f"Input/{Market}.xlsx")
		Products = pandas.DataFrame(exceldata, columns=['ссылка',"артикул"])
		Links = Products["ссылка"].tolist()
		Models = Products["артикул"].tolist()
		DictProducts = dict()

		for Index in range(len(Models)): Models[Index] = str(Models[Index]).strip("'").replace("HAITEC ", "")

		for Index in range(len(Links)): DictProducts[Models[Index]] = Links[Index]

		return DictProducts

	def GetMegaDict(self, flags: list = []):
	
		MegaDict = dict()
		input_list = []
		links_keys = []

		if "wb" in flags: 
			input_list.append(self.__wb)
			links_keys.append("wildberries_link")

		if "oz" in flags: 
			input_list.append(self.__ozon)
			links_keys.append("ozon_link")

		if "ya" in flags: 
			input_list.append(self.__yandex)
			links_keys.append("yandex_link")

		if len(input_list) == 0:
			input_list = [self.__wb, self.__ozon, self.__yandex]
			links_keys = ["wildberries_link", "ozon_link", "yandex_link"]
		
		for index in range(len(input_list)):

			for Key in input_list[index].keys():

				if Key not in MegaDict.keys():
					MegaDict[Key] = {
						"name": None,
						"wildberries_link": None,
						"ozon_link": None,
						"yandex_link": None,
						"wildberries_price_main": None,
						"wildberries_price_secondary": None,
						"wildberries_price_discount": None,
						"ozon_price_main": None,
						"ozon_price_secondary": None,
						"ozon_price_discount": None,
						"yandex_price_main": None,
						"yandex_price_secondary": None,
						"yandex_price_discount": None
					}
			   
				MegaDict[Key][links_keys[index]] = input_list[index][Key]

		return MegaDict