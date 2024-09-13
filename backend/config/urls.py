from django.contrib import admin
from django.urls import path
from attendance.viewsets.AttendanceViewSet import AttendanceViewSet
from attendance.viewsets.GroupViewSet import GroupViewSet
from attendance.viewsets.StudentViewSet import StudentViewSet
from attendance.viewsets.SubjectViewSet import SubjectViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    # Groups
    path('attendance/groups/', GroupViewSet.as_view(
        {'get': 'list',
         'post': 'create',
         'delete': 'destroy'})),
    #  Students
    path('attendance/groups/<str:id_group>/students/', StudentViewSet.as_view(
        {'get': 'list',
         'post': 'create',
         'delete': 'destroy'})),
    #  Attendance
    path('attendance/groups/<str:id_group>/students/<str:id_student>', AttendanceViewSet.as_view(
        {'get': 'retrieve',
         'post': 'create',
         'patch': 'partial_update'})),
    # Subjects
    path('attendance/subjects/', SubjectViewSet.as_view(
        {'get': 'list',
         'post': 'create'})),
    path('attendance/subjects/<str:id_subject>', SubjectViewSet.as_view(
        {'get': 'retrieve'})),
]
