from django.contrib import admin
from .models import Course, Lesson, LessonCategory, LessonProgress, Module, Trail

# Register your models here
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Module)
admin.site.register(LessonCategory)
admin.site.register(Trail)
admin.site.register(LessonProgress)