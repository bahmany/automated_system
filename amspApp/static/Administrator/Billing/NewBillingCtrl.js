'use strict';


angular.module('RahsoonAdminApp')
    .controller("NewBillingController", function ($scope, $timeout, $log,$http) {

        $scope.Billing = {};
        $scope.submit = function () {
            if ($scope.Billing.id){

            $http.patch("/administrator/api/v1/billing/"+$scope.Billing.id+"/", $scope.Billing).success(function (data) {
                $scope.list();
                $scope.Billing = {};
            }).error(function (err) {
                showError(err);
            })

            } else {
            $http.post("/administrator/api/v1/billing/", $scope.Billing).success(function (data) {
                $scope.list();
                $scope.Billing = {};
            }).error(function (err) {
                showError(err);
            })
            }
        }

        $scope.Billings = {};
        $scope.filter = {};
        $scope.filter.address = "/administrator/api/v1/billing/";
        $scope.list = function () {
            $http.get($scope.filter.address).then(function (data) {
                $scope.Billings = data.data;
            })
        }

        $scope.GoToPage = function (addr) {
            $http.get(addr).then(function (data) {
                $scope.Billings = data.data;
            })
        }

        $scope.Edit = function (item) {
            $http.get("/administrator/api/v1/billing/"+item.id+"/").then(function (data) {
                $scope.Billing = data.data;
            })
        }

        $scope.list();

    })

