from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.template.loader import get_template
from django.conf import settings
from members.models import Course, Trail, Module, LessonCategory, Lesson, LessonProgress, User
# ─── Reusable fixtures ────────────────────────────────────────────────────
# Centralize object creation here instead of repeating it in each test.

def make_structure():
    """Create the complete structure: Trail → Module → LessonCategory → Lesson"""
    trail = Trail.objects.create(title="Leadership")
    module = Module.objects.create(trail=trail, title="Communication", order=1)
    category = LessonCategory.objects.create(name="Theory", module=module)
    return trail, module, category


# ─── Trail ────────────────────────────────────────────────────────────────────

class TrailModelTest(TestCase):

    def test_str_returns_title(self):
        trail = Trail.objects.create(title="People Management")
        self.assertEqual(str(trail), "People Management")

    def test_description_can_be_empty(self):
        # blank=True on the field — saving should succeed
        trail = Trail.objects.create(title="Trail Without Description", description="")
        self.assertEqual(trail.description, "")


# ─── Course ───────────────────────────────────────────────────────────────────

class CourseModelTest(TestCase):

    def test_theme_defaults_to_default(self):
        course = Course.objects.create(title="Onboarding")
        self.assertEqual(course.theme_slug, "default")

    def test_add_trail_to_course(self):
        trail = Trail.objects.create(title="Sales")
        course = Course.objects.create(title="Sales Course")
        course.trails.add(trail)
        # Check the ManyToMany relationship in both directions
        self.assertIn(trail, course.trails.all())
        self.assertIn(course, trail.courses.all())

    def test_course_without_trails(self):
        course = Course.objects.create(title="Empty Course")
        self.assertEqual(course.trails.count(), 0)


# ─── Module ───────────────────────────────────────────────────────────────────

class ModuleModelTest(TestCase):

    def setUp(self):
        self.trail = Trail.objects.create(title="Productivity")

    def test_str_includes_trail_name(self):
        module = Module.objects.create(trail=self.trail, title="Focus", order=1)
        self.assertEqual(str(module), "[Productivity] Focus")

    def test_deleting_trail_deletes_modules(self):
        # on_delete=CASCADE — deleting the trail also deletes its modules
        module = Module.objects.create(trail=self.trail, title="Module X", order=1)
        self.trail.delete()
        self.assertFalse(Module.objects.filter(pk=module.pk).exists())


# ─── Lesson ───────────────────────────────────────────────────────────────────

class LessonModelTest(TestCase):

    def setUp(self):
        trail, module, category = make_structure()
        self.module = module
        self.category = category

    def _make_lesson(self, lesson_type, content_data):
        return Lesson.objects.create(
            module=self.module,
            category=self.category,
            title="Test Lesson",
            order=1,
            lesson_type=lesson_type,
            content_data=content_data,
        )

    def test_get_video_url_returns_url(self):
        lesson = self._make_lesson("video", {"url": "https://youtube.com/embed/abc"})
        self.assertEqual(lesson.get_video_url(), "https://youtube.com/embed/abc")

    def test_get_video_url_returns_empty_when_missing(self):
        lesson = self._make_lesson("video", {})
        self.assertEqual(lesson.get_video_url(), "")

    def test_get_text_content(self):
        lesson = self._make_lesson("text", {"content": "<p>Hello world</p>"})
        self.assertEqual(lesson.get_text_content(), "<p>Hello world</p>")

    def test_get_questions_returns_list(self):
        questions = [{"question": "2+2?", "options": ["3", "4"], "answer": 1}]
        lesson = self._make_lesson("choices", {"questions": questions})
        self.assertEqual(len(lesson.get_questions()), 1)
        self.assertEqual(lesson.get_questions()[0]["answer"], 1)

    def test_get_questions_returns_empty_list_when_missing(self):
        lesson = self._make_lesson("choices", {})
        self.assertEqual(lesson.get_questions(), [])

    def test_str_includes_module_name(self):
        lesson = self._make_lesson("text", {})
        self.assertIn("Communication", str(lesson))


# ─── LessonProgress ───────────────────────────────────────────────────────────

