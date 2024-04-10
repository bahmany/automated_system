'use strict';
angular.module('AniTheme')
    .controller(
        'HavalehForooshCtrl',
        function ($scope, $window, $mdMenu, $http, $translate, $rootScope, $stateParams, $location, $$$, $filter) {

            $scope.havales = {};
            $scope.firstData = {};
            $scope.loading_progress = false;

            $scope.showJustMySigns = false;
            $scope.dontShowModiramelWaitings = false;


            // $scope.$watch("showJustMySigns", function (data) {
            //     $scope.getHavalehForoosh(20, 1);
            // })


            $scope.getHavalehForoosh = function (page_size, page) {
                $scope.loading_progress = true;

                $http.get("/api/v1/havakehForoosh/getAggr/?page_size=" + page_size + "&page=" + page + "&search=" + $scope.searchStr).then(function (data) {
                    $scope.havales = data.data;
                    $scope.loading_progress = false;

                }).catch(function (data) {
                    $scope.loading_progress = false;
                })

                // if ($scope.showArchive.toString() === "true") {
                //
                //
                // } else {
                //     $http.get("/api/v1/havakehForoosh/getAggrForInbox/").then(function (data) {
                //         $scope.havales = data.data;
                //     })
                //
                // }

            };

            $scope.gotopage = function (url) {
                $scope.loading_progress = true;
                $http.get(url).then(function (data) {
                    $scope.havales = data.data;
                    $scope.loading_progress = false;

                }).catch(function (data) {
                    $scope.loading_progress = false;
                })
            }

            $scope.$watch("searchStr", function () {
                $scope.getHavalehForoosh(20, 1);
            });
            $scope.searchStr = "";


        });