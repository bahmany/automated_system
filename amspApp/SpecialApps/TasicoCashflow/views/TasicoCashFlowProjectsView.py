from datetime import timedelta, datetime

import decimal
from asq.initiators import query
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from amspApp.Infrustructures.Classes.DateConvertors import sh_to_mil, mil_to_sh
from amspApp.SpecialApps.****Cashflow.models import CashFlow****TaminProject, CashFlow****TaminIncommings, \
    CashFlow****TaminPayments, CashFlow****TaminAllDateTmp
from amspApp.SpecialApps.****Cashflow.serializers.****CashFlowSerializers import \
    CashFlow****TaminProjectSerializer, CashFlow****TaminCashFlow****TaminIncommingsSerializer, \
    CashFlow****TaminPaymentsSerializer, CashFlow****TaminAllDateTmpSerializer


class ****CashFlowProjectsViewset(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = CashFlow****TaminProject.objects.all()
    serializer_class = CashFlow****TaminProjectSerializer

    def get_queryset(self):
        return super(****CashFlowProjectsViewset, self).get_queryset()

    shMonth = [
        "فروردین"
        "اردیبهشت",
        "خرداد",
        "تیر",
        "مرداد",
        "شهریور",
        "مهر",
        "آبان",
        "آذر",
        "دی",
        "بهمن",
        "اسفند",
    ]



    def GenerateAllDayReport(self):
        dt = {}
        dt["year"] = 1396
        dt["start"] = str(dt["year"]) + "/01/01"
        dt["end"] = str(dt["year"]) + "/12/30"
        # -----------------------------------------
        # projects = self.serializer_class(instance=self.get_queryset(), many=True).data
        projects = list(self.get_queryset())
        dates = None
        # dates = cache.get("****list")
        if not dates:
            data = []
            for pr in projects:

                projectTitle = " پروژه تامین "+str(int(pr.tonValue))+" از "+pr.companyLink.name+" "

                pr = pr
                # Goshayeshe Etebar
                ds = {}
                ds["date_mil"] = pr.****Date - timedelta(
                    days=pr.detailLink.daysFromFactoryToShip +
                         pr.detailLink.daysFromIranPortToFactory +
                         pr.detailLink.daysFromShipToIranPort)
                ds["payType"] = 11
                ds["payTypeStr"] = "بابت گشایش اعتبار" + projectTitle
                ds["pay"] = (pr.tonValue * pr.detailLink.moneyRialPerTon) * (pr.detailLink.moneyPercentWhenOpenLC / 100)
                ds["pay"] = int(ds["pay"])
                ds["project"] = self.serializer_class(instance=pr).data
                data.append(ds)
                # Start Haml Ba Kashti
                ds = {}
                ds["date_mil"] = pr.****Date - timedelta(
                    days=pr.detailLink.daysFromIranPortToFactory +
                         pr.detailLink.daysFromShipToIranPort)
                ds["payType"] = 12
                ds["payTypeStr"] = "بابت برگه حمل" + projectTitle
                ds["pay"] = (pr.tonValue * pr.detailLink.moneyRialPerTon) * (
                    pr.detailLink.moneyPercentWhenTransfer / 100)
                ds["pay"] = int(ds["pay"])
                ds["project"] = self.serializer_class(instance=pr).data
                data.append(ds)
                # Residan be Irn PORT
                ds = {}
                ds["date_mil"] = pr.****Date - timedelta(
                    pr.detailLink.daysFromIranPortToFactory)
                ds["payType"] = 13
                ds["payTypeStr"] = "تحویل به گمرک ایران" + projectTitle
                ds["pay"] = (pr.tonValue * pr.detailLink.moneyRialPerTon) * (pr.detailLink.moneyPercentTarafeh / 100)
                ds["pay"] += (pr.tonValue * pr.detailLink.moneyRialPerTon) * (pr.detailLink.moneyPercentHazineh / 100)
                ds["pay"] = int(ds["pay"])
                ds["project"] = self.serializer_class(instance=pr).data
                data.append(ds)
                # Maliate Arzesh Afzoodeh
                ds = {}
                ds["date_mil"] = pr.****Date - timedelta(
                    pr.detailLink.daysFromIranPortToFactory)
                ds["payType"] = 14
                ds["payTypeStr"] = "مالیات ارزش افزوده" + projectTitle
                ds["pay"] = (pr.tonValue * pr.detailLink.moneyRialPerTon) * (
                    pr.detailLink.moneyPercentMaliateArzesh / 100)
                ds["pay"] = int(ds["pay"])
                ds["project"] = self.serializer_class(instance=pr).data
                data.append(ds)

                # Residan Be Karkhooneh
                ds = {}
                ds["date_mil"] = pr.****Date
                ds["payType"] = 15
                ds["payTypeStr"] = "هزینه ی حمل تا کارخانه" + projectTitle
                ds["pay"] = (pr.tonValue * pr.detailLink.moneyRialHamelPerTon)
                ds["pay"] = int(ds["pay"])
                ds["project"] = self.serializer_class(instance=pr).data
                data.append(ds)

                # Hazineh Ghal
                ds = {}
                ds["date_mil"] = pr.****Date
                ds["payType"] = 16
                ds["payTypeStr"] = "هزینه ی قلع" + projectTitle
                ds["pay"] = (pr.tonValue * pr.detailLink.moneyRialGhalPerTon)
                ds["pay"] = int(ds["pay"])
                ds["project"] = self.serializer_class(instance=pr).data
                data.append(ds)

                # Hazineh Shimiayee and other
                ds = {}
                ds["date_mil"] = pr.****Date
                ds["payType"] = 17
                ds["payTypeStr"] = "هزینه شیمیایی و سایر" + projectTitle
                ds["pay"] = (pr.tonValue * pr.detailLink.moneyRialOtherShimiaieePerTon)
                ds["pay"] = int(ds["pay"])
                ds["project"] = self.serializer_class(instance=pr).data
                data.append(ds)

                # Residan Be LC
                ds = {}
                ds["date_mil"] = pr.****Date + timedelta(pr.detailLink.daysFromShippingToLC)
                ds["payType"] = 18
                ds["payTypeStr"] = "تسویه ی LC" + projectTitle
                ds["pay"] = (pr.tonValue * pr.detailLink.moneyRialPerTon) * (pr.detailLink.moneyPercentWhenLC / 100)
                ds["pay"] = int(ds["pay"])
                ds["project"] = self.serializer_class(instance=pr).data
                data.append(ds)





            for d in data:
                # d["pay"] = int(d["pay"]) / 1000000 if d["pay"] != 0 else 0
                d["date_sh"] = mil_to_sh(d["date_mil"])



            dates = data

        # generating one year complete with projects paymanets
        AllDatesInOneYear = []
        startDate = datetime.strptime(sh_to_mil(dt["start"]), "%Y/%m/%d")
        currentYear = dt["year"]
        counter = 0
        while currentYear == 1396:
            d = {}
            d["current"] = startDate + timedelta(days=counter)
            d["current_sh"] = mil_to_sh(d["current"])
            d["current_dayname"] = d["current"].strftime("%A")
            d["current_sh_year"] = int(d["current_sh"].split("/")[0])
            d["current_sh_month"] = int(d["current_sh"].split("/")[1])
            d["current_sh_day"] = int(d["current_sh"].split("/")[2])
            d["income"] = 0
            d["incomeDetails"] = []

            d["pay"] = query(dates).where(
                lambda x: x["date_sh"] == d["current_sh"]).sum(
                lambda x: x["pay"])
            d["payDetails"] = query(dates).where(
                lambda x: x["date_sh"] == d["current_sh"]).to_list()
            d["pay"] = int(d["pay"])
            counter += 1
            currentYear = int(mil_to_sh(d["current"]).split("/")[0])
            AllDatesInOneYear.append(d)

        # calculating incoming from selling
        for p in projects:
            projectTitle = " فروش محصول - " + str(int(pr.tonValue)) + " از " + pr.companyLink.name + " "
            print(p.id)
            sood = 1.11
            income20percent = (p.tonValue * p.detailLink.moneyRialPerTon) * decimal.Decimal(0.2)
            income20percent = income20percent * decimal.Decimal(sood)
            income20day = p.****Date + timedelta(days=20)

            income20percent2 = (p.tonValue * p.detailLink.moneyRialPerTon) * decimal.Decimal(0.2)
            income20percent2 = income20percent2 * decimal.Decimal(sood)
            income20day12 = p.****Date + timedelta(days=40)

            income20percent3 = (p.tonValue * p.detailLink.moneyRialPerTon) * decimal.Decimal(0.2)
            income20percent3 = income20percent3 * decimal.Decimal(sood)
            income20day3 = p.****Date + timedelta(days=60)

            income20percent4 = (p.tonValue * p.detailLink.moneyRialPerTon) * decimal.Decimal(0.2)
            income20percent4 = income20percent4 * decimal.Decimal(sood)
            income20day4 = p.****Date + timedelta(days=80)

            income20percent5 = (p.tonValue * p.detailLink.moneyRialPerTon) * decimal.Decimal(0.2)
            income20percent5 = income20percent5 * decimal.Decimal(sood)
            income20day5 = p.****Date + timedelta(days=100)

            for ad in AllDatesInOneYear:
                ad["projectID"] = p.id
                if ad["current"].strftime('%m/%d/%Y') == income20day.strftime('%m/%d/%Y'):
                    ad["income"] += income20percent
                    ad["income"] = int(ad["income"])
                    ad["incomeDetails"].append({
                        "income": int(income20percent),  # income by 20 percent of selling project
                        "type": 21,  # income by 20 percent of selling project
                        "typeStr": "20درصد فروش نقدی بعد از 20 روز"+projectTitle,  # income by 20 percent of selling project
                        "project": self.serializer_class(instance=p).data
                    })

                if ad["current"].strftime('%m/%d/%Y') == income20day12.strftime('%m/%d/%Y'):
                    ad["income"] += int(income20percent2)
                    ad["incomeDetails"].append({
                        "type": 22,  # income by 80 percent of selling project
                        "income": int(income20percent2),  # income by 80 percent of selling project
                        "typeStr": "20 درصد فروش بعد از 40 روز"+projectTitle,  # income by 80 percent of selling project
                        "project": self.serializer_class(instance=p).data
                    })

                if ad["current"].strftime('%m/%d/%Y') == income20day3.strftime('%m/%d/%Y'):
                    ad["income"] += int(income20percent3)
                    ad["incomeDetails"].append({
                        "type": 23,  # income by 80 percent of selling project
                        "income": int(income20percent3),  # income by 80 percent of selling project
                        "typeStr": "20 درصد فروش بعد از 60 روز"+projectTitle,  # income by 80 percent of selling project
                        "project": self.serializer_class(instance=p).data
                    })

                if ad["current"].strftime('%m/%d/%Y') == income20day4.strftime('%m/%d/%Y'):
                    ad["income"] += int(income20percent4)
                    ad["incomeDetails"].append({
                        "type": 24,  # income by 80 percent of selling project
                        "income": int(income20percent4),  # income by 80 percent of selling project
                        "typeStr": "20 درصد فروش بعد از 80 روز"+projectTitle,  # income by 80 percent of selling project
                        "project": self.serializer_class(instance=p).data
                    })

                if ad["current"].strftime('%m/%d/%Y') == income20day5.strftime('%m/%d/%Y'):
                    ad["income"] += int(income20percent5)
                    ad["incomeDetails"].append({
                        "type": 25,  # income by 80 percent of selling project
                        "income": int(income20percent5),  # income by 80 percent of selling project
                        "typeStr": "20 درصد فروش بعد از 100 روز"+projectTitle,  # income by 80 percent of selling project
                        "project": self.serializer_class(instance=p).data
                    })

        # calculating incomaing from malli
        incomings = CashFlow****TaminIncommings.objects.all()
        for inc in incomings:
            shamsi_date = mil_to_sh(inc.dateOfRecieve)
            for ad in AllDatesInOneYear:
                if shamsi_date == ad["current_sh"]:
                    ad["income"] += int(inc.money)
                    ad["incomeDetails"].append({
                        "type": 3,  # income from Mali
                        "typeStr": inc.name+" اخذ شده از مالی",  # income from Mali
                        "income": CashFlow****TaminCashFlow****TaminIncommingsSerializer(instance=inc).data
                    })

        # calculating payment from malli
        payments = CashFlow****TaminPayments.objects.all()
        for pay in payments:
            shamsi_date = mil_to_sh(pay.dateOfPay)
            for ad in AllDatesInOneYear:
                if shamsi_date == ad["current_sh"]:
                    ad["pay"] += int(pay.pay)
                    ad["payDetails"].append({
                        "type": 4,  # pay from Mali
                        "typeStr": pay.name+" اخذ شده از مالی",  # pay from Mali
                        "pay": CashFlow****TaminPaymentsSerializer(instance=pay).data
                    })

        # getting calculated fees
        beginingMoney = 0
        for a in AllDatesInOneYear:
            beginingMoney = (beginingMoney - a["pay"])
            beginingMoney = (beginingMoney + a["income"])
            a["total"] = int(beginingMoney / 1000000)
            a["income"] = int(a["income"] / 1000000)
            a["pay"] = int(a["pay"] / 1000000)
        return AllDatesInOneYear

    @list_route(methods=["GET", ])
    def getByDate(self, request, *args, **kwargs):
        AllDatesInOneYear = self.GenerateAllDayReport()
        return Response(AllDatesInOneYear)

    @list_route(methods=["GET", ])
    def generateMongoCache(self, request, *args, **kwargs):
        AllDatesInOneYear = self.GenerateAllDayReport()
        CashFlow****TaminAllDateTmp.objects.all().delete()
        for adr in AllDatesInOneYear:
            data = {
                'projectID': adr['projectID'] if "projectID" in adr else 0,
                'current': adr['current'],
                'current_dayname': adr['current_dayname'],
                'current_sh': adr['current_sh'],
                'current_sh_day': adr['current_sh_day'],
                'current_sh_month': adr['current_sh_month'],
                'current_sh_year': adr['current_sh_year'],
                'income': adr['income'],
                'incomeDetails': adr['incomeDetails'],
                'pay': adr['pay'],
                'payDetails': adr['payDetails'],
                'total': adr['total']}
            serial = CashFlow****TaminAllDateTmpSerializer(data=data)
            serial.is_valid(raise_exception=True)
            serial.save()
        return Response({})
