from django_components import Component, register


@register("course-intro")
class CourseIntro(Component):
    template_file = "course-intro.html"
    css_file = "course-intro.css"
