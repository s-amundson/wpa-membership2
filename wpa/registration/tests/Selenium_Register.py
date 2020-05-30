import json
import logging
import os
import sys
import time

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from registration.models import Joad_sessions

from selenium.webdriver.chrome.webdriver import WebDriver
# from selenium.webdriver.firefox.webdriver import WebDriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

logger = logging.getLogger(__name__)


# Create your tests here.

class SeleniumRegisterTests(StaticLiveServerTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        path = os.path.join(settings.BASE_DIR, 'registration', 'fixtures', 'registration_fixture.json')
        logging.debug(path)
        with open(path) as f:
            self.member_data = json.load(f)
        self.member_items = ['first_name', 'last_name', f'dob']
        self.membership_items = ['street', 'city', 'state', 'post_code', 'phone', 'email']
        self.url = 'http://127.0.0.1:8000/registration/register/'


    @classmethod
    def setUpClass(self):
        super().setUpClass()
        logging.debug('setup')
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)
        Joad_sessions.objects.create(start_date="2020-05-15", state="open")

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super().tearDownClass()


    def enter_items(self, member):
        forms = int(member['member_set-TOTAL_FORMS'][0])
        for mem in range(forms):
            # items = [f'member_set-{mem}-first_name', f'member_set-{mem}-last_name', f'member_set-{mem}-dob']
            for i in self.member_items:
                e = self.selenium.find_element_by_id(f'id_member_set-{mem}-' + i)
                e.send_keys(member[f'member_set-{mem}-' + i][0] + Keys.TAB)

            if member[f'member_set-{mem}-joad'][0] != "":
                e = Select(self.selenium.find_element_by_id(f'id_member_set-{mem}-joad'))
                e.select_by_value(member[f'member_set-{mem}-joad'][0])
            if forms > mem + 1:
                # click on add member
                self.selenium.find_element_by_id('id_btn_add_row').click()

        for i in self.membership_items:
            e = self.selenium.find_element_by_id('id_' + i)
            e.send_keys(member[i][0])

        # e = self.selenium.find_element_by_id('id_level')
        e = Select(self.selenium.find_element_by_id('id_level'))
        e.select_by_value(member['level'][0])

        if member.get('benefactor', None) == ['on']:
            e = self.selenium.find_element_by_id('id_benefactor')
            self.selenium.execute_script("arguments[0].click();", e)

        e = self.selenium.find_element_by_id('id_terms')
        self.selenium.execute_script("arguments[0].click();", e)


    def test_enter_items(self):
        for member in self.member_data:
            self.selenium.get('%s%s' % (self.live_server_url, '/registration/register/'))
            self.enter_items(member)
            h = self.selenium.find_element_by_id('cost').get_attribute('innerHTML')
            logging.debug(h)
            self.assertHTMLEqual(h, f"Total Cost: {member['cost'][0]}")
            self.selenium.find_element_by_id('id_submit').click()


    def test_registration_invalid_entry(self):
        member_items = self.member_items.copy()
        membership_items = self.membership_items.copy()

        for i in range(len(member_items)):
            self.selenium.get('%s%s' % (self.live_server_url, '/registration/register/'))
            self.member_items = member_items.copy()
            self.member_items.pop(i)
            self.enter_items(self.member_data[0])
            self.selenium.find_element_by_id('id_submit').click()

            e = self.selenium.find_element_by_id(f'id_member_set-0-' + member_items[i])
            a = self.selenium.switch_to.active_element
            self.assertEquals(a, e)
            a.send_keys(Keys.TAB)
            h = e.get_attribute('style')
            self.assertEquals(h, 'border: 3px solid tomato;')

        self.member_items = member_items
        for i in range(len(membership_items)):
            self.selenium.get('%s%s' % (self.live_server_url, '/registration/register/'))
            self.membership_items = membership_items.copy()
            self.membership_items.pop(i)
            self.enter_items(self.member_data[0])
            self.selenium.find_element_by_id('id_submit').click()

            e = self.selenium.find_element_by_id(f'id_' + membership_items[i])
            logging.debug(e.get_property('id'))
            a = self.selenium.switch_to.active_element
            self.assertEquals(a, e)
            a.send_keys(Keys.TAB)
            h = e.get_attribute('style')
            self.assertEquals(h, 'border: 3px solid tomato;')



