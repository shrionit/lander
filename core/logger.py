from logging import basicConfig, getLogger, BASIC_FORMAT, DEBUG


def createLogger(name, level=DEBUG, format=BASIC_FORMAT):
    basicConfig(level=level, format=format)
    return getLogger(name)
