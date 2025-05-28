from django_components import Component, register


@register("landing-courses")
class LandingCourses(Component):
    template_file = "landing-courses.html"
    css_file = "landing-courses.css"
