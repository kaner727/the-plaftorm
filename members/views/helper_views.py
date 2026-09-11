from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from members.models import LessonProgress
from members.utils import is_superadmin
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(is_superadmin, login_url='/', redirect_field_name=None)
def delete_progress(request, lesson_progress_id):
    lesson_progress = get_object_or_404(LessonProgress, id=lesson_progress_id)
    lesson_progress.delete()
    messages.success(request, "Progress deleted successfully!")
    return redirect(request.META.get('HTTP_REFERER', 'module_view'))