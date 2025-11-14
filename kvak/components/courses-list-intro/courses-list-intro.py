from django_components import Component, register


@register("courses-list-intro")
class CoursesListIntro(Component):
    template_file = "courses-list-intro.html"
    css_file = "courses-list-intro.css"
