'use strict';


angular.module('AniTheme').controller(
    'ControlProjectYearCtrl',
    function ($scope,
              $translate,
              $timeout,
              $http, $filter,
              $q, $mdDialog,
              $rootScope,
              $modal) {

        $scope.year = {};
        $scope.years = {};

        var url = "/api/v1/ControlProject/Year/";


        TableNav(
            $scope,
            $http,
            "years",
            url
            );
        $scope.Post = function () {
            if ($scope.year.id) {
                $http.patch(url + $scope.year.id + "/", $scope.year).then(function (data) {
                    if (data.data.id) {
                        $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                        $("#modal_add_new_year").modal("hide");
                    } else {
                        swal.showInputError("لطفا در ورود اطلاعات دقت نمایید");
                    }


                }).catch(function (data) {

                });

            } else {
                $http.post(url, $scope.year).then(function (data) {
                    if (data.data.id) {
                        $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                        $("#modal_add_new_year").modal("hide");
                    } else {
                        swal.showInputError("لطفا در ورود اطلاعات دقت نمایید");
                    }
                }).catch(function (data) {

                });

            }
        };
        $scope.Cancel = function () {
            $scope.year = {};
        };
        $scope.AddNewYear = function () {
            $scope.year = {};
            $("#modal_add_new_year").modal("show");
        };
        $scope.Edit = function (year) {
            $scope.year = year;
            $("#modal_add_new_year").modal("show");
        };
        $scope.Delete = function ($index, year) {
            swal({
                title: "حذف دوره",
                text: "آیا از حذف دوره انتخابی اطمینان دارید",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "بله",
                closeOnConfirm: false,
                showLoaderOnConfirm: true
            }, function () {
                $http.delete(url + year.id + "/").then(function (data) {
                    swal("حذف شد!", "دوره انتخابی حذف شد", "success");

                })
            });
        };
        $timeout(function () {
                        if (typeof($(".picker").datepicker) !== 'function'){
                return
            }
            $(".picker").datepicker({
                showOn: 'button',
                buttonImage: 'static/images/open-iconic-master/png/calendar-2x.png',
                buttonImageOnly: true,
                dateFormat: 'yy/mm/dd'
            });
        }, 0);

    }
);