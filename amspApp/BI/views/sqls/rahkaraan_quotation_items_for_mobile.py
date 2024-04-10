import json

from asq.initiators import query
import logging

from amspApp.BI.views.sqls.bi_utils import bi_months, get_monthnumber
from amspApp.CompaniesManagment.Connections.models import Connections
from amspApp.CompaniesManagment.Connections.viewes.ConnectionsViews import ConnectionsViewSet
from django.core.cache import cache

from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh, getCurrentYearShamsi
from amspApp.Infrustructures.Classes.convert_sqlresult_to_validstr import convert_sqlresultstr_to_valid_str, \
    convert_sqlresultstr_to_valid_numbers


class rahkaraan_quotation_items_for_mobile():
    refresh_seconds = 1
    connection = None

    quotation_nec_tbl_generator = """
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


	DROP TABLE IF EXISTS mrbPishWithTrace;

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
*
into mrbPishWithTrace
	from #final_pish_report
	where mandeh > 0
	order by QuotationItemPrice desc;
	
select top 1 * from mrbPishWithTrace; 
    """

    rahkaraan_quotation_items_table_names = {
        0: "mrbPishWithTrace"
    }

    properties = {
        'groupby_steps': {
            0: 'QuotationCustomerName',
            1: 'QuotationItemProductNumber_zekhamat',
            2: 'QuotationItemProductName',
        },
        'groupby': 0,
        'show_last_row_date_of_insert_field_name': 'QuotationDate',
        'color_of_current_dataset': '#1565c0',
        'if_month': 'show_month_name',
        'operation': 'sum',
        'shakhes': {
            "field_name": 'mandeh',
            "field_title": 'میزان',
        },
        'filter': [],

        # 'shakhesha': query(charts_map).where(lambda x: x['link'] == 'dasgasdfawfasdvag').first()[
        #     'class']().get_group_by_value_detector()
    }

    catch_name = "_mrbPishWithTrace_"
    rahkaraan_quotation_items_chart_fields = [
        {'type': 'static', 'field_name': 'QuotationItemProductName', 'field_title': 'میزان - کیلوگرم'},
        {'type': 'static', 'field_name': 'vaziat', 'field_title': 'میزان - کیلوگرم'},
        {'type': 'static', 'field_name': 'QuotationCustomerName', 'field_title': 'میزان - کیلوگرم'},
        {'type': 'static', 'field_name': 'QuotationItemProductNumber_zekhamat', 'field_title': 'میزان - کیلوگرم'},
        {'type': 'static', 'field_name': 'mandeh', 'field_title': 'میزان - کیلوگرم'},
        {'type': 'static', 'field_name': 'QuotationItemFee', 'field_title': 'مبلغ جز'},
        {'type': 'static', 'field_name': 'QuotationItemPrice', 'field_title': 'مبلغ کل'},
        {'type': 'formula', 'field_name': 'Count(*)', 'field_title': 'تعداد'},
    ]  # شاخص ها
    rahkaraan_quotation_items_groupbys = [
        {'field_name': 'vaziat', 'field_title': 'وضعیت', 'field_type': 'string'},
        {'field_name': 'QuotationItemProductName', 'field_title': 'نام کالا', 'field_type': 'string'},
        {'field_name': 'QuotationCustomerName', 'field_title': 'نام مشتری', 'field_type': 'nvarchar'},
        {'field_name': 'QuotationItemProductNumber_zekhamat', 'field_title': 'ضخامت', 'field_type': 'string'},
    ]  # ابعاد

    def __init__(self):
        self.connection = Connections.objects.get(databaseName="RahkaranDB")
        self.connection = ConnectionsViewSet().getConnection(self.connection)

    def get_selected_dataset_sqltable_name(self, index):
        return self.rahkaraan_quotation_items_table_names[index]

    def get_data(self,
                 main_class,
                 groupby_index,
                 groupby_dataset_index,
                 groupby_value,
                 chart_type,
                 chart_id,
                 userid,
                 post_data
                 ):
        """ این چند خط ریفرش میکند جدول گلوبال پیش فاکتورهای کامل را """
        kjdhsgfafaodf = cache.get('kjdhsgfafaodf')
        if kjdhsgfafaodf == None:
            connection1 = Connections.objects.get(databaseName="RahkaranDB")
            connection1 = ConnectionsViewSet().getConnectionAutoCommit1(connection1)
            connection1.execute(self.quotation_nec_tbl_generator)
            # connection.close()
            pp = connection1.fetchall()
            connection1.close()

            cache.set('kjdhsgfafaodf', 'it referesh database cache easy two min', 240)
        """--------------------------------------"""

        # pp = convert_sqlresultstr_to_valid_str(pp)
        # pp = convert_sqlresultstr_to_valid_numbers(pp)

        if chart_type == 896742:
            self.properties['filter'].append(
                {
                    "field_name": 'Noe',
                    "field_title": 'نوع',
                    'value': [
                        post_data['onvan']
                    ],
                    'operand': "in"
                }
            )

            self.properties['filter'].append(
                {
                    "field_name": 'vaziat',
                    "field_title": 'وضعیت',
                    'value': [
                        post_data['vaziat']
                    ],
                    'operand': "in"
                }
            )

        # shakhes_ha = self.get_group_by_value_detector()
        where_clause = []

        def convert_alias_value_to_main_value(fieldname, value):
            fieldname_type = query(self.rahkaraan_quotation_items_groupbys).where(
                lambda x: x['field_name'] == fieldname).first()['field_type']

            """
            چهت تبدیل ماه حروفی به ماه عددی
            """
            if fieldname_type == "shamsi_month":
                if type('') == type(value):
                    value = get_monthnumber(value)
            if fieldname_type == "string":
                if type('') == type(value):
                    value = "'{}'".format(str(value))
            if fieldname_type == "nvarchar":
                if type('') == type(value):
                    value = "N'{}'".format(str(value))
            if fieldname_type == "unit_name":
                if type('') == type(value):
                    value = "'{}'".format(str(value))

            if fieldname_type == "customer_number_cast_to_customer_name":
                customers_list = self.get_cutomer_list_to_cache()
                value = query(customers_list).where(lambda x: x['Name'] == value).first()['Number']
                value = "'{}'".format(str(value))
            return value

        def convert_filter_to_clause(value):

            if type([]) == type(value):
                if type(1) == type(value[0]):
                    cc = ",".join(list(map(str, value)))
                    cc = "(" + cc + ")"
                    if cc == "()":
                        cc = None
                    return cc

                if type('') == type(value[0]):
                    cc = "','".join(value)
                    cc = "('" + cc + "')"
                    if cc == "('')":
                        cc = None
                    return cc

            if type(1) == type(value):
                return str(value)
            if type('') == type(value):
                return "'{}'".format(value)

        for p in self.properties['filter']:
            c = '{} {} {}'.format(
                p['field_name'],
                p['operand'],
                convert_filter_to_clause(p['value'])
            )
            where_clause.append(c)
        where_clause = " and ".join(where_clause)

        """
        ---------------------------------------------------------------------------------------------
        ---------------------------------------------------------------------------------------------
        
        تا خط بالا فیلترهای معمولی ساخته می شود
        حالا می بایست فیلترهای مربوط به مراحل مختلف
        استپ ساخته شود
        در اینجا لازم است حلقه ای به ازای استپ ایجاد شود 
        و گروب های قبلی به عنوان فیلتر قرار گیرند
        
        ---------------------------------------------------------------------------------------------
        ---------------------------------------------------------------------------------------------
        """
        more_filter = []
        last_filter_field_name = ""
        last_filter_field_title = ""
        last_filter_field_value = ""
        current_filter_field_name = self.properties['groupby_steps'][groupby_index]
        current_filter_field_title = query(self.rahkaraan_quotation_items_groupbys).where(
            lambda x: x['field_name'] == current_filter_field_name).first()['field_title']
        current_filter_field_type = query(self.rahkaraan_quotation_items_groupbys).where(
            lambda x: x['field_name'] == current_filter_field_name).first()['field_type']
        if groupby_index > 0:
            # prev_tbl_name = "{}___{}___{}___{}___{}".format(
            #     chart_id,
            #     str(chart_type),
            #     groupby_dataset_index,
            #     groupby_index - 1,
            #     str(userid)
            # )
            # last_table = cache.get(
            #     prev_tbl_name
            # )
            filter_to_append = ""
            values = json.loads(post_data['values'])
            labels = post_data['labels'].replace('[','').replace(']','').split(',')
            labels = [x.rstrip().lstrip() for x in labels]

            for i in range(0, groupby_index):
                filter_to_append = "{} in ({})".format(
                    self.properties['groupby_steps'][groupby_index - 1],
                    convert_alias_value_to_main_value(
                        self.properties['groupby_steps'][groupby_index - 1], labels[groupby_value]
                    )
                )
                more_filter.append(filter_to_append)

            last_filter_field_name = self.properties['groupby_steps'][groupby_index - 1]
            last_filter_field_title = query(self.rahkaraan_quotation_items_groupbys).where(
                lambda x: x['field_name'] == last_filter_field_name).first()['field_title']
            last_filter_field_value = labels[groupby_value]
            last_filter_field_type = query(self.rahkaraan_quotation_items_groupbys).where(
                lambda x: x['field_name'] == last_filter_field_name).first()['field_type']
            if type(' ') == type(last_filter_field_value):
                last_filter_field_value = "'" + last_filter_field_value
            # if last_filter_field_type == 'customer_number_cast_to_customer_name':
            #     customers_list = self.get_cutomer_list_to_cache()
            #     last_filter_field_value = query(customers_list).where(lambda x:x['Name'] == last_filter_field_value).first()['Number']

        if len(more_filter) > 0:
            more_filter = ' and '.join(more_filter)
            where_clause = where_clause + " and " + more_filter

        last_field_name = ""

        """
        ---------------------------------------------------------------------------------------------
        ---------------------------------------------------------------------------------------------
        ---------------------------------------------------------------------------------------------
        ---------------------------------------------------------------------------------------------
        ---------------------------------------------------------------------------------------------
        ---------------------------------------------------------------------------------------------
        ---------------------------------------------------------------------------------------------
        ---------------------------------------------------------------------------------------------
        ---------------------------------------------------------------------------------------------
        """

        if where_clause:
            if where_clause != "":
                where_clause = " where " + where_clause
        sql = "select {}({}) as [{}],{} from {} {} group by {} order by {} {}".format(
            self.properties['operation'],
            self.properties['shakhes']['field_name'],
            self.properties['shakhes']['field_title'],
            self.properties['groupby_steps'][groupby_index],
            self.rahkaraan_quotation_items_table_names[groupby_dataset_index],
            where_clause,
            self.properties['groupby_steps'][groupby_index],
            self.properties['groupby_steps'][groupby_index],
            'asc')
        self.connection.execute(sql)
        sql_res = self.connection.fetchall()
        sql_res = convert_sqlresultstr_to_valid_str(sql_res)
        sql_res = convert_sqlresultstr_to_valid_numbers(sql_res)

        legend = self.properties['shakhes']['field_title']
        data = [x[self.properties['shakhes']['field_title']] for x in sql_res]
        labels = [x[self.properties['groupby_steps'][groupby_index]] for x in sql_res]

        """
        ---------------------------------------------------------------------------
        ---------------------------------------------------------------------------
        ---------------------------------------------------------------------------
        برای اینکه بخواهیم آخرین تاریخ ثبت شده ی رکوردی را بدست بیاوریم
        ---------------------------------------------------------------------------
        ---------------------------------------------------------------------------
        ---------------------------------------------------------------------------
        """
        last_sql_res = None
        if self.properties.get('show_last_row_date_of_insert_field_name', None):
            last_sql = "select top 1 {} from {} order by {} desc".format(
                self.properties.get('show_last_row_date_of_insert_field_name', None),
                self.rahkaraan_quotation_items_table_names[groupby_dataset_index],
                self.properties.get('show_last_row_date_of_insert_field_name', None),
            )
            self.connection.execute(last_sql)
            last_sql_res = self.connection.fetchall()
            last_sql_res = mil_to_sh(
                last_sql_res[0][self.properties.get('show_last_row_date_of_insert_field_name', None)])
        """
        ---------------------------------------------------------------------------
        ---------------------------------------------------------------------------
        ---------------------------------------------------------------------------
        ---------------------------------------------------------------------------
        ---------------------------------------------------------------------------
        """

        if self.properties.get('if_month', None):
            if self.properties.get('if_month', None) == 'show_month_name':
                if query(self.rahkaraan_quotation_items_groupbys).where(
                        lambda x: x['field_name'] == self.properties['groupby_steps'][groupby_index]).first()[
                    'field_type'] == 'shamsi_month':
                    labels = [bi_months[x - 1] for x in labels]

        if current_filter_field_type == 'customer_number_cast_to_customer_name':
            customers_list = self.get_cutomer_list_to_cache()
            labels = [
                query(customers_list).where(lambda x: x['Number'] == l).first()['Name'] for l in labels
            ]

        dt = {
            'datasets': [
                {
                    'label': legend,
                    'data': data
                }],
            'max_depth': len(self.properties['groupby_steps']),
            'labels': labels,
            'last_filter_field_name': last_filter_field_name,
            'last_filter_field_title': last_filter_field_title,
            'last_filter_field_value': last_filter_field_value,
            'current_filter_field_name': current_filter_field_name,
            'current_filter_field_title': current_filter_field_title,
            'label_type':
                query(self.rahkaraan_quotation_items_groupbys).where(
                    lambda x: x['field_name'] == self.properties['groupby_steps'][groupby_index]).first()[
                    'field_type'],
            'label_type_title':
                query(self.rahkaraan_quotation_items_groupbys).where(
                    lambda x: x['field_name'] == self.properties['groupby_steps'][groupby_index]).first()[
                    'field_title']
        }

        if last_sql_res: dt['last_insert'] = last_sql_res
        if self.properties.get('color_of_current_dataset', None):
            dt['datasets'][0]['backgroundColor'] = [self.properties.get('color_of_current_dataset', None) for x in data]
        """
        این کش برای زمانی هست که 
        کاربر بخواهد کلیک کند و من 
        نیاز دارم تا داده هایی داشته باشم
        
        chart_id___chart_type___group_by_index___group_by_index___userid
        
        """
        current_tbl_name = "{}___{}___{}___{}___{}".format(
            chart_id,
            str(chart_type),
            groupby_dataset_index,
            groupby_index,
            str(userid))
        cache.set(current_tbl_name,
                  dt, 26000)

        return dt
