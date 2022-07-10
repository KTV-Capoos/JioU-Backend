import numpy as np
from django.test import TestCase

# Create your tests here.
from .enumerations import find_name, Ethnicity
from .kmeans import kMeans


class KMeansTest(TestCase):
    def setUp(self) -> None:
        """Set up the testing set"""
        test_data = np.zeros((16, 4))
        test_data[0:4, :] = 30.0
        test_data[4:8, :] = 60.0
        test_data[8:12, :] = 90.0
        test_data[12:, :] = 120.0
        self.test_vector1 = test_data
        self.test_user_id = np.array([30.0, 60.0, 90.0, 120.0])

    def test_kMeans_valid(self):
        print("hi")
        assert len(kMeans(self.test_vector1, 1, 2)) == 4



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

    
