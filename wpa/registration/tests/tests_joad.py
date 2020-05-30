import csv
import json
import logging
import os

from django.conf import settings
from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.datetime_safe import  date

from registration.models import Joad_sessions, Joad_session_registration, Pin_shoot, Pin_scores


logger = logging.getLogger(__name__)


class JoadRegistrationTests(TestCase):
    fixtures = ['membership1.json']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        path = os.path.join(settings.BASE_DIR, 'registration', 'fixtures', 'membership1.json')
        logging.debug(path)
        with open(path) as f:
            data = json.load(f)
        self.membership_data = []
        self.member_data = []
        self.joad_registration = []


        for r in data:
            if r['model'] == 'registration.membership':
                f = r['fields']
                self.membership_data.append(f)
                if r['pk'] == 5:
                    self.membership = f
            elif r['model'] == 'registration.member':
                f = r['fields']
                self.member_data.append(f)
                if f["membership"] == 5:
                    self.member = f
            elif r['model'] == 'registration.joad_session_registration':
                f = r['fields']
                self.joad_registration.append(f)
        self.joad_mem = {'first_name': self.member['first_name'],
                         'last_name': self.member['last_name'],
                         'email': self.membership['email'],
                         'terms': True}
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

        d = date.fromisoformat("2020-04-18")
        js = Joad_sessions(start_date=d, state='open')
        js.save()



    def test_joad_register_good(self):

        self.client.get(reverse('registration:joad_registration'))
        with self.assertTemplateUsed('registration/joad_registration.html'):
            render_to_string('registration/joad_registration.html')

        self.joad_mem['joad'] = "2020-04-18"
        self.client.post(reverse('registration:joad_registration'), self.joad_mem, follow=True)
        reg = Joad_session_registration.objects.all()
        self.assertEquals(len(reg), len(self.joad_registration) + 1)

    def test_joad_register_invalid_form(self):
        """Leave out one input and submit, check if returns error message"""
        self.joad_mem['joad'] = "2020-04-18"
        logging.debug(self.joad_mem)
        keys = list(self.joad_mem.keys())
        for k in keys:
            jm = self.joad_mem.copy()
            jm.pop(k)
            self.client.get(reverse('registration:joad_registration'))
            with self.assertTemplateUsed('registration/joad_registration.html'):
                render_to_string('registration/joad_registration.html')

            response = self.client.post(reverse('registration:joad_registration'), jm, follow=True)
            with self.assertTemplateUsed('registration/message.html'):
                render_to_string('registration/message.html')
                self.assertContains(response, 'Error on form.')
            reg = Joad_session_registration.objects.all()
            self.assertEquals(len(reg), len(self.joad_registration))

    def test_joad_register_invalid_request_method(self):

        response = self.client.put(reverse('registration:joad_registration'))
        self.assertEqual(response.status_code, 405)
        # with self.assertTemplateUsed('registration/message.html'):
        #     render_to_string('registration/message.html')
        # self.assertContains(response, 'Error on form.')

        response = self.client.delete(reverse('registration:joad_registration'))
        self.assertEqual(response.status_code, 405)


class JoadPinScore(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        with open(os.path.join(settings.BASE_DIR, 'wpa', 'pins.csv'), 'r') as csvfile:
            # fieldnames = ['category', 'bow', 'distance', 'target', 'score', 'stars']
            reader = csv.DictReader(csvfile)
            for row in reader:
                Pin_scores.objects.get_or_create(category=row['category'],
                                                 bow=row['bow'],
                                                 distance=row['distance'],
                                                 target=row['target'],
                                                 score=row['score'],
                                                 stars=row['stars'])

    def test_calculate_pins(self):
        with open(os.path.join(settings.BASE_DIR, 'registration', 'tests', 'pin_tests.csv'), 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for p in reader:
                s = Pin_shoot(category=p['category'],
                              bow=p['bow'],
                              distance=p['distance'],
                              target=p['target'],
                              score=p['score'])

                s.calculate_pins()
                self.assertEqual(s.stars, int(p['stars']))


