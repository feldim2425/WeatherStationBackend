from . import publisher

def _initLuftdaten(cfg):
	return publisher.PubLuftdaten(cfg['luftdaten_id'])

def _initFsApp(cfg):
	return publisher.PubFsApp(cfg['luftdaten_id'])

def _initMadavi(cfg):
	return publisher.PubMadavi(cfg['luftdaten_id'])

def _initOpensense(cfg):
	return publisher.PubOpensense(cfg['opensensemap_sensors'], cfg['opensensemap_boxid'])


def initializePublishers(servConfig):
	publishers = []
	if servConfig['enable_opensensemap']:
		publishers.append(_initOpensense(servConfig))
	
	if servConfig['enable_luftdaten']:
		publishers.append(_initLuftdaten(servConfig))

	if servConfig['enable_fsapp']:
		publishers.append(_initFsApp(servConfig))

	if servConfig['enable_madavi']:
		publishers.append(_initMadavi(servConfig))
	
	return publishers