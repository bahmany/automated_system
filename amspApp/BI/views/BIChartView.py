from datetime import datetime
from io import BytesIO
from random import randint

import pandas as pd
from bs4 import BeautifulSoup

import requests
import sqlparse
from asq.initiators import query
from django.core.cache import cache
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.BI.DataTables.models import DataTable, DataTableValues
from amspApp.BI.models import BIChart, BISqls
from amspApp.BI.serializers.BIChartSerial import BIChartSerializers
from amspApp.BI.serializers.BISqlsSerial import BISqlsLess1Serializers
from amspApp.CompaniesManagment.Connections.models import Connections
from amspApp.CompaniesManagment.Connections.viewes.ConnectionsViews import ConnectionsViewSet
from amspApp.Infrustructures.Classes.convert_sqlresult_to_validstr import convert_sqlresultstr_to_valid_str, \
    convert_sqlresultstr_to_valid_numbers
from amspApp._Share.colors import gen_colors
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class BIChartViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = BIChart.objects.all().order_by('-id')
    serializer_class = BIChartSerializers

    def initial(self, request, *args, **kwargs):
        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            # _mutable = request.data._mutable
            # request.data._mutable = True
            request.data["positionID"] = posiIns.positionID
            # request.data._mutable = _mutable
        return super(BIChartViewSet, self).initial(request, *args, **kwargs)

    def get_tables_specs(self, table_name):
        connection = Connections.objects.get(databaseName="RahkaranDB")
        connection = ConnectionsViewSet().getConnection(connection)
        sql = """
            SELECT COLUMN_NAME,* 
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '%s'
        """ % (table_name,)
        connection.execute(sql)
        sql_res = connection.fetchall()
        sql_res = convert_sqlresultstr_to_valid_str(sql_res)
        sql_res = convert_sqlresultstr_to_valid_numbers(sql_res)
        return sql_res

    def update(self, request, *args, **kwargs):
        # sql_id = request.data.get('details',{}).get('sql',{}).get('id', None)
        chart_instance = self.queryset.get(id=kwargs['id'])
        has_table_def = True
        if not chart_instance.details.get('sql', False):
            has_table_def = False
        if not chart_instance.details.get('sql', {}).get('id', False):
            has_table_def = False
        if not chart_instance.details.get('sql', {}).get('table_spec', False):
            has_table_def = False
        if not chart_instance.details.get('sql', {}).get('table_spec', [{}])[0].get('COLUMN_NAME', False):
            has_table_def = False

        if not has_table_def:
            table_spec = self.get_mssql_table_info(request, *args, **kwargs).data
            if not request.data['details'].get('sql', False):
                request.data['details']['sql'] = {}
            request.data['details']['sql']['table_spec'] = table_spec
        return super(BIChartViewSet, self).update(request, *args, **kwargs)

    @detail_route(methods=['POST'])
    def duplicate_chart(self, request, *args, **kwargs):
        chart_instance = self.queryset.get(id=kwargs['id'])
        ss = self.serializer_class(instance=chart_instance).data
        del ss['id']
        ss['chartTitle'] = request.data['chartTitle']
        ss = self.serializer_class(data=ss)
        ss.is_valid(raise_exception=True)
        ss.save()
        return Response(ss.data)

    @detail_route(methods=['GET'])
    def get_mssql_table_info(self, request, *args, **kwargs):
        chart_instance = self.queryset.get(id=kwargs['id'])
        if chart_instance.details.get('sql', {}).get('id', '') == '':
            return Response([{}])
        instance = BISqls.objects.get(id=chart_instance.details.get('sql', {}).get('id', ''))
        sql_res = self.get_tables_specs(instance.slqscript_selector)
        sql_res = query(sql_res).select(lambda x: {
            'COLUMN_NAME': x['COLUMN_NAME'],
            'DATA_TYPE': x['DATA_TYPE']
        }).to_list()
        return Response(sql_res)

    def generate_filter_clause(self, table_row_def, grouped_value):
        if table_row_def['DATA_TYPE'] == "varchar":
            if grouped_value:
                filter_string = "%s in ('%s')" % (table_row_def['COLUMN_NAME'], grouped_value)
                return filter_string

            if len(table_row_def.get('available_values', [])) != 0:
                __values = query(table_row_def['available_values']).where(
                    lambda x: x.get('checked', False) == True).select(
                    lambda x: x[table_row_def['COLUMN_NAME']]).to_list()
                if len(__values) > 0:
                    __values = ["'" + x + "'" for x in __values]
                    __values = ','.join(__values)
                    filter_string = "%s in (%s)" % (table_row_def['COLUMN_NAME'], __values)
                    return filter_string
        if table_row_def['DATA_TYPE'] == "nvarchar":
            if grouped_value:
                filter_string = "%s in (N'%s')" % (table_row_def['COLUMN_NAME'], grouped_value)
                return filter_string
            if len(table_row_def.get('available_values', [])) != 0:
                __values = query(table_row_def['available_values']).where(
                    lambda x: x.get('checked', False) == True).select(
                    lambda x: x[table_row_def['COLUMN_NAME']]).to_list()
                if len(__values) > 0:
                    __values = ["N'" + x + "'" for x in __values]
                    __values = ','.join(__values)
                    filter_string = "%s in (%s)" % (table_row_def['COLUMN_NAME'], __values)
                    return filter_string

                """
                <option value=1>مساوی</option>
                <option value=2>بزرگتر</option>
                <option value=3>کوچکتر</option>
                <option value=4>بین</option>
                """
        if table_row_def['DATA_TYPE'] in ['int', 'decimal', 'bigint', 'decimal', ]:
            if table_row_def.get('numerial_filter_type', False):

                if grouped_value:
                    filter_string = "%s in (%s)" % (
                        table_row_def['COLUMN_NAME'], str(grouped_value))
                    return filter_string

                if table_row_def.get('numerial_filter_type', -1) == '1':
                    if table_row_def.get('value', False):
                        filter_string = "%s = %s" % (table_row_def['COLUMN_NAME'], str(table_row_def['value']))
                        return filter_string
                if table_row_def.get('numerial_filter_type', -1) == '2':
                    if table_row_def.get('value', False):
                        filter_string = "%s > %s" % (table_row_def['COLUMN_NAME'], str(table_row_def['value']))
                        return filter_string
                if table_row_def.get('numerial_filter_type', -1) == '3':
                    if table_row_def.get('value', False):
                        filter_string = "%s < %s" % (table_row_def['COLUMN_NAME'], str(table_row_def['value']))
                        return filter_string
                if table_row_def.get('numerial_filter_type', -1) == '4':
                    if table_row_def.get('value', -1) >= -1:
                        filter_string = "%s between  %s and %s" % (
                            table_row_def['COLUMN_NAME'], str(table_row_def['value']), str(table_row_def['value_to']))
                        return filter_string

    def ins_query_maker(self, tablename, rowdict):
        keys = tuple(rowdict)
        dictsize = len(rowdict)
        sql = ''
        for i in range(dictsize):
            if (type(rowdict[keys[i]]).__name__ == 'str'):
                sql += "'" + str(rowdict[keys[i]]) + "'"
            else:
                sql += str(rowdict[keys[i]])
            if (i < dictsize - 1):
                sql += ', '
        keys = ['[' + k.replace("'", '') + ']' for k in keys]
        query = "insert into " + str(tablename) + " (" + ','.join(keys) + ") values (" + sql + ")"
        # print(query)  # for demo purposes we do this
        return query  # in real code we do this

    def generate_charting_tsql(self,
                               chartID,
                               level,
                               dataset_index,
                               selected_value_index,
                               user_id,
                               orderByField
                               ):
        chart_instance = self.queryset.get(id=chartID)
        if chart_instance.details.get('chart_type', False) == 'latestdatatable':
            return {
                'chartID': chartID,
                'level': 0,
                'max_level': 0,
                'dataset_index': 0,
                'selected_value_index': 0,
                'user_id': user_id,
                'selected_label': [],
                'selected_value': [],
                'sql': '',

            }

        sql_instance = BISqls.objects.get(id=chart_instance.details.get('sql', {}).get('id', ''))
        if sql_instance.type_of_datasource == 5:  # means no need to run sql filler
            a = 1

        cols_with_details = self.get_tables_specs(sql_instance.slqscript_selector)

        has_right_table_def = True

        if len(chart_instance.details.get('sql', {}).get('table_spec', [])) == 0:
            has_right_table_def = False

        if has_right_table_def == False:
            sqlll = chart_instance.details
            sqlll['sql'] = sqlll['sql'] if sqlll.get('sql', True) else {}
            sqlll['sql']['table_spec'] = cols_with_details
            chart_instance.update(details={})
            chart_instance = self.queryset.get(id=chartID)

            bis = BIChartSerializers(instance=chart_instance, data={'details': sqlll}, partial=True)
            bis.is_valid(raise_exception=True)
            bis.save()
            chart_instance = self.queryset.get(id=chartID)

        # ----------------------------------------------------------------------
        # start grouping operation
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        group_by_field = ""
        if chart_instance.details.get('sql', {}).get('group', False):
            fields_group = query(chart_instance.details.get('sql', {}).get('table_spec', [])).where(
                lambda x: x.get('is_selected_for_group', False) == True).order_by(lambda x: x['order']).to_list()
            # group_by_field = ','.join([x['COLUMN_NAME'] for x in fields_group])
            if chart_instance.details.get('chart_type', '') in ['line', 'bar']:
                if len(fields_group):
                    group_by_field = fields_group[level]['COLUMN_NAME']
            if chart_instance.details.get('chart_type', '') in ['top5']:
                if len(fields_group):
                    group_by_field = ','.join([x.get('COLUMN_NAME', '') for x in fields_group])

            if chart_instance.details.get('chart_type', '') in ['table']:
                if len(fields_group):
                    group_by_field = ','.join([x.get('COLUMN_NAME', '') for x in fields_group])

        if group_by_field != "":
            group_by_field = " group by " + group_by_field
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        # start filtering operation
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        filter_string = ""
        if chart_instance.details.get('sql', {}).get('filter', False):
            fields_filter = query(chart_instance.details.get('sql', {}).get('table_spec', [])).where(
                lambda x: x.get('is_selected_for_filter', False) == True).order_by(
                lambda x: x.get('order', 9999)).to_list()
            filterings = []
            for f in fields_filter:
                filterings.append(self.generate_filter_clause(f, False))
            filter_string = ' and '.join(filterings)
        selected_label = None
        selected_value = None
        filter_string_of_group = ""
        if level != 0:
            prev_group_filter = []
            for i in range(0, level):
                cache_name = "%s-%s-%s" % (chartID, user_id, i)
                cache_name_for_req = "%s-%s-%s-request" % (chartID, user_id, i + 1)
                previous_level_data = cache.get(cache_name)
                previous_level_data_request = cache.get(cache_name_for_req)
                if (previous_level_data is None):
                    """
                    در شرایطی که به هر دلیلی کش پاک شده بود خودش برود به به لول صفر
                    """
                    return self.generate_charting_tsql(
                        chartID=chartID,
                        level=0,
                        dataset_index=0,
                        selected_value_index=0, user_id=user_id, orderByField=None)
                """
                در این مرحله منظور اولین زووم است
                """
                if previous_level_data_request == None:
                    dataset = previous_level_data.get('datasets', [])[dataset_index]
                    selected_label = previous_level_data.get('labels', {})[selected_value_index]
                    selected_value = dataset.get('data')[selected_value_index]
                else:
                    dataset = previous_level_data.get('datasets', [])[
                        previous_level_data_request.get('dataset_index', 0)]
                    selected_label = previous_level_data.get('labels', {})[
                        previous_level_data_request.get('selected_value_index', 0)]
                    selected_value = dataset.get('data')[previous_level_data_request.get('selected_value_index', 0)]

                row_defs = query(chart_instance.details['sql']['table_spec']).where(
                    lambda x: x.get('is_selected_for_group', False) == True).order_by(
                    lambda x: x.get('order', 999)).to_list()[i]

                prev_group_filter.append(self.generate_filter_clause(row_defs, selected_label))
            if len(prev_group_filter) > 0:
                filter_string = filter_string + " and " + ' and '.join(prev_group_filter)

            a = 1

        if filter_string != "":
            filter_string = " where " + filter_string

        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        # start calc operation
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        calc_string = ""
        if chart_instance.details.get('sql', {}).get('operation', False):
            fields_filter = query(chart_instance.details.get('sql', {}).get('table_spec', [])).where(
                lambda x: x.get('is_selected_for_operation', False) == True)
            operations = []
            for f in fields_filter:
                """
                    <option value=1>sum</option>
                    <option value=2>max</option>
                    <option value=3>min</option>
                    <option value=4>count</option>
                    <option value=4>ave</option>
                """
                if f.get('operation_type', False) == '1':
                    operations.append("sum(%s) as %s" % (f['COLUMN_NAME'], f['COLUMN_NAME']))
                if f.get('operation_type', False) == '2':
                    operations.append("max(%s) as %s" % (f['COLUMN_NAME'], f['COLUMN_NAME']))
                if f.get('operation_type', False) == '3':
                    operations.append("min(%s) as %s" % (f['COLUMN_NAME'], f['COLUMN_NAME']))
                if f.get('operation_type', False) == '4':
                    operations.append("count(%s) as %s" % (f['COLUMN_NAME'], f['COLUMN_NAME']))
                if f.get('operation_type', False) == '5':
                    operations.append("avg(%s) as %s" % (f['COLUMN_NAME'], f['COLUMN_NAME']))

            calc_string = ' , '.join(operations)
            calc_string = group_by_field.replace("group by", "") + "," + calc_string

        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        if calc_string == "":
            calc_string = ','.join(query(cols_with_details).select(lambda x: x['COLUMN_NAME']).to_list())
            if chart_instance.details.get('chart_type', '') in ['table']:
                if len(group_by_field) > 0:
                    calc_string = ','.join([x.get('COLUMN_NAME', '') for x in fields_group])

        # cols = self.get_mssql_table_info(request, *args, **kwargs).data
        order_by = ''
        if chart_instance.details.get('sort_type', False):
            if chart_instance.details.get('sort_type', '') == 'label':
                if len(calc_string.split(',')) != 0:
                    order_by = ' order by ' + calc_string.split(',')[0]
            if chart_instance.details.get('sort_type', '') == 'label_desc':
                if len(calc_string.split(',')) != 0:
                    order_by = ' order by ' + calc_string.split(',')[0] + ' desc '
            if chart_instance.details.get('sort_type', '') == 'value':
                if len(calc_string.split(',')) > 1:
                    order_by = ' order by ' + calc_string.split(',')[1]
            if chart_instance.details.get('sort_type', '') == 'value_desc':
                if len(calc_string.split(',')) > 1:
                    order_by = ' order by ' + calc_string.split(',')[1][
                                              0: calc_string.split(',')[1].find('as')] + ' desc '
        top_5 = ""
        if chart_instance.details.get('chart_type', '') in ['top5']:
            top_5 = " top 5 "

        if chart_instance.details.get('chart_type', '') in ['table']:
            """
            در اینجا نام فارسی فیلد ارسال شده است
            حالا باید نام فارسی تبدیل به نام فیلد باشد
            """
            if orderByField is not None:
                has_desc = orderByField.find('-')
                orderByField = orderByField.replace('-', '')
                fieldname = query(fields_group).where(lambda x: x['alias'] == orderByField).first()
                fieldname = fieldname.get('COLUMN_NAME')
                order_by = fieldname
                if has_desc != -1:
                    order_by = " order by " + order_by + " desc "
                else:
                    order_by = " order by " + order_by

        sql = """ select %s from %s""" % (
            top_5 + calc_string,
            sql_instance.slqscript_selector + filter_string + group_by_field + order_by
        )

        sql = sql.replace('select ,', 'select ')
        sql = sql.replace('top 5 ,', 'top 5 ')

        return {
            'chartID': chartID,
            'level': level,
            'max_level': query(chart_instance.details.get('sql', {}).get('table_spec', [])).where(
                lambda x: x.get('is_selected_for_group', False) == True).count(),
            'dataset_index': dataset_index,
            'selected_value_index': selected_value_index,
            'user_id': user_id,
            'selected_label': selected_label,
            'selected_value': selected_value,
            'sql': sqlparse.format(sql, reindent=True, keyword_case='upper'),

        }

    def generate_chart_by_chartDict(self, chart_dict):
        pass

    @detail_route(methods=['POST'])
    def get_distinct(self, request, *args, **kwargs):
        chart_instance = self.queryset.get(id=kwargs['id'])
        sql_instance = BISqls.objects.get(id=chart_instance.details.get('sql', {}).get('id', ''))
        sql = """
        select %s from %s group by %s
        """ % (
            request.data['COLUMN_NAME'], sql_instance.slqscript_selector, request.data['COLUMN_NAME']
        )
        connection = Connections.objects.get(databaseName="RahkaranDB")
        connection = ConnectionsViewSet().getConnection(connection)
        connection.execute(sql)
        sql_res = connection.fetchall()
        sql_res = convert_sqlresultstr_to_valid_str(sql_res)
        sql_res = convert_sqlresultstr_to_valid_numbers(sql_res)
        return Response(sql_res)

    @detail_route(methods=['POST'])
    def get_charting_tsql(self, request, *args, **kwargs):
        res = self.generate_charting_tsql(kwargs['id'], 0, 0, 0, request.user.id, request.data.get('sort', None))
        return Response({"sql": res})

    @detail_route(methods=['GET'])
    def preview_table_by_chartID(self, request, *args, **kwargs):
        sql = self.generate_charting_tsql(kwargs['id'], 0, 0, 0, request.user.id, request.data.get('sort', None))
        if len(sql['sql']) < 2:
            return Response({})

        connection = Connections.objects.get(databaseName="RahkaranDB")
        connection = ConnectionsViewSet().getConnection(connection)
        connection.execute(sql['sql'])
        sql_res = connection.fetchall()
        sql_res = convert_sqlresultstr_to_valid_str(sql_res)
        sql_res = convert_sqlresultstr_to_valid_numbers(sql_res)
        return Response(sql_res)

    def get_chart(self, chart_instance, sql, sql_res, userid, requestdata):
        # detecting labels
        # قانون این است که فقط یک فیلد می تواند گروپ باشد و همان
        # گروپ بعنوان لیبلز در نظر گرفته می شود
        label_field = query(chart_instance.details['sql']['table_spec']).where(
            lambda x: x.get('is_selected_for_group', False) == True).order_by(lambda x: x.get('order', 999)).to_list()
        if len(label_field) > 0:
            label_field = label_field[sql['level']]
            labels = [x[label_field['COLUMN_NAME']] for x in sql_res]
        else:
            if len(sql_res) > 0:
                labels = list(sql_res[0].keys())

        value_fields = query(chart_instance.details['sql']['table_spec']).where(
            lambda x: x.get('is_selected_for_operation', False)).to_list()

        datas = []
        for v in value_fields:
            data = [x[v['COLUMN_NAME']] for x in sql_res]
            dt = {
                'backgroundColor': gen_colors()[randint(0, 9)],
                'label': v.get('alias', 'مقدار'),
                'data': data
            }
            datas.append(dt)
        datas = {
            'datasets': datas,
            'labels': labels,
            'level': sql.get('level', 0),
            'max_level': sql.get('max_level', 0),
            'selected_label': sql.get('selected_label'),
            'selected_value': sql.get('selected_value'),
            'title': chart_instance.chartTitle,
            'description': chart_instance.details.get('description', ''),

        }

        """
        وقتی به هر دلیلی کش مراحل قبل پاک شده بود
        همه چیر باید از اول شروع بشه
        با توجه به اینکه این موضوع در ساخت اس کیو ال دیده شده
        در این قیمت هم کش لول صفر ساخته شود
        """

        current_level_cache_name = "%s-%s-%s" % (str(chart_instance.id), userid, sql['level'])
        current_level_cache_name_for_request = "%s-%s-%s-request" % (str(chart_instance.id), userid, sql['level'])

        cache.set(current_level_cache_name, datas, 360000)
        cache.set(current_level_cache_name_for_request, requestdata, 360000)
        return datas

    def get_top5(self, sql_res, chart_instance):
        res = query(chart_instance.details['sql']['table_spec']).where(
            lambda x: x.get('COLUMN_NAME') in sql_res[0].keys()).to_list()
        ddd = []
        for sr in sql_res:
            ppp = {}
            for k in sr.keys():
                vvv = query(res).where(lambda x: x['COLUMN_NAME'] == k).first_or_default({})
                if vvv.get('alias', '') != '':
                    ppp[vvv.get('alias', '')] = sr[k]
            ddd.append(ppp)
        return {'fields': query(res).select(lambda x: x.get('alias', x.get('COLUMN_NAME', ''))).to_list(),
                'data': ddd
                }

    def get_table(self, sql_res, chart_instance):
        res = query(chart_instance.details['sql']['table_spec']).where(
            lambda x: x.get('COLUMN_NAME') in sql_res[0].keys()).to_list()
        ddd = []
        for sr in sql_res:
            ppp = {}
            for k in sr.keys():
                vvv = query(res).where(lambda x: x['COLUMN_NAME'] == k).first_or_default({})
                if vvv.get('alias', '') != '':
                    ppp[vvv.get('alias', '')] = sr[k]
            ddd.append(ppp)
        return {'fields': query(res).select(lambda x: x.get('alias', x.get('COLUMN_NAME', ''))).to_list(),
                'data': ddd
                }

    def get_latestdatatable(self, chart_instance):
        datatable_instance = BISqls.objects.get(id=chart_instance.details.get('sql', {}).get('id')).datatable_id
        datatable_values_instance = DataTableValues.objects.filter(dataTableLink=datatable_instance.id).order_by(
            "-postDate").first()
        values = datatable_values_instance.values
        vv = []
        for v in values:
            ss = v.get('fieldname', '')
            val = v.get('value', '0')
            if v.get('dataType') == 'int':
                val = int(val)
            # if v.get('dataType') == 'date':
            #     val = datetime.fromordinal(int(val))
            ss = {
                'onvan': ss,
                'meghdar': val,
            }
            vv.append(ss)
        return vv

    @detail_route(methods=['POST'])
    def get_chart_with_request(self, request, *args, **kwargs):
        # previous_level_cache_name = "%s-%s-%s" % (kwargs['id'], request.user.id, request.data['level'] - 1)
        # previous_level_result = cache.get(previous_level_cache_name)

        chart_instance = self.queryset.get(id=kwargs['id'])

        if chart_instance.details.get('chart_type', '') in ['latestdatatable']:
            return Response(self.get_latestdatatable(chart_instance, ))
        if chart_instance.details.get('chart_type', False) == False:
            return Response({
                'chartID': kwargs['id'],
                'level': 0,
                'max_level': 0,
                'dataset_index': 0,
                'selected_value_index': 0,
                'user_id': request.user.id,
                'selected_label': [],
                'selected_value': [],
                'sql': '',

            })

        """
        لازم است اگر لول برای مراحل قبل بوده باشد
        جدول کش شود و از جدول کش شده اطلاعات
        مورد نیاز برای فیلتر نوشتن استفاده شود
        """
        sql = self.generate_charting_tsql(
            kwargs['id'],
            request.data.get('level', 0),
            request.data.get('dataset_index', 0),
            request.data.get('selected_value_index', 0),
            request.user.id,
            request.data.get('sort', None),

        )

        connection = Connections.objects.get(databaseName="RahkaranDB")
        connection = ConnectionsViewSet().getConnection(connection)
        connection.execute(sql['sql'])
        sql_res = connection.fetchall()
        sql_res = convert_sqlresultstr_to_valid_str(sql_res)
        sql_res = convert_sqlresultstr_to_valid_numbers(sql_res)

        if chart_instance.details.get('chart_type', False) == 'top5':
            return Response(self.get_top5(sql_res, chart_instance))

        if chart_instance.details.get('chart_type', False) == 'table':
            return Response(self.get_table(sql_res, chart_instance))

        if chart_instance.details.get('chart_type', False) == 'singlevalue':
            return Response(self.get_top5(sql_res, chart_instance))

        if chart_instance.details.get('chart_type', False) in ['line', 'bar']:
            return Response(self.get_chart(chart_instance, sql, sql_res, request.user.id, request.data))


