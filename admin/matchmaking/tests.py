import random

import numpy as np
from django.test import TestCase

# Create your tests here.
from sklearn.datasets import make_blobs

from .enumerations import find_name, Ethnicity
from .kmeans import kMeans, kmeans_elbow, random_swap, distribute_groups


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
