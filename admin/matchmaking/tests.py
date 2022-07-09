from django.test import TestCase

# Create your tests here.
from .enumerations import find_name, Ethnicity


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
