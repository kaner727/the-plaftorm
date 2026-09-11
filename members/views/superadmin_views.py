from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from members.forms import TrailForm, CourseForm, ModuleForm, LessonCategoryForm, LessonForm
from members.models import Course, LessonCategory, Module, Lesson, User, Trail
from members.utils import is_superadmin
from members.services import build_lesson_content

# ─── HOME ────────────────────────────────────────────────────────────────────
 
@user_passes_test(is_superadmin, login_url='/', redirect_field_name=None) 
def superadmin_home(request): 
    context = {
        'user_list': User.objects.all(),
        'courses': Course.objects.all(),
        'found_user': None
    }
    return render(request, 'superadmin/superadmin_home.html', context)

@user_passes_test(is_superadmin, login_url='/', redirect_field_name=None)
def find_student(request):
    username_query = request.GET.get('username', '')
    email_query = request.GET.get('email', '')
 
    found_user = User.objects.filter(is_superuser=False)
    if username_query:
        found_user = found_user.filter(username__icontains=username_query)
    elif email_query:
        found_user = found_user.filter(email__icontains=email_query)
 
    context = {
        'courses': Course.objects.all(),
        'user_list': User.objects.all(),
        'found_user': found_user.first() if found_user.exists() else None,
    }

    return render(request, 'superadmin/superadmin_home.html', context)

# ─── Trails ────────────────────────────────────────────────────────────────────

@user_passes_test(is_superadmin, login_url='/', redirect_field_name=None)
def manage_trails(request):
    trails = Trail.objects.all()

    context = {
        'trails': trails
    }

    return render(request, 'superadmin/manage_trails.html', context)

@user_passes_test(is_superadmin, login_url='/', redirect_field_name=None)
def create_trail(request):
    if request.method == 'POST':
        form = TrailForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Trail created successfully.")
        else:
            messages.error(request, "Error creating the trail.")

    return redirect(request.META.get('HTTP_REFERER', 'manage_trails'))

@user_passes_test(is_superadmin, login_url='/', redirect_field_name=None)
def edit_trail(request, trail_id):  
    trail = get_object_or_404(Trail, id=trail_id)
    if request.method == 'POST':
        form = TrailForm(request.POST, instance=trail)

        if form.is_valid():
            form.save()
            messages.success(request, "Trail updated successfully.")
        else:
            messages.error(request, "Error updating the trail.")

    return redirect(request.META.get('HTTP_REFERER', 'manage_trails'))

@user_passes_test(is_superadmin, login_url='/', redirect_field_name=None)
def delete_trail(request, trail_id):
    trail = get_object_or_404(Trail, id=trail_id)
    trail.delete()
    messages.success(request, "Trail deleted successfully!")
    return redirect(request.META.get('HTTP_REFERER', 'manage_trails'))

# ─── Courses ────────────────────────────────────────────────────────────────────
 
@user_passes_test(is_superadmin, login_url='/', redirect_field_name=None) 
def manage_courses(request):
    trails = Trail.objects.all()
    courses = Course.objects.all()

    context = {
        'trails': trails,
        'courses': courses,
        'themes': Course.THEME_CHOICES
    }

    return render(request, 'superadmin/manage_courses.html', context)

@user_passes_test(is_superadmin, login_url='/', redirect_field_name=None) 
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Course created successfully.")
        else:
            messages.error(request, "Error creating the course.")

    return redirect(request.META.get('HTTP_REFERER', 'manage_courses'))

@user_passes_test(is_superadmin, login_url='/', redirect_field_name=None)
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':    
        form = CourseForm(request.POST, instance=course)

        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully.")
        else:
            messages.error(request, "Error updating the course.")

    return redirect(request.META.get('HTTP_REFERER', 'manage_courses'))

@user_passes_test(is_superadmin, login_url='/', redirect_field_name=None)
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    messages.success(request, "Course deleted successfully!")
    return redirect(request.META.get('HTTP_REFERER', 'manage_courses')) 

# ─── Modules ────────────────────────────────────────────────────────────────────

@user_passes_test(is_superadmin, login_url='/', redirect_field_name=None)
def manage_modules(request):
    trails = Trail.objects.all()
    modules = Module.objects.select_related('trail').all()

    context = {
        'trails': trails,
        'modules': modules
    }

    return render(request, 'superadmin/manage_modules.html', context)

