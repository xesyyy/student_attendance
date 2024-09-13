from rest_framework import serializers
from rest_enumfield import EnumField
from attendance.models import Student, Subject, AttendanceStatuses, Group, Attendance


class GroupSerializer(serializers.Serializer):
    id_group = serializers.CharField(required=False)
    group_name = serializers.CharField()

    def create(self, validated_data):
        return Group(validated_data['group_name'], None)


class StudentSerializer(serializers.Serializer):
    id_student = serializers.CharField(required=False)
    name = serializers.CharField(required=True)
    id_group = serializers.CharField(required=True)
    group_name = serializers.CharField(required=True)
    semester = serializers.IntegerField(required=False)

    def create(self, validated_data):
        return Student(None, validated_data['name'], validated_data['id_group'], validated_data['group_name'],
                       None)


class SubjectSerializer(serializers.Serializer):
    id_subject = serializers.CharField(required=False)
    name = serializers.CharField()
    room = serializers.CharField()
    professor = serializers.CharField()

    def create(self, validated_data):
        return Subject(None, validated_data['name'],
                       validated_data['room'], validated_data['professor'])


class AttendanceSerializer(serializers.Serializer):
    id_student = serializers.CharField()
    id_subject = serializers.CharField()
    date = serializers.DateField(format="%Y-%m-%d")
    status = EnumField(choices=AttendanceStatuses)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = AttendanceStatuses(instance.status).value
        return representation

    def create(self, validated_data):
        return Attendance(validated_data['id_subject'], validated_data['id_student'], validated_data['date'],
                          validated_data['status'])
