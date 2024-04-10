'use strict';

angular.module('AniTheme').controller(
    'CaAutomatedSumsCtrl',
    function ($scope,
              //$translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {



        $scope.tashimAvalieh = {};
        $scope.getTashimAvalieh = function () {
            $http.get("/Financial/api/v1/ca/getTashimAvalieh/").then(function (data) {
                $scope.tashimAvalieh = data.data;

            })
        }

        $scope.getTashimAvalieh();

        var table;
        $scope.init = function () {
            // $http.get("/Financial/api/v1/ca/getDatatableCols/").then(function (bbdata) {
                // table = $('#divTableAvalieh').DataTable({
                //     "processing": true,
                //     "serverSide": true,
                //     // scrollY: "300px",
                //     // scrollX: true,
                //     // scrollCollapse: true,
                //     "language": {
                //         "decimal": "-",
                //         "thousands": "/"
                //     },
                //     // 'fixedColumns': true,
                //
                //     "order": [[0, "desc"]],
                //     "ajax": {
                //         "url": "/Financial/api/v1/ca/getDt/",
                //         "type": "POST"
                //     },
                //     "columns": bbdata.data,
                // });
            // })


        }

        $scope.init();

        $scope.updateFromSG = function () {
            $http.get("/Financial/api/v1/ca/updateFromSG/").then(function (data) {
                if (data.result) {
                    $scope.getSumTable();
                    table.ajax.reload();

                }
            })
        }
        $scope.getCalcFromSG = function () {
            $http.get("/Financial/api/v1/ca/getCalcFromSG/").then(function (data) {
                if (data.result) {
                    $scope.getSumTable();
                    table.ajax.reload();

                }
            })
        }

        $scope.calcDatmozdSrbar = function () {
            $http.get("/Financial/api/v1/ca/calcDatmozdSrbar/").then(function (data) {
                $scope.getSumTable();
                table.ajax.reload();
            })
        }

        $scope.sum_headers = {};
        $scope.sums = [];
        $scope.getSumTable = function () {
            $http.get("/Financial/api/v1/ca/SumOfCat/callSetting/").then(function (data) {
                if (data.data.details) {
                    $scope.sum_headers = data.data.details.sumOf[0].helper;
                    $scope.sums = data.data.details.sumOf;
                } else {
                    alert("شما هنوز محاسباتی انجام نداده اید")
                }
            });
        }
        $scope.getSumTable();
    });
