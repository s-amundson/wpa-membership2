import csv
import os
import logging

from django.conf import settings
from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.datetime_safe import  date

from registration.models import Member, Joad_sessions, Joad_session_registration, Pin_shoot, Pin_scores


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
        # response = self.client.get(reverse('registration:pin_shoot'), follow=True)
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