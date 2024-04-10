'use strict';


angular.module('RahsoonAdminApp')
    .controller("PaymentController", function ($scope,$http, $timeout, $log) {

        $scope.Payment = {};
        $scope.submit = function () {
            if ($scope.Payment.id){

            $http.patch("/administrator/api/v1/payment/"+$scope.Payment.id+"/", $scope.Payment).success(function (data) {
                $scope.list();
                $scope.Payment = {};
            }).error(function (err) {
                showError(err);
            })

            } else {
            $http.post("/administrator/api/v1/payment/", $scope.Payment).success(function (data) {
                $scope.list();
                $scope.Payment = {};
            }).error(function (err) {
                showError(err);
            })
            }
        }

        $scope.Payments = {};
        $scope.filter = {};
        $scope.filter.address = "/administrator/api/v1/payment/";
        $scope.list = function () {
            $http.get($scope.filter.address).then(function (data) {
                $scope.Payments = data.data;
            })
        }

        $scope.GoToPage = function (addr) {
            $http.get(addr).then(function (data) {
                $scope.Payments = data.data;
            })
        }

        $scope.Edit = function (item) {
            $http.get("/administrator/api/v1/payment/"+item.id+"/").then(function (data) {
                $scope.Payment = data.data;
            })
        }

        $scope.list();
    })

