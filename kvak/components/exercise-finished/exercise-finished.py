from django_components import Component, register


@register("exercise-finished")
class ExerciseFinished(Component):
    template_file = "exercise-finished.html"
    css_file = "exercise-finished.css"

    class Media:
        js = [
            "js/canvas-confetti@1.9.4/confetti.browser.min.js",
            "js/exercise-finished.js",
        ]
