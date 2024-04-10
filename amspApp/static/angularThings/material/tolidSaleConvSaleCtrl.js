'use strict';


angular.module('AniTheme').controller(
    'tolidSaleConvSaleCtrl',
    function ($scope,
              $translate,
              $http, $filter,
              $q, $mdDialog, $element,
              $rootScope, toastConfirm,
              $modal) {

        $scope.getlist = function () {
            $http.get("/api/v1/materialconvsale/").then(function (data) {
                $scope.list = data.data;
            })
        }


        $scope.goto = function (url) {
            $http.get(url).then(function (data) {
                $scope.list = data.data;
            })

        }


        $scope.init = function () {
            $scope.getlist();
        }

        $scope.init();
        $scope.addNewSaleConv = function () {

        }

    });