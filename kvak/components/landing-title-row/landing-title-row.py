from django_components import Component, register


@register("landing-title-row")
class LandingTitleRow(Component):
    template_file = "landing-title-row.html"
    css_file = "landing-title-row.css"

    def get_context_data(self, *args, **kwargs):
        return {**kwargs}
