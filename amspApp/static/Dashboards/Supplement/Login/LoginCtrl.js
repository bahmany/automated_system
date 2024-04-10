'use strict';

angular.module('Supplement').controller(
    'LoginCtrl',
    function ($scope,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {


        // checking if authenticated


        $scope.refreshCaptcha = function () {

            $http(
                {
                    method: 'GET',
                    url: '/captcha/refresh/',
                    headers: {'Content-Type': 'application/json'},
                    responseType: 'json'
                }
            ).then(function (data) {
                angular.element(document.querySelector('#id_captcha_0')).attr("value", data.data.key);
                angular.element(document.querySelector('.captcha')).attr("src", data.data.image_url);
            });
        }


        $scope.loginInf = {};
        $scope.loginErr = {};
        $scope.doLogin = function (e) {
            $scope.loginErr = {};
            e.preventDefault();
            var id_captcha_0 = angular.element(document.querySelector("#id_captcha_0")).val();
            var id_captcha_1 = angular.element(document.querySelector("#id_captcha_1")).val();
            $scope.loginInf.captcha_0 = id_captcha_0;
            $scope.loginInf.captcha_1 = id_captcha_1;

            $http.post("/api/v1/auth/login/", $scope.loginInf).then(function (data) {
                if (data.data.u === 1) {
                    window.location.href = "/";
                }
                if (data.data.u === 2) {
                    window.location.href = "/dashboards/";
                }
                if (data.data.u === 3) {
                    window.location.href = "/dashboards/";
                }
                if (data.data.u === 4) {
                    window.location.href = "/dashboards/";
                }
                if (data.data.u === 5) {
                    window.location.href = "/dashboards/";
                }
                if (data.data.u === 6) {
                    window.location.href = "/dashboards/";
                }
                if (data.data.u === 7) {
                    window.location.href = "/dashboards/";
                }
                if (data.data.u === 8) {
                    window.location.href = "/dashboards/";
                }
            }).catch(function (data) {
                $scope.loginErr = data.data;
                $scope.refreshCaptcha();
            })


        }


        angular.element(document.getElementById("id_captcha_1"))[0].value = "";
        // window.location.href = "/dashboards/";


    });