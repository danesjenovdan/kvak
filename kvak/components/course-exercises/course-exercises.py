from django_components import Component, register


@register("course-exercises")
class CourseExercises(Component):
    template_file = "course-exercises.html"
    css_file = "course-exercises.css"
