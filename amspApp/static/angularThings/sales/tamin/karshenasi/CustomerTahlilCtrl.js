'use strict';
angular.module('AniTheme')
    .controller(
        'CustomerTahlilCtrl',
        function ($scope, $window, $http, $translate, $rootScope, $stateParams, $location, $timeout, $filter, $mdDialog) {


                            $scope.customers = {};
            $scope.list = function (page, search, page_size) {
                $http.get("/api/v1/salesProfile/listMobs/?page=" + page.toString() + "&search=" + search + "&page_size=" + page_size.toString()).then(function (data) {
                    $scope.customers = data.data;
                })
            };


            $scope.profilesSearchText = "";
            $scope.$watch("profilesSearchText", function () {
                $scope.list(1, $scope.profilesSearchText, 20);
            });

            $scope.gotopage = function (url) {
                $http.get(url).then(function (data) {
                    $scope.customers = data.data;
                })

            }





                $scope.getCustomerTotalFinance = function () {

                }


        });

