'use strict';

angular.module('AniTheme').controller(
    'cogReportCtrl',
    function ($scope,
              //$translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {


        $scope.mainReport = [];
        $scope.calc = function () {
            $http.get("/Financial/api/v1/report/get_cal/").then(function (data) {
                $scope.get_report();
                // $scope.mainReport = data.data;
            })
        }

        $scope.saveIt = function () {
            $http.post("/Financial/api/v1/report/save_cal/", $scope.mainReport).then(function (data) {
                // $scope.mainReport = data.data;
            })
        }


        $scope.get_report = function () {
            $http.get('/Financial/api/v1/report/get_report/').then(function (data) {
                $scope.mainReport = data.data;
                $scope.getSaleMaliResponse();
            })
        }

        $scope.getSaleMaliResponse = function(){
            $http.get("/Financial/api/v1/cogb/getSaleMaliResponse/").then(function (data) {
                $scope.currentSaleMali = data.data.year;
            })
        }

        $scope.get_report();


    });
