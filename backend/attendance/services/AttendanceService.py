import sqlite3

from attendance.models import Attendance, AttendanceStatuses


class AttendanceService:
    def __init__(self, connection):
        self.connection = connection

    def add_attendance(self, attendance: Attendance):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO attendance (id_student, id_subject, status, date) VALUES (?, ?, ?, ?)",
                       (attendance.id_student, attendance.id_subject, attendance.status, attendance.date))
        self.connection.commit()

    def set_new_attendance_status(self, attendance: Attendance):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE attendance SET status=? WHERE id_student=? AND id_subject=? AND date=?",
                       (attendance.status.value, attendance.id_student, attendance.id_subject, attendance.date))
        print(attendance.date)
        if cursor.rowcount == 0:
            raise ValueError("Произошла ошибка при установке нового статуса.")
        self.connection.commit()

    def get_attendances_by_date(self, date, id_student):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id_subject, status FROM attendance WHERE date=? AND id_student=?",
                       (date, id_student))
        row = cursor.fetchall()
        list_of_attendances = []
        if row:
            for params in row:
                list_of_attendances.append(Attendance(params[0], id_student, date, AttendanceStatuses(params[1])))
            return list_of_attendances
        else:
            raise ValueError("Посещение для этого студента и предмета не найдено в списке.")