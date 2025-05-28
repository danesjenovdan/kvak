from django_components import Component, register


@register("landing-resources")
class LandingResources(Component):
    template_file = "landing-resources.html"
    css_file = "landing-resources.css"
