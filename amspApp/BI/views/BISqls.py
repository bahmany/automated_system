from datetime import datetime

import sqlparse
from asq.initiators import query
from bson import ObjectId
from django.core.cache import cache
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.BI.models import BISqls, BIStorage
from amspApp.BI.serializers.BISqlsSerial import BISqlsSerializers, BISqlsLess1Serializers
from amspApp.BI.serializers.BIStorageSerial import BIStorageSerial
from amspApp.BI.views.sqls.rahkaraan_factors import rahkaraan_factors
from amspApp.CompaniesManagment.Connections.models import Connections
from amspApp.CompaniesManagment.Connections.viewes.ConnectionsViews import ConnectionsViewSet
from amspApp.Infrustructures.Classes.DateConvertors import get_filter_times, mil_to_sh, getCurrentYearShamsi
from amspApp.Infrustructures.Classes.convert_sqlresult_to_validstr import convert_sqlresultstr_to_valid_str, \
    convert_sqlresultstr_to_valid_numbers
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class BISqlsViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = BISqls.objects.all().order_by('-id')
    serializer_class = BISqlsSerializers
    sharh_compl = {
        '66': 'ورق سیاه',
        '69': 'کلاف سرد',
        '75': 'خدمات قلع ورق سیاه امانی دیگران نزد ما',
        '77': 'کویل قلع اندود',
        '85': 'خدمات قلع اندود و برش و بسته بندی ورق امانی',
        '86': 'خدمات برش و بسته بندی ورق قلع اندود امانی',
        '87': 'خدمات برش و بسته بندي ورق قلع اندود',
        '88': 'ورق قلع اندود',
        '89': 'ورق چاپ و لاک شده',
        '90': 'قوطي کششي ',
        '92': 'قوطي سه تکه ',
        '93': 'درب قوطي آسان بازشو',
        '98': 'ورق قلع اندود برش خورده و چاپ لاک شده',
        '99': 'ضايعات',
    }
    months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']

    backgroundColor = [
        'rgb(255,99,132)',
        'rgb(54,162,235)',
        'rgb(255,206,86)',
        'rgb(75,192,192)',
        'rgb(153,102,255)',
        'rgb(255,159,64)',
        'rgb(255,99,132)',
        'rgb(54,162,235)',
        'rgb(255,206,86)',
        'rgb(75,192,192)',
        'rgb(153,102,255)',
        'rgb(255,159,64)',
    ]
    backgroundColor_colo_1 = [
        'rgb(54,162,235)',
        'rgb(54,162,235)',
        'rgb(54,162,235)',
        'rgb(54,162,235)',
        'rgb(54,162,235)',
        'rgb(54,162,235)',
        'rgb(54,162,235)',
        'rgb(54,162,235)',
        'rgb(54,162,235)',
        'rgb(54,162,235)',
        'rgb(54,162,235)',
        'rgb(54,162,235)',
    ]
    backgroundColor_colo_2 = [
        'rgb(75,192,192)',
        'rgb(75,192,192)',
        'rgb(75,192,192)',
        'rgb(75,192,192)',
        'rgb(75,192,192)',
        'rgb(75,192,192)',
        'rgb(75,192,192)',
        'rgb(75,192,192)',
        'rgb(75,192,192)',
        'rgb(75,192,192)',
        'rgb(75,192,192)',
        'rgb(75,192,192)',
    ]

    heiat_modire_colors = [
        'rgb(164,201,159,0.29)',
        'rgb(164,201,159,0.29)',
        'rgb(164,201,159,0.29)',
        'rgb(164,201,159,0.29)',
        'rgb(164,201,159,0.29)',
        'rgb(164,201,159,0.29)',
        'rgb(164,201,159,0.29)',
        'rgb(164,201,159,0.29)',
        'rgb(164,201,159,0.29)',
        'rgb(164,201,159,0.29)',
        'rgb(164,201,159,0.29)',
        'rgb(164,201,159,0.29)',
    ]

    heiat_modire_for_for_1400 = [
        1500,
        2500,
        3500,
        4000,
        4000,
        4000,
        3500,
        5000,
        6500,
        5000,
        4000,
        1500
    ]

    def initial(self, request, *args, **kwargs):
        # airflow = AirflowConnector()
        # airflow.get_list('connections')

        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            # _mutable = request.data._mutable
            # request.data._mutable = True
            request.data["positionID"] = posiIns.positionID
            # request.data._mutable = _mutable
        return super(BISqlsViewSet, self).initial(request, *args, **kwargs)

    @list_route(methods=['GET'])
    def get_foroosh(self, request, *args, **kwargs):
        all_foroosh = cache.get("all_foroosh")
        if all_foroosh != None:
            return Response(all_foroosh)

        dates = get_filter_times()

        # gets all sharh
        sharhs = BIStorage.objects.aggregate(
            {
                "$match": {
                    "BISqlsLink": ObjectId("61855bd20dd55951cbc3edcc")
                }
            }, {
                "$group": {
                    "_id": {
                        "sharh": "$data.sharh",
                        "year": "$data.year"
                    },
                    "tedade_foroosh": {"$sum": 1},
                    "sum_InvoiceItemQuantity": {"$sum": "$data.InvoiceItemQuantity"},
                    "sum_InvoiceItemTotalPrice": {"$sum": "$data.InvoiceItemTotalPrice"},
                    "lastFactorDate": {"$last": "$data.InvoiceItemDeliveryDate"}

                }
            }, {
                "$sort": {"sum_InvoiceItemQuantity": -1}

            }
        )

        sharhs = list(sharhs)
        result = []
        for sharh in sharhs:
            dtt = {
                'code': sharh["_id"]['sharh'],
                'sum_InvoiceItemQuantity': sharh['sum_InvoiceItemQuantity'],
                'sum_InvoiceItemTotalPrice': sharh['sum_InvoiceItemTotalPrice'],
                'tedade_foroosh': sharh['tedade_foroosh'],
                'lastFactorDate': sharh['lastFactorDate'],
                'title': self.sharh_compl.get(sharh["_id"]['sharh'], "")
            }
            result.append(dtt)

        for key in result:
            key['dates'] = []
            for d in dates['loop']:
                res = BIStorage.objects.aggregate(
                    {
                        "$match": {
                            "BISqlsLink": ObjectId("61855bd20dd55951cbc3edcc"),
                            "data.sharh": key['code'],
                            "data.InvoiceItemDeliveryDate": {
                                "$gte": d[1],
                                "$lte": d[2],
                            }
                        }

                    },
                    {
                        "$group": {
                            "_id": None,
                            "tedade_foroosh": {"$sum": 1},
                            "sum_InvoiceItemQuantity": {
                                "$sum": {"$round": [{"$divide": ["$data.InvoiceItemQuantity", 1000]}, 0]}},
                            "sum_InvoiceItemTotalPrice": {
                                "$sum": {"$round": [{"$divide": ["$data.InvoiceItemTotalPrice", 1000000]}, 0]}}
                        }
                    }

                )
                rrr = list(res)
                res = rrr[0] if len(rrr) > 0 else {}
                res['timeof'] = d[0]
                key['dates'].append(res)
                # result[key]["title"] = res
        result = query(result).order_by_descending(lambda x: x['sum_InvoiceItemQuantity']).to_list()
        cache.set("all_foroosh", result, 240)
        return Response(result)

    @list_route(methods=['GET'])
    def get_faactor_1_for_foroosh(self, request, *args, **kwargs):
        all_foroosh = cache.get("get_faactor_1_for_foroosh")
        if all_foroosh != None:
            return Response(all_foroosh)

        sql_ins = BISqls.objects.get(id='61855bd20dd55951cbc3edcc')
        dates = get_filter_times()
        kgs = ['66', '69', '75', '77', '85', '86', '87', '88']
        current_year = int(getCurrentYearShamsi())
        last_year = int(getCurrentYearShamsi()) - 1
        current_year_ds = BIStorage.objects.aggregate(
            {
                "$match": {
                    "BISqlsLink": sql_ins.id,
                    "data.sharh": {"$in": kgs},
                    "data.tarikh_sodoore_factor_shamsi_year": current_year
                }
            },
            {
                "$group": {
                    "_id": {
                        "month": "$data.tarikh_sodoore_factor_shamsi_month"
                    },
                    "sum_of_tedad": {"$sum": "$data.InvoiceItemQuantity"},
                    "sum_of_price": {"$sum": "$data.InvoiceItemTotalPrice"},

                    # "sum_of_tedad": {"$round": [{"$divide": ["$data.InvoiceItemQuantity", 1000000]}, 0]},
                    # "sum_of_price": {"$round": [{"$divide": ["$data.InvoiceItemTotalPrice", 1000000]}, 0]},
                }
            },
            {
                "$project": {
                    "month": "$_id.month",
                    "sum_of_tedad": {"$round": [{"$divide": ["$sum_of_tedad", 1000]}, 0]},
                    "sum_of_price": {"$round": [{"$divide": ["$sum_of_price", 1000000]}, 0]},
                    "_id": 0
                }
            },
            {"$sort":
                 {"month": 1}
             }
        )
        current_year_ds = list(current_year_ds)

        prev_year_ds = BIStorage.objects.aggregate(
            {
                "$match": {
                    "BISqlsLink": sql_ins.id,
                    "data.sharh": {"$in": kgs},
                    "data.tarikh_sodoore_factor_shamsi_year": last_year
                }
            },
            {
                "$group": {
                    "_id": {
                        "month": "$data.tarikh_sodoore_factor_shamsi_month"
                    },
                    "sum_of_tedad": {"$sum": "$data.InvoiceItemQuantity"},
                    "sum_of_price": {"$sum": "$data.InvoiceItemTotalPrice"},

                    # "sum_of_tedad": {"$round": [{"$divide": ["$data.InvoiceItemQuantity", 1000000]}, 0]},
                    # "sum_of_price": {"$round": [{"$divide": ["$data.InvoiceItemTotalPrice", 1000000]}, 0]},
                }
            },
            {
                "$project": {
                    "month": "$_id.month",
                    "sum_of_tedad": {"$round": [{"$divide": ["$sum_of_tedad", 1000]}, 0]},
                    "sum_of_price": {"$round": [{"$divide": ["$sum_of_price", 1000000]}, 0]},
                    "_id": 0
                }
            },
            {"$sort":
                 {"month": 1}
             }
        )
        prev_year_ds = list(prev_year_ds)

        months = [self.months[x['month'] - 1] for x in prev_year_ds]

        result = {
            "labels": months,
            "datasets": [

                {
                    "label": "فاکتورهای صادره سال {}".format(last_year),
                    "data": [x['sum_of_tedad'] for x in prev_year_ds],
                    "backgroundColor": self.backgroundColor_colo_1,
                    "type": "line"
                },

                {
                    "label": "فاکتورهای صادره سال {}".format(current_year),
                    "data": [x['sum_of_tedad'] for x in current_year_ds],
                    "backgroundColor": self.backgroundColor,
                    "hoverBackgroundColor": ['#131e3a'],
                    "type": "bar",
                }, {
                    "label": "هیات مدیره سال {}".format(1400),
                    "data": self.heiat_modire_for_for_1400,
                    "backgroundColor": self.heiat_modire_colors,
                    "type": "line",
                    "fill": True
                }

            ],

        }
        cache.set("get_faactor_1_for_foroosh", result, 60)
        return Response(result)

    @list_route(methods=['GET'])
    def get_faactor_1_2_for_foroosh(self, request, *args, **kwargs):

        all_foroosh = cache.get("get_faactor_1_2_for_foroosh")
        if all_foroosh != None:
            return Response(all_foroosh)

        month = request.query_params.get('month', None)
        if month is None:
            return Response({})
        month = int(month)
        sql_ins = BISqls.objects.get(id='61855bd20dd55951cbc3edcc')
        dates = get_filter_times()
        kgs = ['66', '69', '75', '77', '85', '86', '87', '88']
        current_year = int(getCurrentYearShamsi())
        last_year = int(getCurrentYearShamsi()) - 1
        current_year_ds = BIStorage.objects.aggregate(
            {
                "$match": {
                    "BISqlsLink": sql_ins.id,
                    "data.sharh": {"$in": kgs},
                    "data.tarikh_sodoore_factor_shamsi_year": current_year,
                    "data.tarikh_sodoore_factor_shamsi_month": month + 1,
                }
            },
            {
                "$group": {
                    "_id": {
                        "day": "$data.tarikh_sodoore_factor_shamsi_day"
                    },
                    "sum_of_tedad": {"$sum": "$data.InvoiceItemQuantity"},
                    "sum_of_price": {"$sum": "$data.InvoiceItemTotalPrice"},

                }
            },
            {
                "$project": {
                    "day": "$_id.day",
                    "sum_of_tedad": {"$round": [{"$divide": ["$sum_of_tedad", 1000]}, 0]},
                    "sum_of_price": {"$round": [{"$divide": ["$sum_of_price", 1000000]}, 0]},
                    "_id": 0
                }
            },
            {"$sort":
                 {"day": 1}
             }
        )
        current_year_ds = list(current_year_ds)

        result = {
            "labels": query([x['day'] for x in current_year_ds]).distinct().to_list(),
            "datasets": [
                {
                    "label": "فاکتورهای صادره سال {}".format(current_year),
                    "data": [x['sum_of_tedad'] for x in current_year_ds],
                    "backgroundColor": self.backgroundColor,
                    "hoverBackgroundColor": ['#131e3a'],
                    "type": "bar",
                }

            ],

        }

        cache.set("get_faactor_1_2_for_foroosh", result, 60)
        return Response(result)

    @list_route(methods=['GET'])
    def convert_old_delphi(self, request, *args, **kwargs):
        # a = 0
        return {}
        from amspApp.BI.views.hamraan_system_jsons import foroosh
        pp = foroosh.foroosh_delphi
        sql_ins = BISqls.objects.get(id='61855bd20dd55951cbc3edcc')
        for p in pp['Sheet1']:
            dt = {}
            dt['data'] = p

            dt['BISqlsLink'] = sql_ins
            dt['data']['InvoiceItemID'] = int(dt['data']['InvoiceItemID'])
            dt['data']['InvoiceItemInvoiceRef'] = int(dt['data']['InvoiceItemInvoiceRef'])

            dt['data']['InvoiceItemDeliveryDate'] = datetime.strptime(dt['data']['InvoiceItemDeliveryDate'], '%Y-%m-%d')
            dt['data']['InvoiceItemTotalPrice'] = int(dt['data']['InvoiceItemTotalPrice'])
            dt['data']['InvoiceItemQuantity'] = int(dt['data']['InvoiceItemQuantity'])
            dt['data']['InvoiceItemFee'] = int(dt['data']['InvoiceItemFee'])

            dt['data']['tarikh_sodoore_factor_shamsi'] = mil_to_sh(dt['data']['InvoiceItemDeliveryDate'])
            dt['data']['tarikh_sodoore_factor_shamsi_year'] = \
                int(mil_to_sh(dt['data']['InvoiceItemDeliveryDate']).split("/")[0])
            dt['data']['tarikh_sodoore_factor_shamsi_month'] = \
                int(mil_to_sh(dt['data']['InvoiceItemDeliveryDate']).split("/")[1])
            dt['data']['tarikh_sodoore_factor_shamsi_day'] = \
                int(mil_to_sh(dt['data']['InvoiceItemDeliveryDate']).split("/")[2])
            dt['data']['tarikh_sodoore_factor_shamsi_year_month'] = "{}-{}".format(
                dt['data']['tarikh_sodoore_factor_shamsi_year'], dt['data']['tarikh_sodoore_factor_shamsi_month'])
            dt['data']['tarikh_sodoore_factor_shamsi_month_day'] = "{}-{}".format(
                dt['data']['tarikh_sodoore_factor_shamsi_month'], dt['data']['tarikh_sodoore_factor_shamsi_day'])

            ser = BIStorageSerial(data=dt)
            ser.is_valid(raise_exception=True)
            ser.save()
            print(str(dt['data']['InvoiceItemID']) + " added")

    @list_route(methods=['GET'])
    def convert_old(self, request, *args, **kwargs):
        # a = 0
        return {}
        # from amspApp.BI.views.hamraan_system_jsons import foroosh
        connection = Connections.objects.get(databaseName="RahkaranDB")
        connection = ConnectionsViewSet().getConnection(connection)
        connection.execute(rahkaraan_factors)
        sql_res = connection.fetchall()

        sql_ins = BISqls.objects.get(id='61855bd20dd55951cbc3edcc')
        for p in sql_res:
            dt = {}
            dt['data'] = p

            dt['BISqlsLink'] = sql_ins
            dt['data']['InvoiceItemID'] = int(dt['data']['InvoiceItemID'])
            dt['data']['InvoiceItemInvoiceRef'] = int(dt['data']['InvoiceItemInvoiceRef'])

            dt['data']['InvoiceItemTotalPrice'] = int(dt['data']['InvoiceItemTotalPrice'])
            dt['data']['InvoiceItemQuantity'] = int(dt['data']['InvoiceItemQuantity'])
            dt['data']['InvoiceItemFee'] = int(dt['data']['InvoiceItemFee'])

            dt['data']['tarikh_sodoore_factor_shamsi'] = mil_to_sh(dt['data']['InvoiceItemDeliveryDate'])
            dt['data']['tarikh_sodoore_factor_shamsi_year'] = \
                int(mil_to_sh(dt['data']['InvoiceItemDeliveryDate']).split("/")[0])
            dt['data']['tarikh_sodoore_factor_shamsi_month'] = \
                int(mil_to_sh(dt['data']['InvoiceItemDeliveryDate']).split("/")[1])
            dt['data']['tarikh_sodoore_factor_shamsi_day'] = \
                int(mil_to_sh(dt['data']['InvoiceItemDeliveryDate']).split("/")[2])
            dt['data']['tarikh_sodoore_factor_shamsi_year_month'] = "{}-{}".format(
                dt['data']['tarikh_sodoore_factor_shamsi_year'], dt['data']['tarikh_sodoore_factor_shamsi_month'])
            dt['data']['tarikh_sodoore_factor_shamsi_month_day'] = "{}-{}".format(
                dt['data']['tarikh_sodoore_factor_shamsi_month'], dt['data']['tarikh_sodoore_factor_shamsi_day'])

            ser = BIStorageSerial(data=dt)
            ser.is_valid(raise_exception=True)
            ser.save()
            print(str(dt['data']['InvoiceItemID']) + " added")

    @list_route(methods=['GET'])
    def bi_get_sqls_brief(self, request, *args, **kwargs):
        sqls = self.queryset.all()
        sqls = BISqlsLess1Serializers(instance=sqls, many=True).data
        return Response(sqls)
