'use strict';
angular.module('AniTheme')
    .controller(
        'KhoroojCtrl',
        function ($scope, $window, $http, $translate, $rootScope, $stateParams, $location, $$$, $filter) {


            $scope.exists = {};
            $scope.searchStr = "";
            $scope.getExitList = function (page) {
                // $http.get("/api/v1/exits/getAggrList/?page="+page+"&search="+$scope.searchStr).then(function (data) {
                $http.get("/api/v1/hamkaranKhorooj/?page_size=20&page=" + page + "&search=" + $scope.searchStr).then(function (data) {
                    $scope.exists = data.data;
                })
            };

            $scope.gotopage = function (url) {
                $http.get(url).then(function (data) {
                    $scope.exists = data.data;
                })
            };






            // $http.get("/api/v1/exits/updateLatest50ChangesFromHamkaran/").then(function (data) {
            // });
            $scope.$watch("searchStr", function () {
                $scope.getExitList(1)
            })





        });



