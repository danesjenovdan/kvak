from django.conf import settings
from django.db import models
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.signals import page_published, page_unpublished

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
                        (
                            "images",
                            blocks.StreamBlock(
                                [
                                    (
                                        "image",
                                        blocks.StructBlock(
                                            [
                                                (
                                                    "image",
                                                    ImageChooserBlock(
                                                        required=True,
                                                        label=_("Image"),
                                                    ),
                                                ),
                                                (
                                                    "link",
                                                    blocks.URLBlock(
                                                        required=False,
                                                        label=_("Link"),
                                                    ),
                                                ),
                                            ],
                                            label=_("Image"),
                                        ),
                                    ),
                                ],
                                required=False,
                                label=_("Images"),
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
        "home.ResourcePage",
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if self.courses_page:
            courses = self.courses_page.get_children().type(CoursePage).specific()
            context["courses"] = courses[:3]
            resources = self.get_children().type(ResourcePage).specific()
            context["resources"] = resources[:3]
        return context


class ResourcePage(Page):
    description = RichTextField(
        blank=True,
        verbose_name=_("Description"),
    )
    link_url = models.URLField(
        blank=True,
        verbose_name=_("Link URL"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("link_url"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = []


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


class CoursePage(RoutablePageMixin, Page):
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
    claim_badge_url = models.URLField(
        blank=True,
        verbose_name=_("Claim badge URL"),
        help_text=_("URL where users can claim their badge after completing a course"),
    )
    badge_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Badge image"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("image"),
        FieldPanel("overview"),
        FieldPanel("claim_badge_url"),
        FieldPanel("badge_image"),
    ]

    parent_page_types = ["home.CoursesListPage"]
    subpage_types = ["home.ExercisePage"]

    @path("")
    def render_custom(self, request):
        if not request.user or request.user.is_anonymous:
            return redirect("register")

        return self.render(request)

    def get_user_progress(self, user):
        # Get all ExercisePage instances that are children of this CoursePage
        total_exercises = self.get_children().type(ExercisePage).count()
        if user.is_anonymous or total_exercises == 0:
            return ProgressTracker(total_exercises, 0)
        total_exercise_pages = self.get_children().type(ExercisePage).specific()
        total_exercises_ids = list(total_exercise_pages.values_list("id", flat=True))
        finished_exercises = UserFinishedExcercisePage.objects.filter(
            user=user, exercise__in=total_exercise_pages
        )
        finished_exercises_count = finished_exercises.count()
        finished_exercises_ids = list(
            finished_exercises.values_list("exercise_id", flat=True)
        )
        print(
            f"Total exercises: {total_exercises}, Finished exercises: {finished_exercises_count}"
        )
        print(
            f"Total exercise IDs: {total_exercises_ids}, Finished exercise IDs: {finished_exercises_ids}"
        )
        return ProgressTracker(
            total_exercises,
            finished_exercises_count,
            total_ids=total_exercises_ids,
            finished_ids=finished_exercises_ids,
        )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        user_progress = self.get_user_progress(request.user)
        context["user_progress"] = user_progress

        if user_progress.finished_ids and user_progress.total_ids:
            next_exercise_id = None
            for exercise_id in user_progress.total_ids:
                if exercise_id not in user_progress.finished_ids:
                    next_exercise_id = exercise_id
                    break

            context["start_exercise_page"] = (
                self.get_children()
                .type(ExercisePage)
                .specific()
                .get(id=next_exercise_id)
                if next_exercise_id
                else None
            )
        else:
            exercise_index = None
            if user_progress.total > 0:
                if user_progress.finished < user_progress.total:
                    exercise_index = user_progress.finished + 1
                elif user_progress.finished == user_progress.total:
                    exercise_index = 1
            context["start_exercise_index"] = exercise_index

            if exercise_index is not None:
                context["start_exercise_page"] = (
                    self.get_children()
                    .type(ExercisePage)
                    .specific()[exercise_index - 1]
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
    congratulations_text = RichTextField(
        null=True,
        blank=True,
        verbose_name=_("Congratulations text"),
        help_text=_("Text to show when this exercise is finished"),
    )
    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("estimated_time"),
        FieldPanel("category"),
        FieldPanel("congratulations_text"),
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
        total_base_materials_ids = list(
            base_material_pages.values_list("id", flat=True)
        )
        finished_bm = UserFinishedBaseMaterial.objects.filter(
            user=user, base_material__in=base_material_pages
        )
        finished_base_materials_count = finished_bm.count()
        finished_base_materials_ids = list(
            finished_bm.values_list("base_material_id", flat=True)
        )
        return ProgressTracker(
            total_base_materials,
            finished_base_materials_count,
            total_ids=total_base_materials_ids,
            finished_ids=finished_base_materials_ids,
        )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        user_progress = self.get_user_progress(request.user)
        context["user_progress"] = user_progress

        finished_query = request.GET.get("finished", None)
        finished = (
            finished_query == "true" and user_progress.finished == user_progress.total
        )

        if finished:
            context["base_material_page_index"] = user_progress.total
            context["show_finished_page"] = True

            parent_page = self.get_parent()
            if parent_page:
                context["course_page"] = parent_page.specific
                course_user_progress = parent_page.specific.get_user_progress(
                    request.user
                )
                context["course_user_progress"] = course_user_progress
                if course_user_progress.finished_ids and course_user_progress.total_ids:
                    next_exercise_id = None
                    for exercise_id in course_user_progress.total_ids:
                        if exercise_id not in course_user_progress.finished_ids:
                            next_exercise_id = exercise_id
                            break

                    context["start_exercise_page"] = (
                        parent_page.specific.get_children()
                        .type(ExercisePage)
                        .specific()
                        .get(id=next_exercise_id)
                        if next_exercise_id
                        else None
                    )
        else:
            page_query = request.GET.get("page", "1")
            try:
                page_index = int(page_query)
            except ValueError:
                page_index = 1
            page_index = max(1, min(user_progress.total, page_index))

            base_material_pages = self.get_children().type(BaseMaterialPage).specific()
            context["base_material_page_index"] = page_index
            context["base_material_page"] = (
                base_material_pages[page_index - 1]
                if page_index <= len(base_material_pages)
                else None
            )
            context["base_material_next_page_index"] = (
                page_index + 1 if page_index < user_progress.total else None
            )
            context["base_material_previous_page_index"] = (
                page_index - 1 if page_index > 1 else None
            )
            if page_index == user_progress.total:
                context["finish_exercise_url"] = "?finished=true"

        return context


class AnswerOptionBlock(blocks.StructBlock):
    """Block for answer options in multiple choice questions"""

    option_text = blocks.CharBlock(
        max_length=255,
        label=_("Option text"),
    )
    option_image = ImageChooserBlock(
        required=False,
        label=_("Option image"),
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
        features=["bold", "italic", "link", "ul", "ol", "image", "embed"],
    )
    answer_options = blocks.ListBlock(
        AnswerOptionBlock(),
        min_num=2,
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
        features=["bold", "italic", "link", "ul", "ol", "image", "embed"],
    )
    answer_options = blocks.ListBlock(
        AnswerOptionBlock(),
        min_num=2,
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
        features=["bold", "italic", "link", "ul", "ol", "image", "embed"],
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
        features=["bold", "italic", "link", "ul", "ol", "image", "embed"],
    )
    priority_options = blocks.ListBlock(
        OrderByPriorityOptionBlock(),
        min_num=2,
        label=_("Priority options"),
        help_text=_(
            "List the options in the correct order here, "
            "users will get a random order of these options to sort!"
        ),
    )

    class Meta:
        icon = "order"
        label = _("Order by Priority Question")


class ConnectTwoAnswersOptionBlock(blocks.StructBlock):
    """Block for options in connect two answers question"""

    option_text_left = blocks.CharBlock(
        max_length=255,
        label=_("Left option text"),
    )
    option_text_right = blocks.CharBlock(
        max_length=255,
        label=_("Right option text"),
    )

    class Meta:
        icon = "list-ul"
        label = _("Connect Two Answers Option")


class ConnectTwoAnswersQuestionBlock(blocks.StructBlock):
    """Block for connect two answers question"""

    question_text = blocks.RichTextBlock(
        label=_("Question text"),
        features=["bold", "italic", "link", "ul", "ol", "image"],
    )
    explanation_text = blocks.RichTextBlock(
        label=_("Explanation text"),
        required=False,
        features=["bold", "italic", "link", "ul", "ol", "image", "embed"],
    )
    answer_options = blocks.ListBlock(
        ConnectTwoAnswersOptionBlock(),
        min_num=2,
        label=_("Answer options"),
    )

    class Meta:
        icon = "list-ul"
        label = _("Connect Two Answers Question")


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
            ("connect_two_answers_question", ConnectTwoAnswersQuestionBlock()),
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


def on_page_published(sender, instance, **kwargs):
    if isinstance(instance, BaseMaterialPage):
        exercise_page = instance.get_parent().specific

        question_ids = set()
        for block in instance.questions:
            question_ids.add(block.id)

        user_finished_qs = UserFinishedBaseMaterial.objects.filter(
            base_material=instance,
        )

        for user_finished in user_finished_qs:
            answered_questions_ids = UserAnsweredQuestion.objects.filter(
                user=user_finished.user,
                base_material_page_id=instance.id,
            ).values_list("question_id", flat=True)
            found_question_ids = set(answered_questions_ids)
            if not question_ids.issubset(found_question_ids):
                print(
                    f"User {user_finished.user} has answered questions {found_question_ids} "
                    f"but current question ids are {question_ids}, deleting finished status"
                )
                user_finished.delete()
                UserFinishedExcercisePage.objects.filter(
                    user=user_finished.user,
                    exercise=exercise_page,
                ).delete()

        user_finished_exercises_qs = UserFinishedExcercisePage.objects.filter(
            exercise=exercise_page,
        )

        for user_finished_exercise in user_finished_exercises_qs:
            user_finished_base_materials = UserFinishedBaseMaterial.objects.filter(
                user=user_finished_exercise.user,
                base_material__in=exercise_page.get_children().type(BaseMaterialPage),
            )
            finished_base_material_ids = set(
                user_finished_base_materials.values_list("base_material_id", flat=True)
            )
            exercise_base_material_ids = set(
                exercise_page.get_children()
                .type(BaseMaterialPage)
                .values_list("id", flat=True)
            )
            if not exercise_base_material_ids.issubset(finished_base_material_ids):
                print(
                    f"User {user_finished_exercise.user} has finished exercise {exercise_page} "
                    f"but has not finished all base materials, deleting finished status"
                )
                user_finished_exercise.delete()


page_published.connect(on_page_published)


def on_page_unpublished(sender, instance, **kwargs):
    if isinstance(instance, BaseMaterialPage):
        print(f"BaseMaterialPage unpublished: {instance.title}")


page_unpublished.connect(on_page_unpublished)
