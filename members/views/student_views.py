from collections import defaultdict
from django.urls import reverse
from members.models import LessonProgress, Module, Lesson
from members.utils import themed_render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from members.utils import is_superadmin
from django.shortcuts import render

@login_required
def dashboard_home(request):
    course = request.user.course

    if not course:
        return render(request, 'general/no_course.html')
    
    completed_lesson_ids = set(
        LessonProgress.objects.filter(user=request.user, completed=True)
        .values_list('lesson_id', flat=True)
    )

    total_lessons = 0
    completed_lessons = 0
    for trail in course.trails.prefetch_related('modules__lessons').all():
        for module in trail.modules.all():
            lessons = module.lessons.all()
            total_lessons += len(lessons)
            completed_lessons += sum(1 for l in lessons if l.id in completed_lesson_ids)

    progress = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0

    context = {
        'course': course,
        'progress': progress,
        'total_lessons': total_lessons,
        'completed_lessons': completed_lessons,
        'is_super': is_superadmin(request.user),
    }

    return themed_render(request, 'dashboard.html', context)

LESSON_TEMPLATES = {
    'video': 'video_lesson.html',
    'text': 'text_lesson.html',
    'choices': 'choices_lesson.html',
    'pdf': 'pdf_lesson.html',
}

@login_required
def module_view(request, module_id):
    module = get_object_or_404(Module, id=module_id)

    has_access = request.user.course.trails.filter(id=module.trail.id).exists()

    if not has_access:
        return redirect('dashboard_home')
    
    lessons = module.lessons.all()

    lesson_id = request.GET.get('lesson')
    if lesson_id:
        current_lesson = get_object_or_404(Lesson, id=lesson_id, module=module)
    else:
        current_lesson = lessons.first()

    if not current_lesson:
        return themed_render(request, 'module_empty.html', {'module': module})

    template_name = LESSON_TEMPLATES.get(current_lesson.lesson_type, 'text_lesson.html')

    lesson_progress = LessonProgress.objects.filter(user = request.user, lesson = current_lesson).first()

    lessons_by_category = defaultdict(list)
    for lesson in lessons:
        lessons_by_category[lesson.category].append(lesson)

    context = {
        'module': module,
        'lessons': lessons,
        'current_lesson': current_lesson,
        'completed': lesson_progress.completed if lesson_progress else False,
        'lesson_progress': lesson_progress,
        'lessons_by_category': dict(lessons_by_category),
    }

    return themed_render(request, template_name, context)

@login_required
def complete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == 'POST':

        LessonProgress.objects.update_or_create(
            user=request.user,
            lesson=lesson,
            defaults={  
                'completed': True,
                'completed_at': timezone.now()
            }
        )

    return redirect(request.META.get( 'HTTP_REFERER', reverse('module_view', args=[lesson.module.id])))

@login_required
def complete_choices_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == 'POST':
        # reset
        if request.POST.get('reset'):
            LessonProgress.objects.filter(user=request.user, lesson=lesson).delete()
            return redirect(reverse('module_view', args=[lesson.module.id]) + f'?lesson={lesson.id}')

        questions = lesson.get_questions()
        answers = []
        correct_count = 0

        for i, question in enumerate(questions):
            selected = request.POST.get(f'q{i}')
            selected = int(selected) if selected is not None else None
            is_correct = selected == question['answer']
            if is_correct:
                correct_count += 1
            answers.append({
                'question': question['question'],
                'selected': selected,
                'correct': is_correct,
            })

        score = (correct_count / len(questions) if questions else 0) * 100.0

        LessonProgress.objects.update_or_create(
            user=request.user,
            lesson=lesson,
            defaults={
                'completed': True,
                'completed_at': timezone.now(),
                'score': score,
                'answers': answers,
            }
        )

    return redirect(reverse('module_view', args=[lesson.module.id]) + f'?lesson={lesson.id}')
