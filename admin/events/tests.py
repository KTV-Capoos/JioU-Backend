from typing import Any
from django.test import TestCase, Client
from json import loads, dumps

from .models import Event


# Create your tests here.
class EventTest(TestCase):
    def setUp(self):
        """Set up the test client"""
        self.client = Client()
        self.test_event1: Event = Event.objects.create(
            event_name='Test Event',
            event_description='Test description',
            event_date='2023-01-01',
            event_time='00:00:00',
            event_duration=1,
            event_location='Test location',
            event_price=10000,
        )
        self.test_event2: Event = Event.objects.create(
            event_name='Test Event 2',
            event_description='Test description 2',
            event_date='2023-01-02',
            event_time='00:00:00',
            event_duration=1,
            event_location='Test location 2',
            event_price=1000,
        )

    def test_all_events(self):
        """Test retrieve all events"""
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)
        expected = {'events': [
            self.test_event1.toCardDict(),
            self.test_event2.toCardDict(),
        ]}
        self.assertEqual(response.json(), expected)

    def test_event_id_found(self):
        """Test event details"""
        response = self.client.get('/events/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.test_event1.toDict())

    def test_event_id_not_found(self):
        """Test event details"""
        response = self.client.get('/events/33333333333')
        self.assertEqual(response.status_code, 404)
