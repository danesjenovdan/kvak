from django_components import Component, register


@register("exercise-base-material")
class ExerciseBaseMaterial(Component):
    template_file = "exercise-base-material.html"
    css_file = "exercise-base-material.css"

    def get_template_data(self, args, kwargs, slots, context):
        return {**kwargs}

    class Media:
        js = [
            "js/Sortable@1.15.6/Sortable.min.js",
            "js/questions.js",
        ]