@user_passes_test(is_superadmin, login_url='/', redirect_field_name=None)
def create_module(request):
    if request.method == 'POST':
        form = ModuleForm(request.POST, request.FILES)

        if form.is_valid():
            form.save() 
            messages.success(request, "Module created successfully.")
        else:
            messages.error(request, "Error creating the module.")
        
    return redirect(request.META.get('HTTP_REFERER', 'manage_modules'))

@user_passes_test(is_superadmin, login_url='/', redirect_field_name=None)
def edit_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)

        if form.is_valid():
            form.save()
            messages.success(request, "Module updated successfully.")
        else:
            messages.error(request, "Error updating the module.")
        
    return redirect(request.META.get('HTTP_REFERER', 'manage_modules'))

@user_passes_test(is_superadmin, login_url='/', redirect_field_name=None)
def delete_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    module.delete()
    messages.success(request, "Module deleted successfully!")
    return redirect(request.META.get('HTTP_REFERER', 'manage_modules'))

# ─── Lessons ────────────────────────────────────────────────────────────────────
 
@user_passes_test(is_superadmin, login_url='/', redirect_field_name=None)
def manage_lessons(request):
    module = Module.objects.select_related('trail').all()
    lessons = Lesson.objects.select_related('module__trail', 'category').all()
    categories = LessonCategory.objects.all()  
    courses = Course.objects.all()
    trails = Trail.objects.all()

    context = {
        'modules': module,
        'lessons': lessons,
        'lesson_types': Lesson.LESSON_TYPES,
        'categories': categories,
        'courses': courses,
        'trails': trails
    }

    return render(request, 'superadmin/manage_lessons.html', context)

@user_passes_test(is_superadmin, login_url='/', redirect_field_name=None)
def create_lesson(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.content_data = build_lesson_content(lesson.lesson_type, request.POST, request.FILES)
            lesson.save()
            messages.success(request, "Lesson created successfully.")
        else:
            messages.error(request, "Error creating the lesson.")

    return redirect(request.META.get('HTTP_REFERER', 'manage_lessons'))

@user_passes_test(is_superadmin, login_url='/', redirect_field_name=None)
def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.content_data = build_lesson_content(lesson.lesson_type, request.POST, request.FILES)
            lesson.save()
            messages.success(request, "Lesson updated successfully.")
        else:
            messages.error(request, "Error updating the lesson")
        
    return redirect(request.META.get('HTTP_REFERER', 'manage_lessons'))

@user_passes_test(is_superadmin, login_url='/', redirect_field_name=None)
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    lesson.delete()
    messages.success(request, "Lesson deleted successfully!") 
    return redirect(request.META.get('HTTP_REFERER', 'manage_lessons'))

# ─── Lesson Categories ────────────────────────────────────────────────────────── 
  
@user_passes_test(is_superadmin, login_url='/', redirect_field_name=None)
def create_lesson_category(request):
    if request.method == 'POST':
        form = LessonCategoryForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully.")
        else:
            messages.error(request, "Error creating the category.")

    return redirect(request.META.get('HTTP_REFERER', 'manage_lessons'))

# The frontend only submits the category name, not the module. Update it to allow editing the module.
@user_passes_test(is_superadmin, login_url='/', redirect_field_name=None)
def edit_lesson_category(request, category_id):
    category = get_object_or_404(LessonCategory, id=category_id)
    if request.method == 'POST':
        form = LessonCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()  
            messages.success(request, "Category updated successfully.")
        else:
            messages.error(request, "Error updating the category.")

    return redirect(request.META.get('HTTP_REFERER', 'manage_lessons'))
 
@user_passes_test(is_superadmin, login_url='/', redirect_field_name=None)
def delete_lesson_category(request, category_id):
    category = get_object_or_404(LessonCategory, id=category_id)
    category.delete()
    messages.success(request, "Category deleted successfully!")
    return redirect(request.META.get('HTTP_REFERER', 'manage_lessons'))

# ─── Fast Enroll ──────────────────────────────────────────────────────────────

@user_passes_test(is_superadmin, login_url='/', redirect_field_name=None)
def fast_enroll(request, user_id):
    if request.method == 'POST':
        # Get the selected student
        user = get_object_or_404(User, id=user_id)
    
        # Get the selected course
        courseid = request.POST.get('course_id')   
        course = get_object_or_404(Course, id=courseid) 

        user.course = course
        user.save() 
        
        messages.success(request, f"Course '{course.title}' assigned to student '{user.username}' successfully!")

    return redirect(request.META.get('HTTP_REFERER', 'superadmin_home'))