from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import RichTextField, StreamField


@register_setting
class HeaderSettings(BaseGenericSetting):
    navigation = StreamField(
        [
            (
                "page_link",
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
                                required=True,
                                label=_("Page"),
                            ),
                        ),
                    ],
                    icon="link",
                    label=_("Internal link"),
                ),
            ),
            (
                "external_link",
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
                            "url",
                            blocks.URLBlock(
                                required=True,
                                label=_("Link"),
                            ),
                        ),
                    ],
                    icon="link",
                    label=_("External link"),
                ),
            ),
        ],
        blank=True,
        verbose_name=_("Navigation"),
    )

    panels = [
        FieldPanel("navigation"),
    ]

    class Meta:
        verbose_name = _("Header Settings")


@register_setting
class MiscSettings(BaseGenericSetting):
    suggest_courses_text = RichTextField(
        blank=True,
        features=["bold", "italic", "link"],
        verbose_name=_("Suggest courses text"),
    )
    suggest_courses_text_2 = RichTextField(
        blank=True,
        features=["bold", "italic", "link"],
        verbose_name=_("Suggest courses text 2"),
    )

    panels = [
        FieldPanel("suggest_courses_text"),
        FieldPanel("suggest_courses_text_2"),
    ]

    class Meta:
        verbose_name = _("Miscellaneous Settings")
