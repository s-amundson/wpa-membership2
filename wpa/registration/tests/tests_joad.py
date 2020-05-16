import csv
import os
import logging

from django.conf import settings
from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.datetime_safe import  date

from registration.models import Member, Joad_sessions, Joad_session_registration, Pin_shoot, Pin_scores


logger = logging.getLogger(__name__)


class JoadRegistrationTests(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.mem = {'first_name': 'Emily',
                    'last_name': 'Conlan',
                    'street': "1984 Jones Avenue",
                    'city': 'Hays',
                    'state': 'NC',
                    'post_code': 28635,
                    'phone': '336-696-6307',
                    'email': 'EmilyNConlan@einrot.com',
                    'dob': '1995-03-12',
                    'level': 'standard',
                    'terms': True}
        self.joad_mem = {'first_name': 'Emily',
                         'last_name': 'Conlan',
                         'email': 'EmilyNConlan@einrot.com',
                         'terms': True}
        d = date.fromisoformat("2020-04-18")
        js = Joad_sessions(start_date=d, state='open')
        js.save()

    def add_joad_member(self):
        self.mem['dob'] = '2010-03-12'
        response = self.client.post(reverse('registration:register'), self.mem, follow=True)
        # session = self.client.session
        self.assertRedirects(response, reverse('registration:register'))
        mem = Member.objects.all()
        self.assertEquals(len(mem), 1)

    def test_joad_register_good(self):
        self.add_joad_member()
        self.client.get(reverse('registration:joad_registration'))
        with self.assertTemplateUsed('registration/joad_registration.html'):
            render_to_string('registration/joad_registration.html')

        self.joad_mem['joad'] = "2020-04-18"
        self.client.post(reverse('registration:joad_registration'), self.joad_mem, follow=True)
        reg = Joad_session_registration.objects.all()
        self.assertEquals(len(reg), 1)

    def test_joad_register_invalid_form(self):
        """Leave out one input and submit, check if returns error message"""
        self.add_joad_member()
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
            self.assertEquals(len(reg), 0)

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


class JoadPinShootTests(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

        d = date.fromisoformat("2020-04-18")
        js = Joad_sessions(start_date=d, state='open')
        js.save()

        self.shoot_record = {'first_name': 'Emily',
                             'last_name': 'Conlan',
                             # 'club': 'WPA',
                             'category': 'joad_indoor',
                             'bow': 'barebow',
                             'shoot_date': '2020-04-18',
                             'distance': 9,
                             'target': 60,
                             'prev_stars': 0,
                             # 'wpa_membership_number': '',
                             'email': 'EmilyNConlan@einrot.com',
                             'score': 58
                             }

    def test_add_shooter(self):
        response = self.client.post(reverse('registration:pin_shoot'), self.shoot_record, follow=True)

        self.assertRedirects(response, reverse('registration:process_payment'))
        ps = Pin_shoot.objects.all()
        self.assertEquals(len(ps), 1)

    def test_get_form(self):
        response = self.client.get(reverse('registration:pin_shoot'), follow=True)
        self.client.get(reverse('registration:pin_shoot'))
        with self.assertTemplateUsed('registration/pin_shoot.html'):
            render_to_string('registration/pin_shoot.html')

    def test_pin_shoot_invalid_form(self):
        """Leave out one input and submit, check if returns error message"""

        keys = list(self.shoot_record.keys())
        for k in keys:
            sr = self.shoot_record.copy()
            sr.pop(k)
            # self.client.get(reverse('registration:pin_shoot'))
            # with self.assertTemplateUsed('registration/pin_shoot.html'):
            #     render_to_string('registration/pin_shoot.html')

            response = self.client.post(reverse('registration:pin_shoot'), sr, follow=True)
            with self.assertTemplateUsed('registration/message.html'):
                render_to_string('registration/message.html')
                self.assertContains(response, 'Error on form.')
            reg = Pin_shoot.objects.all()
            self.assertEquals(len(reg), 0)

    def test_pin_shoot_optional_info(self):
        """Add optional infomration and check"""
        self.shoot_record['club'] = 'WPA'
        self.shoot_record['wpa_membership_number'] = 5

        response = self.client.post(reverse('registration:pin_shoot'), self.shoot_record, follow=True)
        self.assertRedirects(response, reverse('registration:process_payment'))
        reg = Pin_shoot.objects.all()
        self.assertEquals(len(reg), 1)
        self.assertEquals(reg[0].club, self.shoot_record['club'])
        self.assertEquals(reg[0].wpa_membership_number, self.shoot_record['wpa_membership_number'])
