from django import forms
from .models import Trail, Course, Module, Lesson, LessonCategory

class TrailForm(forms.ModelForm):
    class Meta:
        model = Trail
        fields = ['title', 'description']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'trails', 'theme_slug']

class ModuleForm(forms.ModelForm):
    class Meta: 
        model = Module
        fields = ['title', 'trail', 'order', 'cover_image']

class LessonCategoryForm(forms.ModelForm):
    class Meta:
        model = LessonCategory
        fields = ['name', 'module']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['module', 'title', 'category', 'order', 'lesson_type']