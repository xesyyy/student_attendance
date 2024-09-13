import sqlite3

from attendance.models import Student


class StudentService:
    def __init__(self, connection):
        self.connection = connection

    def add_student(self, student: Student):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO students (id_student, name, id_group, semester) VALUES (?, ?, ?, ?)",
                       (student.id_student, student.name, student.id_group, student.semester))
        self.connection.commit()

    def get_student(self, id_student):
        cursor = self.connection.cursor()

        cursor.execute("SELECT name, id_group, semester FROM students WHERE id_student=?", (id_student,))
        row_student = cursor.fetchone()
        if not row_student:
            raise ValueError("Студент не найден.")

        cursor.execute("SELECT group_name FROM groups WHERE id_group=?", (row_student[1],))
        row_group = cursor.fetchone()
        if not row_group:
            raise ValueError("Группа студента не найдена.")

        return Student(id_student, row_student[0], row_student[1], row_group[0],  row_student[2])

    def delete_student(self, id_student):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM students WHERE id_student=?", (id_student,))
        self.connection.commit()
        if cursor.rowcount > 0:
            return True
        else:
            raise ValueError("Студент с указанным ID не найден.")

    def get_students_by_group(self, id_group):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id_student FROM students WHERE id_group=?", (id_group,))
        row = cursor.fetchall()
        if not row:
            raise ValueError("Студенты этой группы не были найдены.")
        return row

    def get_student_group(self, id_student):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id_group FROM students WHERE id_student=?",
                       (id_student,))
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            raise ValueError("Группа студента не найдена.")

    def is_student_in_this_group(self, id_student, id_group):
        try:
            valid_id_group = self.get_student_group(id_student)
            if valid_id_group == id_group:
                return True
            else:
                raise ValueError("Этого студента нет в заданной группе.")
        except Exception:
            raise ValueError("Этого студента нет в заданной группе.")
