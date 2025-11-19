from django_components import Component, register


@register("courses-list-courses")
class CoursesListCourses(Component):
    template_file = "courses-list-courses.html"
    css_file = "courses-list-courses.css"
