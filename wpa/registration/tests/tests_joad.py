import csv
import os

from django.conf import settings
from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.datetime_safe import  date

from registration.models import Member, Joad_sessions, Joad_session_registration, Pin_shoot, Pin_scores

import logging

from views import calculate_pins

logger = logging.getLogger(__name__)


# Create your tests here.


class JoadRegistrtionTests(TestCase):
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
        self.assertEqual(response.status_code, 404)
        # with self.assertTemplateUsed('registration/message.html'):
        #     render_to_string('registration/message.html')
        # self.assertContains(response, 'Error on form.')

        response = self.client.delete(reverse('registration:joad_registration'))
        self.assertEqual(response.status_code, 404)


class JoadPinScore(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        with open(os.path.join(settings.BASE_DIR, 'wpa', 'pins.csv'), 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Pin_scores.objects.get_or_create(category=row['category'],
                       bow=row['bow'],
                       distance=row['distance'],
                       target=row['target'],
                       score=row['score'],
                       stars=row['stars'])


    def test_calculate_pins(self):
        # parameters = [
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 9, 'target': 60, 'score': 39, 'stars': 0},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 9, 'target': 60, 'score': 40, 'stars': 1},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 9, 'target': 60, 'score': 74, 'stars': 1},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 9, 'target': 60, 'score': 75, 'stars': 2},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 9, 'target': 60, 'score': 109, 'stars': 2},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 9, 'target': 60, 'score': 110, 'stars': 3},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 9, 'target': 60, 'score': 144, 'stars': 3},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 9, 'target': 60, 'score': 145, 'stars': 4},
        #
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 29, 'stars': 0},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 30, 'stars': 2},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 49, 'stars': 2},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 50, 'stars': 3},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 99, 'stars': 3},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 100, 'stars': 4},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 139, 'stars': 4},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 140, 'stars': 5},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 184, 'stars': 5},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 185, 'stars': 6},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 229, 'stars': 6},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 230, 'stars': 7},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 254, 'stars': 7},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 255, 'stars': 8},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 264, 'stars': 8},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 265, 'stars': 9},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 274, 'stars': 9},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 275, 'stars': 10},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 279, 'stars': 10},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 280, 'stars': 11},
        #
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 174, 'stars': 0},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 175, 'stars': 6},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 219, 'stars': 6},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 220, 'stars': 7},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 239, 'stars': 7},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 240, 'stars': 8},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 249, 'stars': 8},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 250, 'stars': 9},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 259, 'stars': 9},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 260, 'stars': 10},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 269, 'stars': 10},
        #     {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 270, 'stars': 11},
        #
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 9, 'target': 60, 'score': 49, 'stars': 0},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 9, 'target': 60, 'score': 50, 'stars': 1},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 9, 'target': 60, 'score': 99, 'stars': 1},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 9, 'target': 60, 'score': 100, 'stars': 2},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 9, 'target': 60, 'score': 149, 'stars': 2},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 9, 'target': 60, 'score': 150, 'stars': 3},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 9, 'target': 60, 'score': 199, 'stars': 3},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 9, 'target': 60, 'score': 200, 'stars': 4},
        #
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 29, 'stars': 0},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 30, 'stars': 2},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 49, 'stars': 2},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 50, 'stars': 3},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 99, 'stars': 3},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 100, 'stars': 4},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 149, 'stars': 4},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 150, 'stars': 5},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 199, 'stars': 5},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 200, 'stars': 6},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 249, 'stars': 6},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 250, 'stars': 7},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 269, 'stars': 7},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 270, 'stars': 8},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 284, 'stars': 8},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 285, 'stars': 9},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 289, 'stars': 9},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 290, 'stars': 10},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 294, 'stars': 10},
        #     {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 295, 'stars': 11},
        # ]

        with open(os.path.join(settings.BASE_DIR, 'registration', 'tests', 'pin_tests.csv'), 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for p in reader:
                c = calculate_pins(p)
                self.assertEqual(c, int(p['stars']))


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

        self.assertRedirects(response, reverse('registration:pin_shoot'))
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
        self.assertRedirects(response, reverse('registration:pin_shoot'))
        reg = Pin_shoot.objects.all()
        self.assertEquals(len(reg), 1)
        self.assertEquals(reg[0].club, self.shoot_record['club'])
        self.assertEquals(reg[0].wpa_membership_number, self.shoot_record['wpa_membership_number'])
