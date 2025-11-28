from django_components import Component, register


@register("suggest-courses")
class SuggestCourses(Component):
    template_file = "suggest-courses.html"
    css_file = "suggest-courses.css"
