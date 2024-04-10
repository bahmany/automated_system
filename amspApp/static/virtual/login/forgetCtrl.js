'use strict';

angular.module('RahsoonApp').controller(
    'forgetCtrl',
    function ($scope,
              $translate,
              $q,
              $http, $stateParams,
              $rootScope,
              $timeout) {



        $scope.forgetpass = ForgetPass;
        $scope.errors = [];
        $scope.forget = {};

        $scope.refreshCaptcha = function () {
            $.getJSON('/captcha/refresh/', {}, function (json) {
                //$scope.imgCaptcha = json.image_url;
                $("#id_captcha_0").attr("value", json.key);
                $(".captcha").attr("src", json.image_url);
                //$scope.$apply();
            });
        };

        $scope.wait = false;
        $scope.thenSend = false;
        function ForgetPass($event) {
            $scope.wait = true;

            var defer = $q.defer();
            var ccc = $http.post("/reg/api/v1/forgetpass/", {
                name: $scope.forget.name,
                captcha_0: $("#id_captcha_0")[0].value,
                captcha_1: $("#id_captcha_1")[0].value
            });
            ccc.then(function (data) {
                swal("ارسال شد", "لطفا ایمیل خود را کنترل کنید", "success");
                $scope.thenSend = true;
            $scope.wait = false;
                return defer.resolve();
            });
            ccc.error(function (data) {
                swal("خطا", "ایمیل یا نام کاربری مورد نظر یافت نشد و یا در ورود اطلاعات دقت کنید", "error");

                            $scope.wait = false;

                return defer.reject("");
            });
            return defer.promise;
        }


    });