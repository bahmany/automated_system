'use strict';

angular.module('AniTheme').controller(
    'CogHomeCtrl',
    function ($scope,
              //$translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {


        $scope.getCurrentSaleMali = function () {
            $http.get("/Financial/api/v1/cogb/getSaleMaliResponse/").then(function (data) {
                if (data.data.year) {
                    $scope.saleMali = data.data.year;
                }
            })
        };


        $scope.callIntegrity = function(){
            $http.get("/Financial/api/v1/cogb/callIntegrity/").then(function (data) {

            })
        }


        // $scope.setCurrentYear = function () {
        //     var newYear = prompt("format :  1399-01-01 1399-06-31");
        //     if (newYear) {
        //         $scope.saleMali = newYear;
        //         $http.post("/Financial/api/v1/cogb/addSaleMali/", {
        //             selectedYear: $scope.saleMali
        //         }).then(function (data) {
        //             if (data.data.result === "ok") {
        //                 location.reload();
        //             }
        //         })
        //     }
        // }

        // $scope.setCurrentMonth = function () {
        //     var newYear = prompt("لطفا ماه را وارد کنید نمونه : 06-30 12-30");
        //     if (newYear) {
        //         $scope.saleMali = newYear;
        //         $http.post("/Financial/api/v1/cogb/setMonthMaliResponse/", {
        //             selectedYear: $scope.saleMali
        //         }).then(function (data) {
        //             if (data.data.result === "ok") {
        //                 location.reload();
        //             }
        //         })
        //     }
        // }

        $scope.getCurrentSaleMali();
        // checking if authenticated

        // $scope.RecieveAll = function () {
        //     $http.get("/Financial/api/v1/mAll/RecieveAll/").then(function (data) {
        //
        //     });
        // }


    });
