'use strict';


angular.module('AniTheme').controller(
    'FirstIntroCtrl',
    function ($scope,
              $translate,$state,$timeout,
              $http, $window, $location,
              $q, $mdDialog,
              $rootScope,
              $modal) {


        $scope.pic = {};
        $scope.inf = {};
        $scope.isUploading = false;

        $scope.picChanged = false;

        $scope.$watch("isUploading", function () {
            if ($scope.isUploading) {
                $scope.picChanged = true;
            }
        });


        var url = "/api/v1/profile/";

        $scope.publicEditorOptions = publicEditorOptions;


        $scope.saveCompanyNameAndExp = function () {
            if (!($scope.inf.name) || !($scope.inf.intro)) {
                swal("خطا", "لطفا اطلاعات خواسته شده را تکمیل نمایید", "error");
                return
            }
            if ($scope.inf.name == "" || $scope.inf.intro == "") {
                swal("خطا", "لطفا اطلاعات خواسته شده را تکمیل نمایید", "error");
                return
            }
            $http.post(url + "UpdateCompNameAndU/", $scope.inf).then(function (data) {
                $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                $timeout(function () {
                    $state.go("selectpics");
                }, 1000);
            })
        }

        $scope.nextAndSave = function () {
            if (!($scope.pic.avatar) || !($scope.pic.companyLogo)) {
                swal("خطا", "لطفا عکسی را آپلود نمایید", "error");
                return
            }
            if ($scope.pic.avatar == "" || $scope.pic.companyLogo == "") {
                swal("خطا", "لطفا عکسی را آپلود نمایید", "error");
                return
            }

            $http.post(url + "UpdateProfilePicAndCompanyPic/", $scope.pic).then(function (data) {
                $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                $timeout(function () {
                    $state.go("welcomeDone");
                }, 1000);
            })




            // updating profile pic and company profile pic


        }

        $scope.Finish = function () {
            $http.post(url + "FinishWelcome/", {}).then(function (data) {
                $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                $timeout(function () {
                    $state.go("dashboard");
                }, 1000);
            });


        }


    });