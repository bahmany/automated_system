'use strict';

angular.module('AniTheme').controller('CompanySecretaraitsCtrl', function ($scope, $http, $stateParams, $translate, $rootScope, $location, $modal, CompanySecretiatsService) {

    $scope.DabirkhanehList = {};
    $scope.SelectedCompanyID = $stateParams.companyid;


    $scope.getDabirList = function () {
        $http.get("/api/v1/companies/" + $scope.SelectedCompanyID + "/secretariats/").then(function (data) {
            $scope.DabirkhanehList = data.data.results;
        });
    };


    $scope.deleteDabir = function (item, index) {
        swal({
            title: "Are you ready ?",
            text: "Add or update the secretariat ",
            type: "info",
            showCancelButton: true,
            closeOnConfirm: false,
            showLoaderOnConfirm: true
        }, function () {
            $http.delete("/api/v1/companies/" + $scope.SelectedCompanyID + "/secretariats/" + item.id + "/").then(function (data) {
                $scope.getDabirList();
                swal("Deleted", "Successfully removed", "success");
            }).catch(function (data) {
                swal("Error", "It is not removable because there are letters which get numbers from this.", "error");
            });
        });
    };

    $scope.addUpdateDabir = function (item, index) {
        item.company = parseInt($scope.SelectedCompanyID);
        swal({
            title: "Are you ready ?",
            text: "Add or update the secretariat ",
            type: "info",
            showCancelButton: true,
            closeOnConfirm: false,
            showLoaderOnConfirm: true
        }, function () {
            if (item.hasOwnProperty('id')) {
                $http.put("/api/v1/companies/" + $scope.SelectedCompanyID + "/secretariats/" + item.id + "/", item).then(function (data) {
                    swal("Good job!", "Successfully updated", "success");
                    $scope.getDabirList();
                }).catch(function (data) {
                    swal("Error !", "Please check fields validity, All fields are require", "error");
                });
            } else {
                $http.post("/api/v1/companies/" + $scope.SelectedCompanyID + "/secretariats/", item).then(function (data) {
                    swal("Good job!", "Successfully updated", "success");
                    $scope.getDabirList();
                }).catch(function (data) {
                    swal("Error !", "Please check fields validity, All fields are require", "error");
                });
            }
        });
    };

    $scope.addDabir = function (table) {
        table.push({});
    };

    $scope.getDabirList();


});
