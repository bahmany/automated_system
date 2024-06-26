'use strict';

function chartInbox($scope, $http) {

//-----------------------------------service
    var listCharts = function (companyId, query) {
        return $http.get("/search/charts/members?cid=" + companyId + "&q=" + query)
    };
    var ChartsPageTo = function (SearchChartList, PagerUrl) {
        var qurl = PagerUrl + "&q=" + SearchChartList;
        if (qurl.split("?").length == 1) {
            qurl = qurl.replace("&", "?");
        }
        return $http.get(qurl);
    };
//-------------------------------------

    $scope.charts = [];
    $scope.ChartsSearchText = "";
    $scope.getChartsList = function () {
        $scope.isSearchCallbackCompleted = false;
        listCharts("0", $scope.ChartsSearchText).then(function (data) {
            $scope.charts = data.data;
            $scope.isSearchCallbackCompleted = true;
        }).catch(function (data) {
            $scope.isSearchCallbackCompleted = true;
        })
    };
    $scope.getChartsList();
    $scope.$watch("ChartsSearchText", function () {
        $scope.getChartsList();
    });
    $scope.addChartToSelected = function (chart) {
        for (var i = 0; chart.membersInfo.length > i; i++) {
            $scope.addToSelected(chart.membersInfo[i])
        }
    };
    $scope.ChartsPageTo = function (PageUrl) {
        $scope.isSearchCallbackCompleted = false;
        ChartsPageTo($scope.ProfileSearch, PageUrl).then(function (data) {
            $scope.isSearchCallbackCompleted = true;
            $scope.SearchPersons = data.data;
        }).catch(function (data) {
            $scope.isSearchCallbackCompleted = true;
        });
    };
}