'use strict';

angular.module('AniTheme').controller(
    'CaToDavayereTolidiAfterCalcCtrl',
    function ($scope,
              //$translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {
        $scope.init = function () {
            $scope.getCalcCa();
        }


        $scope.calcList = {};
        // $scope.getCalcCa = function () {
        //     $http.get("/Financial/api/v1/ca_to_davayereh_tolidi/getCAAfterCalc/").then(function (data) {
        //         if (data.data.id) {
        //             $scope.calcList = data.data;
        //
        //         }
        //     })
        // }
        // $scope.getCalcCa = function () {
        //     $http.get("/Financial/api/v1/ca_to_davayereh_tolidi/getCAAfterCalc/").then(function (data) {
        //         if (data.data.id) {
        //             $scope.calcList = data.data;
        //
        //         }
        //     })
        // }

        $scope.init();

    })