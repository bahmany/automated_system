import itertools
from datetime import datetime

import six
from asq.initiators import query
from mongoengine import Q
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param

from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh, is_valid_shamsi_date, mil_to_sh_with_time, \
    sh_to_mil


class ListPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 50


class AllListPagination(PageNumberPagination):
    page_size = 300
    page_size_query_param = 'page_size'
    max_page_size = 50


class DetailsPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 50

    def generateLink(self, page_number):
        url = self.request.build_absolute_uri()
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)

    def get_paginated_response(self, data):
        count = []
        countFinal = []
        count = [i for i in range(self.page.number - 3, self.page.number + 3)]
        b = []

        for c in count:
            if c > 0 and c <= self.page.paginator.num_pages:
                b.append(c)

        count = b
        for i in self.page.paginator.page_range:
            for y in count:
                if y > 0:
                    if i == y:
                        countFinal.append({
                            "index": y,
                            "addr": self.generateLink(y)
                        })
        countFinal = [{"index": i, "addr": self.generateLink(i)} for i in count]
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            # 'page_range': self.page.paginator.page_range,
            'page_myrange': countFinal,
            'num_pages': self.page.paginator.num_pages,
            'first': self.generateLink(1),
            'last': self.generateLink(self.page.paginator.num_pages),
            'current_page': self.page.number,
            'per_page': self.page.paginator.per_page,
            'count': self.page.paginator.count,
            'results': data
        })


from django.core.paginator import InvalidPage, Paginator as DjangoPaginator


class DataTablesPagination(PageNumberPagination):
    # def __init__(self):
    # self.page_size =
    # pass

    page_size = 15
    page_size_query_param = 'iDisplayLength'
    max_page_size = 50

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        self._handle_backwards_compat(view)

        page_size = self.get_page_size(request)

        iDisplayStart = int(request.query_params.get("iDisplayStart", 0))
        iDisplayLength = int(request.query_params.get("iDisplayLength", 0))
        if iDisplayStart == 0 and iDisplayLength == 0:
            page_number = 1
        else:
            page_number = int(iDisplayStart / iDisplayLength) + 1

        if not page_size:
            return None

        paginator = DjangoPaginator(queryset, page_size)
        # page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=six.text_type(exc)
            )
            raise NotFound(msg)

        if paginator.count > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def generateLink(self, page_number):
        url = self.request.build_absolute_uri()
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)

    def get_paginated_response(self, data):
        count = []
        countFinal = []
        count = [i for i in range(self.page.number - 3, self.page.number + 3)]
        b = []

        for c in count:
            if c > 0 and c <= self.page.paginator.num_pages:
                b.append(c)

        count = b
        for i in self.page.paginator.page_range:
            for y in count:
                if y > 0:
                    if i == y:
                        countFinal.append({
                            "index": y,
                            "addr": self.generateLink(y)
                        })
        countFinal = [{"index": i, "addr": self.generateLink(i)} for i in count]
        sEcho = self.request.query_params.get("sEcho")
        if not sEcho:
            sEcho = '0'

        return Response({
            'iTotalRecords': self.page.paginator.object_list._collection.count(),
            'iTotalDisplayRecords': self.page.paginator.count,
            'aaData': data,
            'sEcho': sEcho
        })


