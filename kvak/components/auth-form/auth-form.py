from django_components import Component, register


@register("auth-form")
class AuthForm(Component):
    template_file = "auth-form.html"
    css_file = "auth-form.css"

    def get_context_data(self, *args, **kwargs):
        return {**kwargs}
