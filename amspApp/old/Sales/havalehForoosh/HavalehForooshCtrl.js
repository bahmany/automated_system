'use strict';
angular.module('AniTheme')
    .controller(
        'HavalehForooshCtrl',
        function ($scope, $window, $mdMenu, $http, $translate, $rootScope, $stateParams, $location, $$$, $filter) {

            $scope.havales = {};
            $scope.firstData = {};

            $scope.showArchive = false;


            $scope.$watch("showArchive", function (data) {
                $scope.getHavalehForoosh(20, 1);
            })


            $scope.getHavalehForoosh = function (page_size, page) {

                if ($scope.showArchive.toString() === "true") {

                    $http.get("/api/v1/havakehForoosh/getAggr/?page_size=" + page_size + "&page=" + page + "&search=" + $scope.searchStr + "&archive=" + $scope.showArchive.toString()).then(function (data) {
                        $scope.havales = data.data;
                    })
                } else {
                    $http.get("/api/v1/havakehForoosh/getAggrForInbox/").then(function (data) {
                        $scope.havales = data.data;
                    })

                }

            };

            $scope.gotopage = function (url) {
                $http.get(url).then(function (data) {
                    $scope.havales = data.data;
                })
            }

            $scope.$watch("searchStr", function () {
                $scope.getHavalehForoosh(20, 1);
            });
            $scope.searchStr = "";


        });