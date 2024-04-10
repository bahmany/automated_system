from datetime import datetime, timedelta
from io import BytesIO

import openpyxl
import pandas as pd
from asq.initiators import query
from bs4 import BeautifulSoup
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.BI.models import BIDashboardPage, BIBanksFromSpreadSheet, BIChart
from amspApp.BI.serializers.BIDashboardSerial import BIDashboardPageSerializers
from amspApp.BI.serializers.BIStorageSerial import BIBanksFromSpreadSheetSerial
from amspApp.BI.views.BIAllPages import pages_structure
from amspApp.BI.views.sqls.chart_maps import charts_map, bi_main_menu
from amspApp.BPMSystem.models import DoneProcessArchive
from amspApp.CompaniesManagment.Connections.models import Connections
from amspApp.CompaniesManagment.Connections.viewes.ConnectionsViews import ConnectionsViewSet
from amspApp.Infrustructures.Classes.convert_sqlresult_to_validstr import convert_sqlresultstr_to_valid_str, \
    convert_sqlresultstr_to_valid_numbers
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset
import urllib.request


class BIDashboardPageViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = BIDashboardPage.objects.all().order_by('-id')
    serializer_class = BIDashboardPageSerializers

    def initial(self, request, *args, **kwargs):
        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            # _mutable = request.data._mutable
            # request.data._mutable = True
            request.data["positionID"] = posiIns.positionID
            # request.data._mutable = False
        return super(BIDashboardPageViewSet, self).initial(request, *args, **kwargs)

    @detail_route(methods=['GET'])
    def get_page(self, request, *args, **kwargs):
        page_id = kwargs.get('id', None)
        page_id = int(page_id)
        if page_id:
            find = query(pages_structure).where(lambda x: x['page_id'] == page_id).to_list()
            find = find[0]
            return Response(find)

    @list_route(methods=['POST'])
    def get_type_44312(self, request, *args, **kwargs):
        process_instance = DoneProcessArchive.objects.filter(bpmn__id=request.data.get('process_id')).order_by(
            "-id").first()
        table_values = process_instance.formData[request.data.get('table_element_id')]
        table_structure = query(process_instance.bpmn['form'][0]['schema']['fields']).where(
            lambda x: x['name'] == request.data.get('table_element_id')).first()
        # convert to json

        keys = [{'row': int(x.split("_")[0]), 'col': int(x.split("_")[1]), 'value': table_values[x]} for x in
                table_values.keys()]
        keys = query(keys).group_by(
            lambda x: x['row'],
            result_selector=lambda key, group: {
                'row': key, 'col': query([{'col': x['col'], 'value': x['value']} for x in group]).order_by(
                    lambda x: x['col']).to_list()
            }

        ).to_list()

        json_result = []
        for key in keys:
            new_row = {}
            for thead in table_structure['thead'].keys():
                new_row[table_structure['thead'][thead]['name']] = \
                    query(key['col']).where(lambda x: x['col'] == int(thead)).first()['value']
                if table_structure['thead'][thead]['fieldType'] == "int":
                    new_row[table_structure['thead'][thead]['name']] = int(
                        query(key['col']).where(lambda x: x['col'] == int(thead)).first()['value'])

            json_result.append(new_row)
            dt = {}
            dt['data'] = json_result
            dt['positionName'] = process_instance.positionName
            dt['chartTitle'] = process_instance.chartTitle
            dt['dateOfPost'] = process_instance.postDate
            dt['avatar'] = process_instance.positionPic
        # rahkaraan_quotation_items()
        return Response(dt)


    def retrieve(self, request, *args, **kwargs):
        result = super(BIDashboardPageViewSet, self).retrieve(request, *args, **kwargs)
        for d in result.data.get('details',{}).get('rows',[]):
            for dd in d.get('children', []):
                if dd.get('chartid', False):
                    chart_instance = BIChart.objects.filter(id = dd.get('chartid', None)).first()
                    if chart_instance:
                        dd['chart_type'] = chart_instance.details.get('chart_type', None)
        return result

    # def create(self, request, *args, **kwargs):

    """
    در این تابع
    تمامی شاخص هایی که می تواند موجود باشد 
    را برای چارت می فرستد
    """

    @list_route(methods=['POST'])
    def get_chart_all_shakesh(self, request, *args, **kwargs):
        class_of_chart = query(charts_map).where(lambda x: x['link'] == request.data['chart_id']).first()
        class_of_chart = class_of_chart['class']()
        result = class_of_chart.get_group_by_value_detector()
        return Response(result)

    @list_route(methods=['POST'])
    def get_type_chart(self, request, *args, **kwargs):
        class_of_chart = query(charts_map).where(lambda x: x['link'] == request.data['chart_id']).first()
        class_of_chart = class_of_chart['class']()
        result = class_of_chart.get_structure("sum", "QuotationItemQuantity",
                                              "QuotationItemState,QuotationItemUnitName,QuotationDatePersian_Year, QuotationDatePersian_Month",
                                              "QuotationDatePersian_Year",
                                              "asc")
        return Response(result)

    @list_route(methods=['POST'])
    def get_chart_data(self, request, *args, **kwargs):
        """
        برای موبایل که نمی تواند درخواست هایش را
        در قالب عدد بفرستد
        مجبور شدم همه چیز را در قالب استرینگ بفرستم
        و بعدش جایی این استرینگ ها رو تبدیل به عدد کنم
        """
        for k in request.data.keys():
            if type('') == type(request.data[k]):
                request.data[k] = int(request.data[k]) if request.data[k].replace('-', '').isdigit() else request.data[
                    k]

        find = query(charts_map).where(lambda x: x['link'] == request.data['chart_id']).first()['class']()
        groupby_index = request.data.get('groupby_index', -1)
        groupby_value = request.data.get('groupby_value', -1)
        chart_type = request.data['chart_type']
        chart_id = request.data['chart_id']
        groupby_dataset_index = request.data.get('groupby_dataset_index', -1)

        find.properties['filter'] = []
        result = find.get_data(
            find,
            groupby_index,
            groupby_dataset_index,
            groupby_value,
            chart_type,
            chart_id,
            request.user.id,
            request.data
        )

        return Response(result)

    @list_route(methods=['GET'])
    def get_amar_banks(self, request, *args, **kwargs):
        currenttime = datetime.now()
        sss = BIBanksFromSpreadSheet.objects.filter(
            dateOfPost__gte=currenttime - timedelta(minutes=2)
        )
        if sss.first():
            dt = BIBanksFromSpreadSheetSerial(instance=sss.first()).data
            if request.user.groups.filter(name__contains="group_financial").count() == 0:
                for d in dt['data']:
                    d['ghabelebardasht'] = 0
            return Response(dt)

        with urllib.request.urlopen(
                # 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQujdFwqA8NidS34c3DjrW1L3tswUy_I8wSeRf4VbdVAlgFFRy0EDxJXCKTuALE--MX7UuZhUoKvKxj/pub?output=xlsx'
                # 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQujdFwqA8NidS34c3DjrW1L3tswUy_I8wSeRf4VbdVAlgFFRy0EDxJXCKTuALE--MX7UuZhUoKvKxj/pubhtml?gid=480328920&single=true'
                'https://docs.google.com/spreadsheets/d/e/2PACX-1vQujdFwqA8NidS34c3DjrW1L3tswUy_I8wSeRf4VbdVAlgFFRy0EDxJXCKTuALE--MX7UuZhUoKvKxj/pubhtml?gid=0&single=true'
        ) as f:
            getted = f.read().decode('utf-8')

        soup = BeautifulSoup(getted)
        table = soup.find('table', )
        ress = []
        alls = table.find_all('tr')
        for row in alls:
            res = []
            ppp = row.find_all('td')
            for r in ppp:
                res.append(
                    r.string
                )
            ress.append(res)
        result = []
        for rr in ress:
            if len(rr) > 5:
                cc = 0
                if rr[8] != None:
                    rr[8] = rr[8].replace(',', '').replace(' ', '')
                    if rr[8].isdigit():
                        cc = int(rr[8])

                dt = {}
                dt['name'] = rr[3]
                dt['ghabelebardasht'] = int(cc / 1000000)
                result.append(dt)

        for r in result:
            if r['name'] == 'جمع موجودی بانکها':
                r['sort'] = 1
            else:
                r['sort'] = 0
        result = query(result).where(lambda x: x['ghabelebardasht'] > 0 and x['name'] != 'مانده').order_by_descending(
            lambda x: (x['sort'], x['ghabelebardasht'],)).to_list()
        dt = {
            'dateOfPost': datetime.now(),
            'data': result

        }
        # print(dt['data'][0])
        if request.user.groups.filter(name__contains ="group_financial").count() == 0:
            for d in dt['data']:
                d['ghabelebardasht'] = 0

        sdt = BIBanksFromSpreadSheetSerial(data=dt)
        sdt.is_valid()
        sdt.save()
        return Response(sdt.data)

    @list_route(methods=['GET'])
    def get_amar_pish_for_homepage(self, request, *args, **kwargs):
        sql1 = """
 
 
        

DROP TABLE IF EXISTS #tmptblsq;
DROP TABLE IF EXISTS #tmptbktqnullcheched;
DROP TABLE IF EXISTS #callissuer;
DROP TABLE IF EXISTS #kjdhfkwjdfh;
DROP TABLE IF EXISTS #pishs
DROP TABLE IF EXISTS #final_pish_report

select
llp.IssuePermitItemID,
rsnol.OrderItemID,
(select count(*) FROM [RahkaranDB].[LGS3].[InventoryVoucherItem] where ReferenceRef =  llp.[IssuePermitItemID]) as tedade_havaleh_khorooj,
(select sum(Quantity) FROM [RahkaranDB].[LGS3].[InventoryVoucherItem] where ReferenceRef =  llp.[IssuePermitItemID]) as mizaneh_khorooj_kharej_shode
into #callissuer
FROM [RahkaranDB].[SLS3].[vwRptSalesNewOrderItem]  as rsnol 
inner join (
SELECT  ipi.[IssuePermitItemID] -- در حواله خروج این نوشته می شود - و در فیلد ReferenceRef
, ipi.Quantity
, s2.value('(/ProductInfo/@ProductSourceItemRef)[1]', 'int') as XML_ProductSourceItemRef   -- حواله فروش
  FROM [RahkaranDB].[LGS3].[IssuePermitItem] as ipi
  cross apply  [ExtraData].nodes('ProductInfo') t(s2)

) llp on llp.XML_ProductSourceItemRef = rsnol.OrderItemID
--inner join [RahkaranDB].[LGS3].[IssuePermitItem] cross apply  [ExtraData].nodes('ProductInfo') t(s2) as [ipi] on [ipi]. 



select fkjguh.*, cia.tedade_havaleh_khorooj, cia.mizaneh_khorooj_kharej_shode into #kjdhfkwjdfh from [RahkaranDB].[SLS3].[vwRptSalesNewOrderItem] as fkjguh inner join #callissuer as cia on fkjguh.OrderItemID = cia.OrderItemID



SELECT top (9000)

(select sum(rtsno.[OrderItemQuantity]) from #kjdhfkwjdfh  as rtsno
	where 
	rtsno.[OrderItemSourceNumber] = mrtq.[QuotationNumber] and 
	rtsno.[OrderItemProductNumber] = mrtq.[QuotationItemProductNumber] and 
	rtsno.[OrderItemState] = 'بسته شده'
	) as Order_BastehShodeh,
(select sum(rtsno.[mizaneh_khorooj_kharej_shode]) from #kjdhfkwjdfh  as rtsno
	where 
	rtsno.[OrderItemSourceNumber] = mrtq.[QuotationNumber] and 
	rtsno.[OrderItemProductNumber] = mrtq.[QuotationItemProductNumber] and 
	rtsno.[OrderItemState] = 'بسته شده'
	) as Order_BastehShodeh_KharejShodej,


(select sum(rtsno.[OrderItemQuantity]) from #kjdhfkwjdfh  as rtsno
	where 
	rtsno.[OrderItemSourceNumber] = mrtq.[QuotationNumber] and 
	rtsno.[OrderItemProductNumber] = mrtq.[QuotationItemProductNumber] and 
	rtsno.[OrderItemState] = 'در حال استفاده'
	) as Order_DarHaleEstefadeh,
(select sum(rtsno.[mizaneh_khorooj_kharej_shode]) from #kjdhfkwjdfh  as rtsno
	where 
	rtsno.[OrderItemSourceNumber] = mrtq.[QuotationNumber] and 
	rtsno.[OrderItemProductNumber] = mrtq.[QuotationItemProductNumber] and 
	rtsno.[OrderItemState] = 'در حال استفاده'
	) as Order_DarHaleEstefadeh_KharejShodej,



(select sum(rtsno.[OrderItemQuantity]) from #kjdhfkwjdfh  as rtsno
	where 
	rtsno.[OrderItemSourceNumber] = mrtq.[QuotationNumber] and 
	rtsno.[OrderItemProductNumber] = mrtq.[QuotationItemProductNumber] and 
	rtsno.[OrderItemState] = 'تاييده شده'
	) as Order_TaeedShodeh,
(select sum(rtsno.[mizaneh_khorooj_kharej_shode]) from #kjdhfkwjdfh  as rtsno
	where 
	rtsno.[OrderItemSourceNumber] = mrtq.[QuotationNumber] and 
	rtsno.[OrderItemProductNumber] = mrtq.[QuotationItemProductNumber] and 
	rtsno.[OrderItemState] = 'تاييده شده'
	) as Order_TaeedShodeh_KharejShodej,




(select sum(rtsno.[OrderItemQuantity]) from #kjdhfkwjdfh  as rtsno
	where 
	rtsno.[OrderItemSourceNumber] = mrtq.[QuotationNumber] and 
	rtsno.[OrderItemProductNumber] = mrtq.[QuotationItemProductNumber] and 
	rtsno.[OrderItemState] = 'ثبت شده'
	) as Order_SabtShodeh,

(select sum(rtsno.[mizaneh_khorooj_kharej_shode]) from #kjdhfkwjdfh  as rtsno
	where 
	rtsno.[OrderItemSourceNumber] = mrtq.[QuotationNumber] and 
	rtsno.[OrderItemProductNumber] = mrtq.[QuotationItemProductNumber] and 
	rtsno.[OrderItemState] = 'ثبت شده'
	) as Order_SabtShodeh_KharejShodej,



(select sum(rtsno.[OrderItemQuantity]) from #kjdhfkwjdfh  as rtsno
	where 
	rtsno.[OrderItemSourceNumber] = mrtq.[QuotationNumber] and 
	rtsno.[OrderItemProductNumber] = mrtq.[QuotationItemProductNumber] and 
	rtsno.[OrderItemState] = 'مسدود'
	) as Order_Masdood,

(select sum(rtsno.[mizaneh_khorooj_kharej_shode]) from #kjdhfkwjdfh  as rtsno
	where 
	rtsno.[OrderItemSourceNumber] = mrtq.[QuotationNumber] and 
	rtsno.[OrderItemProductNumber] = mrtq.[QuotationItemProductNumber] and 
	rtsno.[OrderItemState] = 'مسدود'
	) as Order_Masdood_KharejShodej,



--(select sum(ississ.mizaneh_khorooj_kharej_shode) from mizaneh_khorooj_kharej_shode as ississ where ississ.IssuePermitItemID = mrtq.Refere


mrtq.[QuotationItemQuotationID]
      ,mrtq.[QuotationItemID]
      ,mrtq.[QuotationItemRowNumber]
      ,mrtq.[QuotationItemUnitName]
      ,mrtq.[QuotationItemProductNumber]
      ,mrtq.[QuotationItemProductNumber_sharh]
	  ,mrtq.[QuotationItemProductName]
      ,mrtq.[QuotationItemProductNumber_BP]
      ,mrtq.[QuotationItemProductNumber_TEMPER]
      ,mrtq.[QuotationItemProductNumber_sath]
      ,mrtq.[QuotationItemProductNumber_zekhamat]
      ,mrtq.[QuotationItemProductNumber_arz]
      ,mrtq.[QuotationItemProductNumber_darajeh]
      ,mrtq.[QuotationItemProductNumber_tool]
      ,mrtq.[QuotationItemProductNumber_zekhamat_arz]
      ,mrtq.[QuotationItemProductNumber_zekhamat_arz_tool]
      ,mrtq.[QuotationItemProductNumber_zekhamat_arz_tool_temper_keshvar]
      ,mrtq.[QuotationCustomerName]
      ,mrtq.[QuotationCustomerNumber]
      ,mrtq.[QuotationNumber]
      ,mrtq.[QuotationItemQuantity]
      ,mrtq.[QuotationItemPriceBaseFee]
      ,mrtq.[QuotationItemFee]
      ,mrtq.[QuotationItemPrice]
      ,mrtq.[QuotationItemAdditionAmount]
      ,mrtq.[QuotationItemReductionAmount]
      ,mrtq.[QuotationDate]
      ,mrtq.[QuotationDatePersian]
      ,mrtq.[QuotationDatePersian_YearMonth]
      ,mrtq.[QuotationDatePersian_Year]
      ,mrtq.[QuotationDatePersian_Day]
      ,mrtq.[QuotationDatePersian_Month]
      ,mrtq.[QuotationItemState]
	  into #tmptblsq

  FROM [RahkaranDB].[SLS3].[MRBvwRptSalesNewQuotationItem]  as mrtq;

  select 
    cast(isnull(Order_BastehShodeh, 0) as int) as  Order_BastehShodehNullCheck,
    cast(isnull(Order_BastehShodeh_KharejShodej, 0) as int) as  Order_BastehShodeh_KharejShodejNullCheck,
	
	cast(isnull(Order_DarHaleEstefadeh, 0) as int) as Order_DarHaleEstefadehNullCheck,
	cast(isnull(Order_DarHaleEstefadeh_KharejShodej, 0) as int) as Order_DarHaleEstefadeh_KharejShodejNullCheck,
	
	cast(isnull(Order_TaeedShodeh, 0) as int) as Order_TaeedShodehNullCheck,
	cast(isnull(Order_TaeedShodeh_KharejShodej, 0) as int) as Order_TaeedShodehNull_KharejShodejCheck,
	
	cast(isnull(Order_SabtShodeh, 0) as int) as Order_SabtShodehNullCheck,
	cast(isnull(Order_SabtShodeh_KharejShodej, 0) as int) as Order_SabtShodehNull_KharejShodejCheck,

	cast(isnull(Order_Masdood, 0) as int) as Order_MasdoodNullCheck,
	cast(isnull(Order_Masdood_KharejShodej, 0) as int) as Order_MasdoodNull_KharejShodejCheck,

	
	
	* 
	into #pishs
	from #tmptblsq

	order by QuotationDate desc;


	select 
	Order_BastehShodeh_KharejShodejNullCheck+
	Order_DarHaleEstefadeh_KharejShodejNullCheck+
	Order_TaeedShodehNull_KharejShodejCheck+
	Order_TaeedShodehNull_KharejShodejCheck+
	Order_MasdoodNull_KharejShodejCheck mizane_kole_kharej_shode,


	case when Order_MasdoodNull_KharejShodejCheck > 0 then 0 else 
	QuotationItemQuantity - (Order_BastehShodeh_KharejShodejNullCheck+
	Order_DarHaleEstefadeh_KharejShodejNullCheck+
	Order_TaeedShodehNull_KharejShodejCheck+
	Order_TaeedShodehNull_KharejShodejCheck+
	Order_MasdoodNull_KharejShodejCheck ) end as mandeh,
	
	* into #final_pish_report from #pishs  
	where QuotationItemState != 'باطل شده'
	order by QuotationItemID desc;




	select 
	
	case QuotationItemState 
	when 'بسته شده' then 'در جریان'
	when 'ثبت شده' then 'منتظر مشتری'
	when NULL then 'نامشخص'
	else 'دارای توضیحات'
	end as vaziat
	
	,
	case QuotationItemProductNumber_sharh 
	when '75' then 'کویل قلع امانی'
	when '88' then 'ورق قلع برش خورده'
	when '69' then 'کلاف سرد'
	when '85' then 'خدمات قلع و برش'
	when '77' then 'کویل قلع اندود'
	when '86' then 'خدمات برش'
	when '89' then 'چاپ و لاک'
	when '66' then 'ورق سیاه'
	when '87' then 'ماکسان'
	when '92' then 'قوطی'
	when '93' then 'درب'
	else 'سایر'
	end as Noe
	,
	cast(sum(mandeh) / 1000 as int) as mandeh ,
	case QuotationItemUnitName
	when 'کیلوگرم' then 'تن'
	when 'عدد' then 'هزارعدد'
	else 'تن'
	end as unit
	,
	cast(sum(QuotationItemPrice) / 1000000 as int) as mablagh
	
	from #final_pish_report
	where mandeh > 0
	group by QuotationItemState, QuotationItemProductNumber_sharh, QuotationItemUnitName
	order by sum(QuotationItemPrice) desc;
        
 
         """
        connection = Connections.objects.get(databaseName="RahkaranDB")
        connection = ConnectionsViewSet().getConnection(connection)
        connection.execute(sql1)
        result = connection.fetchall()
        result = convert_sqlresultstr_to_valid_str(result)
        result = convert_sqlresultstr_to_valid_numbers(result)
        return Response({'main': result})

    @list_route(methods=['GET'])
    def __get_amar_pish_for_homepage(self, request, *args, **kwargs):
        sql1 = """select top 5
sum(QuotationItemQuantity)/1000 as [ton] , 
(select top 1 eee.Name from [RahkaranDB].[SLS3].[vwCustomer] as eee where eee.Number = QuotationCustomerNumber) as CustomerName,
QuotationCustomerNumber from [SLS3].[MRBvwRptSalesNewQuotationItem]
where QuotationDatePersian_Year in (1400) 
and QuotationItemState in ('ثبت شده') 
and ([QuotationItemProductNumber_sharh] in ('66','69','75','77','85','86','87','88','89','90','92','93','98'))

group by QuotationCustomerNumber order by sum(QuotationItemQuantity) desc"""
        self.connection = Connections.objects.get(databaseName="RahkaranDB")
        self.connection = ConnectionsViewSet().getConnection(self.connection)
        self.connection.execute(sql1)
        top3 = self.connection.fetchall()

        sql2 = """select sum(QuotationItemQuantity)/1000 as sumof
				 
			from [SLS3].[MRBvwRptSalesNewQuotationItem]
			where 
				QuotationDatePersian_Year in (1400) 
			and QuotationItemState in ('ثبت شده') 
		   and ([QuotationItemProductNumber_sharh] in ('66','69','75','77','85','86','87','88','89','90','92','93','98'))"""
        connection = ConnectionsViewSet().getConnection(Connections.objects.get(databaseName="RahkaranDB"))
        connection.execute(sql2)
        mainAdad = connection.fetchall()

        sql3 = """
        /****** Script for SelectTopNRows command from SSMS  ******/

DROP TABLE IF EXISTS ##tmptblsq;
DROP TABLE IF EXISTS ##tmptbktqnullcheched;

SELECT top (9000)
(select sum(rtsno.[OrderItemQuantity]) from [RahkaranDB].[SLS3].[vwRptSalesNewOrderItem]  as rtsno
	where 
	rtsno.[OrderItemSourceNumber] = mrtq.[QuotationNumber] and 
	rtsno.[OrderItemProductNumber] = mrtq.[QuotationItemProductNumber] and 
	rtsno.[OrderItemState] = 'بسته شده'
	) as TaeenVaTklifShodeh,
(select sum(rtsno.[OrderItemQuantity]) from [RahkaranDB].[SLS3].[vwRptSalesNewOrderItem]  as rtsno
	where 
	rtsno.[OrderItemSourceNumber] = mrtq.[QuotationNumber] and 
	rtsno.[OrderItemProductNumber] = mrtq.[QuotationItemProductNumber] and 
	rtsno.[OrderItemState] = 'در حال استفاده'
	) as DarJaryan,
(select sum(rtsno.[OrderItemQuantity]) from [RahkaranDB].[SLS3].[vwRptSalesNewOrderItem]  as rtsno
	where 
	rtsno.[OrderItemSourceNumber] = mrtq.[QuotationNumber] and 
	rtsno.[OrderItemProductNumber] = mrtq.[QuotationItemProductNumber] and 
	rtsno.[OrderItemState] = 'تاييده شده'
	) as TaeedShodeh,

mrtq.[QuotationItemQuotationID]
      ,mrtq.[QuotationItemID]
      ,mrtq.[QuotationItemRowNumber]
      ,mrtq.[QuotationItemUnitName]
      ,mrtq.[QuotationItemProductNumber]
      ,mrtq.[QuotationItemProductNumber_sharh]
      ,mrtq.[QuotationItemProductNumber_BP]
      ,mrtq.[QuotationItemProductNumber_TEMPER]
      ,mrtq.[QuotationItemProductNumber_sath]
      ,mrtq.[QuotationItemProductNumber_zekhamat]
      ,mrtq.[QuotationItemProductNumber_arz]
      ,mrtq.[QuotationItemProductNumber_darajeh]
      ,mrtq.[QuotationItemProductNumber_tool]
      ,mrtq.[QuotationItemProductNumber_zekhamat_arz]
      ,mrtq.[QuotationItemProductNumber_zekhamat_arz_tool]
      ,mrtq.[QuotationItemProductNumber_zekhamat_arz_tool_temper_keshvar]
      ,mrtq.[QuotationCustomerName]
      ,mrtq.[QuotationCustomerNumber]
      ,mrtq.[QuotationNumber]
      ,mrtq.[QuotationItemProductName]
      ,mrtq.[QuotationItemQuantity]
      ,mrtq.[QuotationItemPriceBaseFee]
      ,mrtq.[QuotationItemFee]
      ,mrtq.[QuotationItemPrice]
      ,mrtq.[QuotationItemAdditionAmount]
      ,mrtq.[QuotationItemReductionAmount]
      ,mrtq.[QuotationDate]
      ,mrtq.[QuotationDatePersian]
      ,mrtq.[QuotationDatePersian_YearMonth]
      ,mrtq.[QuotationDatePersian_Year]
      ,mrtq.[QuotationDatePersian_Day]
      ,mrtq.[QuotationDatePersian_Month]
      ,mrtq.[QuotationItemState]
	  into ##tmptblsq

  FROM [RahkaranDB].[SLS3].[MRBvwRptSalesNewQuotationItem]  as mrtq
  
  
  order by [QuotationItemID] desc

		
		
		  select 
    isnull(TaeenVaTklifShodeh, 0) as  TaeenVaTaklifShodehNullCheck,
	isnull(DarJaryan, 0) as DarJaryanNullCheck,
	isnull(TaeedShodeh, 0) as TaeedShodehNullCheck,
	*
	into ##tmptbktqnullcheched
	from ##tmptblsq 
	
	where DarJaryan > 0 order by DarJaryan desc;
	


  select case QuotationItemUnitName when 'عدد' then 'هزارعدد' else 'تن' end as QuotationItemUnitName ,		
		sum(DarJaryanNullCheck)/1000 - sum(TaeenVaTaklifShodehNullCheck)/1000 + sum(TaeedShodehNullCheck)/1000   as ton 
		from ##tmptbktqnullcheched where DarJaryan > 0 group by QuotationItemUnitName order by sum(QuotationItemQuantity) desc;
        """
        connection = ConnectionsViewSet().getConnection(Connections.objects.get(databaseName="RahkaranDB"))
        connection.execute(sql3)
        darjaryan = connection.fetchall()
        darjaryan = convert_sqlresultstr_to_valid_str(darjaryan)
        darjaryan = convert_sqlresultstr_to_valid_numbers(darjaryan)

        sql4 = """
        
        /****** Script for SelectTopNRows command from SSMS  ******/

DROP TABLE IF EXISTS #tmptblsq;
DROP TABLE IF EXISTS #tmptbktqnullcheched;

SELECT top (9000)
(select sum(rtsno.[OrderItemQuantity]) from [RahkaranDB].[SLS3].[vwRptSalesNewOrderItem]  as rtsno
	where 
	rtsno.[OrderItemSourceNumber] = mrtq.[QuotationNumber] and 
	rtsno.[OrderItemProductNumber] = mrtq.[QuotationItemProductNumber] and 
	rtsno.[OrderItemState] = 'بسته شده'
	) as TaeenVaTklifShodeh,
(select sum(rtsno.[OrderItemQuantity]) from [RahkaranDB].[SLS3].[vwRptSalesNewOrderItem]  as rtsno
	where 
	rtsno.[OrderItemSourceNumber] = mrtq.[QuotationNumber] and 
	rtsno.[OrderItemProductNumber] = mrtq.[QuotationItemProductNumber] and 
	rtsno.[OrderItemState] = 'در حال استفاده'
	) as DarJaryan,
(select sum(rtsno.[OrderItemQuantity]) from [RahkaranDB].[SLS3].[vwRptSalesNewOrderItem]  as rtsno
	where 
	rtsno.[OrderItemSourceNumber] = mrtq.[QuotationNumber] and 
	rtsno.[OrderItemProductNumber] = mrtq.[QuotationItemProductNumber] and 
	rtsno.[OrderItemState] = 'تاييده شده'
	) as TaeedShodeh,

mrtq.[QuotationItemQuotationID]
      ,mrtq.[QuotationItemID]
      ,mrtq.[QuotationItemRowNumber]
      ,mrtq.[QuotationItemUnitName]
      ,mrtq.[QuotationItemProductNumber]
      ,mrtq.[QuotationItemProductNumber_sharh]
      ,mrtq.[QuotationItemProductNumber_BP]
      ,mrtq.[QuotationItemProductNumber_TEMPER]
      ,mrtq.[QuotationItemProductNumber_sath]
      ,mrtq.[QuotationItemProductNumber_zekhamat]
      ,mrtq.[QuotationItemProductNumber_arz]
      ,mrtq.[QuotationItemProductNumber_darajeh]
      ,mrtq.[QuotationItemProductNumber_tool]
      ,mrtq.[QuotationItemProductNumber_zekhamat_arz]
      ,mrtq.[QuotationItemProductNumber_zekhamat_arz_tool]
      ,mrtq.[QuotationItemProductNumber_zekhamat_arz_tool_temper_keshvar]
      ,mrtq.[QuotationCustomerName]
      ,mrtq.[QuotationCustomerNumber]
      ,mrtq.[QuotationNumber]
      ,mrtq.[QuotationItemProductName]
      ,mrtq.[QuotationItemQuantity]
      ,mrtq.[QuotationItemPriceBaseFee]
      ,mrtq.[QuotationItemFee]
      ,mrtq.[QuotationItemPrice]
      ,mrtq.[QuotationItemAdditionAmount]
      ,mrtq.[QuotationItemReductionAmount]
      ,mrtq.[QuotationDate]
      ,mrtq.[QuotationDatePersian]
      ,mrtq.[QuotationDatePersian_YearMonth]
      ,mrtq.[QuotationDatePersian_Year]
      ,mrtq.[QuotationDatePersian_Day]
      ,mrtq.[QuotationDatePersian_Month]
      ,mrtq.[QuotationItemState]
	  into #tmptblsq

  FROM [RahkaranDB].[SLS3].[MRBvwRptSalesNewQuotationItem]  as mrtq
  
  
  order by [QuotationItemID] desc

		
		
		  select 
    isnull(TaeenVaTklifShodeh, 0) as  TaeenVaTaklifShodehNullCheck,
	isnull(DarJaryan, 0) as DarJaryanNullCheck,
	isnull(TaeedShodeh, 0) as TaeedShodehNullCheck,
	*
	into #tmptbktqnullcheched
	from #tmptblsq 
	
	where DarJaryan > 0 order by DarJaryan desc;
	


  select top 5 QuotationCustomerName,		
  (sum(DarJaryanNullCheck)  - sum(TaeenVaTaklifShodehNullCheck))/1000 + sum(TaeedShodehNullCheck)/1000 as ton, 
    
  case QuotationItemUnitName when 'عدد' then 'هزارعدد' else 'تن' end as QuotationItemUnitName 


		from #tmptbktqnullcheched where DarJaryan > 0  
		group by QuotationCustomerName, QuotationItemUnitName
		order by (sum(DarJaryanNullCheck)  - sum(TaeenVaTaklifShodehNullCheck)) desc
        
        """
        connection = ConnectionsViewSet().getConnection(Connections.objects.get(databaseName="RahkaranDB"))
        connection.execute(sql4)
        darjaryantop5 = connection.fetchall()
        darjaryantop5 = convert_sqlresultstr_to_valid_str(darjaryantop5)
        darjaryantop5 = convert_sqlresultstr_to_valid_numbers(darjaryantop5)

        return Response({
            'top3': top3,
            'main': mainAdad,
            'darjaryan': darjaryan,
            'darjaryan_top': darjaryantop5,
        })



    @list_route(methods=['GET'])
    def get_dashboard_main_menu(self, request, *args, **kwargs):
        return Response(bi_main_menu)
