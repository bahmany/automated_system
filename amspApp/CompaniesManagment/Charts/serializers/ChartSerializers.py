from asq.initiators import query
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from amspApp.CompaniesManagment.Charts.models import Chart
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp._Share.DynamicFieldModelSerializer import DynamicFieldsModelSerializer

__author__ = 'mohammad'


class ChartSerializer(DynamicFieldsModelSerializer):
    title = serializers.CharField(
        required=True,
        help_text=_("Title of the position you prefer to make in your organization"),
        label=_("Position title"),
        max_length=30,
        min_length=3,
        allow_null=False,
        allow_blank=False,

        style={
            'ng-model': 'chart.title'
        }
    )

    CompanyID = serializers.CharField(source="owner.id", read_only=True)
    CompanyName = serializers.CharField(source="owner.name", read_only=True)

    rank = serializers.IntegerField(required=False, allow_null=True, default=-1)

    class Meta:
        model = Chart
        fields = ("id", "title", "top", "post_date", "owner", 'CompanyID', "CompanyName", "rank",)

    def save(self, **kwargs):
        result = super(ChartSerializer, self).save(**kwargs)

        posDocs = PositionsDocument.objects.filter(chartID=result.id)

        for pos in posDocs:
            pos.chartName = result.title
            pos.save()
        return result

    """
    this def creates default chart for default company automatically after
     user registration
     and then return second chart created as CEO

    """

    def create_default_chart(self, companyInstance):
        newChart1 = Chart(
            top=None,
            title=companyInstance.name,
            owner=companyInstance,
        )
        newChart1.save()
        newChart2 = Chart(
            top=newChart1,
            title=_("CEO"),
            owner=companyInstance
        )
        newChart2.save()
        newChart3 = Chart(
            top=newChart2,
            title=_("Commerce Manager"),
            owner=companyInstance
        )
        newChart3.save()
        newChart4 = Chart(
            top=newChart2,
            title=_("Finance Manager"),
            owner=companyInstance
        )
        newChart4.save()
        newChart5 = Chart(
            top=newChart2,
            title=_("Assistant"),
            owner=companyInstance
        )
        newChart5.save()
        return newChart2

    def get_json_chart(self, companyInstace):
        charts = Chart.objects.all().filter(owner=companyInstace)
        # if charts.count() == 0:
        # self.create_default_chart(companyInstace)
        #     self.get_json_chart(companyInstace)
        # # getting top level of chart
        for chart in charts:
            if chart.top == None:
                stater = chart

        output = {}

        def createDict(dict, parentItem, items):
            subitems = items.filter(top_id=parentItem)
            v = []
            for item in subitems:
                v.append({"name": item.title + " - " +str(item.rank), "id": item.id, "rank": item.rank,
                          "children": createDict(output, item.id, charts)})
            return v

        output = {"name": stater.title, "id": stater.id, "rank": stater.rank,
                  "children": createDict(output, stater.id, charts)}
        return output

    def get_dict_chart_from_chartID(self, chartID):
        stater = Chart.objects.all().get(id=chartID)
        charts = Chart.objects.filter(owner=stater.owner)
        # if charts.count() == 0:
        # self.create_default_chart(companyInstace)
        #     self.get_json_chart(companyInstace)
        # # getting top level of chart

        output = {}

        def createDict(dict, parentItem, items):
            subitems = items.filter(top_id=parentItem)
            v = []
            for item in subitems:
                v.append({"name": item.title, "id": item.id, "children": createDict(output, item.id, charts)})
            return v

        output = {"name": stater.title, "id": stater.id,
                  "children": createDict(output, stater.id, charts)}
        return output

    def get_list_chart_from_chartID(self, chartID):
        res = self.get_dict_chart_from_chartID(chartID)
        b = []

        def cv(obj):
            if obj["children"]:
                for c in obj["children"]:
                    cv(c)
            b.append(obj)

        cv(res)
        return [a['id'] for a in b]

    def get_list_top_chart_from_chartID(self, chartID):
        currentChartInstance = ChartSerializer(instance=Chart.objects.get(id=chartID)).data
        charts = ChartSerializer(instance=Chart.objects.all().filter(owner=currentChartInstance["owner"]),
                                 many=True).data
        result = []

        def getTop(c):
            list = query(charts).where(lambda x: x["id"] == c["top"]).to_list()
            for l in list:
                getTop(l)
            if "top" in c:
                if c["top"]:
                    result.append(c)

        getTop(currentChartInstance)
        result = query([r["id"] for r in result]).distinct().to_list()
        return result
