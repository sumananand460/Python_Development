from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from attendance.models import SchoolClass, Student, Notice, Attendance

class Command(BaseCommand):
    help = "Seed demo classes, students, notices, and attendance"

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(username="admin", defaults={"is_staff": True, "is_superuser": True, "email": "admin@example.com"})
        if not admin.has_usable_password():
            admin.set_password("admin123")
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()

        classes = []
        for class_name, section in [("10", "A"), ("10", "B"), ("11", "A"), ("12", "A")]:
            obj, _ = SchoolClass.objects.get_or_create(class_name=class_name, section=section)
            classes.append(obj)

        sample_students = [
            ("101", "Aarav Sharma", classes[0], "aarav@example.com"),
            ("102", "Ananya Das", classes[0], "ananya@example.com"),
            ("103", "Kabir Singh", classes[1], "kabir@example.com"),
            ("104", "Meera Patel", classes[2], "meera@example.com"),
            ("105", "Rohan Gupta", classes[3], "rohan@example.com"),
        ]
        for roll, name, cls, email in sample_students:
            student, _ = Student.objects.get_or_create(
                roll_number=roll,
                defaults={"full_name": name, "school_class": cls, "email": email, "admission_date": timezone.localdate()},
            )
            if student.full_name != name:
                student.full_name = name
                student.school_class = cls
                student.email = email
                student.save()

        Notice.objects.get_or_create(
            title="Annual Sports Day",
            defaults={
                "description": "Annual sports day will be held next month.",
                "notice_type": Notice.ACADEMIC,
                "is_important": True,
                "created_by": admin,
            },
        )
        Notice.objects.get_or_create(
            title="Fee Submission Reminder",
            defaults={
                "description": "Please complete fee submission before the due date.",
                "notice_type": Notice.GENERAL,
                "is_important": False,
                "created_by": admin,
            },
        )

        today = timezone.localdate()
        for student in Student.objects.all():
            Attendance.objects.get_or_create(student=student, date=today, defaults={"status": Attendance.PRESENT})

        self.stdout.write(self.style.SUCCESS("Demo data created successfully."))
