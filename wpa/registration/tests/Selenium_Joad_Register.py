from registration.models import Member, Family, Joad_sessions, Joad_session_registration, Pin_shoot
from django.test import LiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.select import Select

import logging

logger = logging.getLogger(__name__)


# Create your tests here.

class SeleniumJoadRegisterTests(LiveServerTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.entry_data = {'first_name': 'Emily',
                           'last_name': 'Conlan',
                           'email': 'EmilyNConlan@einrot.com'}
        # 'level': 'standard',
        # 'terms': True
        self.select_data = {'joad': '2020-04-19'}
        self.click_data = {'terms': True}
        self.url = 'http://127.0.0.1:8000/registration/joad_registration/'

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

        e = self.selenium.find_element_by_id('id_terms')
        self.selenium.execute_script("arguments[0].click();", e)


    def test_joad_registration_invalid_entry(self):
        keys = list(self.entry_data.keys())
        for k in keys:
            sr = self.entry_data.copy()
            sr.pop(k)
            self.enter_items(sr, self.select_data)
            e = self.selenium.find_element_by_id('id_submit')
            e.click()
            self.assertEquals(len(Member.objects.all()), 0)

        keys = list(self.select_data.keys())
        for k in keys:
            sr = self.select_data.copy()
            sr.pop(k)
            self.enter_items(self.entry_data, sr)
            e = self.selenium.find_element_by_id('id_submit')
            e.click()
            self.assertEquals(len(Member.objects.all()), 0)

        self.enter_items(self.entry_data, sr)

        e = self.selenium.find_element_by_id('id_terms')
        self.selenium.execute_script("arguments[0].click();", e)

        e = self.selenium.find_element_by_id('id_submit')
        e.click()
        self.assertEquals(len(Member.objects.all()), 0)