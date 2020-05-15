import sys
import time
import pdb

from django.conf import settings
from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.datetime_safe import datetime, date
from registration.models import Member, Family, Joad_sessions, Joad_session_registration, Pin_shoot
from django.test import LiveServerTestCase
# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver


import logging

from selenium.webdriver.support.select import Select

logger = logging.getLogger(__name__)

logging.debug(f"DEBUG= {settings.DEBUG}, EMAIL_DEBUG= {settings.EMAIL_DEBUG}")
# Create your tests here.

# class Temporary_Tests(TestCase):
class PinShootTests(LiveServerTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entry_data = {'first_name': 'Emily',
                           'last_name': 'Conlan',
                           'club':'',
                           'shoot_date': date.today().isoformat(),
                           'email': 'EmilyNConlan@einrot.com',
                           'wpa_membership_number':'',
                           'score': 52}

        self.select_data = {'category': 'JOAD Indoor',
                            'bow': 'Barebow/Basic Compound/Traditional',
                            'distance': '9',
                            'target': '60',
                            'prev_stars': '0'}
        self.click_data = {'terms': True}
        self.url = 'http://127.0.0.1:8000/registration/pin_shoot/'
        self.bow_choices = {'':'---------',
                            'barebow':'Barebow/Basic Compound/Traditional',
                            'olympic': 'Olympic Recurve',
                            'compound': 'Compound',
                            }

        self.distance_choices = {'': '---------', '18': 18, '9': 9}
        self.target_choices = {'': '---------', '60': 60, '40': 40}
        self.prev_stars_choices = {'': '---------', '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6}




    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super().tearDownClass()

    def enter_items(self, entry_data, select_data):
        self.selenium.get(self.url)
        for k, v in entry_data.items():
            e = self.selenium.find_element_by_id('id_' + k)
            e.send_keys(v)

        for k, v in select_data.items():
            e = Select(self.selenium.find_element_by_id('id_' + k))
            e.select_by_visible_text(v)



    # def test_pin_shoot_invalid_entry(self):
    #     keys = list(self.entry_data.keys())
    #     for k in keys:
    #         sr = self.entry_data.copy()
    #         sr.pop(k)
    #         self.enter_items(sr, self.select_data)
    #         e = self.selenium.find_element_by_id('id_submit')
    #         e.click()
    #         self.assertEquals(len(Pin_shoot.objects.all()), 0)
    #
    #     keys = list(self.select_data.keys())
    #     for k in keys:
    #         sr = self.select_data.copy()
    #         sr.pop(k)
    #         self.enter_items(self.entry_data, sr)
    #         e = self.selenium.find_element_by_id('id_submit')
    #         e.click()
    #         self.assertEquals(len(Pin_shoot.objects.all()), 0)
    #
    #     # self.enter_items(self.entry_data, sr)
    #     #
    #     # # e = self.selenium.find_element_by_id('id_terms')
    #     # # self.selenium.execute_script("arguments[0].click();", e)
    #     #
    #     # e = self.selenium.find_element_by_id('id_submit')
    #     # e.click()
    #     # self.assertEquals(len(Pin_shoot.objects.all()), 0)

    # def test_pin_shoot_valid_entry(self):
    #     self.enter_items(self.entry_data, self.select_data)
    #
    #     e = self.selenium.find_element_by_id('id_submit')
    #     e.click()
    #     time.sleep(5)
    #     self.assertEquals(len(Pin_shoot.objects.all()), 1)

    def test_entry(self):
        print(Pin_shoot.objects.all())







