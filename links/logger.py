import logging

logging.basicConfig(level=logging.INFO)


def get_logger(name):
    """

    :param name:
    :return:
    """
    return logging.getLogger(name)


