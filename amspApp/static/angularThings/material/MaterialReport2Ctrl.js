'use strict';


angular.module('AniTheme').controller(
    'MaterialReport2Ctrl',
    function ($scope,
              $translate,
              $http,
              $filter,
              $q,
              $mdDialog,
              $element,
              $rootScope,
              $modal) {


        $scope.barcodes = [];
        $scope.filter = {};
        $scope.dates = {};
        $scope.listDates = function () {
            $http.post("/api/v1/barcodes/getdates_of_showreport2/", $scope.filter).then(function (data) {
                $scope.dates = data.data;
            })

        }


        $scope.init = function () {
            $scope.listDates();
            // $scope.list();
        }


        $scope.loadMore = function () {
            $scope.filter.limit = $scope.dates.limit;
            $scope.filter.skip = $scope.dates.limit + $scope.dates.skip;
            $http.post("/api/v1/barcodes/getdates_of_showreport2/", $scope.filter).then(function (data) {
                for (let i = 0; data.data.result.length > i; i++) {
                    $scope.dates.result.push(data.data.result[i]);
                }
                $scope.dates.limit = data.data.limit;
                $scope.dates.skip = data.data.skip;

            })


        }

        $scope.init();


        $scope.reportResult = [];
        $scope.currentRep = {};
        $scope.currentRepSums = 0;
        $scope.loadReport = function (dateOf) {
            $scope.currentRep = dateOf;
            $http.post("/api/v1/barcodes/showreport2/", {dateOf: dateOf}).then(function (data) {
                $scope.reportResult = data.data.result;
                $scope.currentRepSums = data.data.sums;
            })
        }


    });