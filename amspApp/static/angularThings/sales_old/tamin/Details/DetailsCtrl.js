'use strict';
angular.module('AniTheme')
    .controller(
        'TaminDetailsCtrl',
        function ($scope, $window, $http, $translate, $rootScope, $stateParams, $location, $$$, $filter) {

            $scope.detail = {};
            $scope.details = {};

            var url = "/api/v1/saleTaminProjectDetail/";

            $scope.post = function () {
                $http.post(url, $scope.detail).then(function (data) {

                })
            };


            $scope.details = {};

            $scope.list = function () {
                $http.get(url).then(function (data) {
                    $scope.details = data.data;
                })

            }
            $scope.list();


        });