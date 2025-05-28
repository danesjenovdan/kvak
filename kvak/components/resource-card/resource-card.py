from django_components import Component, register


@register("resource-card")
class ResourceCard(Component):
    template_file = "resource-card.html"
    css_file = "resource-card.css"

    def get_context_data(self, *args, **kwargs):
        return {**kwargs}
