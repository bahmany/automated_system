'use strict';

angular.module('Supplement').controller(
    'ForgetRegCtrl',
    function ($scope,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {


        $scope.forget = {};

        $scope.waitingForSMS = false;

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
        };

        $scope.err = {};

        $scope.sendForget = function (e) {
            $scope.err = {};
            e.preventDefault();
            angular.element(document.querySelector("#btn-forgetpass")).disabled = true;
            angular.element(document.querySelector("#btn-forgetpass")).text = "درحال ارسال پیام کوتاه ...";
            $scope.hasError = false;
            $scope.firstRegErr = {};
            var id_captcha_0 = angular.element(document.querySelector("#id_captcha_0")).val();
            var id_captcha_1 = angular.element(document.querySelector("#id_captcha_1")).val();
            $scope.forget.captcha_0 = id_captcha_0;
            $scope.forget.captcha_1 = id_captcha_1;
            $http.post("/dashboards/api/v1/firstreg/sendForgetPassVerficationCode/", $scope.forget).then(function (data) {
                angular.element(document.querySelector("#btn-forgetpass")).text = "ارسال شد";
                $scope.verfCode.hash = data.data.data;
                $scope.waitingForSMS = true;
            }).catch(function (data) {
                if (data.data.result === "error") {
                    console.log("error found");
                    $scope.err = data.data;

                }
                angular.element(document.querySelector("#btn-forgetpass")).text = "ارسال کد پیگیری";
                angular.element(document.querySelector("#btn-forgetpass")).disabled = false;
                $scope.refreshCaptcha();
            });
        }


        $scope.verfCode = {};
        $scope.sendVerfForget = function (e) {
            e.preventDefault();
            $http.post("/dashboards/api/v1/firstreg/verifyForgetPassVerficationCode/", $scope.verfCode).then(function (data) {
                debugger;
                if (data.data.result === "ok") {
                    window.location.href = "/dashboards/";
                }
            }).catch(function (data) {

            });


        }
                angular.element(document.getElementById("id_captcha_1"))[0].value = "";

    }
)

