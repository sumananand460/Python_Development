from datetime import date
from calendar import monthrange
from collections import defaultdict
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_POST

from .decorators import admin_required
from .forms import SchoolClassForm, StudentForm, NoticeForm, StudentSearchForm, AttendanceFilterForm
from .models import SchoolClass, Student, Attendance, Notice
from .utils import monthly_attendance_stats, export_attendance_excel, export_attendance_pdf

def home(request):
    return redirect("dashboard")

def custom_logout(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard_router(request):
    if request.user.is_staff:
        return redirect("admin_dashboard")
    return redirect("student_dashboard")

@admin_required
def admin_dashboard(request):
    today = timezone.localdate()
    active_notices = Notice.objects.filter(
        publish_date__lte=today
    ).filter(Q(expiry_date__isnull=True) | Q(expiry_date__gte=today))
    total_students = Student.objects.filter(active_status=True).count()
    total_classes = SchoolClass.objects.count()
    present_today = Attendance.objects.filter(date=today, status=Attendance.PRESENT).count()
    absent_today = Attendance.objects.filter(date=today, status=Attendance.ABSENT).count()

    monthly_labels = []
    monthly_values = []
    for month in range(1, 13):
        monthly_labels.append(date(today.year, month, 1).strftime("%b"))
        monthly_values.append(
            Attendance.objects.filter(date__year=today.year, date__month=month, status=Attendance.PRESENT).count()
        )

    class_stats = []
    for cls in SchoolClass.objects.all():
        class_students = cls.students.filter(active_status=True)
        total = class_students.count()
        present = Attendance.objects.filter(
            student__school_class=cls, status=Attendance.PRESENT, date=today
        ).count()
        absent = Attendance.objects.filter(
            student__school_class=cls, status=Attendance.ABSENT, date=today
        ).count()
        class_stats.append({"label": str(cls), "present": present, "absent": absent, "total": total})

    recent_students = Student.objects.order_by("-created_at")[:5]
    recent_notices = Notice.objects.order_by("-created_at")[:5]
    recent_updates = Attendance.objects.select_related("student").order_by("-id")[:8]

    important_notices = active_notices.filter(is_important=True).order_by("-publish_date", "-created_at")[:5]

    context = {
        "total_students": total_students,
        "present_today": present_today,
        "absent_today": absent_today,
        "total_classes": total_classes,
        "active_notices_count": active_notices.count(),
        "monthly_labels": monthly_labels,
        "monthly_values": monthly_values,
        "class_stats": class_stats,
        "recent_students": recent_students,
        "recent_notices": recent_notices,
        "recent_updates": recent_updates,
        "important_notices": important_notices,
    }
    return render(request, "attendance/admin_dashboard.html", context)

@login_required
def student_dashboard(request):
    try:
        student = request.user.student_profile
    except Exception:
        raise Http404("Student profile not found.")
    stats = monthly_attendance_stats(student)
    today = timezone.localdate()
    important_notices = Notice.objects.filter(
        is_important=True,
        publish_date__lte=today
    ).filter(Q(expiry_date__isnull=True) | Q(expiry_date__gte=today))[:5]
    recent_notices = Notice.objects.filter(publish_date__lte=today).order_by("-created_at")[:5]
    attendance_qs = student.attendance_records.order_by("-date")[:12]
    monthly_history = student.attendance_records.filter(date__year=today.year, date__month=today.month).order_by("date")
    context = {
        "student": student,
        "stats": stats,
        "important_notices": important_notices,
        "recent_notices": recent_notices,
        "attendance_history": attendance_qs,
        "monthly_history": monthly_history,
    }
    return render(request, "attendance/student_dashboard.html", context)

@admin_required
def class_list(request):
    classes = SchoolClass.objects.all()
    return render(request, "attendance/class_list.html", {"classes": classes})

@admin_required
def class_create(request):
    form = SchoolClassForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Class added successfully.")
        return redirect("class_list")
    return render(request, "attendance/form.html", {"form": form, "title": "Add Class"})

@admin_required
def class_update(request, pk):
    obj = get_object_or_404(SchoolClass, pk=pk)
    form = SchoolClassForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Class updated successfully.")
        return redirect("class_list")
    return render(request, "attendance/form.html", {"form": form, "title": "Edit Class"})

@admin_required
def class_delete(request, pk):
    obj = get_object_or_404(SchoolClass, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Class deleted.")
        return redirect("class_list")
    return render(request, "attendance/confirm_delete.html", {"object": obj, "title": "Delete Class"})

@admin_required
def student_list(request):
    qform = StudentSearchForm(request.GET or None)
    students = Student.objects.select_related("school_class").all().order_by("full_name", "roll_number")
    q = request.GET.get("q", "")
    if q:
        students = students.filter(Q(full_name__icontains=q) | Q(roll_number__icontains=q))
    paginator = Paginator(students, 10)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    return render(request, "attendance/student_list.html", {"page_obj": page_obj, "qform": qform, "query": q})

@admin_required
def student_create(request):
    form = StudentForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        student = form.save(commit=False)
        password = form.cleaned_data.get("password")
        if password:
            username = student.roll_number
            user, created = User.objects.get_or_create(username=username, defaults={"email": student.email})
            user.email = student.email
            user.set_password(password)
            user.save()
            student.user = user
        student.save()
        messages.success(request, "Student added successfully.")
        return redirect("student_list")
    return render(request, "attendance/form.html", {"form": form, "title": "Add Student", "multipart": True})

@admin_required
def student_update(request, pk):
    obj = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        student = form.save(commit=False)
        password = form.cleaned_data.get("password")
        if password:
            if student.user:
                student.user.set_password(password)
                student.user.email = student.email
                student.user.save()
            else:
                user = User.objects.create_user(username=student.roll_number, email=student.email, password=password)
                student.user = user
        student.save()
        messages.success(request, "Student updated successfully.")
        return redirect("student_list")
    return render(request, "attendance/form.html", {"form": form, "title": "Edit Student", "multipart": True})

@admin_required
def student_delete(request, pk):
    obj = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        if obj.user:
            obj.user.delete()
        obj.delete()
        messages.success(request, "Student deleted.")
        return redirect("student_list")
    return render(request, "attendance/confirm_delete.html", {"object": obj, "title": "Delete Student"})

@admin_required
def mark_attendance(request):
    classes = SchoolClass.objects.all()
    selected_class_id = request.GET.get("class_obj") or request.POST.get("class_obj")
    selected_date = request.GET.get("date") or request.POST.get("date") or timezone.localdate().isoformat()
    attendance_date = parse_date(selected_date) or timezone.localdate()
    selected_class = None
    students = Student.objects.none()
    current_map = {}
    attendance_rows = []

    if selected_class_id:
        selected_class = get_object_or_404(SchoolClass, pk=selected_class_id)
        students = Student.objects.filter(school_class=selected_class, active_status=True).order_by("full_name", "roll_number")
        existing = Attendance.objects.filter(date=attendance_date, student__in=students)
        current_map = {a.student_id: a.status for a in existing}
        attendance_rows = [{"student": s, "status": current_map.get(s.id)} for s in students]

    if request.method == "POST":
        if not selected_class_id:
            messages.error(request, "Please select a class.")
            return redirect("mark_attendance")
        selected_class = get_object_or_404(SchoolClass, pk=selected_class_id)
        students = Student.objects.filter(school_class=selected_class, active_status=True).order_by("full_name", "roll_number")
        errors = []
        for student in students:
            status = request.POST.get(f"status_{student.id}")
            if status not in [Attendance.PRESENT, Attendance.ABSENT]:
                errors.append(student.full_name)
                continue
            Attendance.objects.update_or_create(
                student=student,
                date=attendance_date,
                defaults={"status": status},
            )
        if errors:
            messages.error(request, f"Attendance missing for: {', '.join(errors)}")
        else:
            messages.success(request, "Attendance saved successfully.")
            return redirect(f"{reverse('mark_attendance')}?class_obj={selected_class.id}&date={attendance_date.isoformat()}")

    return render(request, "attendance/mark_attendance.html", {
        "classes": classes,
        "selected_class": selected_class,
        "selected_class_id": int(selected_class_id) if selected_class_id else None,
        "students": students,
        "attendance_rows": attendance_rows,
        "attendance_date": attendance_date,
        "current_map": current_map,
    })

@admin_required
def attendance_history(request):
    form = AttendanceFilterForm(request.GET or None)
    records = Attendance.objects.select_related("student", "student__school_class").all()
    class_obj = request.GET.get("class_obj")
    date_param = request.GET.get("date")
    month_param = request.GET.get("month")
    status = request.GET.get("status")
    if class_obj:
        records = records.filter(student__school_class_id=class_obj)
    if date_param:
        records = records.filter(date=parse_date(date_param))
    if month_param:
        dt = parse_date(month_param + "-01")
        if dt:
            records = records.filter(date__year=dt.year, date__month=dt.month)
    if status:
        records = records.filter(status=status)
    records = records.order_by("-date", "student__full_name")
    paginator = Paginator(records, 20)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "attendance/attendance_history.html", {"page_obj": page_obj, "form": form})

@admin_required
def notice_list(request):
    notices = Notice.objects.all()
    notice_type = request.GET.get("notice_type")
    filter_status = request.GET.get("filter")
    if notice_type:
        notices = notices.filter(notice_type=notice_type)
    today = timezone.localdate()
    if filter_status == "active":
        notices = notices.filter(publish_date__lte=today).filter(Q(expiry_date__isnull=True) | Q(expiry_date__gte=today))
    elif filter_status == "expired":
        notices = notices.filter(expiry_date__lt=today)
    elif filter_status == "important":
        notices = notices.filter(is_important=True)
    paginator = Paginator(notices.order_by("-is_important", "-publish_date"), 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "attendance/notice_list.html", {"page_obj": page_obj})

@admin_required
def notice_create(request):
    form = NoticeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        notice = form.save(commit=False)
        notice.created_by = request.user
        if notice.notice_type == Notice.IMPORTANT:
            notice.is_important = True
        notice.save()
        messages.success(request, "Notice created successfully.")
        return redirect("notice_list")
    return render(request, "attendance/form.html", {"form": form, "title": "Create Notice"})

@admin_required
def notice_update(request, pk):
    obj = get_object_or_404(Notice, pk=pk)
    form = NoticeForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        notice = form.save(commit=False)
        notice.created_by = request.user
        if notice.notice_type == Notice.IMPORTANT:
            notice.is_important = True
        notice.save()
        messages.success(request, "Notice updated.")
        return redirect("notice_list")
    return render(request, "attendance/form.html", {"form": form, "title": "Edit Notice"})

@admin_required
def notice_delete(request, pk):
    obj = get_object_or_404(Notice, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Notice deleted.")
        return redirect("notice_list")
    return render(request, "attendance/confirm_delete.html", {"object": obj, "title": "Delete Notice"})

@admin_required
def reports_dashboard(request):
    return render(request, "attendance/reports_dashboard.html")

@admin_required
def daily_report(request):
    d = parse_date(request.GET.get("date") or timezone.localdate().isoformat()) or timezone.localdate()
    records = Attendance.objects.filter(date=d).select_related("student", "student__school_class").order_by("student__full_name")
    rows = [("Roll Number", "Student", "Class", "Status", "Date")]
    for r in records:
        rows.append((r.student.roll_number, r.student.full_name, str(r.student.school_class), r.status, r.date.isoformat()))
    export = request.GET.get("export")
    if export == "excel":
        return export_attendance_excel(rows, title=f"Daily Attendance Report - {d}")
    if export == "pdf":
        return export_attendance_pdf(rows, title=f"Daily Attendance Report - {d}")
    return render(request, "attendance/report_table.html", {"title": "Daily Report", "rows": rows, "report_date": d})

@admin_required
def monthly_report(request):
    month_param = request.GET.get("month")
    month_date = parse_date(month_param + "-01") if month_param else timezone.localdate().replace(day=1)
    students = Student.objects.select_related("school_class").all().order_by("full_name")
    rows = [("Roll Number", "Student", "Class", "Present", "Absent", "Percentage")]
    for student in students:
        present = student.attendance_records.filter(date__year=month_date.year, date__month=month_date.month, status=Attendance.PRESENT).count()
        absent = student.attendance_records.filter(date__year=month_date.year, date__month=month_date.month, status=Attendance.ABSENT).count()
        total = present + absent
        pct = round((present / total) * 100, 2) if total else 0.0
        rows.append((student.roll_number, student.full_name, str(student.school_class), present, absent, f"{pct}%"))
    export = request.GET.get("export")
    if export == "excel":
        return export_attendance_excel(rows, title=f"Monthly Attendance Report - {month_date:%B %Y}")
    if export == "pdf":
        return export_attendance_pdf(rows, title=f"Monthly Attendance Report - {month_date:%B %Y}")
    return render(request, "attendance/report_table.html", {"title": "Monthly Report", "rows": rows, "report_date": month_date})

@admin_required
def class_report(request):
    classes = SchoolClass.objects.all()
    rows = [("Class", "Total Students", "Present Today", "Absent Today")]
    today = timezone.localdate()
    for cls in classes:
        total = cls.students.filter(active_status=True).count()
        present = Attendance.objects.filter(student__school_class=cls, date=today, status=Attendance.PRESENT).count()
        absent = Attendance.objects.filter(student__school_class=cls, date=today, status=Attendance.ABSENT).count()
        rows.append((str(cls), total, present, absent))
    export = request.GET.get("export")
    if export == "excel":
        return export_attendance_excel(rows, title="Class-wise Attendance Report")
    if export == "pdf":
        return export_attendance_pdf(rows, title="Class-wise Attendance Report")
    return render(request, "attendance/report_table.html", {"title": "Class Report", "rows": rows, "report_date": today})
