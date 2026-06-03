from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils import timezone
from .models import SchoolClass, Student, Notice

class SchoolClassForm(ModelForm):
    class Meta:
        model = SchoolClass
        fields = ["class_name", "section"]
        widgets = {
            "class_name": forms.TextInput(attrs={"class": "form-control"}),
            "section": forms.TextInput(attrs={"class": "form-control"}),
        }

class StudentForm(ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"class": "form-control"}), help_text="Optional. If provided, a login user will be created for the student.")

    class Meta:
        model = Student
        fields = [
            "roll_number", "full_name", "school_class", "email", "phone",
            "profile_photo", "admission_date", "active_status",
        ]
        widgets = {
            "roll_number": forms.TextInput(attrs={"class": "form-control"}),
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "school_class": forms.Select(attrs={"class": "form-select"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "admission_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "active_status": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "profile_photo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

class NoticeForm(ModelForm):
    class Meta:
        model = Notice
        fields = ["title", "description", "notice_type", "is_important", "publish_date", "expiry_date"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "notice_type": forms.Select(attrs={"class": "form-select"}),
            "is_important": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "publish_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "expiry_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

class AttendanceFilterForm(forms.Form):
    class_obj = forms.ModelChoiceField(queryset=SchoolClass.objects.all(), required=False, label="Class", widget=forms.Select(attrs={"class": "form-select"}))
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))
    month = forms.DateField(required=False, widget=forms.DateInput(attrs={"class": "form-control", "type": "month"}))
    status = forms.ChoiceField(required=False, choices=[("", "All"), ("Present", "Present"), ("Absent", "Absent")], widget=forms.Select(attrs={"class": "form-select"}))

class StudentSearchForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search by name or roll number"}))
