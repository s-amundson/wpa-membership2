import logging

logger = logging.getLogger(__name__)


def print_result(task):
    logging.debug(task.result)
