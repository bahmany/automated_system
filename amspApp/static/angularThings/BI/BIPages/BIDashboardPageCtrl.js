'use strict';


angular.module('AniTheme').controller(
    'BIDashboardPageCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope, $stateParams,
              $mdDialog,
              $location,
              $http) {


        $scope.dashboard_pages = [];
        $scope.dashboard_page = {};
        $scope.listDashboardPages = function () {
            $http.get('/api/v1/bi_dashboard_page/').then(function (data) {
                $scope.dashboard_pages = data.data;
            })
        }

        $scope.listDashboardPages();
        $scope.createDashboard = function () {
            swal({
                title: 'صفحه جدید',
                text: 'نام صفحه جدید را وارد نمایید',
                type: "input",
                inputValue: $scope.dashboard_page.title,
                showCancelButton: true,
                closeOnConfirm: false,
                animation: "slide-from-top",
                inputPlaceholder: 'نام صفحه'
            }, function (inputValue) {
                if (inputValue === false) return false;
                if (inputValue === "") {
                    swal.showInputError('نامی را وارد نمایید');
                    return false
                }
                $scope.dashboard_page.pageTitle = inputValue;
                $http.post("/api/v1/bi_dashboard_page/", $scope.dashboard_page).then(function (data) {
                    swal('پیام', 'با موفقیت ثبت شد', "success");
                    $scope.listDashboardPages();
                    // $scope.listGroup();
                }).catch(function (data) {
                    swal('خطا', 'نام گروه ثبت نشد بدلیل خطا', "error");
                });
            });
        }
        $scope.editDashboard = function (event, dashboard_page) {
            swal({
                title: 'تغییر نام',
                text: 'نام مورد نظر را وارد نمایید',
                type: "input",
                inputValue: dashboard_page.pageTitle,
                showCancelButton: true,
                closeOnConfirm: false,
                animation: "slide-from-top",
                inputPlaceholder: 'نام صفحه'
            }, function (inputValue) {
                if (inputValue === false) return false;
                if (inputValue === "") {
                    swal.showInputError('نامی را وارد نمایید');
                    return false
                }


                dashboard_page.pageTitle = inputValue
                $http.patch("/api/v1/bi_dashboard_page/" + dashboard_page.id + '/', dashboard_page).then(function (data) {
                    if (data.data.id) {
                        swal('پیام', 'با موفقیت ثبت شد', "success");
                        $scope.listDashboardPages();

                    } else {
                        swal('پیام', 'این نام قبلا استفاده شده است', "error");

                    }
                    // $scope.listGroup();
                }).catch(function (data) {
                    swal('خطا', 'نام گروه ثبت نشد بدلیل خطا', "error");
                });
            });
        }


        $scope.deleteDashboard = function (event, dashboard_page) {
            swal({
                title: 'حذف',
                text: 'آیا اطمینان دارید ؟',
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: 'بله حذف شود',
                showLoaderOnConfirm: true,
                closeOnConfirm: false
            }, function () {

                $http.delete("/api/v1/bi_dashboard_page/" + dashboard_page.id + "/").then(function (data) {
                    if (data.data.msg) {
                        swal('خطا', 'ابتدا اعضا را حذف نمایید', "error");
                        return

                    }
                    swal('حذف شد', 'با موفقیت حذف شد', "success");
                    $scope.listDashboardPages();

                });
            });
        };


    })