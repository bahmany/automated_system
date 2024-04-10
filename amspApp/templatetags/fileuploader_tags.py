import uuid

__author__ = 'mohammad'

from django import template


register = template.Library()



@register.inclusion_tag(
    "share/filecloud/FileUploader.html",
    takes_context=True)
def FileUploader(context, **kwargs):
    kwargs["width"] = kwargs["width"] if "width" in kwargs else '100px'
    kwargs["readonly"] = kwargs["readonly"] if "readonly" in kwargs else 'true'
    return kwargs

@register.inclusion_tag(
    "share/filecloud/FileUploader2.html",
    takes_context=True)
def FileUploader2(context, **kwargs):
    kwargs["width"] = kwargs["width"] if "width" in kwargs else '100px'
    kwargs["readonly"] = kwargs["readonly"] if "readonly" in kwargs else 'true'
    return kwargs
