'use strict';

angular.module('Supplement').controller(
    'FirstRegCtrl',
    function ($scope,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {

        $scope.reg = {};
        $scope.showHints = true;

        $scope.result = {};
        $scope.post = function (e) {
            e.preventDefault();
            $scope.hasError = false;
            $scope.firstRegErr = {};
            var id_captcha_0 = angular.element(document.querySelector("#id_captcha_0")).val();
            var id_captcha_1 = angular.element(document.querySelector("#id_captcha_1")).val();
            $scope.reg.captcha_0 = id_captcha_0;
            $scope.reg.captcha_1 = id_captcha_1;

            $http.post("/dashboards/api/v1/firstreg/regWithCell/", $scope.reg).then(function (data) {
                if (data.data.result === "error") {
                    $scope.refreshCaptcha();

                }

                if (data.data.result === "ok") {
                    // angular.element(document.querySelector("#contentReg")).fadeOut();
                    // angular.element(document.querySelector("#contentVerf")).fadeIn();
                    $scope.result = data.data;
                }
            }).catch(function (data) {
                $scope.refreshCaptcha();
                $scope.hasError = true;
                $scope.firstRegErr = data.data;

            });


        }


        $scope.postVerf = function (e) {
            e.preventDefault();
            $http.post("/dashboards/api/v1/firstreg/verfCode/", $scope.result).then(function (data) {
                if (data.data.result === "error") {
                    // $scope.refreshCaptcha();

                }

                if (data.data.result === "ok") {
                    // angular.element(document.querySelector("#contentReg")).fadeOut();
                    // angular.element(document.querySelector("#contentVerf")).fadeIn();
                    // $scope.result = data.data;
                    window.location.href = "/dashboards/";

                }
            }).catch(function (data) {
                // $scope.refreshCaptcha();

            });
        }


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
        $timeout(function () {
        angular.element(document.getElementById("id_captcha_1"))[0].value = "";

        }, 500)

    }
)

