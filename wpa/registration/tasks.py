import logging
from datetime import timedelta, date
from uuid import uuid4

from registration.models import Membership
from registration.src.Email import Email

logger = logging.getLogger(__name__)


def renew_email_task():
    logging.debug('renew_email_task')
    d = date.today() + timedelta(days=15)
    # logging.debug(d)
    try:
        reg_mem = Membership.objects.filter(exp_date=d)
        for mem in reg_mem:
            mem.verification_code = str(uuid4())
            mem.save()
            Email.renewal_notice(mem)

    except Membership.DoesNotExist:
        logging.debug('No members found')
        return

