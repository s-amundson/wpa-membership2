import logging

from django.shortcuts import render
from django.views.generic.base import View

logger = logging.getLogger(__name__)


class MessageView(View):
    """Shows a message page"""
    def get(self, request, text=""):
        logging.debug("message")
        return render(request, 'registration/message.html', {'message': text})
