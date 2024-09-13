import os
import sqlite3
from datetime import datetime

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from attendance.models import AttendanceStatuses
from attendance.serializers import SubjectSerializer, AttendanceSerializer, StudentSerializer
from attendance.services.AttendanceService import AttendanceService
from attendance.services.GroupService import GroupService
from attendance.services.StudentService import StudentService
from attendance.services.SubjectService import SubjectService


class AttendanceViewSet(ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Получаем путь к текущему каталогу
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Формируем путь к базе данных, используя относительный путь от текущего каталога
        db_path = os.path.join(current_dir, '..', '..', 'attendance.sqlite3')
        # Устанавливаем соединение с базой данных
        connection = sqlite3.connect(db_path)
        self.attendance_service = AttendanceService(connection)
        self.subject_service = SubjectService(connection)
        self.student_service = StudentService(connection)
        self.group_service = GroupService(connection)

    def create(self, request):
        #  Проверка на существование студента и предмета
        id_subject = request.data.get('id_subject')
        id_student = request.data.get('id_student')
        try:
            self.student_service.get_student(id_student)
            self.subject_service.get_subject(id_subject)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            attendance = serializer.save()
            self.attendance_service.add_attendance(attendance)
            return Response(AttendanceSerializer(instance=attendance).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, id_group, id_student):
        #  Проверка на соответствие группы и студента
        try:
            self.student_service.is_student_in_this_group(id_student, id_group)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        #  При отсутствии заданной даты используется текущая
        date_param = request.query_params.get('date')
        if not date_param:
            date_param = datetime.now().strftime("%Y-%m-%d")
        print(date_param)

        #  Список посещаемости студента
        try:
            list_of_attendances = self.attendance_service.get_attendances_by_date(date_param,
                                                                                  id_student)
            dict_of_attendances = AttendanceSerializer(instance=list_of_attendances, many=True).data
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        #  Подробные данные о предметах из посещаемости
        dict_of_subjects = []
        for attendances in list_of_attendances:
            dict_of_subjects.append(
                SubjectSerializer(
                    instance=self.subject_service.get_subject(attendances.id_subject)
                ).data)

        #  Подробные данные о студенте
        student = StudentSerializer(instance=self.student_service.get_student(list_of_attendances[0].id_student)).data

        response_date = {
            'student': student,
            'attendances': dict_of_attendances,
            'subjects': dict_of_subjects
        }
        return Response(response_date, status=status.HTTP_200_OK)

    def partial_update(self, request, id_group, id_student):
        request_data = request.data.copy()  # Создаем копию данных запроса
        request_data['id_student'] = id_student
        #  При отсутствии заданной даты используется текущая
        date = request.query_params.get('date')
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        request_data['date'] = date
        serializer = AttendanceSerializer(data=request_data)
        if serializer.is_valid():
            attendance = serializer.save()
            try:
                self.attendance_service.set_new_attendance_status(attendance)
                return Response(status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
