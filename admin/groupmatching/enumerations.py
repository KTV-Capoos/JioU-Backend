from enum import Enum
from typing import Any, Optional


def find_name(enum: Enum, name: str, default: Any = None) -> Optional[int]:
    """Find the int value of a name in an enum."""
    name = name.title()
    try:
        return enum[name]
    except KeyError:
        return default


class Ethnicity(Enum):
    Chinese = 1
    Malay = 2
    Indian = 3
    Others = 4


class Religion(Enum):
    Buddhist = 1
    Christian = 2
    Muslim = 3
    Taoist = 4
    Hindu = 5
    AReligious = 6
    Others = 7


class Nationality(Enum):
    Singaporean = 1
    Others = 2

class Gender(Enum):
    Male = 1
    Female = 2
    Others = 3


class AgeRange():
    thresholds = [25, 35, 50]
    # 18

    @classmethod
    def valueToName(cls, age):
        if age < 18:
            return -10
        for i in range(len(cls.thresholds)):
            if age <= AgeRange.thresholds[i]:
                return i+1
        return len(AgeRange.thresholds) + 1
