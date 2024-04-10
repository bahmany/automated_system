'use strict';
angular.module('AniTheme')
    .controller(
        'SalesProfileDetailsCtrl',
        function ($scope, $window, $http, $translate, $element, $rootScope, $stateParams, $location, $$$, $filter, $mdDialog) {

            $scope.profile = {};
            $scope.getProfile = function () {
                $http.get("/api/v1/salesProfile/" + $stateParams.profileID + "/").then(function (data) {
                    $scope.profile = data.data;
                });

            };
            $scope.getProfile();
// ---------------------------------------------------------
// ---------------------------------------------------------
// ---------------------------------------------------------
// ---------------------------------------------------------
// ---------------------------------------------------------
// ---------------------------------------------------------
// ---------------------------------------------------------
            $scope.profileSize = {};
            $scope.profileSizes = {};

            $scope.profileSizesList = function () {
                $http.get("/api/v1/salesProfileSizes/?profileID="+$stateParams.profileID, $scope.profileSize).then(function (data) {
                    $scope.profileSizes = data.data;
                })
            };

            $scope.profileSizesList();

            $scope.addProfileSize = function () {
                $scope.profileSize.profileLink = $stateParams.profileID;

                $http.post("/api/v1/salesProfileSizes/", $scope.profileSize).then(function (data) {
                    $scope.profileSizesList();
                })
            };

            $scope.back = function () {
                $state.go("SalesProfile");
            };
// ---------------------------------------------------------
// ---------------------------------------------------------
// ---------------------------------------------------------
// ---------------------------------------------------------
// ---------------------------------------------------------
// ---------------------------------------------------------


        });