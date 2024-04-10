'use strict';

angular.module('Supplement').controller(
    'SecondRegistrationStepCtrl',
    function ($scope,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {


        $scope.hamkariType = {};

        $scope.sendSecondReg = function (e) {
            e.preventDefault();
            $http.post("/dashboards/api/v1/firstreg/updateSecondReg/", $scope.hamkariType).then(function (data) {
                location.href = "/dashboards/";
            })

        }


    }
);

