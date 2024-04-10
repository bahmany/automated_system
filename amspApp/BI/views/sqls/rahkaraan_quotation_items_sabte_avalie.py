from asq.initiators import query

from amspApp.BI.views.sqls.bi_utils import bi_months, get_monthnumber
from amspApp.CompaniesManagment.Connections.models import Connections
from amspApp.CompaniesManagment.Connections.viewes.ConnectionsViews import ConnectionsViewSet
from django.core.cache import cache

from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh, getCurrentYearShamsi


class rahkaraan_quotation_items_sabte_avalieh():
    refresh_seconds = 1
    connection = None
    customer_list = """
    /****** Script for SelectTopNRows command from SSMS  ******/
SELECT top(1000) *  FROM [RahkaranDB].[SLS3].[vwCustomer]  
    """
    rahkaraan_quotation_items_main_sql = """
    /****** Script for SelectTopNRows command from SSMS  ******/
/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [QuotationItemQuotationID]
      ,[QuotationItemID]
      ,[QuotationItemRowNumber]
	        ,[QuotationItemUnitName]
			      ,[QuotationItemProductNumber]
      ,[QuotationItemProductNumber_sharh]
      ,[QuotationItemProductNumber_BP]
      ,[QuotationItemProductNumber_TEMPER]
      ,[QuotationItemProductNumber_sath]
      ,[QuotationItemProductNumber_zekhamat]
      ,[QuotationItemProductNumber_arz]
      ,[QuotationItemProductNumber_darajeh]
      ,[QuotationItemProductNumber_tool]
      ,[QuotationItemProductNumber_zekhamat_arz]
      ,[QuotationItemProductNumber_zekhamat_arz_tool]
      ,[QuotationItemProductNumber_zekhamat_arz_tool_temper_keshvar]
      ,[QuotationCustomerName]
      ,[QuotationCustomerNumber]
      ,[QuotationItemProductName]
      ,[QuotationItemQuantity]
      ,[QuotationItemPriceBaseFee]
      ,[QuotationItemFee]
      ,[QuotationItemPrice]
      ,[QuotationItemAdditionAmount]
      ,[QuotationItemReductionAmount]
      ,[QuotationDate]
      ,[QuotationDatePersian]
      ,[QuotationDatePersian_YearMonth]
      ,[QuotationDatePersian_Year]
      ,[QuotationDatePersian_Day]
      ,[QuotationDatePersian_Month]
      ,[QuotationItemState]
      ,[QuotationItemSalesAreaCode]
      ,[QuotationItemBlockedQuantity]
      ,[QuotationItemDeliveryAddress]
      ,[QuotationItemDeliveryAddressProvinceName]
      ,[QuotationItemDeliveryAddressCity1Name]
      ,[QuotationItemRecipient]
  FROM [RahkaranDB].[SLS3].[MRBvwRptSalesNewQuotationItem]
  where 
  [QuotationItemQuotationID] in (SELECT [QuotationID]  FROM [RahkaranDB].[SLS3].[MRBvwRptSalesNewQuotation] where QuotationState = 1) and ([QuotationItemProductNumber_sharh] in ('66','69','75','77','85','86','87','88','89','90','92','93','98'))
    """
    rahkaraan_quotation_items_table_names = {
        0: "[SLS3].[MRBvwRptSalesNewQuotationItem]"
    }

    properties = {
        'groupby_steps': {
            0: 'QuotationItemUnitName',
            1: 'QuotationCustomerNumber',
            2: 'QuotationItemProductName',
        },
        'groupby': 1,
        'show_last_row_date_of_insert_field_name': 'QuotationDate',
        'color_of_current_dataset': '#1565c0',
        'if_month': 'show_month_name',
        'operation': 'sum',
        'shakhes': {
            "field_name": 'QuotationItemQuantity',
            "field_title": 'میزان - کیلوگرم',
        },
        'filter': [
            {
                "field_name": 'QuotationDatePersian_Year',
                "field_title": 'سال شمسی',
                'value': [
                    int(getCurrentYearShamsi())
                ],
                'operand': "in"
            },
            {
                'field_name': 'QuotationItemState',
                'field_title': 'وضعیت',
                'value': [
                    # 'بسته شده',
                    'ثبت شده',
                    # 'در حال استفاده',
                ],
                'operand': "in"
            }
        ],
        # 'shakhesha': query(charts_map).where(lambda x: x['link'] == 'dasgasdfawfasdvag').first()[
        #     'class']().get_group_by_value_detector()
    }

    catch_name = "_SLS3_MRBvwRptSalesNewQuotationItem_"
    rahkaraan_quotation_items_chart_fields = [
        {'type': 'static', 'field_name': 'QuotationItemQuantity', 'field_title': 'میزان - کیلوگرم'},
        {'type': 'static', 'field_name': 'QuotationItemFee', 'field_title': 'مبلغ جز'},
        {'type': 'static', 'field_name': 'QuotationItemPrice', 'field_title': 'مبلغ کل'},
        {'type': 'formula', 'field_name': 'Count(*)', 'field_title': 'تعداد'},
    ]  # شاخص ها
    rahkaraan_quotation_items_groupbys = [
        {'field_name': 'QuotationItemQuantity', 'field_title': 'نوع کالا', 'field_type': 'string'},
        {'field_name': 'QuotationItemState', 'field_title': 'وضعیت', 'field_type': 'string'},
        {'field_name': 'QuotationItemUnitName', 'field_title': 'واحد شمارش', 'field_type': 'unit_name'},
        {'field_name': 'QuotationDatePersian_Year', 'field_title': 'سال شمسی', 'field_type': 'shamsi_year'},
        {'field_name': 'QuotationDatePersian_Month', 'field_title': 'ماه شمسی', 'field_type': 'shamsi_month'},
        {'field_name': 'QuotationDatePersian_Day', 'field_title': 'روز شمسی', 'field_type': 'shamsi_day'},
        {'field_name': 'QuotationItemProductName', 'field_title': 'عنوان کالا', 'field_type': 'string'},
        {'field_name': 'QuotationCustomerNumber', 'field_title': 'مشتری',
         'field_type': 'customer_number_cast_to_customer_name'},
    ]  # ابعاد

    def get_cutomer_list_to_cache(self):
        res = cache.get("customers_list")
        if res != None:
            return res
        self.connection = Connections.objects.get(databaseName="RahkaranDB")
        self.connection = ConnectionsViewSet().getConnection(self.connection)
        self.connection.execute(self.customer_list)
        sql_res = self.connection.fetchall()
        cache.set('customers_list', sql_res, 360)
        return sql_res

    def get_customer_name_from_number(self, customer_number):
        customer_list = self.get_cutomer_list_to_cache()
        result = query(customer_list).where(lambda x: x['CustomerID'] == customer_number).first()
        return result['Name']

    def get_group_by_value_detector(self):
        cac = cache.get(self.catch_name + "_unique_values")
        if cac:
            return cac
        self.connection = Connections.objects.get(databaseName="RahkaranDB")
        self.connection = ConnectionsViewSet().getConnection(self.connection)

        for r in self.rahkaraan_quotation_items_groupbys:
            sql = "select distinct({}) from {}".format(r['field_name'], self.rahkaraan_quotation_items_table_name)
            self.connection.execute(sql)
            sql_res = self.connection.fetchall()
            sql_res = [x[r['field_name']] for x in sql_res]
            r['results'] = sql_res
        cache.set(self.catch_name + "_unique_values", self.rahkaraan_quotation_items_groupbys, self.refresh_seconds * 3)
        return self.rahkaraan_quotation_items_groupbys

    def __init__(self):
        self.connection = Connections.objects.get(databaseName="RahkaranDB")
        self.connection = ConnectionsViewSet().getConnection(self.connection)

    def get_selected_dataset_sqltable_name(self, index):
        return self.rahkaraan_quotation_items_table_names[index]

    def get_data(self, main_class, groupby_index, groupby_dataset_index, groupby_value, chart_type, chart_id, userid):

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
            prev_tbl_name = "{}___{}___{}___{}___{}".format(
                chart_id,
                str(chart_type),
                groupby_dataset_index,
                groupby_index - 1,
                str(userid)
            )
            last_table = cache.get(
                prev_tbl_name
            )
            filter_to_append = ""

            for i in range(0, groupby_index):
                filter_to_append = "{} in ({})".format(
                    self.properties['groupby_steps'][groupby_index - 1],
                    convert_alias_value_to_main_value(
                        self.properties['groupby_steps'][groupby_index - 1], last_table['labels'][groupby_value]
                    )
                )
                more_filter.append(filter_to_append)

            last_filter_field_name = self.properties['groupby_steps'][groupby_index - 1]
            last_filter_field_title = query(self.rahkaraan_quotation_items_groupbys).where(
                lambda x: x['field_name'] == last_filter_field_name).first()['field_title']
            last_filter_field_value = last_table['labels'][groupby_value]
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
