'use strict';
angular
    .module('login', [])
    .config(function ($interpolateProvider, $httpProvider) {
        $interpolateProvider.startSymbol('//');
        $interpolateProvider.endSymbol('//');
        $httpProvider.defaults.timeout = 1;
        $httpProvider.defaults.xsrfCookieName = 'rahsoon-CSRF-TOKEN';
        $httpProvider.defaults.xsrfHeaderName = 'rahsoon-csrftoken';
    })
    .controller('LoginCtrl', function ($scope, $timeout, $q, $rootScope, $http) {


        $scope.login = {};


        $scope.forgetPassPanel = function () {

            $(".login-form").fadeOut(function () {
                $(".forget-pass").fadeIn();
            })
        };
        $scope.backReg = function () {
            $(".forget-pass").fadeOut(function () {
                $(".login-form").fadeIn();
            })
        }

        $scope.login = function () {
            $http.post('/api/v1/auth/login/', {
                username: $scope.login.username,
                password: $scope.login.password,
                remember: $scope.login.remember
            }).then(function (data) {
                window.location = "/";
                // window.location.reload();
            }).catch(function (data) {
                $(".invalid").fadeIn();
            });
        }



    });