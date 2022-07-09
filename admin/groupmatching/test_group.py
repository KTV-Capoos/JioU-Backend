from .enumerations import find_name, Ethnicity


def test_enum_string_parse_valid():
    """Test if the string parsing is correct"""
    assert find_name(
        Ethnicity,
        "Chinese",
        Ethnicity.Others
    ) == Ethnicity.Chinese, "Find_name is incorrect"

def test_string_parse_chinese_random_case():
    """Test if wrong casing will lead to correct cast for enum"""
    assert find_name(
        Ethnicity,
        "ChInEsE",
        Ethnicity.Others
    ) == Ethnicity.Chinese, "Find_name is incorrect"

def test_enum_string_parse_others():
    """Test if the string parsing is correct"""
    assert find_name(
        Ethnicity,
        "Eurasian",
        Ethnicity.Others
    ) == Ethnicity.Others, "Find_name is incorrect"
