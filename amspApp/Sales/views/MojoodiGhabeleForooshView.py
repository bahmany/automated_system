from datetime import datetime

from asq.initiators import query
from django.core.cache import cache
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Connections.models import Connections
from amspApp.CompaniesManagment.Connections.viewes.ConnectionsViews import ConnectionsViewSet
from amspApp.Infrustructures.Classes.DateConvertors import getCurrentYearShamsi
from amspApp.Infrustructures.Classes.convert_sqlresult_to_validstr import convert_sqlresultstr_to_valid_str, \
    convert_sqlresultstr_to_valid_numbers
from amspApp.Sales.models import MojoodiGhabeleForoosh, MojoodiGhabeleForooshKeifi
from amspApp.Sales.serializers.MojoodiGhabeleForooshSerializer import MojoodiGhabeleForooshSerializer, \
    MojoodiGhabeleForooshKeifiSerializer
from amspApp._Share.ListPagination import DetailsPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class MojoodiGhabeleForooshViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = MojoodiGhabeleForoosh.objects.all()
    serializer_class = MojoodiGhabeleForooshSerializer
    pagination_class = DetailsPagination

    def update_with_rahkaraan(self):
        prev = MojoodiGhabeleForoosh.objects.aggregate({
            "$project": {
                "PartCode": 1,
                "Year": 1
            }
        })
        prev = [{'PartCode': x['PartCode'], 'Year': x['Year']} for x in prev]
        if len(prev) > 0:
            prev = "where PartCode+'_'+CAST(PerDate_year as char(4)) not in (%s)" % (
                ','.join(["'" + x['PartCode'] + "_" + str(x['Year']) + "'" for x in prev]),
            )
        else:
            prev = ""
        sql = """
        select top 10000 * from mrbCardexMojoodi_Group %s
        """ % (prev,)
        connection = Connections.objects.get(databaseName="RahkaranDB")
        connection = ConnectionsViewSet().getConnection(connection)
        connection.execute(sql)
        sql_res = connection.fetchall()
        sql_res = convert_sqlresultstr_to_valid_str(sql_res)
        sql_res = convert_sqlresultstr_to_valid_numbers(sql_res)
        bulk_insert = [{'PartCode': x['PartCode'], 'Year': x['PerDate_year'], 'details': {}} for x in sql_res]
        bulk_insert = self.serializer_class(data=bulk_insert, many=True)
        bulk_insert.is_valid(raise_exception=True)
        bulk_insert.save()

    @list_route(methods=["GET"])
    def update_from_rahkaraan(self, request, *args, **kwargs):
        self.update_with_rahkaraan()
        return Response({})

    def get_pish_from_rahkaraan(self):
        sql_res = cache.get('get_pish_from_rahkaraan')
        if sql_res == None:
            sql = """
            select * from mrbPishWithTrace
            """
            connection = Connections.objects.get(databaseName="RahkaranDB")
            connection = ConnectionsViewSet().getConnection(connection)
            connection.execute(sql)
            sql_res = connection.fetchall()
            sql_res = convert_sqlresultstr_to_valid_str(sql_res)
            sql_res = convert_sqlresultstr_to_valid_numbers(sql_res)
            cache.set('get_pish_from_rahkaraan', sql_res, 120)
        return sql_res


    @list_route(methods=['GET'])
    def get_pishfactors_mandeh(self, request, *args, **kwargs):
        result = self.get_pish_from_rahkaraan()
        return Response(result)

    @detail_route(methods=['POST'])
    def add_keifi(self, request, *args, **kwargs):
        sr = request.data
        sr['HavalehForooshApproveLink'] = kwargs['id']
        positionid = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        sr['positionID'] = positionid.positionID
        sr['dateOfPost'] = datetime.now()
        sr['details'] = {}
        sr = MojoodiGhabeleForooshKeifiSerializer(data=sr)
        sr.is_valid(raise_exception=True)
        sr.save()
        return Response(sr.data)

    @detail_route(methods=['POST'])
    def change_aneal(self, request, *args, **kwargs):
        instance = MojoodiGhabeleForoosh.objects.get(id=kwargs['id'])
        details = MojoodiGhabeleForooshSerializer(instance=instance).data
        details = instance.details
        instance.update(details={})
        anealing = request.data.get('details', {}).get('details', {}).get('aneal', None)
        details['aneal'] = anealing
        sr = MojoodiGhabeleForooshSerializer(instance=instance, data={'details': details}, partial=True)
        sr.is_valid(raise_exception=True)
        sr.save()
        return Response(sr.data)

    @detail_route(methods=['POST'])
    def toggle_setareh(self, request, *args, **kwargs):
        instance = MojoodiGhabeleForoosh.objects.get(id=kwargs['id'])
        details = MojoodiGhabeleForooshSerializer(instance=instance).data
        details = instance['details']
        instance.update(details={})
        star = False
        if not details.get("star", False):
            star = True
        details['star'] = star
        sr = MojoodiGhabeleForooshSerializer(instance=instance, data={'details': details}, partial=True)
        sr.is_valid(raise_exception=True)
        sr.save()
        return Response(sr.data)

    @detail_route(methods=['POST'])
    def remove_keifi(self, request, *args, **kwargs):
        MojoodiGhabeleForooshKeifi.objects.get(id=kwargs['id']).delete()
        return Response({'result': 'deleted'})

    def get_rahkaraan_cardex(self, year, show_zero, show_minus, only_zero, only_minus):
        sql = """
        select top 10000 * from mrbCardexMojoodi_Group where PerDate_year in (%s)
        """ % (str(year))

        if not show_zero and not show_minus:
            sql = sql + " and Meghdar > 0"

        if show_zero and show_minus:
            sql = sql + " "

        if show_minus:
            sql = sql + " "
        if only_zero:
            sql = sql + ' and  Meghdar = 0'
        if only_minus:
            sql = sql + ' and  Meghdar < 0'

        connection = Connections.objects.get(databaseName="RahkaranDB")
        connection = ConnectionsViewSet().getConnection(connection)
        connection.execute(sql)
        sql_res = connection.fetchall()
        sql_res = convert_sqlresultstr_to_valid_str(sql_res)
        sql_res = convert_sqlresultstr_to_valid_numbers(sql_res)
        return sql_res

    def cast_bp_to_company_name(self, bp):
        result = "نامعلوم"
        if bp == "0":
            return "JOLEE"
        if bp == "1":
            return "POSCO"
        if bp == "2":
            return "TIANJIN"
        if bp == "3":
            return "SWKD"
        if bp == "4":
            return "MMK"
        if bp == "5":
            return "SHOUGANG"
        if bp == "6":
            return "COMAT"
        if bp == "7":
            return "F.M=7 ********ه"
        if bp == "8":
            return "7D هفت ****"
        if bp == "9":
            return "F.GH **** غرب"
        if bp == "A":
            return "DONG CHONG"
        if bp == "B":
            return "BLXG"
        if bp == "C":
            return "CHAN YUEN TAI"
        if bp == "D":
            return "BAOWU"
        if bp == "E":
            return "ARCELO MITTAL"
        if bp == "F":
            return "SINO"
        if bp == "G":
            return "YIEBO"
        if bp == "H":
            return "HBIS"
        if bp == "S":
            return "SUXUN"
        if bp == "I":
            return "CUNRUI"
        return result

    @list_route(methods=["POST"])
    def get_anbar_cardex(self, request, *args, **kwargs):
        filters = request.data
        current_year = int(filters.get('current_year', getCurrentYearShamsi()))
        show_zero = filters.get('show_zero', False)
        show_minus = filters.get('show_minus', False)
        only_zero = filters.get('only_zero', False)
        only_minus = filters.get('only_minus', False)
        cache_name = "%s_%s_%s_%s_%s_rahkaran_cardex" % (current_year, show_zero, show_minus, only_zero, only_minus)
        data = cache.get(cache_name)
        if data == None:
            data = self.get_rahkaraan_cardex(current_year, show_zero, show_minus, only_zero, only_minus)
            cache.set(cache_name, data, 2220)
        if len(data) == 0:
            data = self.get_rahkaraan_cardex(current_year, show_zero, show_minus, only_zero, only_minus)
            cache.set(cache_name, data, 2220)

        details = self.queryset.filter(
            PartCode__in=[d['PartCode'] for d in data],
            Year=current_year
        )
        ds = self.serializer_class(instance=details, many=True).data
        for d in data:
            d['details'] = query(ds).where(lambda x: x['Year'] == current_year).where(
                lambda x: x['PartCode'] == d['PartCode']).first_or_default({})

        result = query(data).group_by(
            lambda x: x['QuotationItemProductNumber_sharh'],
            result_selector=lambda key, group: {
                'QuotationItemProductNumber_sharh': key,
                'details': group.group_by(
                    lambda x: x['QuotationItemProductNumber_BP'],
                    result_selector=lambda _key, _group: {
                        'QuotationItemProductNumber_BP': _key,
                        'SazandehTitle': self.cast_bp_to_company_name(_key),
                        'details': _group.to_list()
                    }
                ).to_list()

            }
        ).to_list()

        return Response(result)
