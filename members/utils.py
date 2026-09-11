from django.shortcuts import render

def get_student_theme(request):
    if not hasattr(request, '_cached_theme'):
        course = request.user.course
        request._cached_theme = course.theme_slug if course else 'default'
    return request._cached_theme
    
def themed_render(request, template_name, context=None):
    if context is None:
        context = {}
    
    student_theme = get_student_theme(request)
    context['base_module'] = f'themes/{student_theme}/base_module.html'

    templates = [
        f'themes/{student_theme}/{template_name}',
        f'themes/default/{template_name}',
        f'themes/default/ysbh.html',
    ]
    return render(request, templates, context)

def is_superadmin(user):
    return user.is_active and user.is_superuser
