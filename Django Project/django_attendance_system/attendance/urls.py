from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard_router, name="dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("student-dashboard/", views.student_dashboard, name="student_dashboard"),
    path("classes/", views.class_list, name="class_list"),
    path("classes/add/", views.class_create, name="class_create"),
    path("classes/<int:pk>/edit/", views.class_update, name="class_update"),
    path("classes/<int:pk>/delete/", views.class_delete, name="class_delete"),
    path("students/", views.student_list, name="student_list"),
    path("students/add/", views.student_create, name="student_create"),
    path("students/<int:pk>/edit/", views.student_update, name="student_update"),
    path("students/<int:pk>/delete/", views.student_delete, name="student_delete"),
    path("attendance/", views.mark_attendance, name="mark_attendance"),
    path("attendance/history/", views.attendance_history, name="attendance_history"),
    path("notices/", views.notice_list, name="notice_list"),
    path("notices/add/", views.notice_create, name="notice_create"),
    path("notices/<int:pk>/edit/", views.notice_update, name="notice_update"),
    path("notices/<int:pk>/delete/", views.notice_delete, name="notice_delete"),
    path("reports/", views.reports_dashboard, name="reports_dashboard"),
    path("reports/daily/", views.daily_report, name="daily_report"),
    path("reports/monthly/", views.monthly_report, name="monthly_report"),
    path("reports/class/", views.class_report, name="class_report"),
]
