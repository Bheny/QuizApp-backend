from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(Option)
admin.site.register(Classroom)
admin.site.register(Student)
admin.site.register(Submission)
admin.site.register(Assessment)