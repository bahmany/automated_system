import operator

from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets
from amspApp.SpecialApps.****Cashflow.models import CashFlow****TaminAllDateTmp
from amspApp.SpecialApps.****Cashflow.serializers.****CashFlowSerializers import \
    CashFlow****TaminAllDateTmpSerializer
from amspApp._Share.ListPagination import DetailsPagination


class ****CashflowAllDatesViewset(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = CashFlow****TaminAllDateTmp.objects.all()
    serializer_class = CashFlow****TaminAllDateTmpSerializer
    pagination_class = DetailsPagination

    @list_route(methods=["POST", ])
    def getMonthly(self, request, *args, **kwargs):
        result = list(self.queryset.aggregate(request.data))
        return Response(result)

    @list_route(methods=["GET", ])
    def getSimpleList(self, request, *args, **kwargs):
        dt = {}
        dt["year"] = 1396
        dt["start"] = str(dt["year"]) + "/01/01"
        dt["end"] = str(dt["year"]) + "/12/30"



        objs = []
        for line in self.queryset:

            for li in line.payDetails:
                dt = {}

                dt["2_payTypeStr"] = li["payTypeStr"] if "payTypeStr" in li else li["typeStr"]
                dt["4_payType"] = li["payType"] if "payType" in li else li["type"]
                dt["3_date"] = line.current.strftime("%y-%m-%d")
                dt["1_date_sh"] = line.current_sh
                if type(li["pay"]) == int:
                    dt["7_pay"] = int(float(li["pay"]))
                else :
                    dt["7_pay"] = int(float(li["pay"]["pay"]))
                if dt["7_pay"] > 0 :
                    dt["7_pay"] = int(dt["7_pay"] / 1000000)
                dt["8_income"] = 0

                if dt["1_date_sh"] == "1396/01/19":
                    pass
                dt["5_projectID"] = li["project"]["id"] if "project" in li else 0
                dt["6_companyName"] = li["project"]["companyLink"]["name"] if "project" in li else "Not"
                # dt["tp"] = "pay"
                objs.append(dt)

            for li in line.incomeDetails:
                dt = {}
                dt["2_payTypeStr"] = li["typeStr"]
                dt["4_payType"] = li["type"]
                dt["3_date"] = line.current.strftime("%y-%m-%d")
                dt["1_date_sh"] = line.current_sh
                dt["7_pay"] = 0
                if "project" in li :
                    dt["8_income"] = int(float(li["income"]))

                else:
                    dt["8_income"] = int(float(li["income"]["money"]))
                if dt["8_income"] > 0 :
                    dt["8_income"] = int(dt["8_income"] / 1000000)
                if "project" in li:
                    pass
                dt["5_projectID"] = li["project"]["id"] if "project" in li else 0
                dt["6_companyName"] = li["project"]["companyLink"]["name"] if "project" in li else "Not"
                objs.append(dt)

            for o in objs:
                o = sorted(o.items(), key=operator.itemgetter(0))


        return Response(objs)
