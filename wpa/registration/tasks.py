import logging
from datetime import timedelta, date

from registration.models import Membership

logger = logging.getLogger(__name__)


def renew_email_task():
    logging.debug('renew_email_task')
    d = date.today() - timedelta(days=15)
    try:
        reg_mem = Membership.objects.filter(exp_date=d)
    except Membership.DoesNotExist:
        logging.debug('No members found')
        return

