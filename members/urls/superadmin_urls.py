from django.urls import path
from members.views import superadmin_views

urlpatterns = [
    # Home
    path('', superadmin_views.superadmin_home, name='superadmin'),
    path('find_student/', superadmin_views.find_student, name='find_student'),
   
    # Course 
    path('manage_courses/', superadmin_views.manage_courses, name='manage_courses'),
    path('manage_courses/create/', superadmin_views.create_course, name='create_course'),
    path('manage_courses/edit/<int:course_id>/', superadmin_views.edit_course, name='edit_course'),
    path('manage_courses/delete/<int:course_id>/', superadmin_views.delete_course, name='delete_course'),
    path('enroll/<int:user_id>', superadmin_views.fast_enroll, name='enroll'),

    # Trail 
    path('manage_trails/', superadmin_views.manage_trails, name='manage_trails'),
    path('manage_trails/create/', superadmin_views.create_trail, name='create_trail'),
    path('manage_trails/edit/<int:trail_id>/', superadmin_views.edit_trail, name='edit_trail'),
    path('manage_trails/delete/<int:trail_id>/', superadmin_views.delete_trail, name='delete_trail'),
    
    # Lesson Category 
    # path('manage_lesson_categories/', superadmin_views.manage_lesson_categories, name='manage_lesson_categories'), Obsolete because categories are managed within manage_lessons
    path('manage_lesson_categories/create/', superadmin_views.create_lesson_category, name='create_lesson_category'),
    path('manage_lesson_categories/edit/<int:category_id>/', superadmin_views.edit_lesson_category, name='edit_lesson_category'),
    path('manage_lesson_categories/delete/<int:category_id>/', superadmin_views.delete_lesson_category, name='delete_lesson_category'),
    
    # Module
    path('manage_modules/', superadmin_views.manage_modules, name='manage_modules'),
    path('manage_modules/create/', superadmin_views.create_module, name='create_module'),
    path('manage_modules/edit/<int:module_id>/', superadmin_views.edit_module, name='edit_module'),
    path('manage_modules/delete/<int:module_id>/', superadmin_views.delete_module, name='delete_module'),
    
    # Lesson
    path('manage_lessons/', superadmin_views.manage_lessons, name='manage_lessons'),
    path('manage_lessons/create/', superadmin_views.create_lesson, name='create_lesson'),
    path('manage_lessons/edit/<int:lesson_id>/', superadmin_views.edit_lesson, name='edit_lesson'),
    path('manage_lessons/delete/<int:lesson_id>/', superadmin_views.delete_lesson, name='delete_lesson'), 
]