from django_components import Component, register


@register("landing-intro")
class LandingIntro(Component):
    template_file = "landing-intro.html"
    css_file = "landing-intro.css"
