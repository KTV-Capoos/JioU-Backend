from datetime import datetime, timedelta
from typing import List

from .enumerations import find_name, Ethnicity, Religion, Gender, Nationality, AgeRange

from ..events.models import Event
from ..attendance.models import Attendance


def knn_endpoint() -> None:
    events = Event.objects.filter(
        event_date__lte=datetime.now().date + timedelta(days=3),
        event_date__gte=datetime.now()
    ).all()
    for event in events:
        event_attendance: List[Attendance] = Attendance.objects.filter(
            event=event).all()
        participants = [
            participant.user.toDict() for participant in map(lambda x: x.user, event_attendance)
        ]
        print(participants)


def yearsago(years, from_date=None):
    if from_date is None:
        from_date = datetime.now()
    try:
        return from_date.replace(year=from_date.year - years)
    except ValueError:
        # Must be 2/29!
        assert from_date.month == 2 and from_date.day == 29  # can be removed
        return from_date.replace(month=2, day=28,
                                 year=from_date.year-years)


def num_years(begin, end=None):
    if end is None:
        end = datetime.now()
    num_years = int((end - begin).days / 365.2425)
    if begin > yearsago(num_years, end):
        return num_years - 1
    else:
        return num_years


def response_to_vect(data: dict) -> tuple[int, list]:
    '''Assume data given is json or dict data'''
    vect = []
    user_id = data['user_id']
    vect.append(find_name(
        Ethnicity,
        data['ethnicity'],
        Ethnicity.Others
    ))
    vect.append(find_name(
        Religion,
        data['religion'],
        Religion.Others
    ))
    vect.append(find_name(
        Gender,
        data['gender'],
        Gender.Others
    ))
    vect.append(find_name(
        Nationality,
        data['nationality'],
        Nationality.Others
    ))
    # Assume this is datetime data
    vect.append(AgeRange.valueToName(yearsago(data['dob'], datetime.now())))
    return user_id, vect
