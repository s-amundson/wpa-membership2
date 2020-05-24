import logging
import time

from django.test import LiveServerTestCase
from registration.models import Member

from selenium.webdriver.chrome.webdriver import WebDriver
# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.select import Select

logger = logging.getLogger(__name__)


# Create your tests here.

class SeleniumRegisterTests(LiveServerTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entry_data = {'first_name': 'Emily',
                           'last_name': 'Conlan',
                           'street': "1984 Jones Avenue",
                           'city': 'Hays',
                           'state': 'NC',
                           'post_code': "28635",
                           'phone': '336-696-6307',
                           'email': 'EmilyNConlan@einrot.com',
                           'dob': '1995-03-12'}

        self.select_data = {'level': 'Standard'}
        self.click_data = {'benefactor': True, 'terms': True}
        self.url = 'http://127.0.0.1:8000/registration/register/'
        self.enter_items(self.entry_data, self.select_data)

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        logging.debug('setup')
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super().tearDownClass()


    def enter_items(self, entry_data, select_data):
        self.setUpClass()

        # self.selenium.get('%s%s' % (self.live_server_url, '/registration/register/'))
        self.selenium.get(self.url)
        time.sleep(10)


        member = ['street', 'city', 'state', 'post_code', 'phone', 'email']
        # for k, v in select_data.items():
        for i in member:
            e = self.selenium.find_element_by_id('id_' + i)
            e.send_keys(entry_data[i])

        for k, v in select_data.items():
            e = Select(self.selenium.find_element_by_id('id_' + k))
            e.select_by_visible_text(v)

        member = ["fist_name", "last_name", 'dob']
        for i in member:
            e = self.selenium.find_element_by_id('member_set-0-' + i)
            e.send_keys(entry_data[i])

        e = self.selenium.find_element_by_id('id_terms')
        self.selenium.execute_script("arguments[0].click();", e)
        time.sleep(5)

    def test_enter_items(self):
        self.enter_items(self.entry_data, self.select_data)

    # def test_costs(self):
    #     # self.selenium.get('%s%s' % (self.live_server_url, '/registration/register/'))
    #     self.selenium.get(self.url)
    #     dob = self.selenium.find_element_by_id('id_dob')
    #     level = Select(self.selenium.find_element_by_id('id_level'))
    #     joad = Select(self.selenium.find_element_by_id('id_joad'))
    #     benefactor = self.selenium.find_element_by_id('id_benefactor')
    #     costs = self.selenium.find_element_by_id('cost')
    #     cases = [{'level': 'Standard', 'dob': '2010-05-05', 'joad': None, 'cost': 20},
    #              {'level': 'JOAD', 'dob': '2010-05-05', 'joad': None, 'cost': 18},
    #              {'level': 'Family', 'dob': '2010-05-05', 'joad': None, 'cost': 40},
    #              {'level': 'Senior', 'dob': '1950-05-05', 'joad': None, 'cost': 18},
    #              {'level': 'Standard', 'dob': '2010-05-05', 'joad': '2020-04-19', 'cost': 20 + 95},
    #              {'level': 'JOAD', 'dob': '2010-05-05', 'joad': '2020-04-19', 'cost': 18 + 95},
    #              {'level': 'Family', 'dob': '2010-05-05', 'joad': '2020-04-19', 'cost': 40 + 95}]
    #
    #     for case in cases:
    #         dob.clear()
    #         dob.send_keys(case['dob'])
    #         level.select_by_visible_text(case['level'])
    #         if case['joad'] is not None:
    #             joad.select_by_visible_text(case['joad'])
    #         else:
    #             joad.select_by_visible_text("None")
    #         logging.debug(f"level = {case['level']}  html = {costs.get_attribute('innerHTML')}")
    #         self.assertEquals(f"Total Cost: {case['cost']}", costs.get_attribute('innerHTML'))
    #
    #     self.selenium.execute_script("arguments[0].click();", benefactor)
    #
    #     for case in cases:
    #         dob.clear()
    #         dob.send_keys(case['dob'])
    #         cost = 100
    #         level.select_by_visible_text(case['level'])
    #         if case['joad'] is not None:
    #             cost += 95
    #             joad.select_by_visible_text(case['joad'])
    #         else:
    #             joad.select_by_visible_text("None")
    #         logging.debug(f"level = {case['level']}  html = {costs.get_attribute('innerHTML')}")
    #         self.assertEquals(f"Total Cost: {cost}", costs.get_attribute('innerHTML'))

    # def test_registration_invalid_entry(self):
    #
    #     keys = list(self.entry_data.keys())
    #     for k in keys:
    #         sr = self.entry_data.copy()
    #         sr.pop(k)
    #         self.enter_items(sr, self.select_data)
    #         e = self.selenium.find_element_by_id('id_submit')
    #         e.click()
    #         self.assertEquals(len(Member.objects.all()), 0)
    #
    #     keys = list(self.select_data.keys())
    #     for k in keys:
    #         sr = self.select_data.copy()
    #         sr.pop(k)
    #         self.enter_items(self.entry_data, sr)
    #
    #     e = self.selenium.find_element_by_id('id_submit')
    #     e.click()
    #     time.sleep(2)
    #     self.assertEquals(len(Member.objects.all()), 0)
