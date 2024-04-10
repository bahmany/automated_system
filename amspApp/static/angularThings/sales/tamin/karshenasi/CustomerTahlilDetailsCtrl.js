'use strict';
angular.module('AniTheme')
    .controller(
        'CustomerTahlilDetailsCtrl',
        function ($scope, $window, $http, $translate, $rootScope, $stateParams, $location, $timeout, $filter, $mdDialog) {

            $scope.yearStart = 97;
            $scope.yearEnd = 97;
            $scope.AccSathe4 = {};
            $scope.customer = "";


            $scope.getTahlil = function () {
                $http.get("/api/v1/salesProfile/" + $stateParams.cusID + "/tahlilAccCus/?s=" + $scope.yearStart.toString() + "&e=" + $scope.yearEnd.toString()).then(function (data) {
                    $scope.AccSathe4 = data.data.AccSathe4;
                })
            };


            $scope.getCustomerProfile = function(){

            }

            $scope.getTahlil();


        });

