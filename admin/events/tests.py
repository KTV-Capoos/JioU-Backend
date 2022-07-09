from django.contrib.auth.models import User
from django.test import Client, TestCase

from .models import Event


# Create your tests here.
class EventTest(TestCase):
    def setUp(self) -> None:
        """Set up the test client"""
        self.client = Client()
        User.objects.create_user(username="admin", password="password")
        self.test_event1: Event = Event.objects.create(
            event_name="Test Event",
            event_description="Test description",
            event_date="2023-01-01",
            event_time="00:00:00",
            event_duration=1,
            event_limit=10,
            event_location="Test location",
            event_category="Test category",
            event_price=10000,
        )
        self.test_event2: Event = Event.objects.create(
            event_name="Test Event 2",
            event_description="Test description 2",
            event_date="2023-01-02",
            event_time="00:00:00",
            event_duration=1,
            event_location="Test location 2",
            event_category="Test category",
            event_limit=10,
            event_price=1000,
        )

    def login(self) -> None:
        """Login to the server"""
        credentials = {
            "username": "admin",
            "password": "password",
        }
        response = self.client.post("/auth/login/", credentials)
        self.assertEqual(response.status_code, 200, response)

    def test_all_event_no_login(self) -> None:
        """Test retrieve all events"""
        response = self.client.get("/events/")
        self.assertEqual(response.status_code, 401)

    def test_all_events(self) -> None:
        """Test retrieve all events"""
        self.login()
        response = self.client.get("/events/")
        self.assertEqual(response.status_code, 200)
        expected = {
            "events": [
                self.test_event1.toCardDict(),
                self.test_event2.toCardDict(),
            ]
        }
        self.assertEqual(response.json(), expected)

    def test_event_id_found_no_login(self) -> None:
        """Test event details"""
        response = self.client.get("/events/1")
        self.assertEqual(response.status_code, 401)

    def test_event_id_found(self) -> None:
        """Test event details"""
        self.login()
        response = self.client.get("/events/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.test_event1.toDict())

    def test_event_id_not_found_no_login(self) -> None:
        """Test event details"""
        response = self.client.get("/events/33333333333")
        self.assertEqual(response.status_code, 401)

    def test_event_id_not_found(self) -> None:
        """Test event details"""
        self.login()
        response = self.client.get("/events/33333333333")
        self.assertEqual(response.status_code, 404)
