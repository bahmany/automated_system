from random import randint

from mongoengine import Q
from amspApp.Infrustructures.odoo_connector.connectors import OdooConnector
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amsp import settings
from amspApp.Dashboards.Supply.models import GoodsProviders
from amspApp.Dashboards.Supply.serialization.GoodsSupplaySerializer import GoodsProvidersSerializer, \
    SupplementCategoriesSerializer
from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh_with_time
from amspApp._Share.ListPagination import ListPagination, DataTablesPagination
from amspApp.amspUser.models import MyUser


class AdminTaminDakheliViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = GoodsProviders.objects.all().order_by("-id")
    serializer_class = GoodsProvidersSerializer
    pagination_class = ListPagination

    def retrieve(self, request, *args, **kwargs):
        result = super(AdminTaminDakheliViewSet, self).retrieve(request, *args, **kwargs)
        userInstance = MyUser.objects.get(id=result.data["extra"]["userID"])
        result.data["reg_type"] = userInstance.account_type

        if result.data["reg_type"] == 4:
            result.data['reg_type_str'] = "فروشنده"
        if result.data["reg_type"] == 5:
            result.data['reg_type_str'] = "خدمات دهنده"
        if result.data["reg_type"] == 6:
            result.data['reg_type_str'] = "سازنده"

        if result.data["reg_type"] == 4:
            result.data["reg_type"] = 0
        if result.data["reg_type"] == 5:
            result.data["reg_type"] = 1
        if result.data["reg_type"] == 6:
            result.data["reg_type"] = 2

        if result.data.get("extra"):
            if result.data.get("extra").get("frm1"):
                if result.data.get("extra").get("frm1").get("name"):
                    result.data["name"] = result.data.get("extra").get("frm1").get("name")
            if result.data.get("extra").get("frm2"):
                if result.data.get("extra").get("frm2").get("name"):
                    result.data["name"] = result.data.get("extra").get("frm2").get("name")
            if result.data.get("extra").get("frm3"):
                if result.data.get("extra").get("frm3").get("name"):
                    result.data["name"] = result.data.get("extra").get("frm3").get("name")
        return result

    @list_route(methods=["GET"])
    def getForDataTables(self, request, *args, **kwargs):
        if request.user.groups.filter(name='foroosh').count() == 0:
            return Response({})
        self.pagination_class = DataTablesPagination
        # get users
        searchStr = request.query_params.get("sSearch")
        if searchStr:
            if searchStr != "":
                users = [x["id"] for x in list(MyUser.objects.filter(username__contains=searchStr).values("id"))]
                q_users = [Q(extra__userID=x) for x in users]
                query = Q()
                if len(q_users) != 0:
                    query = q_users.pop()
                for item in q_users:
                    query |= item
                query |= Q(extra__frm1__name__contains=searchStr)
                query |= Q(extra__frm2__name__contains=searchStr)
                query |= Q(extra__frm3__name__contains=searchStr)
                query |= Q(extra__gen_code__contains=searchStr)
                query |= Q(extra__type_of_provider__contains=searchStr)
                self.queryset = self.queryset.filter(query)

        result = self.list(request, args, kwargs)
        for r in result.data["aaData"]:
            if r["extra"].get("gen_code") is None:
                r["extra"]["gen_code"] = "NULL"
            if r.get("extra").get("step2") is None:
                r["extra"]["step2"] = {}
            if r["extra"]["step2"].get("name") is None:
                r["extra"]["step2"]["name"] = "NULL"
            if r["extra"].get("type_of_provider") is None:
                r["extra"]["type_of_provider"] = "NULL"
                """
                    1 = automation
                    2 = First Try
                    4 = supplier seller
                    5 = supplier service
                    6 = supplier factory
                    7 = hire
                
                """
            if r['extra'].get("userID"):
                userInstance = MyUser.objects.get(id=r['extra']['userID'])
                r['extra']['type_of_provider'] = ""
                if userInstance.account_type == 4:
                    r['extra']['type_of_provider'] = "فروشنده"
                if userInstance.account_type == 5:
                    r['extra']['type_of_provider'] = "خدمات دهنده"
                if userInstance.account_type == 6:
                    r['extra']['type_of_provider'] = "سازنده"

            r["extra"]["name"] = ""
            if r.get("extra"):
                if r.get("extra").get("frm1"):
                    if r.get("extra").get("frm1").get("name"):
                        r["extra"]["name"] = r.get("extra").get("frm1").get("name")
                if r.get("extra").get("frm2"):
                    if r.get("extra").get("frm2").get("name"):
                        r["extra"]["name"] = r.get("extra").get("frm2").get("name")
                if r.get("extra").get("frm3"):
                    if r.get("extra").get("frm3").get("name"):
                        r["extra"]["name"] = r.get("extra").get("frm3").get("name")

            r["dateOfPost"] = mil_to_sh_with_time(r["dateOfPost"])

            ff = MyUser.objects.filter(id=r.get("extra").get("userID")).first()
            r["extra"]["username"] = ""
            if ff:
                r["extra"]["username"] = ff.username
        return result

    def checkPerm(self, req):
        if req.user.groups.filter(name__contains="foroosh").count() == 0:
            raise Exception("مجوز دسترسی ندارید")


    def list(self, request, *args, **kwargs):
        self.checkPerm(request)
        return super(AdminTaminDakheliViewSet, self).list(request, *args, **kwargs)

    @list_route(methods=["POST"])
    def genOdooContact(self, request, *args, **kwargs):
        self.checkPerm(request)

        odoo = OdooConnector(endpoint=settings.ODOO_HTTP_REFERER,
                             dbname='odooDB',
                             username='bahmanymb@gmail.com',
                             password='****')
        uid = odoo.connect()
        result = odoo.search(uid=uid,
                             model='res.partner',
                             action='search',
                             queries=[[['name', '=', "tttttttt"]]],
                             parameters={'limit': 5}
                             )

        # odoo = OdooConnector(endpoint=ODOO_Platform,
        #                      dbname='odoodb',
        #                      username='bahmanymb@gmail.com',
        #                      password='****')
        # data = [{
        #     "name":"tttttttt",
        #     "street":"fdgdfsg dsfg",
        # }]
        #
        # result = odoo.write(uid=uid, model='res.partner', action='create', data=

        pass

    @list_route(methods=["GET"])
    def createSuppCats(self, request, *args, **kwargs):
        self.checkPerm(request)

        return Response({})
        p1 = {'code': -1, "name": "تجهیزات و قطعات مکانیکی "}
        p2 = {'code': -1, "name": "تجهیزات و قطعات برقی "}
        p3 = {'code': -1, "name": "قطعات عمومی صنعتی و ابزار آلات "}
        p4 = {'code': -1, "name": "لوازم و قطعات تاسیسات "}
        p5 = {'code': -1, "name": "مصالح، مواد شیمیایی و اقلام مصرفی "}
        p6 = {'code': -1, "name": "ملزومات اداری و اقلام عمومی "}
        p7 = {'code': -1, "name": "اقلام ایمنی و بهداشت "}
        p8 = {'code': -1, "name": "خدمات "}

        ins1 = SupplementCategoriesSerializer(data=p1)
        ins2 = SupplementCategoriesSerializer(data=p2)
        ins3 = SupplementCategoriesSerializer(data=p3)
        ins4 = SupplementCategoriesSerializer(data=p4)
        ins5 = SupplementCategoriesSerializer(data=p5)
        ins6 = SupplementCategoriesSerializer(data=p6)
        ins7 = SupplementCategoriesSerializer(data=p7)
        ins8 = SupplementCategoriesSerializer(data=p8)

        ins1.is_valid(raise_exception=True)
        ins2.is_valid(raise_exception=True)
        ins3.is_valid(raise_exception=True)
        ins4.is_valid(raise_exception=True)
        ins5.is_valid(raise_exception=True)
        ins6.is_valid(raise_exception=True)
        ins7.is_valid(raise_exception=True)
        ins8.is_valid(raise_exception=True)

        ins1 = ins1.save()
        ins2 = ins2.save()
        ins3 = ins3.save()
        ins4 = ins4.save()
        ins5 = ins5.save()
        ins6 = ins6.save()
        ins7 = ins7.save()
        ins8 = ins8.save()



        for c in csss:
            psa = SupplementCategoriesSerializer(data=c)
            psa.is_valid(raise_exception=True)
            psa.save()

        return Response({})

    @list_route(methods=["GET"])
    def getRegisteredCount(self, request, *args, **kwargs):
        count = self.queryset.count()
        return Response({"count": count})

    @detail_route(methods=["POST"])
    def setType(self, request, *args, **kwargs):
        id = kwargs.get("id")
        instance = self.queryset.get(id=id)
        userinstance = MyUser.objects.get(id=instance.extra.get("userID"))
        tp = int(request.data.get("newType"))
        if tp in [4, 5, 6]:
            userinstance.account_type = tp
            userinstance.save()
        return Response({"result": "ok"})

    @detail_route(methods=["POST"])
    def removeIt(self, request, *args, **kwargs):
        id = kwargs.get("id")
        instance = self.queryset.get(id=id)
        rand_id = randint(1520025, 8999999)
        rm = "remove_" + str(rand_id) + "__"
        userinstance = MyUser.objects.filter(id=instance.extra.get("userID")).first()
        tp = request.data.get("newType")
        if tp == "OK":
            if userinstance:
                userinstance.username = rm + userinstance.username
                userinstance.email = rm + userinstance.email
                userinstance.cellphone = rm + userinstance.cellphone
                userinstance.save()
            instance.delete()
            return Response({"result": "ok"})
        return Response({"result": "no change"})

    @detail_route(methods=["POST"])
    def changePass(self, request, *args, **kwargs):
        id = kwargs.get("id")
        newPass = request.data.get("newPass")
        instance = self.queryset.get(id=id)
        userinstance = MyUser.objects.get(id=instance.extra.get("userID"))
        if newPass != "":
            userinstance.set_password(newPass)
            userinstance.save()
            return Response({"result": "ok"})
        return Response({"result": "no change"})
