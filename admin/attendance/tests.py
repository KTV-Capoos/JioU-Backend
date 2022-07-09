from attendance.models import Attendance
from auth_backend.models import User
from django.test import TestCase
from events.models import Event


# Create your tests here.
class AttendanceTestCase(TestCase):
    def setUp(self: "AttendanceTestCase") -> None:
        """Set up the test cases"""
        self.user = User.objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.user2 = User.objects.create_user(
            username="test_user2",
            password="test_password",
        )
        self.updated_event = Event.objects.create(
            event_name="Test Event",
            event_description="Test Event Description",
            event_limit=1,
            event_date="2023-01-01",
            event_time="00:00:00",
            event_duration=1,
            event_location="Test location",
            event_price=10000,
        )

        self.old_event = Event.objects.create(
            event_name="Test Event",
            event_description="Test Event Description",
            event_limit=10,
            event_date="2019-01-01",
            event_time="00:00:00",
            event_duration=1,
            event_location="Test location",
            event_price=10000,
        )

    def login(self: "AttendanceTestCase") -> None:
        """Log the user in"""
        self.client.login(username="test_user", password="test_password")

    def test_get_empty_user_participating(self: "AttendanceTestCase") -> None:
        """Test the get_user_participating view"""
        self.login()
        response = self.client.get("/attendance/my_events")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["events"], [])

    def test_get_user_participating(self: "AttendanceTestCase") -> None:
        """Test the get_user_participating view"""
        self.login()
        Attendance.objects.create(
            user=self.user,
            event=self.updated_event,
        )
        response = self.client.get("/attendance/my_events")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["events"]), 1)
        self.assertEqual(response.json()["events"][0]["event_name"], "Test Event")

    def test_add_user_participating(self: "AttendanceTestCase") -> None:
        """Test the add_user_participating view"""
        self.login()
        response = self.client.post(f"/attendance/{self.updated_event.event_id}/join")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertTrue(
            Attendance.objects.filter(
                user=self.user,
                event=self.updated_event,
            ).exists()
        )

    def test_add_user_to_non_existent_event(self: "AttendanceTestCase") -> None:
        """Test the add_user_participating view"""
        self.login()
        response = self.client.post(f"/attendance/3000/join")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"], "Event not found")

    def test_add_user_to_old_event(self: "AttendanceTestCase") -> None:
        """Test the add_user_participating view"""
        self.login()
        response = self.client.post(f"/attendance/{self.old_event.event_id}/join")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Event already happened")

    def test_add_user_to_already_joined_event(self: "AttendanceTestCase") -> None:
        """Test the add_user_participating view"""
        self.login()
        Attendance.objects.create(
            user=self.user,
            event=self.updated_event,
        )
        response = self.client.post(f"/attendance/{self.updated_event.event_id}/join")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "User already participating")

    def test_add_user_to_full_event(self: "AttendanceTestCase") -> None:
        """Add user to full event view"""
        self.login()
        Attendance.objects.create(
            user=self.user2,
            event=self.updated_event,
        )
        response = self.client.post(f"/attendance/{self.updated_event.event_id}/join")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Event is full")
