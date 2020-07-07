import logging
import asyncio
import urllib.parse
import json

from hbmqtt.client import MQTTClient, ConnectException
from hbmqtt.mqtt.constants import QOS_2

logger = logging.getLogger('MqttHandler')

class MqttHandler:
	def __init__(self, loop, publishers, cfg):
		self.__publishers = publishers
		self.__conf = cfg
		self.__client = None

	async def run(self):
		await self.__tryConnecting()

		subscriptions = []
		for topic in self.__conf['topics']:
			subscriptions.append((topic, QOS_2))

		await self.__client.subscribe(subscriptions)
		while True:
			message = await self.__client.deliver_message()
			if message.data:
				self.__handleMessage(message.data)



	async def __tryConnecting(self):
		if self.__client:
			return

		uriAuth = ''
		if type(self.__conf['username']) == str and type(self.__conf['password']) == str and len(self.__conf['username']) > 0 and len(self.__conf['password']) > 0:
			uriAuth = '{}:{}@'.format(urllib.parse.quote(self.__conf['username']), urllib.parse.quote(self.__conf['password']))

		self.__client = MQTTClient(config={
			'auto_reconnect': True,
			'reconnect_retries': 20,
			'reconnect_max_interval': 5
		})
		connected = False
		while not connected:
			try:
				await self.__client.connect('mqtt://{}{}:{}/'.format(uriAuth, self.__conf['host'], self.__conf['port']))
				logger.info('Conencted to \"%s:%s\"', self.__conf['host'], self.__conf['port'])
				connected = True
			except ConnectException as e:
				logger.warn('Connection failed: \"%s\". Trying to reconnect', str(e))
				await asyncio.sleep(3)
	
	def __handleMessage(self, message):
		data = None
		try:
			data = json.loads(message)
		except BaseException as e:
			logger.warn("Invalid JSON Message received, %s", e)
			return

		for pub in self.__publishers:
			pub.handleData(data)