'use strict';


angular.module('AniTheme').controller(
    'BIChartsCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope, $stateParams,
              $mdDialog,
              $location,
              $http) {


        $scope.charts = [];
        $scope.chart = {};
        $scope.listCharts = function () {
            $http.get('/api/v1/bi_chart/').then(function (data) {
                $scope.charts = data.data;
            })
        }

        $scope.listCharts();
        $scope.createChart = function () {
            swal({
                title: 'چارت جدید',
                text: 'نام صفحه جدید را وارد نمایید',
                type: "input",
                inputValue: '',
                showCancelButton: true,
                closeOnConfirm: false,
                animation: "slide-from-top",
                inputPlaceholder: 'نام چارت'
            }, function (inputValue) {
                if (inputValue === false) return false;
                if (inputValue === "") {
                    swal.showInputError('نامی را وارد نمایید');
                    return false
                }
                $scope.chart.chartTitle = inputValue;
                $http.post("/api/v1/bi_chart/", $scope.chart).then(function (data) {
                    if (data.data.id) {
                        swal('پیام', 'با موفقیت ثبت شد', "success");
                        $scope.listCharts();
                    } else {
                        swal('پیام', 'این نام قبلا استفاده شده است', "error");
                    }
                    // $scope.listGroup();
                }).catch(function (data) {
                    swal('خطا', 'نام چارت ثبت نشد بدلیل خطا', "error");
                });
            });
        }
        $scope.editChart = function (event, chart) {
            swal({
                title: 'تغییر نام',
                text: 'نام مورد نظر را وارد نمایید',
                type: "input",
                inputValue: chart.chartTitle,
                showCancelButton: true,
                closeOnConfirm: false,
                animation: "slide-from-top",
                inputPlaceholder: 'نام چارت'
            }, function (inputValue) {
                if (inputValue === false) return false;
                if (inputValue === "") {
                    swal.showInputError('نامی را وارد نمایید');
                    return false
                }


                chart.chartTitle = inputValue
                $http.patch("/api/v1/bi_chart/" + chart.id + '/', chart).then(function (data) {
                    if (data.data.id) {
                        swal('پیام', 'با موفقیت ثبت شد', "success");
                        $scope.listCharts();

                    } else {
                        swal('پیام', 'این نام قبلا استفاده شده است', "error");

                    }
                    // $scope.listGroup();
                }).catch(function (data) {
                    swal('خطا', 'نام چارت ثبت نشد بدلیل خطا', "error");
                });
            });
        }
        $scope.dupChart = function (event, chart) {
            swal({
                title: 'نام جدید',
                text: 'نام مورد نظر را وارد نمایید',
                type: "input",
                inputValue: chart.chartTitle,
                showCancelButton: true,
                closeOnConfirm: false,
                animation: "slide-from-top",
                inputPlaceholder: 'نام چارت'
            }, function (inputValue) {
                if (inputValue === false) return false;
                if (inputValue === "") {
                    swal.showInputError('نامی را وارد نمایید');
                    return false
                }


                chart.chartTitle = inputValue
                $http.post("/api/v1/bi_chart/" + chart.id + '/duplicate_chart/', chart).then(function (data) {
                    if (data.data.id) {
                        swal('پیام', 'با موفقیت ایجاد شد', "success");
                        $scope.listCharts();

                    } else {
                        swal('پیام', 'این نام قبلا استفاده شده است', "error");

                    }
                    // $scope.listGroup();
                }).catch(function (data) {
                    swal('خطا', 'نام چارت ثبت نشد بدلیل خطا', "error");
                });
            });
        }


        $scope.deleteChart = function (event, chart) {
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

                $http.delete("/api/v1/bi_chart/" + chart.id + "/").then(function (data) {
                    if (data.data.msg) {
                        swal('خطا', 'ابتدا اعضا را حذف نمایید', "error");
                        return

                    }
                    swal('حذف شد', 'با موفقیت حذف شد', "success");
                    $scope.listCharts();

                });
            });
        };


    })