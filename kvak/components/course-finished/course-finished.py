from django_components import Component, register


@register("course-finished")
class CourseFinished(Component):
    template_file = "course-finished.html"
    css_file = "course-finished.css"
