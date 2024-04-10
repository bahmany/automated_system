'use strict';

angular.module('RahsoonApp').controller(
    'loginCtrl',
    function ($scope,
              $translate,
              $q, $location,
              $http,
              $rootScope,
              $timeout) {

        $scope.loginInf = {};
        $scope.errors = {};

        $scope.imgCaptcha = "";
        $scope.refreshCaptcha = function () {
            $.getJSON('/captcha/refresh/', {}, function (json) {
                //$scope.imgCaptcha = json.image_url;
                $("#id_captcha_0").attr("value", json.key);
                $(".captcha").attr("src", json.image_url);
                //$scope.$apply();
            });
        };
        $scope.doLogin = function () {
            $.ajax({
                type: "POST",
                url: "/reg/api/v1/login/login/",
                data: $("#frmLogin").serialize(),
                success: function (data) {
                    if (data.form_errors) {
                        $scope.errors = data.form_errors;
                        $("#id_captcha_0").attr("value", data.new_cptch_key);
                        $(".captcha").attr("src", data.new_cptch_image);
                        $("#id_captcha_1").val("");
                        $scope.$apply();
                        return
                    }
                    console.log("login seucc");
                    window.location.href = "/reg/";
                    // $location.url("/home/profile/introduction");
                    // $scope.$apply();
                    return
                },
                error: function (data) {
                    $scope.refreshCaptcha();
                    $("#id_captcha_1").val("");
                    $scope.$apply();

                }
            })
        };
        $scope.Register = function () {
            $location.url("/register");
        }


    });