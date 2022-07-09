from enum import Enum
class Ethnicity(Enum):
    Chinese = 1
    Malay = 2
    Indian = 3
    Others = 4

    @classmethod
    def valueToName(cls, name):
        name = name.lower().capitalise()
        for i in cls:
            if name == i.name:
                return i.value
        return Ethnicity.Others.value

class Religion(Enum):
    Buddhist = 1
    Christian = 2
    Muslim = 3
    Taoist = 4
    Hindu = 5
    AReligious = 6
    Others = 7

    @classmethod
    def valueToName(cls, name):
        for i in cls:
            if name == i.name:
                return i.value
        return Religion.Others.value

class Nationality(Enum):
    Singaporean = 1
    Others = 2

    @classmethod
    def valueToName(cls, name):
        name = name.lower().capitalise()
        for i in cls:
            if name == i.name:
                return i.value
        return Nationality.Others.value


class Gender(Enum):
    Male = 1
    Female = 2
    Others = 3

    @classmethod
    def valueToName(cls, name):
        name = name.lower().capitalise()
        for i in cls:
            if name == i.name:
                return i.value
        return Gender.Others.value

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

