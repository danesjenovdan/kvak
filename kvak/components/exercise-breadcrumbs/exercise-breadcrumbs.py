from django_components import Component, register


@register("exercise-breadcrumbs")
class ExerciseBreadcrumbs(Component):
    template_file = "exercise-breadcrumbs.html"
    css_file = "exercise-breadcrumbs.css"
