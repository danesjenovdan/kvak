from django.core.management.base import BaseCommand
from django.utils.text import slugify
from wagtail.models import Page
from wagtail.rich_text import RichText
from wagtail.templatetags.wagtailcore_tags import richtext

from home.models import (
    BaseMaterialPage,
    CoursePage,
    CoursesListPage,
    ExcerciseCategoryPage,
    ExercisePage,
    HomePage,
)


class Command(BaseCommand):
    help = "Export course texts"

    def write_out(self, text):
        # self.stdout.write(text)
        with open("courses_texts.md", "a") as f:
            f.write(text)

    def write_out_answers(self, question_value):
        answers = question_value.get("answer_options", [])
        if not answers:
            answers = question_value.get("priority_options", [])
        if not answers:
            return

        # option_text
        # is_correct
        # option_text_left
        # option_text_right

        self.write_out("###### Answer options\n\n")
        for answer in answers:
            if "option_text_left" in answer and "option_text_right" in answer:
                option_text_left = answer.get("option_text_left", "") or ""
                option_text_left = option_text_left.replace(".", "\\.")
                option_text_right = answer.get("option_text_right", "") or ""
                option_text_right = option_text_right.replace(".", "\\.")
                self.write_out(
                    f"- {richtext(option_text_left)} | {richtext(option_text_right)}\n"
                )
                continue
            option_text = answer.get("option_text", "") or ""
            option_text = option_text.replace(".", "\\.")
            is_correct = answer.get("is_correct", False)
            is_correct_text = "(Correct)" if is_correct else ""
            self.write_out(f"- {richtext(option_text)} {is_correct_text}\n")
        self.write_out("\n")

    def handle(self, *args, **options):
        self.stdout.write("Starting export ...")

        with open("courses_texts.md", "w") as f:
            f.write("# Courses\n\n")

        courses = CoursePage.objects.all().live()
        for course in courses:
            self.stdout.write(f"Exporting course: {course.title}")

            self.write_out(f"---\n\n")

            self.write_out(f"## {course.title}\n\n")
            self.write_out(f"{richtext(course.overview)}\n\n")

            exercises = ExercisePage.objects.descendant_of(course).live()
            for exercise in exercises:
                self.write_out(f"### {exercise.title}\n\n")
                self.write_out(f"{richtext(exercise.description)}\n\n")

                base_materials = BaseMaterialPage.objects.descendant_of(exercise).live()
                for material in base_materials:
                    self.write_out(f"#### {material.title}\n\n")
                    self.write_out(f"{richtext(material.text)}\n\n")

                    for question in material.questions:
                        self.write_out("##### Question\n\n")
                        self.write_out(
                            f"{richtext(question.value["question_text"])}\n\n"
                        )
                        self.write_out("###### Explanation\n\n")
                        self.write_out(
                            f"{richtext(question.value["explanation_text"])}\n\n"
                        )
                        self.write_out_answers(question.value)

        self.stdout.write(self.style.SUCCESS("Done!"))
