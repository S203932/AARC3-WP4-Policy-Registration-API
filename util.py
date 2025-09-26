import logging


def get_logger(str:name):
    logger = logging.getLogger("API")
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(name)-1s] %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


