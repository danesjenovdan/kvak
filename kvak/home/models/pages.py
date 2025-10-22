from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page


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
        FieldPanel("resources_description"),
        FieldPanel("about_columns"),
    ]

    parent_page_types = ["wagtailcore.Page"]
    subpage_types = [
        "home.CoursesListPage", 
        "home.ExcerciseCategoryPage", 
        "home.GenericPage"
    ]


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
    overview = RichTextField(
        blank=True,
        verbose_name=_("Course overview"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("overview"),
    ]

    parent_page_types = ["home.CoursesListPage"]
    subpage_types = ["home.ExercisePage"]


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


class ExercisePage(Page):
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
        features=["bold", "italic", "link", "ul", "ol"],
    )
    explanation_text = blocks.RichTextBlock(
        label=_("Explanation text"),
        required=False,
        features=["bold", "italic", "link", "ul", "ol"],
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
        features=["bold", "italic", "link", "ul", "ol"],
    )
    explanation_text = blocks.RichTextBlock(
        label=_("Explanation text"),
        required=False,
        features=["bold", "italic", "link", "ul", "ol"],
    )
    answer_options = blocks.ListBlock(
        AnswerOptionBlock(),
        min_num=2,
        max_num=10,
        label=_("Answer options"),
    )

    class Meta:
        icon = "radio-full"
        label = _("One Correct Answer Question")


class TextAnswerQuestionBlock(blocks.StructBlock):
    """Block for question with text answer"""

    question_text = blocks.RichTextBlock(
        label=_("Question text"),
        features=["bold", "italic", "link", "ul", "ol"],
    )
    explanation_text = blocks.RichTextBlock(
        label=_("Explanation text"),
        required=False,
        features=["bold", "italic", "link", "ul", "ol"],
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
        features=["bold", "italic", "link", "ul", "ol"],
    )
    explanation_text = blocks.RichTextBlock(
        label=_("Explanation text"),
        required=False,
        features=["bold", "italic", "link", "ul", "ol"],
    )
    priority_options = blocks.ListBlock(
        OrderByPriorityOptionBlock(),
        min_num=2,
        max_num=10,
        label=_("Priority options"),
    )

    class Meta:
        icon = "order"
        label = _("Order by Priority Question")


class BaseMaterialPage(Page):
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
