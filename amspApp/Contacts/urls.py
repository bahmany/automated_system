from django.conf.urls import patterns, include, url

from rest_framework.routers import SimpleRouter
from amspApp.Contacts.views.ContactsView import ContactsViewSet, ContactsGroupsViewSet, ContactsItemsGroupsViewSet

contacs_router = SimpleRouter()
contacs_router.register("contacts", ContactsViewSet, base_name="contacts-list")

contacs_group_router = SimpleRouter()
contacs_group_router.register("groups-contacts", ContactsGroupsViewSet, base_name="contacts-list")

contacs_group_items_router = SimpleRouter()
contacs_group_items_router.register("items-groups-contacts", ContactsItemsGroupsViewSet, base_name="contacts-list")

urlpatterns = patterns('',
                       url(r'^page/contacts', ContactsViewSet.as_view({"get": "template_view"})),
                       url(r'^page/edit-contact', ContactsViewSet.as_view({"get": "template_view_edit"})),
                       url(r'^api/v1/', include(contacs_router.urls)),
                       url(r'^api/v1/', include(contacs_group_router.urls)),
                       url(r'^api/v1/', include(contacs_group_items_router.urls)),
)
