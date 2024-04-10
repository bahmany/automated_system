'use strict';

angular.module('Supplement').controller(
    'navCtrl',
    function ($scope,
              $q,
              $http,
              $location, $state,
              $rootScope,
              $timeout) {


        // checking if authenticated


        $scope.logout = function () {
            $http.get('/api/v1/auth/logout/').then(function (data) {
                window.location.href = "/";
            });
        };


        $scope.gotoProfile = function () {
            $state.go("profile");
        }






    });