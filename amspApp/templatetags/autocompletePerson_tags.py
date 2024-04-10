from django import template
from django.template.loader_tags import register


@register.inclusion_tag(
    "generic-templates/Autocomplete/member.html",
    takes_context=True)
def AutocompleteMemberTag(context, **kwargs):
    if not "modelname" in kwargs: kwargs["modelname"] = ""
    if not "caption" in kwargs: kwargs["caption"] = "Select a person"
    context = context

    return kwargs