import logging

from django.utils.datetime_safe import date
# from models import Pin_scores

logger = logging.getLogger(__name__)


def joad_check_date(dob):
    d = date.today()
    # logging.debug(d.year)
    d = d.replace(year=d.year - 21)
    # logging.debug(dob)
    return dob > d
