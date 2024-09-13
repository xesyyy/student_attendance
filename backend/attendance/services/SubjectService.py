import sqlite3

from attendance.models import Subject


class SubjectService:
    def __init__(self, connection):
        self.connection = connection

    def add_subject(self, subject: Subject):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO subjects (id_subject, name, room, professor) VALUES "
                       "(?, ?, ?, ?)",
                       (subject.id_subject, subject.name, subject.room, subject.professor))
        self.connection.commit()

    def get_subject(self, subject_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id_subject, name, room, professor FROM subjects WHERE id_subject=?",
                       (subject_id,))
        row = cursor.fetchone()
        if row:
            return Subject(row[0], row[1], row[2], row[3])
        else:
            raise ValueError("Предмет с указанным идентификатором не найден в базе данных.")

    def get_all_subjects(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM subjects",
                       ())
        row = cursor.fetchall()
        list_of_subjects = []
        for subjects in row:
            list_of_subjects.append(Subject(subjects[0], subjects[1], subjects[2], subjects[3]))
        print(list_of_subjects)
        return list_of_subjects
