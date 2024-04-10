from asq.initiators import query
from mongoengine import Q
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.BI.models import BIMenu, BIMenuItem
from amspApp.BI.serializers.BIMenu import BIMenuSerializers, BIMenuItemSerializers, BIMenuItemSumSerializers
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class BIMenuViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = BIMenu.objects.all().order_by('-id')
    serializer_class = BIMenuSerializers

    @list_route(methods=["post"])
    def dup_menu(self, request, *args, **kwargs):
        menu_items = BIMenuItem.objects.filter(menu=request.data['id'])
        menu_items = BIMenuItemSerializers(instance=menu_items, many=True).data
        old_menu_id = request.data['id']
        del request.data['id']
        result = self.create(request, *args, **kwargs)
        new_id = result.data['id']

        parent_menu = query(menu_items).where(lambda x: x['parent'] is None).to_list()
        for parent in parent_menu:
            old_id = parent['id']
            del parent['id']
            parent['menu'] = new_id
            parent['parent'] = None

            parent2 = BIMenuItemSerializers(data=parent)
            parent2.is_valid(raise_exception=True)
            parent2 = parent2.save()
            parent2 = dict(BIMenuItemSerializers(instance=parent2).data)
            parent2['old_id'] = old_id
            parent.update(parent2)

        for parent in parent_menu:
            old_menus = query(menu_items).where(lambda x: str(x['parent']) == parent['old_id']).to_list()
            if len(old_menus) > 0:
                for o in old_menus:
                    del o['id']
                    o['parent'] = parent['id']
                    o['menu'] = new_id

                sr = BIMenuItemSerializers(data=old_menus, many=True)
                sr.is_valid(raise_exception=True)
                sr.save()


        return result


class BIMenuItemsViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = BIMenuItem.objects.all().order_by('-id')
    serializer_class = BIMenuItemSerializers

    @detail_route(methods=["get"])
    def get_just_parent(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(menu=kwargs['id'], parent=None, page=None).order_by('-order, _id')
        return Response(self.serializer_class(instance=self.queryset, many=True).data)

    @detail_route(methods=["get"])
    def get_one_step_menu(self, request, *args, **kwargs):
        parents = self.queryset.filter(menu=kwargs['id'], parent=None).order_by('-order, _id')

        items = []
        for p in parents:
            it = self.serializer_class(instance=p).data
            it['children'] = self.serializer_class(
                instance=self.queryset.filter(menu=kwargs['id'], parent=p.id).order_by('-order, _id'),
                many=True).data
            items.append(it)
        return Response(items)

    @list_route(methods=["get"])
    def get_menu(self, request, *args, **kwargs):
        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        # parents = self.queryset.filter(parent=None).order_by('-order, _id')
        menu_ins = BIMenu.objects.filter(Q(groups_allowed__groupMember__positionID=posiIns.positionID) | Q(
            users_allowed__positionID=posiIns.positionID))
        menu_ins = [x.id for x in menu_ins]

        parents = self.queryset.filter(menu__in=menu_ins, parent=None).order_by('-order, _id')
        items = []
        for p in parents:
            it = BIMenuItemSumSerializers(instance=p).data
            it['children'] = BIMenuItemSumSerializers(
                instance=self.queryset.filter(parent=p.id).order_by('-order, _id'),
                many=True).data
            items.append(it)

        return Response(items)
