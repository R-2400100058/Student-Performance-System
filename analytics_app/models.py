from django.db import models
from django.contrib.auth.models import User



class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
=======
class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20)
    department = models.CharField(max_length=100)


    def __str__(self):
        return self.name



class Mark(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.FloatField()
    total_marks = models.FloatField(default=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.subject.name}"

    @property
    def percentage(self):
        return (self.marks_obtained / self.total_marks) * 100


class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)

    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.student.username} - {status} - {self.date}"
=======
class Subject(models.Model):
    subject_name = models.CharField(max_length=100)

    def __str__(self):
        return self.subject_name


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField()
    attendance_percentage = models.FloatField()

    def __str__(self):
        return f"{self.student.name} - {self.subject.subject_name}"

