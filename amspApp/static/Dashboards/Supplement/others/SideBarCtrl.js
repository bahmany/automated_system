'use strict';

angular.module('Supplement').controller(
    'SideBarCtrl',
    function ($scope,
              $translate,
              $q,
              $http,
              $mdDialog,
              $location,
              $rootScope,
              $timeout) {

        // $scope.saleMali = 0;
        //
        // $scope.getCurrentSaleMali = function () {
        //     $http.get("/Financial/api/v1/tashbasehamk/getSaleMaliResponse/").then(function (data) {
        //         if (data.data.year) {
        //             $scope.saleMali = data.data.year;
        //         }
        //     })
        // };
        //
        //
        // $scope.setCurrentYear = function () {
        //     $http.post("/Financial/api/v1/tashbasehamk/setSaleMaliResponse/", {
        //         selectedYear: $scope.saleMali
        //     }).then(function (data) {
        //
        //     })
        // }

        // $scope.getCurrentSaleMali();
    });
