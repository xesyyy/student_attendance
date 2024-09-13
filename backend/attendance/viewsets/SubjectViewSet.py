import os
import sqlite3

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from attendance.serializers import SubjectSerializer
from attendance.services.GroupService import GroupService
from attendance.services.SubjectService import SubjectService


class SubjectViewSet(ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Получаем путь к текущему каталогу
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Формируем путь к базе данных, используя относительный путь от текущего каталога
        db_path = os.path.join(current_dir, '..', '..', 'attendance.sqlite3')
        # Устанавливаем соединение с базой данных
        connection = sqlite3.connect(db_path)
        self.subject_service = SubjectService(connection)
        self.group_service = GroupService(connection)

    def list(self, request):
        list_of_subjects = self.subject_service.get_all_subjects()
        subject_data = SubjectSerializer(instance=list_of_subjects, many=True).data
        print(list_of_subjects)
        return Response(subject_data, status=status.HTTP_200_OK)

    def retrieve(self, request, id_subject):
        subject = self.subject_service.get_subject(id_subject)
        subject_data = SubjectSerializer(instance=subject).data
        print(subject_data)
        return Response(subject_data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = SubjectSerializer(data=request.data)
        id_group = request.data.get('id_group')
        if serializer.is_valid() and (self.group_service.get_group_name(id_group)):
            subject = serializer.save()
            self.subject_service.add_subject(subject)
            return Response(SubjectSerializer(instance=subject).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
