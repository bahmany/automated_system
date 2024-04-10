'use strict';


angular.module('AniTheme').controller(
    'costCalOutcomeTypesCtrl',
    function ($scope,
              $translate,
              $http,
              $q, $mdDialog,
              $rootScope, $timeout,
              $modal) {

        // $scope.AddNewOutcomeType = function () {
        //     $("modal_add_new_outcome_type").modal("show");
        // }
        //

        $scope.outcomeType = {};
        $scope.outcomeTypes = {};

        var url = "/api/v1/CostCal/outcomeTypes/";


        TableNav(
            $scope,
            $http,
            "outcomeTypes",
            url
        );


        $scope.Post = function () {
            if ($scope.outcomeType.id) {
                $http.patch(url + $scope.outcomeType.id + "/", $scope.outcomeType).then(function (data) {
                    if (data.data.id) {
                        $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                        $("#modal_add_new_outcome_type").modal("hide");
                    } else {
                        swal.showInputError("لطفا در ورود اطلاعات دقت نمایید");
                    }


                }).catch(function (data) {

                });

            } else {
                $http.post(url, $scope.outcomeType).then(function (data) {
                    if (data.data.id) {
                        $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                        $scope.outcomeTypesList();
                        $("#modal_add_new_outcome_type").modal("hide");
                    } else {
                        swal.showInputError("لطفا در ورود اطلاعات دقت نمایید");
                    }
                }).catch(function (data) {

                });

            }
        };
        $scope.Cancel = function () {
            $scope.outcomeType = {};
        };
        $scope.AddNewOutcomeType = function () {
            $scope.outcomeType = {};
            $("#modal_add_new_outcome_type").modal("show");
        };
        $scope.Edit = function (outcomeType) {
            $scope.outcomeType = outcomeType;
            $("#modal_add_new_outcome_type").modal("show");
        };
        $scope.Delete = function ($index, outcomeType) {
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
                $http.delete(url + outcomeType.id + "/").then(function (data) {
                    $scope.outcomeTypesList();
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