from django.test import TestCase, Client

# Create your tests here.
class EventTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_all_events(self):
        """Test retrieve all events"""
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)