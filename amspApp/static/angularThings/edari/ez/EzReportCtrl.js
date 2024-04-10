'use strict';


angular.module('AniTheme').controller(
    'EzReportCtrl',
    function ($scope,
              $translate, $stateParams,
              $q, $http, $state,
              $rootScope,
              $modal) {


        $scope.ezs = {}
        $scope.list = function () {
            $http.get("/api/v1/ez/get_report/").then(function (data) {
                $scope.ezs = data.data;
            })
        }


        $scope.init = function () {
            $scope.list();
        }
        $scope.init();

    })