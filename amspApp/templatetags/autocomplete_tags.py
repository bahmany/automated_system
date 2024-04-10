from django import template
from django.template.loader_tags import register


@register.inclusion_tag(
    "generic-templates/Autocomplete/custome.html",
    takes_context=True)
def AutocompleteTag(context, **kwargs):
    if not "modelname" in kwargs: kwargs["modelname"] = ""
    if not "placeholder" in kwargs: kwargs["placeholder"] = ""
    if not "icon" in kwargs: kwargs["icon"] = ""
    if not "modelOfValue1" in kwargs: kwargs["modelOfValue1"] = ""
    if not "modelOfValue2" in kwargs: kwargs["modelOfValue2"] = ""
    return kwargs
