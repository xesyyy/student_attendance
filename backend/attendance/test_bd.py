from uuid import uuid4
from datetime import datetime
import sqlite3

# Создаем подключение к базе данных
connection = sqlite3.connect(r'C:/Users/rexes/PycharmProjects/courseStudentAttendance/attendance.sqlite3')
cursor = connection.cursor()

id_group1 = str(uuid4())
id_group2 = str(uuid4())
id_group3 = str(uuid4())
data_group = [
    (id_group1, "ИНБО-10-21"),
    (id_group2, "ИНБО-08-21"),
    (id_group3, "ИНБО-07-21")
]

# Примеры данных для вставки
data = [
    (str(uuid4()), "Mathematics", "Room 101", "John Doe", datetime.now().strftime("%Y-%m-%d"), id_group1),
    (str(uuid4()), "Physics", "Room 201", "Jane Smith", datetime.now().strftime("%Y-%m-%d"), id_group1),
    (str(uuid4()), "Chemistry", "Room 301", "Bob Johnson", datetime.now().strftime("%Y-%m-%d"), id_group1),
]

# Вставляем данные в таблицу
cursor.executemany('''INSERT INTO groups (id_group, group_name) 
VALUES (?, ?)''', data_group)

cursor.executemany('''INSERT INTO subjects (id_subject, name, room, professor, date, id_group) 
VALUES (?, ?, ?, ?, ?, ?)''', data)
connection.commit()

# Закрываем соединение
connection.close()
