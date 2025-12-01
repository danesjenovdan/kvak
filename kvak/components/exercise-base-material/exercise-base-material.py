from django_components import Component, register


@register("exercise-base-material")
class ExerciseBaseMaterial(Component):
    template_file = "exercise-base-material.html"
    css_file = "exercise-base-material.css"

    class Media:
        js = [
            "js/Sortable@1.15.6/Sortable.min.js",
            "js/questions.js",
        ]
