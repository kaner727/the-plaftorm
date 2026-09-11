from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    course = models.ForeignKey('Course', null=True, blank=True, on_delete=models.SET_NULL, related_name="students")

class Trail(models.Model):
    title = models.CharField(max_length=200, verbose_name="Trail Title", null=False, blank=False)
    description = models.TextField(blank=True, verbose_name="Description")
 
    def __str__(self):
        return self.title
 
class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Course Name", null=False, blank=False)
    description = models.TextField(blank=True, verbose_name="Description")
    trails = models.ManyToManyField(Trail, related_name="courses", verbose_name="Course Trails", blank=True)
 
    THEME_CHOICES = [
        ('default', 'Default'),
        ('notdefault', 'Not default style theme just for testing'),
    ]   
    theme_slug = models.CharField(max_length=50, choices=THEME_CHOICES, default='default', verbose_name="Student Theme")
 
    def __str__(self):
        return self.title
 
class Module(models.Model):
    trail = models.ForeignKey(Trail, related_name="modules", on_delete=models.CASCADE, verbose_name="Trail", null=False, blank=False)
    title = models.CharField(max_length=200, verbose_name="Module Title", null=False, blank=False)
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    cover_image = models.ImageField(default='/module_images/default.jpg', upload_to='module_images/', null=False, blank=False, verbose_name="Module Image")
 
    class Meta:
        ordering = ['trail__title', 'order']
 
    def __str__(self):
        return f"[{self.trail.title}] {self.title}"
 
 
class LessonCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category Name", blank=False, null=False)
    module = models.ForeignKey(Module, related_name="categories", on_delete=models.CASCADE, verbose_name="Module", null=False, blank=False)
 
    def __str__(self):
        return self.name

class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name="lessons", on_delete=models.CASCADE, verbose_name="Module", null=False, blank=False)
    category = models.ForeignKey(LessonCategory, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Lesson Category")
    title = models.CharField(max_length=200, verbose_name="Lesson Title", null=False, blank=False)
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")

    LESSON_TYPES = [
        ('video', 'Video lesson'),
        ('text', 'Text lesson'),
        ('choices', 'Activity/test lesson'),
        ('pdf', 'PDF viewer'),
    ]
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPES, verbose_name="Lesson Type", default="text", null=False, blank=False)
    
    content_data = models.JSONField(default=dict)
 
    class Meta:
        ordering = ['module__title', 'order']
 
    def __str__(self):
        return f"[{self.module.title}] {self.title}"
 
    def get_video_url(self):
        return self.content_data.get('url', '')
 
    def get_text_content(self):
        return self.content_data.get('content', '')
 
    def get_pdf_url(self):
        path = self.content_data.get('url', '')
        if not path:
            return ''
        return f"{settings.MEDIA_URL}{path}"
    
    def get_questions(self):
        return self.content_data.get('questions', [])
 
 
class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress_records')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    answers = models.JSONField(null=True, blank=True)
 
    class Meta:
        unique_together = ('user', 'lesson')
 
    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} ({'✓' if self.completed else '✗'})"