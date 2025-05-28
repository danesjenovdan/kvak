from django_components import Component, register


@register("landing-about")
class LandingAbout(Component):
    template_file = "landing-about.html"
    css_file = "landing-about.css"
