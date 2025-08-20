from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
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


class GenericPage(Page):
    pass
