from django_components import Component, register


@register("course-card")
class CourseCard(Component):
    template_file = "course-card.html"
    css_file = "course-card.css"

    def get_template_data(self, args, kwargs, slots, context):
        return {**kwargs}
