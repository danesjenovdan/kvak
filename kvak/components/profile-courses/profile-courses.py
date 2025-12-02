from django_components import Component, register


@register("profile-courses")
class ProfileCourses(Component):
    template_file = "profile-courses.html"
    css_file = "profile-courses.css"
