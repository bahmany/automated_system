'use strict';


function zoneInbox($scope, $http) {


    var listZones = function (companyId, query) {
        return $http.get("/search/zones/members?cid=" + companyId + "&q=" + query)
    };

    var ZonesPageTo = function (SearchChartList, PagerUrl) {
        var qurl = PagerUrl + "&q=" + SearchChartList;

        if (qurl.split("?").length == 1) {
            qurl = qurl.replace("&", "?");
        }
        return $http.get(qurl);
    };


    $scope.zones = [];
    $scope.ZonesSearchText = "";
    $scope.getZonesList = function () {
        $scope.isSearchCallbackCompleted = false;
        listZones("0", $scope.ZonesSearchText).then(function (data) {
            $scope.zones = data.data;
            $scope.isSearchCallbackCompleted = true;
        }).catch(function (data) {
            $scope.isSearchCallbackCompleted = true;
        })
    };
    $scope.getZonesList();
    $scope.$watch("ZonesSearchText", function () {
        $scope.getZonesList();
    });
    $scope.addZoneToSelected = function (zone) {
        for (var i = 0; zone.membersInfo.length > i; i++) {
            $scope.addToSelected(zone.membersInfo[i])
        }

    };
    $scope.ZonesPageTo = function (PageUrl) {
        $scope.isSearchCallbackCompleted = false;
        ZonesPageTo($scope.ProfileSearch, PageUrl).then(function (data) {
            $scope.isSearchCallbackCompleted = true;
            $scope.SearchPersons = data.data;
        }).catch(function (data) {
            $scope.isSearchCallbackCompleted = true;
        });
    };
}