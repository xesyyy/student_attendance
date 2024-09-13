import os
import sqlite3

# Получаем абсолютный путь к текущему рабочему каталогу
current_dir = os.getcwd()
# Получаем абсолютный путь к родительскому каталогу текущего рабочего каталога
parent_dir = os.path.dirname(current_dir)
# Формируем путь к базе данных
db_path = os.path.join(parent_dir, 'attendance.sqlite3')
# Устанавливаем соединение с базой данных
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Создаем таблицу групп
cursor.execute('''CREATE TABLE IF NOT EXISTS groups (
                  id_group VARCHAR(45) PRIMARY KEY NOT NULL,
                  group_name VARCHAR(45) NOT NULL)''')

# Создаем таблицу студентов
cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                  id_student VARCHAR(45) PRIMARY KEY NOT NULL,
                  name VARCHAR(45) NOT NULL,
                  id_group VARCHAR(45) NOT NULL,
                  semester INTEGER,
                  FOREIGN KEY (id_group) REFERENCES groups (id_group)
                    ON DELETE NO ACTION
                    ON UPDATE NO ACTION)''')

# Создаем таблицу предметов
cursor.execute('''CREATE TABLE IF NOT EXISTS subjects (
                  id_subject VARCHAR(45) PRIMARY KEY NOT NULL,
                  name VARCHAR(45) NOT NULL,
                  room VARCHAR(45) NULL,
                  professor VARCHAR(45) NULL)''')

# Создаем таблицу связи многие-ко-многим для предметов и групп
cursor.execute('''CREATE TABLE NOT EXISTS subjects_have_students (
                id_subject VARCHAR(45) NOT NULL,
                id_group VARCHAR(45) NOT NULL,
                FOREIGN KEY(id_group) REFERENCES groups(id_group),
                FOREIGN KEY(id_subject) REFERENCES subjects(id_subject),
                PRIMARY KEY("id_subject","id_group")''')

# Создаем таблицу посещаемости
cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                  id_student VARCHAR(45) NOT NULL,
                  id_subject VARCHAR(45) NOT NULL,
                  status VARCHAR(45) NOT NULL,
                  date VARCHAR(45) NOT NULL,
                  PRIMARY KEY (id_student, id_subject),
                  FOREIGN KEY (id_student) REFERENCES students (id_student)
                    ON DELETE NO ACTION
                    ON UPDATE NO ACTION,
                  FOREIGN KEY (id_subject) REFERENCES subjects (id_subject)
                    ON DELETE NO ACTION
                    ON UPDATE NO ACTION)''')

connection.commit()
cursor.close()
