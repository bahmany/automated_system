'use strict';


function TableNav(scope, http, listModelStr, listURL) {

    // defining table fileters and pagination prop
    var tableFilterModelName = listModelStr + "TablePropStr";
    var tableFilterStr = listModelStr + "TableFilterStr";

    scope[tableFilterModelName] = {};
    scope[tableFilterModelName].pagination = {};
    scope[tableFilterModelName].pagination.size = 10;
    scope[tableFilterModelName].pagination.total = 0;
    scope[tableFilterModelName].isShow = false;
    scope[tableFilterModelName].currentPage = 1;
    scope[tableFilterStr] = "";

    scope[listModelStr + "TablePagination"] = function () {
        if (scope[tableFilterModelName].pagination.size == 40) {
            scope[tableFilterModelName].pagination.size = 5;
        }
        scope[tableFilterModelName].pagination.size = scope[tableFilterModelName].pagination.size + 5;
        scope[listModelStr + "List"]();
    };
    scope[listModelStr + "PageTo"] = function (url) {
        http.get(url).then(function (data) {
            scope[listModelStr] = data.data;

        })
    };
    scope[listModelStr + "List"] = function () {
        scope.waitForLoading = true;
        return http.get(listURL + "?search=" + scope[tableFilterStr] + "&ordering=" + scope[listModelStr + "OrderingStr"] + "&page_size=" + scope[tableFilterModelName].pagination.size).then(function (data) {
            scope[listModelStr] = data.data;
            scope.waitForLoading = false;

        }).catch(function (data) {
            scope.waitForLoading = false;

        })
    };
    scope[listModelStr + "OrderedList"] = [];
    scope[listModelStr + "ChangeOrdering"] = function (fieldName) {
        var found = false;
        var ordered = scope[listModelStr + "OrderedList"];
        var posType = 0; // 0=unsort  1=asc  2=desc
        var spliceIndex = -1;
        for (var i = 0; ordered.length > i; i++) {
            if (ordered[i].fieldName == fieldName) {
                found = true;
                ordered[i].value += ordered[i].value;
                if (ordered[i].value > 2) {
                    ordered[i].value = 0;
                    spliceIndex = i;
                }
            }
        }
        if (spliceIndex != -1) {
            ordered.splice(spliceIndex, 1);
        }

        if (!found) {
            ordered.push(
                {
                    fieldName: fieldName,
                    value: 1
                }
            )
        }

        var sortStr = "";
        for (var i = 0; ordered.length > i; i++) {
            var spliter = "";
            if (sortStr != "") {
                spliter = ","
            }
            if (ordered[i].value == 2) {
                sortStr = sortStr + spliter + "-" + ordered[i].fieldName;
            }
            if (ordered[i].value == 1) {
                sortStr = sortStr + spliter + ordered[i].fieldName;
            }

        }

        scope[listModelStr + "OrderingStr"] = sortStr;
        scope[listModelStr + "OrderedList"] = ordered;

    }
    scope.$watch(tableFilterStr, function () {
        scope[listModelStr + "List"]();
    });
    scope.$watch(listModelStr + "OrderingStr", function () {
            scope[listModelStr + "List"]();
        }
    );

}