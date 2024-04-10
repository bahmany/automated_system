'use strict';

angular.module('RahsoonApp').controller(
    'regCtrl',
    function ($scope,
              $translate,
              $q, $location,
              $http,
              $rootScope,
              $timeout) {


        $scope.imgCaptcha = "";
        $scope.refreshCaptcha = function () {
            $.getJSON('/captcha/refresh/', {}, function (json) {
                $("#id_captcha2_0").attr("value", json.key);
                $(".captcha").attr("src", json.image_url);
            });
        };
        $scope.errors = {};
        $scope.register = {};


        $scope.doRegister = function () {
            $("#btn_submit").html('لطفا صبر کنید');
            $("#btn_submit").prop('disabled', true);
            $scope.register.captcha2_0 = angular.element("#id_captcha2_0").val();
            $scope.register.captcha2_1 = angular.element("#id_captcha2_1").val();
            $scope.register.captcha2 = angular.element("#id_captcha2_1").val();

            $http.post("/reg/api/v1/login/register/", $scope.register).then(function (data) {
                if ((data.message)) {
                    $scope.errors = {};
                    $scope.errors = data.data;
                    $scope.refreshCaptcha();
                } else {
                    $location.url("/reg/home");
                }
            }).catch(function(data){
                    $scope.errors = {};
                    $scope.errors = data;
                    $scope.refreshCaptcha();
            })


        }

    });