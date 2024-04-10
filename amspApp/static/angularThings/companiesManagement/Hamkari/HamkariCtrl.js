'use strict';
angular.module('AniTheme')
    .controller('HamkariCtrl', function ($scope, $http, $translate, $rootScope, $stateParams, $location, $$$, $filter) {
        $scope.companyId = $stateParams.companyid;
        $scope.hamkaries = {};
        $scope.wait = false;
        $scope.HamkariSearchText = "";
        function init() {
            $scope.hamkari = {};
            $scope.hamkari.jobs = [];
            $scope.hamkari.extraFields = [];
            $scope.showEdit = false;
        }

        $scope.HamkariPageTo = function (page) {
            if (page) {
                $scope.wait = true;
                $http.get(page).then(function (data) {
                    $scope.hamkaries = data.data;
                    $scope.wait = false;
                }).catch(function () {
                    $scope.wait = false;
                });
            }
        }

        $scope.$watch("HamkariSearchText", function () {
            $scope.list();
        });


        $scope.publish = function (item) {
            item.publish = false;
            $http.patch("/api/v1/companies/" + $stateParams.companyid + "/hamkari/" + item.id + "/",
                {
                    publish: item.publish
                }).then(function (data) {
            })
        }
        $scope.unpublish = function (item) {
            item.publish = true;
            $http.patch("/api/v1/companies/" + $stateParams.companyid + "/hamkari/" + item.id + "/",
                {
                    publish: item.publish
                }).then(function (data) {
            })
        }


        $scope.DeleteHamkari = function (item) {
            swal({
                title: "آیا اطمینان دارید",
                text: "آیا اطمینان دارید که می خواهید آیتم انتخابی را حذف نمایید",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "بله حذف شود",
                closeOnConfirm: false
            }, function () {
                $http.delete("/api/v1/companies/" + $scope.companyId + "/hamkari/" + item.id + "/").then(function (data) {
                    $scope.list();
                    init();
                    swal("انجام شد", "حذف شد", "success");
                })
            });
        };
        $scope.page = 1;
        $scope.list = function () {
            $scope.wait = true;
            $http.get("/api/v1/companies/" + $scope.companyId + "/hamkari/?q="+$scope.HamkariSearchText+"&page="+$scope.page.toString()+"&page_size=10").then(function (data) {
                $scope.wait = false;
                $scope.hamkaries = data.data;
                $scope.page = data.data.current_page;
            })
        };

        init();

    });
