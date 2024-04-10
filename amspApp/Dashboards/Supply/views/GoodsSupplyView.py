from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_mongoengine import viewsets

from amspApp.Dashboards.Supply.models import GoodsProviders
from amspApp.Dashboards.Supply.serialization.GoodsSupplaySerializer import GoodsProvidersSerializer
from amspApp._Share.ListPagination import ListPagination


class GoodsProvidersApi(ViewSet):

    def post(self, request, *args, **kwargs):
        userID = request.user.id
        dt = {}
        dt = request.data
        countOf = GoodsProviders.objects.filter(extra__userID=userID).count()
        if countOf == 0:
            dt['extra']['userID'] = userID
            serial = GoodsProvidersSerializer(data=dt)
            serial.is_valid(raise_exception=True)
            serial.save()
            return Response({"msg": "ok"})

        goodProvInstance = GoodsProviders.objects.filter(extra__userID=userID).first()
        dt['extra']['userID'] = userID
        serial = GoodsProvidersSerializer(instance=goodProvInstance, data={"extra": dt["extra"]}, partial=True)
        serial.is_valid(raise_exception=True)
        serial.save()
        return Response({"msg": "ok"})

    """
    editing goods provider via admin 
    """

    def post_sp(self, request, *args, **kwargs):
        userID = request.user.id
        instance = GoodsProviders.objects.filter(id=request.data.get("instanceID")).first()
        userID = instance.extra.get("userID")

        dt = {}
        dt = request.data
        countOf = GoodsProviders.objects.filter(extra__userID=userID).count()
        if countOf == 0:
            dt['extra']['userID'] = userID
            serial = GoodsProvidersSerializer(data=dt)
            serial.is_valid(raise_exception=True)
            serial.save()
            return Response({"msg": "ok"})

        goodProvInstance = GoodsProviders.objects.filter(extra__userID=userID).first()
        dt['extra']['userID'] = userID
        serial = GoodsProvidersSerializer(instance=goodProvInstance, data={"extra": dt["extra"]}, partial=True)
        serial.is_valid(raise_exception=True)
        serial.save()
        return Response({"msg": "ok"})

    def get_ozviat_code(self, request, *args, **kwargs):
        userID = request.user.id
        dt = {}
        dt = request.data
        goodProvInstance = GoodsProviders.objects.filter(extra__userID=userID).first()
        first_part_code = request.user.account_type
        if first_part_code == 4:
            first_part_code = 1
        if first_part_code == 5:
            first_part_code = 2
        if first_part_code == 6:
            first_part_code = 3
        secondPart = GoodsProviders.objects.all().count()
        cccc = None
        if goodProvInstance.extra.get("ozviatcode"):
            cccc = goodProvInstance.extra.get("ozviatcode")
        if not goodProvInstance.extra.get("ozviatcode"):
            cccc = str(first_part_code) + "-" + str(secondPart)
            goodProvInstance.update(extra__ozviatcode=cccc)
        return Response({"code": cccc})

    def get(self, request, *args, **kwargs):
        userID = request.user.id
        dt = {}
        dt = request.data
        countOf = GoodsProviders.objects.filter(extra__userID=userID).count()
        if countOf == 0:
            return Response({})
        instance = GoodsProviders.objects.filter(extra__userID=userID).first()
        serial = GoodsProvidersSerializer(instance=instance).data
        return Response(serial)


class GoodsProvidersViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = GoodsProviders.objects.all()
    serializer_class = GoodsProvidersSerializer
    pagination_class = ListPagination

    def update(self, request, *args, **kwargs):
        return super(GoodsProvidersViewSet, self).update(request, *args, **kwargs)
