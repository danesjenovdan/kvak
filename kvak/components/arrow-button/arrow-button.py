from django_components import Component, register


@register("arrow-button")
class ArrowButton(Component):
    template_file = "arrow-button.html"
    css_file = "arrow-button.css"

    def get_context_data(self, *args, **kwargs):
        return {**kwargs}
