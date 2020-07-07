from .publisher import Publisher
import json
import asyncio
import aiohttp
import logging

logger = logging.getLogger("Opensense Publisher")

class PubOpensense(Publisher):
	
	def __init__(self, sensors, boxid):
		self.__sensors = sensors
		self.__boxid = boxid
		self.__valid = len(sensors) >= 6 and boxid != None
		if not self.__valid:
			logger.warning("Sensor IDs for opensensemap are not set correctly")
			
	"""
	:param 
	"""
	def handleData(self, data):
		logger.log(logging.DEBUG, "Recieved valid data")
		
		if self.__valid:
			asyncio.ensure_future(self.sendOpenSense(data))
	
	async def sendOpenSense(self, data):
		jsonData = {}
		if "temp" in data:
			jsonData[self.__sensors[0]] = "{value:.2f}".format(value=data["temp"])
		if "humid" in data:
			jsonData[self.__sensors[1]] = "{value:.2f}".format(value=data["humid"])
		if "pressure" in data:
			jsonData[self.__sensors[2]] = "{value:.2f}".format(value=data["pressure"])
		if "pm25" in data:
			jsonData[self.__sensors[3]] = "{value:.2f}".format(value=data["pm25"])
		if "pm10" in data:
			jsonData[self.__sensors[4]] = "{value:.2f}".format(value=data["pm10"])
		if "rain" in data:
			jsonData[self.__sensors[5]] = "{value:.2f}".format(value=data["rain"])
		
		if len(jsonData) == 0:
			logger.log(logging.DEBUG, "No data for OpenSenseMap. Abort")
			return

		headers = {
			"content-type": "application/json"
		}

		url = "https://api.opensensemap.org/boxes/{id}/data".format(id = self.__boxid)
		#url = "http://localhost:8889/boxes/{id}/sensors".format(id = self.__boxid)

		async with aiohttp.ClientSession() as session:
			await session.request(method = "POST", url = url, headers = headers, json = jsonData)
