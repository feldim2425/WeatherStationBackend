import logging
import asyncio
import functools
import signal
import argparse
from .mqttHandler import MqttHandler
from .setupPublisher import initializePublishers
from .config  import readConfiguration

FORMAT = '[%(asctime)s] [%(levelname)s] [%(name)s] :> %(message)s'

if __name__ == "__main__":
	
	# Parsing arguments
	parser = argparse.ArgumentParser(description='Backend for MQTT Weatherstation')
	parser.add_argument('--config', '-c', dest='config', default=None, help='Path to configuration INI file')
	parser.add_argument('--debug', dest='debug', default=False, action='store_true', help='Set logging to debug')
	args = parser.parse_args()

	# Setup logging
	logging.basicConfig(level=(logging.DEBUG if args.debug else logging.INFO), format=FORMAT)
	logging.getLogger("transitions").setLevel(logging.INFO)
	logger = logging.getLogger('WeatherBackend')
	
	try:
		# Create the Asyncio eventloop
		loop = asyncio.get_event_loop()
		logger.info('Starting...')
		
		# Callback function to stop the asyncio loop when a signal arrives
		def sigExit(signame):
			logger.info("Signal recieved: %s", signame)
			loop.stop()

		# Register signalhandler for interrupt and termination
		for signame in ('SIGINT', 'SIGTERM'):
			loop.add_signal_handler(getattr(signal, signame), functools.partial(sigExit, signame))

		# Read and parse the configuration file     
		configuration = readConfiguration(args.config)

		handler = MqttHandler(loop, initializePublishers(configuration['services']), configuration['mqtt'])
		loop.create_task(handler.run())

		loop.run_forever()
	except Exception as e:
		logger.error(e, exc_info=True)
	finally:
		logger.info('Stopping...')
		if loop != None:
			loop.stop()
		#if handler != None:
		#	handler.stop()
		logger.info('Stopped')
