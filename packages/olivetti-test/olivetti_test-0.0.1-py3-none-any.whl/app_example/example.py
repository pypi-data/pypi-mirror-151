import logging, coloredlogs

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger) #instanciando sistema de loggin y añadiendo funcionalidad de colores

logger.debug("Aloha!!!!!")

def add_one(number): #no es tipo number
    return number+1

print(add_one(3))

