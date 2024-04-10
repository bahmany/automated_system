'use strict';


angular.module('AniTheme').controller(
    'ChangeCrtl',
    function ($scope,
              $translate,
              $q,
              $http,
              $timeout,
              $rootScope, $$$,
              $mdToast,
              $modal) {

        $scope.password = {};
        $scope.signpassword = {};
        $scope.email = {};
        $scope.ChangePassword = function () {
            $http.post("/api/v1/settings/change/changepassword/", $scope.password).then(function (data) {
                // debugger;
                if (!(data.data.error == "")) {
                    $scope.password = {};
                    sweetAlert("تغییرات با موفقیت ثبت شد", "رمز ورود به سیستم شما تغییر کرد", "success");

                } else {
                    sweetAlert("خطا", "رمز عبور تغییر نکرد لطفا رمز دیگری را انتخاب نموده یا در ورود آن دقت نمایید", "error");

                }
            }).catch(function () {
                sweetAlert("خطا", "رمز عبور تغییر نکرد لطفا رمز دیگری را انتخاب نموده یا در ورود آن دقت نمایید", "error");
            })
        }

        $scope.ChangeEmail = function () {
            $http.post("/api/v1/settings/change/changeemail/", $scope.email).then(function (data) {
                if (!(data.data.error == "")) {
                    $scope.email = {};
                    sweetAlert("تغییرات ثبت شد", "ایمیل ثبت شده ی شما با موفقیت تغییر کرد", "success");
                } else {
                    sweetAlert("خطا", "ایمیل وارد شده فاقد اعتبار است لطفا ایمیل دیگری را انتخاب نمایید", "error");
                }
            }).catch(function () {
                sweetAlert("خطا", "ایمیل وارد شده فاقد اعتبار است لطفا ایمیل دیگری را انتخاب نمایید", "error");
            })
        }


        $scope.ChangeSignPassword = function () {
            $http.post("/api/v1/settings/change/changeSignPass/", $scope.signpassword).then(function (data) {
                if (data.data.ok) {
                    $scope.email = {};
                    sweetAlert("تغییرات ثبت شد", "همکنون کدی برای شما اس ام اس می شود", "success");
                } else {
                    sweetAlert("خطا", data.data.error, "error");
                }
            }).catch(function () {
                sweetAlert("خطا", "رمز شما ثبت نشد لطفا رمز را تغییر و در ورود آن دقت نمایید", "error");
            })
        }

        $scope.SubmitSMSPass = function () {
            $http.post("/api/v1/settings/change/changeSignVerifySMS/", $scope.signpassword).then(function (data) {
                if (!(data.data.error)) {
                    $scope.email = {};
                    sweetAlert("تغییرات ثبت شد", "رمز امضای شما تغییر کرد", "success");
                } else {
                    sweetAlert("خطا", data.data.error, "error");
                }
            }).catch(function () {
                sweetAlert("خطا", "رمز شما ثبت نشد لطفا رمز را تغییر و در ورود آن دقت نمایید", "error");
            })
        }


    });

