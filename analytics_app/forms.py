from django import forms
from .models import Student, Subject, Mark


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_no', 'department']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control-custom w-100',
                'placeholder': 'Enter student name'
            }),
            'roll_no': forms.TextInput(attrs={
                'class': 'form-control-custom w-100',
                'placeholder': 'e.g., STU001'
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control-custom w-100',
                'placeholder': 'e.g., Science'
            }),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_name']
        widgets = {
            'subject_name': forms.TextInput(attrs={
                'class': 'form-control-custom w-100',
                'placeholder': 'Enter subject name'
            }),
        }


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['student', 'subject', 'marks_obtained', 'attendance_percentage']
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-control-custom w-100'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control-custom w-100'
            }),
            'marks_obtained': forms.NumberInput(attrs={
                'class': 'form-control-custom w-100',
                'placeholder': 'Marks obtained (0-100)',
                'min': '0',
                'max': '100'
            }),
            'attendance_percentage': forms.NumberInput(attrs={
                'class': 'form-control-custom w-100',
                'placeholder': 'Attendance percentage (0-100)',
                'min': '0',
                'max': '100'
            }),
        }
