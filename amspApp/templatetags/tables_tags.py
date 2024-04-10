import uuid

__author__ = 'mohammad'

from django import template

register = template.Library()

"""
main_model_name = this model is fill by server side and send to angular model with DetailsPagination
table_go_to_page_func_name = this func go to next/prev page of the table
table_handle_pagination_func_name = this func is switch 10 to 15 to 20 to ... table paging count
table_info_model_name = this model store table info
table_search_watch_model_name = search in $watch
"""


@register.inclusion_tag(
    "generic-templates/Table/pagination.html",
    takes_context=True)
def tablePagination(context, **kwargs):
    if not "main_model_name" in kwargs: kwargs["main_model_name"] = ""
    if not "table_go_to_page_func_name" in kwargs: kwargs["table_go_to_page_func_name"] = ""
    if not "table_handle_pagination_func_name" in kwargs: kwargs["table_handle_pagination_func_name"] = ""
    if not "table_info_model_name" in kwargs: kwargs["table_info_model_name"] = ""
    if not "table_search_watch_model_name" in kwargs: kwargs["table_search_watch_model_name"] = ""
    return kwargs


@register.inclusion_tag(
    "generic-templates/Table/pagination.html",
    takes_context=True)
def tablePagination2(context, **kwargs):
    if not "main_model_name" in kwargs: kwargs["main_model_name"] = ""
    kwargs["table_go_to_page_func_name"] = kwargs["main_model_name"] + "PageTo"
    kwargs["table_handle_pagination_func_name"] = kwargs["main_model_name"] + "TablePagination"
    kwargs["table_info_model_name"] = kwargs["main_model_name"] + "TablePropStr"
    kwargs["table_search_watch_model_name"] = kwargs["main_model_name"] + "TableFilterStr"
    return kwargs


@register.inclusion_tag(
    "generic-templates/Table/pagination_simple.html",
    takes_context=True)
def tablePaginationSimple(context, **kwargs):
    if not "main_model_name" in kwargs: kwargs["main_model_name"] = ""
    if not "table_go_to_page_func_name" in kwargs: kwargs["table_go_to_page_func_name"] = ""
    if not "table_handle_pagination_func_name" in kwargs: kwargs["table_handle_pagination_func_name"] = ""
    if not "table_info_model_name" in kwargs: kwargs["table_info_model_name"] = ""
    if not "table_search_watch_model_name" in kwargs: kwargs["table_search_watch_model_name"] = ""
    return kwargs
