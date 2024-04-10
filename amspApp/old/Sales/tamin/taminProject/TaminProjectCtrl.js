'use strict';
angular.module('AniTheme')
    .controller(
        'TaminProjectCtrl',
        function ($scope, $window, $http, $translate, $rootScope, $stateParams, $location, $timeout, $filter) {

            $scope.taminProject = {};
            $scope.taminProjects = {};
            $scope.cancel = function () {
                $scope.taminProject = {};
            }

// ------------------------------------------------
// ------------------------------------------------
// ------------------------------------------------

            $scope.searchTaminProject = "";
            $scope.$watch("searchTaminProject", function () {
                $scope.getTaminProject();
            });
            $scope.getTaminProject = function () {
                $http.get("/api/v1/salesProjects/?search=" + $scope.searchTaminProject + "&page=" + $scope.taminProjectpage.toString() + "&page_size=20").then(function (data) {
                    $scope.taminProjects = data.data;
                });
            };
            $scope.taminProjectpage = 1;
            $scope.taminProjectwait = false;
            $scope.taminProjectPageTo = function (page) {
                $scope.tatboghwait = true;
                if (page) {
                    $http.get(page).then(function (data) {
                        $scope.taminProjectwait = false;
                        $scope.taminProjects = data.data;
                    }).catch(function () {
                        $scope.taminProjectwait = false;
                    });
                }
            }

// ------------------------------------------------
// ------------------------------------------------
// ------------------------------------------------
// ------------------------------------------------


            $scope.delete = function (item) {
                if (confirm("آبا از حذف آیتم انتخاب شده     اطمینان دارید ؟")) {
                    $http.delete("/api/v1/salesProjects/" + item.id + "/").then(function () {
                            $scope.getTaminProject();
                    })
                }
            }
            $scope.post = function () {
                if ($scope.taminProject.id) {
                    $http.patch("/api/v1/salesProjects/"+$scope.taminProject.id+"/", $scope.taminProject).then(function (data) {
                        if (data.data.id) {
                            $scope.getTaminProject();
                            $scope.showList();
                        } else {


                        }
                    }).catch(function (data) {

                    })
                } else {
                    $http.post("/api/v1/salesProjects/", $scope.taminProject).then(function (data) {
                        if (data.data.id) {
                            $scope.getTaminProject();
                            $scope.showList();
                        } else {


                        }
                    }).catch(function (data) {

                    })

                }


            }
            $timeout(function () {
                $('#txtDateStart').datepicker({
                    dateFormat: 'yy/mm/dd'
                });
            }, 0);
            $scope.showList = function () {
                $("#divEdit").fadeOut(function () {
                    $("#divList").fadeIn();
                })
            };
            $scope.new = function () {
                $scope.taminProject = {};
                $scope.showEdit();
            }
            $scope.cancel = function () {
                $scope.showList();
            }
            $scope.edit = function (item) {
                $scope.taminProject = item;
                $scope.showEdit();
            }
            $scope.showEdit = function () {
                $("#divList").fadeOut(function () {
                    $("#divEdit").fadeIn();
                })
            }

        });