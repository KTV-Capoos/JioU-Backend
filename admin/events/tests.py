from django.test import TestCase, Client

# Create your tests here.
class EventTest(TestCase):
    def setUp(self):
        """Set up the test client"""
        self.client = Client()

    def test_all_events(self):
        """Test retrieve all events"""
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)

    def test_event_id(self):
        """Test event details"""
        response = self.client.get('/events/1')
        self.assertEqual(response.status_code, 200)