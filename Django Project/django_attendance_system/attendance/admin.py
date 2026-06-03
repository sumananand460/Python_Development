from django.contrib import admin
from .models import SchoolClass, Student, Attendance, Notice

@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ("class_name", "section", "created_at", "updated_at")
    search_fields = ("class_name", "section")
    list_filter = ("class_name", "section")

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("roll_number", "full_name", "school_class", "email", "active_status")
    search_fields = ("full_name", "roll_number", "email")
    list_filter = ("school_class", "active_status")
    ordering = ("full_name",)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "date", "status")
    list_filter = ("date", "status", "student__school_class")
    search_fields = ("student__full_name", "student__roll_number")
    ordering = ("-date", "student__full_name")

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("title", "notice_type", "is_important", "publish_date", "expiry_date", "created_by")
    list_filter = ("notice_type", "is_important", "publish_date", "expiry_date")
    search_fields = ("title", "description")
    ordering = ("-is_important", "-publish_date")
