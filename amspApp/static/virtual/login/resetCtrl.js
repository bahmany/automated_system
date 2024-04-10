'use strict';

angular.module('RahsoonApp').controller(
    'resetCtrl',
    function ($scope,
              $translate,
              $q,
              $http, $stateParams,
              $rootScope,
              $timeout) {


        //$scope.ForgetEmail = "";

        $scope.changepass = ChangePass;
        $scope.errors = [];
        $scope.NewPass = "";
        $scope.ConfirmNewPass = "";
        $scope.reset = {};

        $scope.refreshCaptcha = function () {
            $.getJSON('/captcha/refresh/', {}, function (json) {
                $("#id_captcha_0").attr("value", json.key);
                $(".captcha").attr("src", json.image_url);
            });
        };

        $scope.wait = false;
        $scope.thenSend = false;

        function ChangePass($event) {
            var defer = $q.defer();
            $scope.wait = true;

            $scope.reset.captcha_0 = $("#id_captcha_0")[0].value;
            $scope.reset.captcha_1 = $("#id_captcha_1")[0].value;
            $scope.reset.uid = $stateParams.uid;
            $($event.target).text("لطفا صبر کنید").attr("disabled", "true");
            var ccc = $http.post("/reg/api/v1/forgetpass/reset/", $scope.reset);
            ccc.then(function (data) {
                $($event.target).text("رمز عبور تغییر کرد").attr("disabled", "true");
                swal("رمز عبور", "رمز عبور شما با موفقیت تغییر کرد", "success");
        $scope.thenSend = true;

                return defer.resolve();
            });
            ccc.error(function (data) {
                $scope.wait = false;

                $($event.target).text("تغییر رمز عبور").attr("disabled", null);
                swal("خطا", data.message, "error");
                return defer.reject("");
            });
            return defer.promise;
        }

    });