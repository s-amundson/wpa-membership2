import logging

from django.db import OperationalError
from registration.models import Joad_sessions

logger = logging.getLogger(__name__)


def joad_sessions():
    sessions = Joad_sessions.objects.filter(state__exact='open')
    d = [("", "None")]
    try:  # this has caused a error when migration is needed, but also blocks migrations from working
        for s in sessions:
            d.append((str(s.start_date), str(s.start_date)))
    except OperationalError as e:  # pragma: no cover
        logging.error(f"Operational Error: {e}")
    return d
