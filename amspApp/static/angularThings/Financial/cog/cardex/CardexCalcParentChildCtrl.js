'use strict';

angular.module('AniTheme').controller(
    'CardexCalcParentChildCtrl',
    function ($scope,
              //$translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {

        $scope.GetCardexCalcFromHamkaran = function () {
            $http.get("/Financial/api/v1/cardexcalchamk/getFromHakaranCalc/").then(function (data) {

            })
        }


    });