from django.contrib import admin

from .models import Subject, Mark, Attendance

admin.site.register(Subject)
admin.site.register(Mark)
admin.site.register(Attendance)
=======
from .models import Student, Subject, Mark


admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Mark)