"""
Parameter name	Type	Description
draw	integer	Draw counter. This is used by DataTables to ensure that the Ajax returns from server-side processing requests are drawn in sequence by DataTables (Ajax requests are asynchronous and thus can return out of sequence). This is used as part of the draw return parameter (see below).
start	integer	Paging first record indicator. This is the start point in the current data set (0 index based - i.e. 0 is the first record).
length	integer	Number of records that the table can display in the current draw. It is expected that the number of records returned will be equal to this number, unless the server has fewer records to return. Note that this can be -1 to indicate that all records should be returned (although that negates any benefits of server-side processing!)
search[value]	string	Global search value. To be applied to all columns which have searchable as true.
search[regex]	boolean	true if the global filter should be treated as a regular expression for advanced searching, false otherwise. Note that normally server-side processing scripts will not perform regular expression searching for performance reasons on large data sets, but it is technically possible and at the discretion of your script.
order[i][column]	integer	Column to which ordering should be applied. This is an index reference to the columns array of information that is also submitted to the server.
order[i][dir]	string	Ordering direction for this column. It will be asc or desc to indicate ascending ordering or descending ordering, respectively.
columns[i][data]	string	Column's data source, as defined by columns.data.
columns[i][name]	string	Column's name, as defined by columns.name.
columns[i][searchable]	boolean	Flag to indicate if this column is searchable (true) or not (false). This is controlled by columns.searchable.
columns[i][orderable]	boolean	Flag to indicate if this column is orderable (true) or not (false). This is controlled by columns.orderable.
columns[i][search][value]	string	Search value to apply to this specific column.
columns[i][search][regex]	boolean	Flag to indicate if the search term for this column should be treated as regular expression (true) or not (false). As with global search, normally server-side processing scripts will not perform regular expression searching for performance reasons on large data sets, but it is technically possible and at the discretion of your script.
"""


class ColsOfDatatable():
    cols = []
    pass


class DataTablesPaginationNewVersion(PageNumberPagination):
    pass


