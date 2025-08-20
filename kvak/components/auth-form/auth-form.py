from django_components import Component, register


@register("auth-form")
class AuthForm(Component):
    template_file = "auth-form.html"
    css_file = "auth-form.css"
    js_file = "auth-form.js"

    def get_template_data(self, args, kwargs, slots, context):
        return {**kwargs}

    class Media:
        js = [
            "js/autocomplete-js@3.0.3/autocomplete.min.js",
        ]
        css = [
            "js/autocomplete-js@3.0.3/style.css",
        ]
