from django.conf import settings
from django.db import models
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

from .utils import ProgressTracker


class HomePage(Page):
    intro_text = RichTextField(
        blank=True,
        features=["bold", "italic", "link"],
        verbose_name=_("Introduction text"),
    )
    courses_description = models.TextField(
        blank=True,
        verbose_name=_("Courses description"),
    )
    courses_page = models.ForeignKey(
        "home.CoursesListPage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("Courses page"),
    )
    resources_description = models.TextField(
        blank=True,
        verbose_name=_("Resources description"),
    )
    about_columns = StreamField(
        [
            (
                "about_column",
                blocks.StructBlock(
                    [
                        (
                            "title",
                            blocks.CharBlock(
                                required=True,
                                max_length=255,
                                label=_("Title"),
                            ),
                        ),
                        (
                            "page",
                            blocks.PageChooserBlock(
                                required=False,
                                label=_("Page"),
                            ),
                        ),
                        (
                            "description",
                            blocks.RichTextBlock(
                                required=False,
                                features=["bold", "italic", "link", "ul", "ol", "hr"],
                                label=_("Description"),
                            ),
                        ),
                    ],
                    icon="link",
                    label=_("Internal link"),
                ),
            )
        ],
        blank=True,
        verbose_name=_("About columns"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro_text"),
        FieldPanel("courses_description"),
        FieldPanel("courses_page"),
        FieldPanel("resources_description"),
        FieldPanel("about_columns"),
    ]

    parent_page_types = ["wagtailcore.Page"]
    subpage_types = [
        "home.CoursesListPage",
        "home.ExcerciseCategoryPage",
        "home.GenericPage",
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if self.courses_page:
            courses = self.courses_page.get_children().type(CoursePage).specific()
            context["courses"] = courses[:3]
        return context


class GenericPage(Page):
    body = RichTextField(
        blank=True,
        verbose_name=_("Body"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = []


class CoursesListPage(Page):
    intro_text = RichTextField(
        blank=True,
        features=["bold", "italic", "link"],
        verbose_name=_("Introduction text"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro_text"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.CoursePage"]


class CoursePage(Page):
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Course image"),
    )
    overview = RichTextField(
        blank=True,
        verbose_name=_("Course overview"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("image"),
        FieldPanel("overview"),
    ]

    parent_page_types = ["home.CoursesListPage"]
    subpage_types = ["home.ExercisePage"]

    def get_user_progress(self, user):
        # Get all ExercisePage instances that are children of this CoursePage
        total_exercises = self.get_children().type(ExercisePage).count()
        if user.is_anonymous or total_exercises == 0:
            return ProgressTracker(total_exercises, 0)
        finished_exercises = UserFinishedExcercisePage.objects.filter(
            user=user, exercise__in=self.get_children().type(ExercisePage)
        ).count()
        return ProgressTracker(total_exercises, finished_exercises)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        user_progress = self.get_user_progress(request.user)
        context["user_progress"] = user_progress

        exercise_index = None
        if user_progress.total > 0:
            if user_progress.finished < user_progress.total:
                exercise_index = user_progress.finished + 1
            elif user_progress.finished == user_progress.total:
                exercise_index = 1
        context["start_exercise_index"] = exercise_index

        if exercise_index is not None:
            context["start_exercise_page"] = (
                self.get_children().type(ExercisePage).specific()[exercise_index - 1]
            )

        return context


class ExcerciseCategoryPage(Page):
    description = RichTextField(
        blank=True,
        verbose_name=_("Category description"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("description"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = []


class ExercisePage(RoutablePageMixin, Page):
    description = RichTextField(
        blank=True,
        verbose_name=_("Exercise description"),
    )
    estimated_time = models.PositiveIntegerField(
        verbose_name=_("Estimated time (minutes)"),
    )
    category = models.ForeignKey(
        ExcerciseCategoryPage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="exercises",
        verbose_name=_("Category"),
    )
    order = models.PositiveIntegerField(
        verbose_name=_("Order"),
        default=0,
    )
    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("estimated_time"),
        FieldPanel("category"),
        FieldPanel("order"),
    ]

    parent_page_types = ["home.CoursePage"]
    subpage_types = ["home.BaseMaterialPage"]

    @path("")
    def render_custom(self, request):
        if not request.user or request.user.is_anonymous:
            parent_page = self.get_parent()
            if parent_page:
                return redirect(parent_page.get_url())

        return self.render(request)

    def get_user_progress(self, user):
        # Get all BaseMaterialPage instances that are children of this ExercisePage
        total_base_materials = self.get_children().type(BaseMaterialPage).count()
        if user.is_anonymous or total_base_materials == 0:
            return ProgressTracker(total_base_materials, 0)
        # Get finished BaseMaterialPage instances that are children of this ExercisePage
        base_material_pages = self.get_children().type(BaseMaterialPage).specific()
        finished_base_materials = UserFinishedBaseMaterial.objects.filter(
            user=user, base_material__in=base_material_pages
        ).count()
        return ProgressTracker(total_base_materials, finished_base_materials)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        user_progress = self.get_user_progress(request.user)
        context["user_progress"] = user_progress

        page_query = request.GET.get("page", "1")
        try:
            page_index = int(page_query)
        except ValueError:
            page_index = 1
        page_index = max(1, min(user_progress.total, page_index))

        context["base_material_page_index"] = page_index
        context["base_material_page"] = (
            self.get_children().type(BaseMaterialPage).specific()[page_index - 1]
        )
        context["base_material_next_page_index"] = (
            page_index + 1 if page_index < user_progress.total else None
        )
        context["base_material_previous_page_index"] = (
            page_index - 1 if page_index > 1 else None
        )
        if page_index == user_progress.total:
            parent_page = self.get_parent()
            if parent_page:
                context["finish_exercise_url"] = parent_page.get_url()

        return context


class AnswerOptionBlock(blocks.StructBlock):
    """Block for answer options in multiple choice questions"""

    option_text = blocks.CharBlock(
        max_length=255,
        label=_("Option text"),
    )
    is_correct = blocks.BooleanBlock(
        required=False,
        default=False,
        label=_("Is correct"),
    )

    class Meta:
        icon = "list-ul"
        label = _("Answer option")


class MultipleChoiceQuestionBlock(blocks.StructBlock):
    """Block for multiple choice question (multiple correct answers possible)"""

    question_text = blocks.RichTextBlock(
        label=_("Question text"),
        features=["bold", "italic", "link", "ul", "ol", "image"],
    )
    explanation_text = blocks.RichTextBlock(
        label=_("Explanation text"),
        required=False,
        features=["bold", "italic", "link", "ul", "ol", "image"],
    )
    answer_options = blocks.ListBlock(
        AnswerOptionBlock(),
        min_num=2,
        max_num=10,
        label=_("Answer options"),
    )

    class Meta:
        icon = "list-ul"
        label = _("Multiple Choice Question")


class OneCorrectAnswerQuestionBlock(blocks.StructBlock):
    """Block for question with one correct answer"""

    question_text = blocks.RichTextBlock(
        label=_("Question text"),
        features=["bold", "italic", "link", "ul", "ol", "image"],
    )
    explanation_text = blocks.RichTextBlock(
        label=_("Explanation text"),
        required=False,
        features=["bold", "italic", "link", "ul", "ol", "image"],
    )
    answer_options = blocks.ListBlock(
        AnswerOptionBlock(),
        min_num=2,
        # max_num=10,
        label=_("Answer options"),
    )

    class Meta:
        icon = "radio-full"
        label = _("One Correct Answer Question")


class TextAnswerQuestionBlock(blocks.StructBlock):
    """Block for question with text answer"""

    question_text = blocks.RichTextBlock(
        label=_("Question text"),
        features=["bold", "italic", "link", "ul", "ol", "image"],
    )
    explanation_text = blocks.RichTextBlock(
        label=_("Explanation text"),
        required=False,
        features=["bold", "italic", "link", "ul", "ol", "image"],
    )

    class Meta:
        icon = "edit"
        label = _("Text Answer Question")


class OrderByPriorityOptionBlock(blocks.StructBlock):
    """Block for options in priority ordering question"""

    option_text = blocks.CharBlock(
        max_length=255,
        label=_("Option text"),
    )

    class Meta:
        icon = "order"
        label = _("Priority option")


class OrderByPriorityQuestionBlock(blocks.StructBlock):
    """Block for priority ordering question"""

    question_text = blocks.RichTextBlock(
        label=_("Question text"),
        features=["bold", "italic", "link", "ul", "ol", "image"],
    )
    explanation_text = blocks.RichTextBlock(
        label=_("Explanation text"),
        required=False,
        features=["bold", "italic", "link", "ul", "ol", "image"],
    )
    priority_options = blocks.ListBlock(
        OrderByPriorityOptionBlock(),
        min_num=2,
        # max_num=10,
        label=_("Priority options"),
    )

    class Meta:
        icon = "order"
        label = _("Order by Priority Question")


class BaseMaterialPage(RoutablePageMixin, Page):
    text = RichTextField(
        blank=True,
        verbose_name=_("Text"),
    )
    video_url = models.URLField(
        blank=True,
        verbose_name=_("Video URL"),
    )
    questions = StreamField(
        [
            ("multiple_choice_question", MultipleChoiceQuestionBlock()),
            ("one_correct_answer_question", OneCorrectAnswerQuestionBlock()),
            ("text_answer_question", TextAnswerQuestionBlock()),
            ("order_by_priority_question", OrderByPriorityQuestionBlock()),
        ],
        blank=True,
        null=True,
        verbose_name=_("Questions"),
        help_text=_("Add questions for this material"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("text"),
        FieldPanel("video_url"),
        FieldPanel("questions"),
    ]

    parent_page_types = ["home.ExercisePage"]
    subpage_types = []

    @path("")
    def render_custom(self, request):
        # serve_preview is overridden by RoutablePageMixin to point here as well
        if getattr(request, "is_preview", False):
            return self.render(request)

        else:  # Not a preview
            parent_page = self.get_parent()
            if parent_page:
                if self.id:
                    child_page_ids = list(
                        parent_page.get_children()
                        .type(BaseMaterialPage)
                        .values_list("id", flat=True)
                    )
                    page_index = child_page_ids.index(self.id) + 1
                    return redirect(f"{parent_page.get_url()}?page={page_index}")

        return self.render(request)


class UserAnsweredQuestion(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="answered_questions",
        verbose_name=_("User"),
    )
    base_material_page_id = models.PositiveIntegerField(
        verbose_name=_("Base Material Page ID"),
    )
    question_id = models.CharField(
        max_length=255,
        verbose_name=_("Question ID"),
    )
    answer_data = models.JSONField(
        verbose_name=_("Answer data"),
    )
    answered_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Answered at"),
    )


class UserFinishedBaseMaterial(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="finished_exercises",
        verbose_name=_("User"),
    )
    base_material = models.ForeignKey(
        BaseMaterialPage,
        on_delete=models.CASCADE,
        related_name="finished_by_users",
        verbose_name=_("Base Material"),
    )
    finished_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Finished at"),
    )


class UserFinishedExcercisePage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="finished_courses",
        verbose_name=_("User"),
    )
    exercise = models.ForeignKey(
        ExercisePage,
        on_delete=models.CASCADE,
        related_name="finished_by_users",
        verbose_name=_("Exercise"),
    )
    finished_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Finished at"),
    )
