'use strict';


angular.module('AniTheme').controller(
    'ControlProjectIncomeTypesCtrl',
    function ($scope,
              $translate,
              $http,
              $q, $mdDialog,
              $rootScope,
              $modal) {
        $scope.incomeType = {};
        $scope.incomeTypes = {};

        var url = "/api/v1/ControlProject/incomeTypes/";


        TableNav(
            $scope,
            $http,
            "incomeTypes",
            url
        );


        $scope.Post = function () {
            if ($scope.incomeType.id) {
                $http.patch(url + $scope.incomeType.id + "/", $scope.incomeType).then(function (data) {
                    if (data.data.id) {
                        $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                        $("#modal_add_new_income_type").modal("hide");
                    } else {
                        swal.showInputError("لطفا در ورود اطلاعات دقت نمایید");
                    }


                }).catch(function (data) {

                });

            } else {
                $http.post(url, $scope.incomeType).then(function (data) {
                    if (data.data.id) {
                        $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                        $scope.incomeTypesList();
                        $("#modal_add_new_income_type").modal("hide");
                    } else {
                        swal.showInputError("لطفا در ورود اطلاعات دقت نمایید");
                    }
                }).catch(function (data) {

                });

            }
        };
        $scope.Cancel = function () {
            $scope.incomeType = {};
        };
        $scope.AddNewincomeType = function () {
            $scope.incomeType = {};
            $("#modal_add_new_income_type").modal("show");
        };
        $scope.Edit = function (incomeType) {
            $scope.incomeType = incomeType;
            $("#modal_add_new_income_type").modal("show");
        };
        $scope.Delete = function ($index, incomeType) {
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
                $http.delete(url + incomeType.id + "/").then(function (data) {
                    $scope.incomeTypesList();
                    swal("حذف شد!", "دوره انتخابی حذف شد", "success");

                })
            });
        };


        $scope.BindCountType = function (bindID) {
            if (bindID == "1") {
                return "کیلوگرم"
            }
            if (bindID == "2") {
                return "عدد"
            }
            if (bindID == "3") {
                return "ریال"
            }
            if (bindID == "4") {
                return "دلار"
            }
            if (bindID == "5") {
                return "یوان"
            }
            if (bindID == "6") {
                return "یورو"
            }
            if (bindID == "7") {
                return "بسته"
            }
            if (bindID == "8") {
                return "جین"
            }
        }

    });