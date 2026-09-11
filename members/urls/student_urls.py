from django.urls import path
from members.views import student_views

urlpatterns = [
    path('', student_views.dashboard_home, name='dashboard'),
    path('module/<int:module_id>/', student_views.module_view, name='module_view'),
    path('module/lesson/complete/<int:lesson_id>/', student_views.complete_lesson, name='complete_lesson'),
    path('module/lessons/complete/choices/<int:lesson_id>/', student_views.complete_choices_lesson, name='complete_choices_lesson'),
]
