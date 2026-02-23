from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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