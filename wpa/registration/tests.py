import csv
import os
from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.datetime_safe import datetime, date

from django.conf import settings
from .models import Pin_scores
from views import calculate_pins
# from registration.models import Member, Family, Joad_sessions, Joad_session_registration

import logging

logger = logging.getLogger(__name__)

path = os.path.join(settings.BASE_DIR, 'wpa', 'pins.csv')
logging.debug(path)
# logging.debug(os.getcwd())
# Create your tests here.

class Temporary_Tests(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        with open(path, 'r') as csvfile:
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