class DataTableForNewDatables_net(DataTablesPaginationNewVersion, ColsOfDatatable):
    page_size = 15
    max_page_size = 100
    params = []
    dtcols = None

    def paginate_queryset(self, queryset, request, view=None):
        self._handle_backwards_compat(view)
        # saleMali = CogBaseViewSet().getSaleMali(request.user.id)[0]

        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """

        """
        filtering and sorting 
        """
        # columns = query(request.query_params).where(lambda x:x[])
        self.params = request.query_params
        if len(request.data) > 2:
            self.params = request.data
        cols = query(self.params.keys()).where(lambda x: x[0:7] == "columns").select(
            lambda x: x[x.find("[") + 1:x.find("]")]).distinct().to_list()

        filtering = []
        for c in cols:
            f = {
                "name": self.params.get("columns[" + c + "][name]"),
                "data": self.params.get("columns[" + c + "][data]"),
                "searchable": self.params.get("columns[" + c + "][searchable]"),
                "orderable": self.params.get("columns[" + c + "][orderable]"),
                "search_value": self.params.get("columns[" + c + "][search][value]"),
                "search_regex": self.params.get("columns[" + c + "][search][regex]"),
            }

            filtering.append(f)
        totalSearchValue = self.params.get("search[value]")
        orderCol = self.params.get("order[0][column]")
        orderColDesc = self.params.get("order[0][dir]")

        if orderCol:
            if orderCol != "":
                if orderCol != "0":
                    asds = ""
                    if orderColDesc == "desc":
                        asds = "-"
                    queryset = queryset.order_by(
                        asds + self.params.get("columns[" + orderCol + "][data]").replace(".", "__"))

        qr = Q()

        for c in self.dtcols:
            for f in filtering:
                if c['data'] == f['data']:
                    f['type'] = c['type']
                a = 1

        if totalSearchValue:
            if totalSearchValue != "":
                for c in self.dtcols:
                    if c["type"] == "string":
                        qr |= Q(**{c["data"].replace(".", "__") + "__contains": totalSearchValue})
                    if c["type"] == "num-fmt" and totalSearchValue.isdigit():
                        qr |= Q(**{c["data"].replace(".", "__"): float(totalSearchValue)})

        for f in filtering:
            if f.get('search_value'):
                if f.get('search_value'):
                    if f.get('search_value') != '':
                        if f.get('search_value') != 'undefined':
                            if f["type"] == "string":
                                qr |= Q(**{f['data'].replace(".", "__") + "__contains": f['search_value']})
                            if f["type"] == "num-fmt" and f['search_value'].isdigit():
                                qr |= Q(**{f["data"].replace(".", "__"): float(f['search_value'])})

        queryset = queryset.filter(qr)

        start = int(self.params.get("start", '1'))
        length = int(self.params.get("length", '1'))

        if start == 0 and length == 0:
            page_number = 1
        else:
            if start == 1 and length == 1:
                page_number = 1
            else:
                page_number = int(start / length) + 1

        # if not page_size:
        #     return None

        paginator = DjangoPaginator(queryset, length)
        # page_number = self.params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=six.text_type(exc)
            )
            raise NotFound(msg)

        if paginator.count > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def generateLink(self, page_number):
        url = self.request.build_absolute_uri()
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)

    def get_paginated_response(self, data):
        count = []
        countFinal = []
        count = [i for i in range(self.page.number - 3, self.page.number + 3)]
        b = []

        for c in count:
            if c > 0 and c <= self.page.paginator.num_pages:
                b.append(c)

        count = b
        for i in self.page.paginator.page_range:
            for y in count:
                if y > 0:
                    if i == y:
                        countFinal.append({
                            "index": y,
                            "addr": self.generateLink(y)
                        })
        # countFinal = [{"index": i, "addr": self.generateLink(i)} for i in count]
        echo = self.params.get("echo")
        draw = int(self.params.get("draw", "1"))
        if not echo:
            echo = '0'

        currentPageSum = 0
        FilteredSum = 0
        AllSum = 0

        tt = 0
        for d in data:
            tt += 1
            d["DT_RowId"] = "row_" + str(tt)
            d["DT_RowData"] = {"pkey": d["id"]}

        return Response({
            'draw': draw,
            'recordsTotal': self.page.paginator.object_list._collection.count(),
            'recordsFiltered': self.page.paginator.count,
            'data': data,
            'echo': echo
        })


class DataTableForNewDatablesForAgg_post(DataTablesPaginationNewVersion, ColsOfDatatable):
    page_size = 15
    max_page_size = 100
    params = []
    dtcols = None

    def paginate_queryset(self, queryset, defaultAggr_project, request, view=None):

        # aggs_query = queryset.aggregate(defaultAggr_project, defaultAggr_sort)
        # self._handle_backwards_compat(view)
        # saleMali = CogBaseViewSet().getSaleMali(request.user.id)[0]

        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """

        """
        filtering and sorting 
        اول لینک می شود 
        بر اساس بار کد با مدل آیتم سفارشات
        
        """

        lookup = {'$lookup': {
            'from': "material_tolid_order_items",
            'localField': "_id",
            'foreignField': "linkBarcode",
            'as': "tolid"
        }}

        addfield = {"$addFields":
            {
                'sumOfTolid':
                    {
                        '$sum': '$tolid.mizaneMasraf'
                    },
                'baghimandeh':
                    {
                        '$subtract': ['$vazneKhales', {'$sum': '$tolid.mizaneMasraf'}]
                    }
            }
        }

        # columns = query(request.query_params).where(lambda x:x[])
        self.params = request.data
        # if len(request.data) > 2:
        #     self.params = request.data
        cols = query(self.params.keys()).where(lambda x: x[0:7] == "columns").select(
            lambda x: x[x.find("[") + 1:x.find("]")]).distinct().to_list()

        filtering = []
        for c in cols:
            f = {
                "name": self.params.get("columns[" + c + "][name]"),
                "data": self.params.get("columns[" + c + "][data]"),
                "searchable": self.params.get("columns[" + c + "][searchable]"),
                "orderable": self.params.get("columns[" + c + "][orderable]"),
                "search_value": self.params.get("columns[" + c + "][search][value]"),
                "search_regex": self.params.get("columns[" + c + "][search][regex]"),
            }

            filtering.append(f)
        totalSearchValue = self.params.get("search[value]")
        orderCol = self.params.get("order[0][column]")
        orderColDesc = self.params.get("order[0][dir]")

        sortFieldName = {"hoursInAnbar": 1}
        if orderCol:
            if orderCol != "":
                if orderCol != "0":
                    asds = 1
                    if orderColDesc == "desc":
                        asds = -1
                    # sortFieldName = asds + self.params.get("columns[" + orderCol + "][data]").replace(".", "__")

                    sortFieldName = {self.params.get("columns[" + orderCol + "][data]").replace(".", "__"): asds}

                    # queryset = queryset.order_by(
                    #     asds + self.params.get("columns[" + orderCol + "][data]").replace(".", "__"))

        qr = Q()

        for c in self.dtcols:
            for f in filtering:
                if c['data'] == f['data']:
                    f['type'] = c['type']
                a = 1

        if totalSearchValue:
            if totalSearchValue != "":
                for c in self.dtcols:
                    if c["type"] == "string":
                        qr |= Q(**{c["data"].replace(".", "__") + "__contains": totalSearchValue})
                    if c["type"] == "num-fmt" and totalSearchValue.isdigit():
                        qr |= Q(**{c["data"].replace(".", "__"): float(totalSearchValue)})

        match = []
        search = {}
        search['start_date'] = request.data['search[start_date]']
        search['end_date'] = request.data['search[end_date]']
        search['days_arrow'] = request.data['search[days_arrow]']
        search['day1'] = request.data['search[day1]']
        search['day2'] = request.data['search[day2]']
        search['correct'] = True if request.data['search[correct]'] == "true" else False
        search['scrap'] = True if request.data['search[scrap]'] == "true" else False
        search['scrap_and_store'] = True if request.data['search[scrap_and_store]'] == "true" else False

        iinn = []
        xxxx = []
        if search['correct']:
            xxxx.append({'position': 87976544})
        if search['scrap']:
            iinn.append(8845344)
        if search['scrap_and_store']:
            iinn.append(7463333)

        if len(iinn) > 0:
            xxxx.append({'$and': [
                {'position':
                    {
                        "$in": iinn
                    }
                },
                {
                    'desc.ready_to_tolid': True
                }
            ]})

        # xxxx.append({'confirmLocation':True})
        match.append({'$or': xxxx})

        for f in filtering:
            if f.get('search_value'):
                if f.get('search_value'):
                    if f.get('search_value') != '':
                        if f.get('search_value') != 'undefined':
                            if f["type"] == "string":
                                # qr |= Q(**{f['data'].replace(".", "__") + "__contains": f['search_value']})
                                match.append({f['data']: {'$regex': ".*" + f['search_value'] + ".*", "$options": "i"}})
                            if f["type"] == "num-fmt" and f['search_value'].isdigit():
                                match.append({f['data']: int(f['search_value'])})
                                # qr |= Q(**{f["data"].replace(".", "__"): float(f['search_value'])})

        # queryset = queryset.filter(qr)

        search['start_date'] = sh_to_mil(search['start_date']) if is_valid_shamsi_date(search['start_date']) else None
        search['end_date'] = sh_to_mil(search['end_date']) if is_valid_shamsi_date(search['end_date']) else None
        search['day1'] = int(search['day1']) if search['day1'].isdigit() else 0
        search['day2'] = int(search['day2']) if search['day2'].isdigit() else 0
        search['scrap'] = True if search['scrap'] == "true" else False
        search['scrap_and_store'] = True if search['scrap_and_store'] == "true" else False

        if search["start_date"] and search["end_date"] == None:
            gte = datetime.strptime(
                sh_to_mil(request.data['search[start_date]'] + " 00:00:01", has_time=True, ResultSplitter="/"),
                "%Y/%m/%d %H:%M:%S")
            lt = datetime.strptime(
                sh_to_mil(request.data['search[start_date]'] + " 23:59:59", has_time=True, ResultSplitter="/"),
                "%Y/%m/%d %H:%M:%S")
            match.append({
                "dateOfPost": {
                    "$gte": gte,
                    "$lt": lt,
                }
            })
        if search["start_date"] and search["end_date"]:
            gte = datetime.strptime(
                sh_to_mil(request.data['search[start_date]'] + " 00:00:01", has_time=True, ResultSplitter="/"),
                "%Y/%m/%d %H:%M:%S")
            lt = datetime.strptime(
                sh_to_mil(request.data['search[end_date]'] + " 23:59:59", has_time=True, ResultSplitter="/"),
                "%Y/%m/%d %H:%M:%S")
            match.append({
                "dateOfPost": {
                    "$gte": gte,
                    "$lte": lt,
                }
            })

        if search["days_arrow"] == "1" and search["day1"] != 0:
            match.append({
                "hoursInAnbar": {
                    "$gte": float(search["day1"]),
                    "$lte": float(search["day1"]) + 0.9,
                }
            })

        if search["days_arrow"] == "2" and search["day1"] != 0:
            match.append({
                "hoursInAnbar": {"$gte": float(search['day1'])}
            })

        if search["days_arrow"] == "3" and search["day1"] != 0:
            match.append({
                "hoursInAnbar": {"$lte": float(search['day1'])}
            })

        if search["days_arrow"] == "4" and search["day1"] != 0 and search["day2"] != 0:
            match.append({
                "hoursInAnbar": {
                    "$gte": float(search["day1"]),
                    "$lte": float(search["day2"]),
                }
            })

        # if search["scrap"] == True:
        #     match.append({
        #
        #     })

        start = int(self.params.get("start", '1'))
        length = int(self.params.get("length", '1'))

        facet = {
            "$facet": {
                "data": [
                    {"$sort": sortFieldName},
                    {"$skip": start},
                    {"$limit": length},

                ],
                "pageInfo": [
                    {"$group": {"_id": None, "coil_count": {"$sum": 1}, "vazn": {"$sum": '$baghimandeh'}}},
                ],
                "chart": [
                    {"$group": {"_id": "$zekhamat", "coil_count": {"$sum": 1}, "vazn": {"$sum": '$baghimandeh'}}},
                ],
                "chart66": [
                    {"$group": {"_id": "$zekhamat", "coil_count": {"$sum": 1}, "vazn": {"$sum": '$baghimandeh'}}},
                ],
                "chart65": [
                    {"$group": {"_id": "$zekhamat", "coil_count": {"$sum": 1}, "vazn": {"$sum": '$baghimandeh'}}},
                ],
            },
        }

        if len(match) > 0:
            facet['$facet']['data'].insert(0, {"$match": {"$and": match}})
            facet['$facet']['pageInfo'].insert(0, {"$match": {"$and": match}})
            facet['$facet']['chart'].insert(0, {"$match": {"$and": match}})

            match66 = match.copy()
            match65 = match.copy()
            match66.append({'noe': '66'})
            match65.append({'noe': '65'})
            facet['$facet']['chart66'].insert(0, {"$match": {"$and": match66}})
            facet['$facet']['chart65'].insert(0, {"$match": {"$and": match65}})
            # ppset = (*ppset, {"$match": {"$and": match}})

        ppset = (lookup, defaultAggr_project, addfield, facet,)

        qq = queryset.aggregate(*ppset)
        res = list(qq)
        res = res[0] if len(res) > 0 else {'data': []}
        res['darw'] = 1 + int(request.data.get('draw'))
        res['echo'] = request.data.get('echo', "0")
        res['recordsFiltered'] = res["pageInfo"][0]['coil_count'] if res.get('pageInfo') else 0
        res['recordsTotal'] = queryset.count()

        return res


class ListPaginationSmall(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class ListObjectPaging:
    def paginate(self, seq, page_size):
        i = iter(seq)
        while True:
            page = tuple(itertools.islice(i, 0, page_size))
            if len(page):
                yield page
            else:
                return


class PaginateRequest:
    def paginate(self, request):
        params = request.query_params
        page = params.get("page", 1)
        page_size = params.get("page_size", 20)
        next_page = params.get("page", 1) + 1
        prev_page = params.get("page", 1) - 1

        skip = (page - 1) * page_size
        limit = page_size
        return dict(
            page=page,
            page_size=page_size,
            next_page=next_page,
            prev_page=prev_page,
            skip=skip,
            limit=limit
        )
