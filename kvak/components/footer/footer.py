from django_components import Component, register


@register("footer")
class Footer(Component):
    template_file = "footer.html"
    css_file = "footer.css"
