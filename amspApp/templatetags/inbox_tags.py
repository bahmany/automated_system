import uuid

__author__ = 'mohammad'

from django import template


register = template.Library()



@register.inclusion_tag(
    "generic-templates/Inbox/ListHeaderButtons.html",
    takes_context=True)
def InboxHeaderList(context, **kwargs):
    if not "loadingComposeLetter" in kwargs: kwargs["loadingComposeLetter"] = "loadingComposeLetter"
    if not "loadingComposeLetter_NewLetter" in kwargs: kwargs["loadingComposeLetter_NewLetter"] = "loadingComposeLetter||NewLetter()"
    if not "ComposeTooltip" in kwargs: kwargs["ComposeTooltip"] = "New letter"
    if not "InboxList_selected_ForwardSelected" in kwargs: kwargs["InboxList_selected_ForwardSelected"] = "!InboxList.selected||ForwardSelected()"
    if not "InboxList_selected_ForwardSelectedArcive" in kwargs: kwargs["InboxList_selected_ForwardSelectedArcive"] = "!InboxList.selected||ForwardSelectedArchve()"
    if not "chevron_disable_InboxList_selected" in kwargs: kwargs["chevron_disable_InboxList_selected"] = "{'chevron-disable': !InboxList.selected}"
    if not "forward_selected_items_tip" in kwargs: kwargs["forward_selected_items_tip"] = "forward selected items"
    if not "InboxList_selected_MoveToArchive" in kwargs: kwargs["InboxList_selected_MoveToArchive"] = "!InboxList.selected||MoveToArchive()"
    if not "chevron_disable_InboxList_selected" in kwargs: kwargs["chevron_disable_InboxList_selected"] = "{'chevron-disable': !InboxList.selected}"
    if not "archvie_selected_items_tip" in kwargs: kwargs["archvie_selected_items_tip"] = "archvie selected items"
    if not "InboxList_selected_TrashSelected" in kwargs: kwargs["InboxList_selected_TrashSelected"] = "!InboxList.selected||TrashSelected()"
    if not "chevron_disable_InboxList_selected" in kwargs: kwargs["chevron_disable_InboxList_selected"] = "{'chevron-disable': !InboxList.selected}"
    if not "move_selected_items_to_trash" in kwargs: kwargs["move_selected_items_to_trash"] = "move selected items to trash"
    if not "InboxList_previous_InboxPageTo_InboxList_previous" in kwargs: kwargs["InboxList_previous_InboxPageTo_InboxList_previous"] = "!InboxList.previous||InboxPageTo(InboxList.previous)"
    if not "chevron_disable_InboxList_previous" in kwargs: kwargs["chevron_disable_InboxList_previous"] = "{'chevron-disable': !InboxList.previous}"
    if not "go_to_next_page" in kwargs: kwargs["go_to_next_page"] = "go to next page"
    if not "InboxList_from_1" in kwargs: kwargs["InboxList_from_1"] = "InboxList.from+1"
    if not "InboxList_to" in kwargs: kwargs["InboxList_to"] = "InboxList.to"
    if not "InboxList_total" in kwargs: kwargs["InboxList_total"] = "InboxList.total"
    if not "InboxList_next_InboxPageTo_InboxList_next" in kwargs: kwargs["InboxList_next_InboxPageTo_InboxList_next"] = "!InboxList.next||InboxPageTo(InboxList.next)"
    if not "chevron_disable_InboxList_next" in kwargs: kwargs["chevron_disable_InboxList_next"] = "{'chevron-disable': !InboxList.next}"
    if not "go_to_previous_page" in kwargs: kwargs["go_to_previous_page"] = "go to previous page"
    if not "showNums" in kwargs: kwargs["showNums"] = "true"
    return kwargs