class LessonProgressModelTest(TestCase):

    def setUp(self):
        trail, module, category = make_structure()
        self.user = User.objects.create_user(username="arthur", password="password123")
        self.lesson = Lesson.objects.create(
            module=module,
            category=category,
            title="Progress Lesson",
            order=1,
            lesson_type="text",
            content_data={"content": "Text"},
        )

    def test_progress_starts_incomplete(self):
        progress = LessonProgress.objects.create(user=self.user, lesson=self.lesson)
        self.assertFalse(progress.completed)
        self.assertIsNone(progress.completed_at)

    def test_unique_together_prevents_duplicates(self):
        from django.db import IntegrityError
        LessonProgress.objects.create(user=self.user, lesson=self.lesson)
        with self.assertRaises(IntegrityError):
            LessonProgress.objects.create(user=self.user, lesson=self.lesson)

    def test_str_indicates_status(self):
        progress = LessonProgress.objects.create(user=self.user, lesson=self.lesson, completed=True)
        self.assertIn("✓", str(progress))

    def test_score_can_be_null(self):
        progress = LessonProgress.objects.create(user=self.user, lesson=self.lesson)
        self.assertIsNone(progress.score)


class EnglishInterfaceTest(TestCase):
    def setUp(self):
        self.trail, self.module, self.category = make_structure()
        self.user = User.objects.create_user(username='student', password='test-password')
        self.course = self.user.course
        self.course.trails.add(self.trail)
        self.lesson = Lesson.objects.create(
            module=self.module, category=self.category, title='Quiz', order=2,
            lesson_type='choices', content_data={'questions': [
                {'question': '2+2?', 'options': ['3', '4'], 'answer': 1},
            ]},
        )
        self.client.force_login(self.user)

    def test_all_project_templates_compile(self):
        for path in (settings.BASE_DIR / 'templates').rglob('*.html'):
            with self.subTest(template=path):
                get_template(path.relative_to(settings.BASE_DIR / 'templates').as_posix())

    def test_both_themes_render_every_lesson_type(self):
        for theme, _ in Course.THEME_CHOICES:
            self.course.theme_slug = theme
            self.course.save()
            self.assertContains(self.client.get(reverse('dashboard')), 'lang="en"')
            for kind, label in Lesson.LESSON_TYPES:
                self.lesson.lesson_type = kind
                self.lesson.save()
                url = reverse('module_view', args=[self.module.pk]) + f'?lesson={self.lesson.pk}'
                with self.subTest(theme=theme, kind=kind):
                    response = self.client.get(url)
                    self.assertEqual(response.context['current_lesson'], self.lesson)
                    self.assertContains(response, 'lang="en"')
                    self.assertContains(response, label)

    def test_quiz_submission_and_reset(self):
        url = reverse('complete_choices_lesson', args=[self.lesson.pk])
        response = self.client.post(url, {'q0': '1'})
        expected = reverse('module_view', args=[self.module.pk]) + f'?lesson={self.lesson.pk}'
        self.assertRedirects(response, expected)
        progress = LessonProgress.objects.get(user=self.user, lesson=self.lesson)
        self.assertEqual(progress.score, 100)
        self.assertTrue(progress.answers[0]['correct'])
        self.assertContains(self.client.get(expected), 'Correct answer')
        self.assertRedirects(self.client.post(url, {'reset': '1'}), expected)
        self.assertFalse(LessonProgress.objects.filter(user=self.user, lesson=self.lesson).exists())

    def test_completion(self):
        response = self.client.post(reverse('complete_lesson', args=[self.lesson.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(LessonProgress.objects.get(user=self.user, lesson=self.lesson).completed)

    def test_account_and_admin_pages_render(self):
        self.client.logout()
        for name, text in [('account_login', 'Sign in to your account'),
                           ('account_signup', 'Create your free account'),
                           ('account_reset_password', 'Password recovery')]:
            self.assertContains(self.client.get(reverse(name)), text)
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        self.client.force_login(self.user)
        for name, text in [('superadmin', 'Operations Dashboard'),
                           ('manage_courses', 'Manage Courses'),
                           ('manage_trails', 'Manage Trails'),
                           ('manage_modules', 'Manage Modules'),
                           ('manage_lessons', 'Manage Lessons'),
                           ('account_email', 'Manage Email Addresses'),
                           ('account_change_password', 'Change Password'),
                           ('account_logout', 'Are you sure you want to sign out?')]:
            with self.subTest(page=name):
                self.assertContains(self.client.get(reverse(name)), text)
