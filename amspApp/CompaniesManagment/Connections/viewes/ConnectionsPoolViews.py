from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from amspApp.CompaniesManagment.Connections.models import ConnectionPools
from amspApp.CompaniesManagment.Connections.serializers.ConnectionsSerializers import ConnectionPoolSerializer
from amspApp.CompaniesManagment.Connections.viewes.ConnectionsViews import ConnectionsViewSet
from amspApp.CompaniesManagment.permissions.CompanyPermissions import CanCruid
from amspApp.CompaniesManagment.permissions.PermissionChecker import get_permissions
from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh, mil_to_sh_with_time
from amspApp._Share.ListPagination import ListPagination


class ConnectionPoolsViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = ConnectionPools.objects.all()
    serializer_class = ConnectionPoolSerializer
    pagination_class = ListPagination
    permission_name = "Can_edit_connections"
    permission_classes = (CanCruid,)

    # def template_page(self, request, *args, **kwargs):
    #     return render_to_response("companyManagement/Connections/base.html", {},
    #                               context_instance=RequestContext(self.request))
    def get_permissions(self):
        return get_permissions(self, ConnectionPoolsViewSet)

    def filter_queryset(self, queryset):
        queryset = queryset.filter(companyID=int(self.kwargs['companyID_id']))
        queryset = queryset.filter(connection=self.kwargs['connectionID_id'])
        return super(ConnectionPoolsViewSet, self).filter_queryset(queryset)

    def list(self, request, *args, **kwargs):
        return super(ConnectionPoolsViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request.data["userID"] = request.user.id
        request.data["companyID"] = kwargs["companyID_id"]  # has security bug and must be correct later
        request.data["connection"] = kwargs["connectionID_id"]
        return super(ConnectionPoolsViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(ConnectionPoolsViewSet, self).destroy(request, *args, **kwargs)

    def convert_list_to_htmltable(self, cols, rows):
        # th
        th = ""
        td = ""
        for col in cols:
            th = th + "<th>" + col + "</th>"
        for row in rows:
            td += "<tr>"
            for r in row:
                td = td + "<td>" + str(r) + "</td>"
            td += "</tr>"

        return "<table class='table mini table-bordered table-striped'><thead>" + th + "</thead><tbody>" + td + "</tbody></table>"

    @list_route(methods=["post"])
    def runSql(self, request, *args, **kwargs):
        # if self:
        #     return Response({}) # disabled for sec porpose
        currentCompany = request.user.current_company
        sql = request.data["commands"]
        codeOf = request.data['connection']
        params = request.data['variables']
        # getting current connection prop
        connection = self.queryset.get(id=codeOf)
        # parsing sql command
        for p in params:
            value = p["value"] if "value" in p else ""
            if p["type"] != "int":
                value = "'" + str(value) + "'"
            if p["type"] == "int":
                sql = sql.replace("<:" + p["type"] + "__" + p["name"] + ":>", str(value))
            if p["type"] == "str":
                sql = sql.replace("<:" + p["type"] + "__" + p["name"] + ":>", str(value))
            if p["type"] == "date":
                sql = sql.replace("<:" + p["type"] + "__" + p["name"] + ":>", mil_to_sh(str(value), splitter="/"))
            if p["type"] == "datetime":
                sql = sql.replace("<:" + p["type"] + "__" + p["name"] + ":>",
                                  str(mil_to_sh_with_time(str(value), splitter="/")))
            if p["type"] == "time":
                sql = sql.replace("<:" + p["type"] + "__" + p["name"] + ":>", str(value))

        print(sql)
        connection = ConnectionsViewSet().getConnection(connection)
        connection.execute(sql)
        result = connection.fetchall()
        if len(result) > 0:
            resList = []
            cols = list(result[0].keys())
            for r in result:
                dd = []
                for c in cols:
                    dd.append(r[c])
                resList.append(dd)

            result = self.convert_list_to_htmltable(cols, resList)
            return HttpResponse(result)

    @list_route(methods=["post"])
    def test(self, request, *args, **kwargs):
        # if self:
        #     return Response({}) # disabled for sec porpose
        sqls = request.data["sqls"]
        for sql in sqls:
            parser = sql["code"].split("<:")
            controllers = []
            for s in parser:
                posIff = s.find(":>")
                if posIff > 0:
                    txt = s[0:posIff]
                    controllers.append({
                        "name": txt.split("__")[1],
                        "type": txt.split("__")[0]})
            sql["controllers"] = controllers
            request.data["sqls"] = sqls
        return Response(request.data)

    @list_route(methods=["post"])
    def runSql(self, request, *args, **kwargs):
        # if self:
        #     return Response({}) # disabled for sec porpose
        currentCompany = request.user.current_company
        sqls = request.data["sqls"]
        codeOf = request.data['connection']
        # params = request.data['variables']
        # getting current connection prop
        connection = ConnectionsViewSet().queryset.get(id=codeOf["id"])
        connection = ConnectionsViewSet().getConnection(connection)
        # parsing sql command
        results = []
        for s in sqls:
            sql = s["code"]
            for p in s["controllers"]:
                value = p["value"] if "value" in p else ""
                if p["type"] != "int":
                    value = "'" + str(value) + "'"
                if p["type"] == "int":
                    sql = sql.replace("<:" + p["type"] + "__" + p["name"] + ":>", str(value))
                if p["type"] == "str":
                    sql = sql.replace("<:" + p["type"] + "__" + p["name"] + ":>", str(value))
                if p["type"] == "date":
                    sql = sql.replace("<:" + p["type"] + "__" + p["name"] + ":>", mil_to_sh(str(value), splitter="/"))
                if p["type"] == "datetime":
                    sql = sql.replace("<:" + p["type"] + "__" + p["name"] + ":>",
                                      str(mil_to_sh_with_time(str(value), splitter="/")))
                if p["type"] == "time":
                    sql = sql.replace("<:" + p["type"] + "__" + p["name"] + ":>", str(value))
            connection.execute(sql)
            sql_res = connection.fetchall()
            tbl = ""
            if len(sql_res) > 0:
                resList = []
                cols = list(sql_res[0].keys())
                for r in sql_res:
                    dd = []
                    for c in cols:
                        dd.append(r[c])
                    resList.append(dd)
                tbl = self.convert_list_to_htmltable(cols, resList)

            results.append({
                "name": s["name"],
                "result": tbl
            })
        return Response(results)

    def runCode(self, connection, pool, value):
        # if self:
        #     return Response({}) # disabled for sec porpose
        pool = self.serializer_class(instance=pool).data
        connection = ConnectionsViewSet().getConnection(connection)
        sqls = pool["sqls"]
        results = {}
        result = {}

        # generating header
        def makeItForTable(result):
            r = result
            lst = []
            lst = r.get("results")
            if lst:
                r["cols"] = lst[0].keys()
            return r

        def generate_sqls():
            for s in sqls:
                sql = s.get("code")
                if s.get("controllers") == None:
                    s["controllers"] = []
                for p in s.get("controllers"):
                    value = p["value"] if "value" in p else ""
                    if p["type"] != "int":
                        value = "'" + str(value) + "'"
                    if p["type"] == "int":
                        sql = sql.replace("<:" + p["type"] + "__" + p["name"] + ":>", str(value))
                    if p["type"] == "str":
                        sql = sql.replace("<:" + p["type"] + "__" + p["name"] + ":>", str(value))
                    if p["type"] == "date":
                        sql = sql.replace("<:" + p["type"] + "__" + p["name"] + ":>",
                                          mil_to_sh(str(value), splitter="/"))
                    if p["type"] == "datetime":
                        sql = sql.replace("<:" + p["type"] + "__" + p["name"] + ":>",
                                          str(mil_to_sh_with_time(str(value), splitter="/")))
                    if p["type"] == "time":
                        sql = sql.replace("<:" + p["type"] + "__" + p["name"] + ":>", str(value))
                # connection.execute(sql)
                # sql_res = connection.fetchall()
                results[s["name"]] = sql

        # generate_sqls()
        exec(pool['pythonCode'])
        return result

    @list_route(methods=["post"])
    def run(self, connection, pool, values):
        # if self:
        #     return Response({}) # disabled for sec porpose
        pool = self.serializer_class(instance=pool).data
        connection = ConnectionsViewSet().getConnection(connection)
        sqls = pool["sqls"]
        results = {}
        result = {}

        # generating header
        def makeItForTable(result):
            r = result
            lst = []
            lst = r.get("results")
            if lst:
                r["cols"] = lst[0].keys()
            return r

        def generate_sqls():
            for s in sqls:
                sql = s.get("code")
                if s.get("controllers") == None:
                    s["controllers"] = []
                for p in s.get("controllers"):
                    # value = p["value"] if "value" in p else ""
                    # if p["type"] != "int":
                    #     value = "'" + str(values) + "'"
                    if p["type"] == "int":
                        sql = sql.replace("<:" + p["type"] + "__" + p["name"] + ":>", str(values[p["name"]]))
                    if p["type"] == "str":
                        sql = sql.replace("<:" + p["type"] + "__" + p["name"] + ":>", str(values[p["name"]]))
                    if p["type"] == "date":
                        sql = sql.replace("<:" + p["type"] + "__" + p["name"] + ":>",
                                          mil_to_sh(str(values[p["name"]]), splitter="/"))
                    if p["type"] == "datetime":
                        sql = sql.replace("<:" + p["type"] + "__" + p["name"] + ":>",
                                          str(mil_to_sh_with_time(str(values[p["name"]]), splitter="/")))
                    if p["type"] == "time":
                        sql = sql.replace("<:" + p["type"] + "__" + p["name"] + ":>", str(values[p["name"]]))
                # connection.execute(sql)
                # sql_res = connection.fetchall()
                results[s["name"]] = sql

        # generate_sqls()
        try:
            # generate_sqls()
            # connection.execute(results["Person"])
            # person = connection.fetchall()
            # result["results"] = person
            # connection.execute(results["PersonCount"])
            # personCount = connection.fetchall()
            # result["count"] = personCount[0]["countOf"]
            # result = makeItForTable(result)
            exec(pool['pythonCode'])
        except Exception as ee:
            return {"error": ee}


        return result
