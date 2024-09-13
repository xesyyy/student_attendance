import sqlite3

from attendance.models import Group


class GroupService:
    def __init__(self, connection):
        self.connection = connection

    def add_group(self, group: Group):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO groups (id_group, group_name) VALUES (?, ?)",
                       (group.id_group, group.group_name))
        self.connection.commit()

    def get_all_groups(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id_group, group_name FROM groups")
        row = cursor.fetchall()
        print(row)
        list_of_groups = {}
        if row:
            for params in row:
                list_of_groups[params[1]] = Group(group_name=params[1], id_group=params[0])
            return list_of_groups
        else:
            raise ValueError("В базе данных не содержится ни одной группы.")

    def get_group(self, id_group):
        cursor = self.connection.cursor()
        cursor.execute("SELECT group_name FROM groups WHERE id_group=?",
                       (id_group,))
        row = cursor.fetchone()
        if row:
            return Group(group_name=row[0], id_group=id_group)
        else:
            raise ValueError(f"Группа с идентификатором {id_group} не была найдена в БД.")

    def get_id_group_by_name(self, group_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id_group FROM groups WHERE group_name=?",
                       (group_name,))
        row = cursor.fetchone()
        if row:
            return row[0]

    def get_group_name(self, id_group):
        cursor = self.connection.cursor()
        cursor.execute("SELECT group_name FROM groups WHERE id_group=?",
                       (id_group,))
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            raise ValueError(f"Группа с идентификатором {id_group} не была найдена в БД.")

    def delete_group(self, id_group):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM groups WHERE id_group=?", (id_group,))
        self.connection.commit()
        if cursor.rowcount > 0:
            return True
        else:
            raise ValueError("Группа с указанным ID не найдена.")
