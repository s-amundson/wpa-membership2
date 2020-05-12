import csv

from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.datetime_safe import datetime, date

from .models import Pin_scores
from views import calculate_pins
# from registration.models import Member, Family, Joad_sessions, Joad_session_registration

import logging

logger = logging.getLogger(__name__)


# Create your tests here.

class Temporary_Tests(TestCase):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     logging.debug('init')
    #     with open('pins.csv', 'r') as csvfile:
    #         reader = csv.DictReader(csvfile)
    #         for row in reader:
    #             print(row)
    #             Pin_scores(category=row['category'],
    #                        bow=row['bow'],
    #                        distance=row['distance'],
    #                        target=row['target'],
    #                        score=row['score'],
    #                        stars=row['stars']).save()

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        logging.debug('init')
        # with open('pins.csv', 'r') as csvfile:
        #     reader = csv.DictReader(csvfile)
        #     for row in reader:
        #         print(row)
        #         Pin_scores(category=row['category'],
        #                    bow=row['bow'],
        #                    distance=row['distance'],
        #                    target=row['target'],
        #                    score=row['score'],
        #                    stars=row['stars']).save()
    def test_equal(self):
        self.assertEqual(1, 1)
    #     self.mem = {'first_name': 'Emily',
    #                 'last_name': 'Conlan',
    #                 'street': "1984 Jones Avenue",
    #                 'city': 'Hays',
    #                 'state': 'NC',
    #                 'post_code': 28635,
    #                 'phone': '336-696-6307',
    #                 'email': 'EmilyNConlan@einrot.com',
    #                 'dob': '1995-03-12',
    #                 'level': 'standard',
    #                 'terms': True}
    #
    #
    # def add_member(self):
    #     # submit a registration to be added.
    #     response = self.client.post(reverse('registration:register'), self.mem, follow=True)
    #     session = self.client.session
    #     self.assertRedirects(response, reverse('registration:register'))
    #     self.assertEquals(len(Member.objects.all()), 1)
    #     self.assertEquals(len(session.items()), 0)
    #
    # def test_joad_register_invalid_request_method(self):
    #     response = self.client.put(reverse('registration:register'))
    #     self.assertEqual(response.status_code, 404)
    #
    #     response = self.client.delete(reverse('registration:register'))
    #     self.assertEqual(response.status_code, 404)

    def test_calculate_pins(self):
        parameters = [
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 9, 'target': 60, 'score': 39, 'stars': 0},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 9, 'target': 60, 'score': 40, 'stars': 1},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 9, 'target': 60, 'score': 74, 'stars': 1},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 9, 'target': 60, 'score': 75, 'stars': 2},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 9, 'target': 60, 'score': 109, 'stars': 2},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 9, 'target': 60, 'score': 110, 'stars': 3},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 9, 'target': 60, 'score': 144, 'stars': 3},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 9, 'target': 60, 'score': 145, 'stars': 4},

            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 29, 'stars': 0},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 30, 'stars': 2},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 49, 'stars': 2},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 50, 'stars': 3},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 99, 'stars': 3},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 100, 'stars': 4},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 139, 'stars': 4},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 140, 'stars': 5},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 184, 'stars': 5},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 185, 'stars': 6},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 229, 'stars': 6},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 230, 'stars': 7},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 254, 'stars': 7},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 255, 'stars': 8},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 264, 'stars': 8},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 265, 'stars': 9},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 274, 'stars': 9},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 275, 'stars': 10},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 279, 'stars': 10},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 60, 'score': 280, 'stars': 11},

            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 174, 'stars': 0},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 175, 'stars': 6},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 219, 'stars': 6},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 220, 'stars': 7},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 239, 'stars': 7},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 240, 'stars': 8},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 249, 'stars': 8},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 250, 'stars': 9},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 259, 'stars': 9},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 260, 'stars': 10},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 269, 'stars': 10},
            {'category': 'joad_indoor', 'bow': 'barebow', 'distance': 18, 'target': 40, 'score': 270, 'stars': 11},

            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 9, 'target': 60, 'score': 49, 'stars': 0},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 9, 'target': 60, 'score': 50, 'stars': 1},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 9, 'target': 60, 'score': 99, 'stars': 1},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 9, 'target': 60, 'score': 100, 'stars': 2},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 9, 'target': 60, 'score': 149, 'stars': 2},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 9, 'target': 60, 'score': 150, 'stars': 3},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 9, 'target': 60, 'score': 199, 'stars': 3},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 9, 'target': 60, 'score': 200, 'stars': 4},

            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 29, 'stars': 0},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 30, 'stars': 2},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 49, 'stars': 2},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 50, 'stars': 3},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 99, 'stars': 3},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 100, 'stars': 4},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 149, 'stars': 4},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 150, 'stars': 5},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 199, 'stars': 5},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 200, 'stars': 6},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 249, 'stars': 6},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 250, 'stars': 7},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 269, 'stars': 7},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 270, 'stars': 8},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 284, 'stars': 8},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 285, 'stars': 9},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 289, 'stars': 9},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 290, 'stars': 10},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 294, 'stars': 10},
            {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 295, 'stars': 11},
        ]

        # with open('tests/pins.csv') as csvfile:
        #     reader = csv.DictReader(csvfile)
        #     for p in reader:
        #         c = calculate_pins(p)
        #         print(c)
        #         self.assertEqual(c, p['stars'])

        for p in parameters:
            c = calculate_pins(p)
            print(c)
            self.assertEqual(c, p['stars'])
