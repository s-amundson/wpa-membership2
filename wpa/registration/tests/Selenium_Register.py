from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

import logging
logger = logging.getLogger(__name__)

# Create your tests here.

# TODO create tests for registration validation.


class MySeleniumTests(LiveServerTestCase):
    # fixtures = ['user-data.json']
    self.entry_data = {'first_name': 'Emily',
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
    self.click_data = {'benefactor': True, 'terms': True}
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)


    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_registration(self):
        valid_style = 'border: 3px solid Green;'
        invalid_style = 'border: 3px solid Tomato;'
        self.selenium.get('%s%s' % (self.live_server_url, '/registration/register/'))
        for k,v in self.entry_data:
            e = self.selenium.find_element_by_id(k)
            e.send_keys(v)
            assert(e.get_attribute('style', valid_style)


        username_input = self.selenium.find_element_by_id("first_name")
        username_input.send_keys(self.entry_data['first_name'])
        password_input = self.selenium.find_element_by_name("last_name")
        password_input.send_keys(self.entry_data['last_name'])
        self.selenium.find_element_by_name('benefactor').click()




