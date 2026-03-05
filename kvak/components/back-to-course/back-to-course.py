from django_components import Component, register


@register("back-to-course")
class BackToCourse(Component):
    template_file = "back-to-course.html"
    css_file = "back-to-course.css"
