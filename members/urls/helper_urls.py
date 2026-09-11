from django.urls import path
from members.views import helper_views

urlpatterns = [
    path('superadmin/helper/delete_progress/<int:lesson_progress_id>/', helper_views.delete_progress, name='delete_progress'),
]