from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView

from home.models import BaseMaterialPage, CoursePage, UserAnsweredQuestion
from users.forms import CustomUserCreationForm


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("register_done")
    template_name = "registration/register.html"


class RegisterDoneView(TemplateView):
    template_name = "registration/register_done.html"


@method_decorator(login_required, name="dispatch")
class ProfileView(TemplateView):
    template_name = "registration/profile.html"

    def _get_started_courses(self, user):
        bm_ids = (
            UserAnsweredQuestion.objects.filter(user=user)
            .values_list("base_material_page_id", flat=True)
            .distinct()
        )
        bm_pages = BaseMaterialPage.objects.filter(id__in=bm_ids)

        courses = set()
        for page in bm_pages:
            course_page = page.get_parent().get_parent().specific
            if isinstance(course_page, CoursePage):
                courses.add(course_page)

        # sort completed first
        def is_completed(course):
            user_progress = course.get_user_progress(user)
            return user_progress.total == user_progress.finished

        return list(sorted(courses, key=is_completed, reverse=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self._get_started_courses(self.request.user)

        class DummyForm:
            def __iter__(self):
                return iter([])

        context["form"] = DummyForm()
        context["started_courses"] = self._get_started_courses(self.request.user)

        return context
