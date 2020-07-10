from .pubSenseComREST import PubSensComREST

class PubFsApp(PubSensComREST):
	
	def __init__(self, id):
		super().__init__(id, "https://h2801469.stratoserver.net/data.php", "FSApp")