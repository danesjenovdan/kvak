from django_components import Component, register


@register("progress-pips")
class ProgressPips(Component):
    template_file = "progress-pips.html"
    css_file = "progress-pips.css"

    def get_template_data(self, args, kwargs, slots, context):
        return {**kwargs}
