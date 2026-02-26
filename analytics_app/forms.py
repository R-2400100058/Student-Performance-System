from django import forms
from .models import Student, Subject, Mark


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_no', 'department']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control-custom w-100',
                'placeholder': 'Enter student name',
                'required': 'required',
                'maxlength': '100'
            }),
            'roll_no': forms.TextInput(attrs={
                'class': 'form-control-custom w-100',
                'placeholder': 'e.g., STU001',
                'required': 'required',
                'maxlength': '20'
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control-custom w-100',
                'placeholder': 'e.g., Science',
                'required': 'required',
                'maxlength': '100'
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or len(name.strip()) == 0:
            raise forms.ValidationError('Student name cannot be empty')
        return name.strip()

    def clean_roll_no(self):
        roll_no = self.cleaned_data.get('roll_no')
        if not roll_no or len(roll_no.strip()) == 0:
            raise forms.ValidationError('Roll number cannot be empty')
        return roll_no.strip()

    def clean_department(self):
        dept = self.cleaned_data.get('department')
        if not dept or len(dept.strip()) == 0:
            raise forms.ValidationError('Department cannot be empty')
        return dept.strip()


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_name']
        widgets = {
            'subject_name': forms.TextInput(attrs={
                'class': 'form-control-custom w-100',
                'placeholder': 'Enter subject name',
                'required': 'required',
                'maxlength': '100'
            }),
        }

    def clean_subject_name(self):
        name = self.cleaned_data.get('subject_name')
        if not name or len(name.strip()) == 0:
            raise forms.ValidationError('Subject name cannot be empty')
        return name.strip()


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['student', 'subject', 'marks_obtained', 'attendance_percentage']
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-control-custom w-100',
                'required': 'required'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control-custom w-100',
                'required': 'required'
            }),
            'marks_obtained': forms.NumberInput(attrs={
                'class': 'form-control-custom w-100',
                'placeholder': 'Marks obtained (0-100)',
                'min': '0',
                'max': '100',
                'step': '0.5',
                'required': 'required'
            }),
            'attendance_percentage': forms.NumberInput(attrs={
                'class': 'form-control-custom w-100',
                'placeholder': 'Attendance percentage (0-100)',
                'min': '0',
                'max': '100',
                'step': '0.5',
                'required': 'required'
            }),
        }

    def clean_marks_obtained(self):
        marks = self.cleaned_data.get('marks_obtained')
        if marks is None or marks == '':
            raise forms.ValidationError('Marks are required')
        if not (0 <= marks <= 100):
            raise forms.ValidationError('Marks must be between 0 and 100')
        return marks

    def clean_attendance_percentage(self):
        attendance = self.cleaned_data.get('attendance_percentage')
        if attendance is None or attendance == '':
            raise forms.ValidationError('Attendance percentage is required')
        if not (0 <= attendance <= 100):
            raise forms.ValidationError('Attendance must be between 0 and 100')
        return attendance

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        subject = cleaned_data.get('subject')
        
        if student and subject:
            # Check if this mark entry already exists
            existing = Mark.objects.filter(
                student=student,
                subject=subject
            ).exclude(pk=self.instance.pk if self.instance.pk else None)
            
            if existing.exists():
                raise forms.ValidationError(
                    f'Mark entry for {student.name} in {subject.subject_name} already exists. '
                    'Please edit the existing entry instead.'
                )
        
        return cleaned_data
