from django.contrib.auth.models import User
from django.test import TestCase


# Create your tests here.
class AuthTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="admin", password="password")

    def test_login_success(self):
        response = self.client.post(
            "/auth/login/",
            {
                "username": "admin",
                "password": "password",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True})

    def test_login_fail(self):
        response = self.client.post(
            "/auth/login/",
            {
                "username": "admin",
                "password": "wrong",
            },
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                "error": "Invalid username or password"
            }
        )

    def test_logout(self):
        self.client.login(username="admin", password="password")
        response = self.client.post("/auth/logout/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True})

    def test_signup(self):
        response = self.client.post(
            "/auth/signup/",
            {
                "username": "admin1",
                "password": "password123",
                "email": 'test@test.com',
                "gender": "test",
                "dob": "2000-10-06",
                "mobile_number": "test",
                "nok": "test",
                "religion": "test",
                "nationality": "test",
                "ethnicity": "test",
                "medical_conditions": "medical_conditions",
                "allergies": "allergies",
                "dietary_restrictions": "dietary_restrictions",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True})
        response = self.client.post(
            "/auth/login/",
            {
                "username": "admin1",
                "password": "password123",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True})

    def test_signup_alr_exists(self):
        response = self.client.post(
            "/auth/signup/",
            {
                "username": "admin",
                "password": "password",
                "gender": "test",
                "email": 'test@test.com',
                "dob": "2000-10-06",
                "mobile_number": "test",
                "nok": "test",
                "religion": "test",
                "nationality": "test",
                "ethnicity": "test",
                "medical_conditions": "medical_conditions",
                "allergies": "allergies",
                "dietary_restrictions": "dietary_restrictions",
            },
        )
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(), {"error": "Username already exists"})
