from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.datetime_safe import datetime, date
from .models import Member, Family, Joad_sessions, Joad_session_registration


# Create your tests here.

# TODO create tests for registration validation.


class MemberModelTests(TestCase):
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
               'terms':True}
    def test_add_member(self):
        # submit a registration to be added.
        response = self.client.post(reverse('registration:register'), self.mem, follow=True)
        self.assertRedirects(response, reverse('registration:register'))
        self.assertEquals(len(Member.objects.all()), 1)
        # TODO test session clear


    def test_duplicate_member(self):
        # submit a registration to be added.
        response = self.client.post(reverse('registration:register'), self.mem, follow=True)
        self.assertRedirects(response, reverse('registration:register'))
        # resubmit a registration to test duplication.
        response = self.client.post(reverse('registration:register'), self.mem, follow=True)

        with self.assertTemplateUsed('registration/message.html'):
            render_to_string('registration/message.html')
        self.assertEquals(len(Member.objects.all()), 1)
        # TODO test session clear


    def test_invalid_level(self):
        # if javascript is off then the form could be submitted with and invalid value.
        self.mem['level'] = 'invalid'
        response = self.client.post(reverse('registration:register'), self.mem, follow=True)

        with self.assertTemplateUsed('registration/message.html'):
            render_to_string('registration/message.html')

        # TODO test session clear


    def test_joad_session_good(self):
        d = date.fromisoformat("2020-04-18")
        js = Joad_sessions(start_date=d, state='open')
        js.save()
        self.mem['joad'] = "2020-04-18"
        self.mem['dob'] = '2010-03-12'
        response = self.client.post(reverse('registration:register'), self.mem, follow=True)
        self.assertRedirects(response, reverse('registration:register'))
        mem = Member.objects.all()
        self.assertEquals(len(mem), 1)
        # self.assertEquals(Member.objects.get(pk=1).joad, d)
        jsr = Joad_session_registration.objects.filter(mem=mem[0])
        self.assertEquals(len(jsr), 1)
        # TODO test session clear



    def test_joad_session_to_old(self):
        d = date.fromisoformat("2020-04-18")
        js = Joad_sessions(start_date=d, state='open')
        js.save()
        self.mem['joad'] = "2020-04-18"
        response = self.client.post(reverse('registration:register'), self.mem, follow=True)
        self.assertRedirects(response, reverse('registration:register'))
        mem = Member.objects.all()
        self.assertEquals(len(mem), 1)
        # self.assertEquals(Member.objects.get(pk=1).joad, d)
        jsr = Joad_session_registration.objects.filter(mem=mem[0])
        self.assertEquals(len(jsr), 0)
        # TODO test session clear
