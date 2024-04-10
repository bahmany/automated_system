'use strict';

angular.module('RahsoonApp').controller(
    'homeCtrl',
    function ($scope,
              $translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {

        $scope.getProfileLevel = function () {
            $http.get("/api/v1/users/GetProfileLevel/").then(function (data) {
                $scope.level = data;
            })
        };
        $scope.getProfileLevel();
        // checking if authenticated

        $scope.checkIfLogin = function () {
            $http.get("/reg/api/v1/login/check_logined/").then(function (data) {
                if (data.data.is_active == false) {
                    $location.url("/login")
                }
            })
        };

        $scope.logout = function () {
            $http.get('/api/v1/auth/logout/').then(function (data) {
                window.location.href = "/";
            });

        };

        // $scope.checkIfLogin();


    });