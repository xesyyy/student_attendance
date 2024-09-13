import os
import sqlite3

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from attendance.serializers import GroupSerializer, StudentSerializer
from attendance.services.GroupService import GroupService
from attendance.services.StudentService import StudentService


class GroupViewSet(ViewSet):
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

    def list(self, request):
        try:
            list_of_groups = self.group_service.get_all_groups()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        for id_group, group in list_of_groups.items():
            group_data = GroupSerializer(instance=group).data
            list_of_groups[id_group] = group_data
        return Response(list_of_groups, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save()
            self.group_service.add_group(group)
            return Response(GroupSerializer(instance=group).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request):
        id_group = request.data.get('id_group')
        try:
            self.group_service.delete_group(id_group)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)