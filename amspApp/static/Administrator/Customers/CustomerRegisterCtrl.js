'use strict';


angular.module('RahsoonAdminApp')
    .controller("CustomerRegistrationController", function (
        $scope, $timeout, $log, $http) {
        $scope.Customer = {};
        $scope.submit = function () {
            if ($scope.Customer.id){

            $http.patch("/administrator/api/v1/customer/"+$scope.Customer.id+"/", $scope.Customer).success(function (data) {
                $scope.list();
                $scope.Customer = {};
                showSucc("با موفقیت ثبت شد")
            }).error(function (err) {
                showError(err);
            })

            } else {
            $http.post("/administrator/api/v1/customer/", $scope.Customer).success(function (data) {
                $scope.list();
                $scope.Customer = {};
                showSucc("با موفقیت ثبت شد")
            }).error(function (err) {
                showError(err);
            })
            }
        }

        $scope.Customers = {};
        $scope.filter = {};
        $scope.filter.address = "/administrator/api/v1/customer/";
        $scope.list = function () {
            $http.get($scope.filter.address).then(function (data) {
                $scope.Customers = data.data;
            })
        }

        $scope.GoToPage = function (addr) {
            $http.get(addr).then(function (data) {
                $scope.Customers = data.data;
            })
        }

        $scope.Edit = function (item) {
            $http.get("/administrator/api/v1/customer/"+item.id+"/").then(function (data) {
                $scope.Customer = data.data;
            })
        }

        $scope.list();

    })

