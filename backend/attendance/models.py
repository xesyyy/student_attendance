import enum
from uuid import UUID, uuid4
from datetime import datetime


class Group:
    def __init__(self,
                 group_name: str,
                 id_group=None,
                 ):
        self.group_name = group_name
        self.id_group = id_group or str(uuid4())


class Student:
    def __init__(self,
                 id_student=None,
                 name=None,
                 id_group=None,
                 group_name=None,
                 semester=None,
                 ):
        self.id_student = id_student or str(uuid4())
        self.name = name
        self.id_group = id_group
        self.group_name = group_name
        self.semester = semester


class Subject:
    def __init__(
            self,
            id_subject=None,
            name=None,
            room=None,
            professor=None,
    ):
        self.name = name
        self.id_subject = id_subject or str(uuid4())
        self.room = room
        self.professor = professor


class AttendanceStatuses(enum.Enum):
    UNKNOWN = 'Студент еще не был отмечен'
    LEGITIMATE = 'Пропуск по уважительной причине'
    ILLEGITIMATE = 'Пропуск по неуважительной причине'
    PRESENT = 'Студент присутствовал'


class Attendance:
    def __init__(
            self,
            id_subject,
            id_student,
            date,
            status=AttendanceStatuses.UNKNOWN
    ):
        self.id_subject = id_subject
        self.id_student = id_student
        self.date = date
        self.status = status
