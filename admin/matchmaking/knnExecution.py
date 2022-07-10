from datetime import datetime, timedelta
from typing import List
import numpy as np

from admin.matchmaking.knn import kMeans

from .enumerations import find_name, Ethnicity, Religion, Gender, Nationality, AgeRange
from ..auth_backend.models import UserInfo, User
from ..events.models import Event
from ..attendance.models import Attendance


def parse_user_to_format(user: User) -> dict[str, str]:
    """
    Returns a dict with keys
    - user_id
    - ethinicity
    - religion
    - gender
    - nationality
    - dob
    """
    user_info: UserInfo = UserInfo.objects.filter(user=user).get()
    return {
        'user_id': user.user_id,
        'ethnicity': user_info.ethnicity,
        'religion': user_info.religion,
        'gender': user_info.gender,
        'nationality': user_info.nationality,
        'dob': user_info.dob
    }


def knn_endpoint() -> List[List[int]]:
    events = Event.objects.filter(
        event_date__lte=datetime.now().date + timedelta(days=3),
        event_date__gte=datetime.now()
    ).all()
    for event in events:
        event_attendance: List[Attendance] = Attendance.objects.filter(
            event=event).all()
        participants = [
            response_to_vect(
                parse_user_to_format(participant)
            ) for participant in event_attendance
        ]
        ids, vectors = zip(*participants)
        userIds = np.array(ids)
        vectors = np.array(vectors)
        grouping = kMeans(vectors, 1, 5)
        finalgrouping = []
        for group in grouping:
            finalgrouping.append(userIds[group])

        return finalgrouping


def yearsago(years: int, from_date=None):
    if from_date is None:
        from_date = datetime.now()
    try:
        return from_date.replace(year=from_date.year - years)
    except ValueError:
        # Must be 2/29!
        assert from_date.month == 2 and from_date.day == 29  # can be removed
        return from_date.replace(month=2, day=28,
                                 year=from_date.year-years)


def num_years(begin: datetime, end=None):
    if end is None:
        end = datetime.now()
    num_years = int((end - begin).days / 365.2425)
    if begin > yearsago(num_years, end):
        return num_years - 1
    else:
        return num_years


def response_to_vect(data: dict) -> tuple[int, list]:
    '''
    Assume data given is json or dict data
    - user_id
    - ethinicity
    - religion
    - gender
    - nationality
    - dob
    '''
    vect = [find_name(e, data[e.name.lower()], e.Others)
            for e in [Ethnicity, Religion, Gender, Nationality]]
    # Assume this is datetime data
    vect.append(AgeRange.valueToName(yearsago(data['dob'], datetime.now())))
    return data['user_id'], vect
