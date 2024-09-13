import os
import sqlite3

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from attendance.serializers import GroupSerializer, StudentSerializer
from attendance.services.GroupService import GroupService
from attendance.services.StudentService import StudentService


class StudentViewSet(ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Получаем путь к текущему каталогу
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Формируем путь к базе данных, используя относительный путь от текущего каталога
        db_path = os.path.join(current_dir, '..', '..', 'attendance.sqlite3')
        # Устанавливаем соединение с базой данных
        connection = sqlite3.connect(db_path)
        self.group_service = GroupService(connection)
        self.student_service = StudentService(connection)

    def list(self, request, id_group):
        try:
            #  Данные группы
            group = self.group_service.get_group(id_group)
            group_data = GroupSerializer(instance=group).data

            #  Данные студентов этой группы
            id_students_row = self.student_service.get_students_by_group(id_group)
            print(id_students_row)
            students_list = []
            for id_student in id_students_row:
                students_list.append(self.student_service.get_student(id_student[0]))
            serialized_students = StudentSerializer(instance=students_list, many=True).data

            all_serialized_data = {'group': group_data, 'students': serialized_students}
            return Response(all_serialized_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, id_group):
        request_data = request.data.copy()  # Создаем копию данных запроса
        request_data['id_group'] = id_group  # Добавляем id_group в данные запрос
        serializer = StudentSerializer(data=request_data)
        if serializer.is_valid():
            student = serializer.save()
            self.student_service.add_student(student)
            return Response(StudentSerializer(instance=student).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, id_group):
        id_student = request.data.get('id_student')
        try:
            self.student_service.delete_student(id_student)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

