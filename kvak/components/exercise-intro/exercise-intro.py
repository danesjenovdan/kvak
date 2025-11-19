from django_components import Component, register


@register("exercise-intro")
class ExerciseIntro(Component):
    template_file = "exercise-intro.html"
    css_file = "exercise-intro.css"
