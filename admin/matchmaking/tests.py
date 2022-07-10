import random

import numpy as np
from django.contrib.auth.models import User
from django.test import TestCase, Client

# Create your tests here.
from sklearn.datasets import make_blobs

from .enumerations import find_name, Ethnicity
from .kmeans import kMeans, kmeans_elbow, random_swap, distribute_groups
from ..events.models import Event


class AuthTest():
    def setUp(self) -> None:
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
        response = self.client.post()
        self.assertEqual(response.status_code, 401)


class KMeansTest(TestCase):
    def setUp(self) -> None:
        """Set up the testing set"""
        X, y = make_blobs(
            n_samples=200, n_features=5,
            centers=4, cluster_std=0.3,
            shuffle=True, random_state=0
        )

        self.test_valid_vector1 = X
        self.test_user_id = np.arange(0, len(y))

        # set randomness to a reproducible seed value
        np.random.seed(0)
        random.seed(0)

    def test_kMeans_elbow_valid(self):
        self.assertEqual(len(set(kmeans_elbow(self.test_valid_vector1, 9))), 3)  # conservative estimate

    def test_kMeans_elbow_zero(self):
        self.assertEqual(len(set(kmeans_elbow(self.test_valid_vector1, 1))), 1)  # conservative estimate

    def test_random_swap(self):
        test1 = [[1, 2, 3, 4], [5, 6, 7, 8]]
        random_swap(test1, 0, 1)
        expected1 = [[8, 2, 3, 4], [5, 6, 7, 1]]
        self.assertEqual(test1, expected1)

    def test_distribute_group_all_group(self):
        singleValue = np.zeros(10)
        self.assertEqual(len(distribute_groups(singleValue, 5, 0)), 2)
        # self.assertRaises(ZeroDivisionError, distribute_groups(singleValue, 0, 0))
        rangedValues = np.arange(10)
        # wrong remain value is protected against
        self.assertEqual(len(distribute_groups(rangedValues, 1, 1)), 10)



class EnumTest(TestCase):
    def test_enum_string_parse_valid(self):
        """Test if the string parsing is correct"""
        assert find_name(
            Ethnicity,
            "Chinese",
            Ethnicity.Others
        ) == Ethnicity.Chinese, "Find_name is incorrect"

    def test_string_parse_chinese_random_case(self):
        """Test if wrong casing will lead to correct cast for enum"""
        assert find_name(
            Ethnicity,
            "ChInEsE",
            Ethnicity.Others
        ) == Ethnicity.Chinese, "Find_name is incorrect"

    def test_enum_string_parse_others(self):
        """Test if the string parsing is correct"""
        assert find_name(
            Ethnicity,
            "Eurasian",
            Ethnicity.Others
        ) == Ethnicity.Others, "Find_name is incorrect"
