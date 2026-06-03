from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone

class SchoolClass(models.Model):
    class_name = models.CharField(max_length=50)
    section = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["class_name", "section"]
        unique_together = ("class_name", "section")

    def __str__(self):
        return f"{self.class_name} - {self.section}"

class Student(models.Model):
    roll_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=150, db_index=True)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name="students")
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=15,
        blank=True,
        validators=[RegexValidator(r"^[0-9+\-\s]{7,15}$", "Enter a valid phone number.")]
    )
    profile_photo = models.ImageField(upload_to="students/", blank=True, null=True)
    admission_date = models.DateField(default=timezone.localdate)
    active_status = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="student_profile")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["full_name", "roll_number"]

    def __str__(self):
        return f"{self.full_name} ({self.roll_number})"

class Attendance(models.Model):
    PRESENT = "Present"
    ABSENT = "Absent"
    STATUS_CHOICES = [
        (PRESENT, "Present"),
        (ABSENT, "Absent"),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ("student", "date")
        ordering = ["-date", "student__full_name"]

    def __str__(self):
        return f"{self.student.full_name} - {self.date} - {self.status}"

class Notice(models.Model):
    GENERAL = "General"
    IMPORTANT = "Important"
    EMERGENCY = "Emergency"
    ACADEMIC = "Academic"
    NOTICE_TYPES = [
        (GENERAL, "General"),
        (IMPORTANT, "Important"),
        (EMERGENCY, "Emergency"),
        (ACADEMIC, "Academic"),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    notice_type = models.CharField(max_length=20, choices=NOTICE_TYPES, default=GENERAL)
    is_important = models.BooleanField(default=False)
    publish_date = models.DateField(default=timezone.localdate)
    expiry_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_notices")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_important", "-publish_date", "-created_at"]

    def __str__(self):
        return self.title

    @property
    def is_active(self):
        today = timezone.localdate()
        if self.publish_date and self.publish_date > today:
            return False
        if self.expiry_date and self.expiry_date < today:
            return False
        return True
