'use strict';

angular.module('AniTheme').controller(
    'GardesheAsaanBazShooCtrl',
    function ($scope,
              //$translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {

        var table;

        $scope.list = function () {
            $http.get("/Financial/api/v1/AsaanBazSho/getDatatableCols/").then(function (bbdata) {

                for (var i = 0; bbdata.data.length > i; i++) {
                    if (bbdata.data[i]['type'] === "num-fmt") {
                        bbdata.data[i]['render'] = $.fn.dataTable.render.number(',', '.', 1, '')
                    }
                }


            });
        }

        $scope.init = function () {
            $http.get("/Financial/api/v1/AsaanBazSho/getDatatableCols/").then(function (bbdata) {

                for (var i = 0; bbdata.data.length > i; i++) {
                    if (bbdata.data[i]['type'] === "num-fmt") {
                        bbdata.data[i]['render'] = $.fn.dataTable.render.number(',', '.', 1, '')
                    }
                }

                table = $('#divTable77').DataTable({
                    "processing": true,
                    "serverSide": true,
                    "order": [[0, "desc"]],
                    "ajax": {
                        "url": "/Financial/api/v1/AsaanBazSho/",
                        "type": "GET"
                    },
                    "columns": bbdata.data
                });
            });
        }

        $scope.init();

        $scope.bugs = [];
        $scope.StartGardeshProcess = function () {
            $http.get("/Financial/api/v1/AsaanBazSho/startCalcGardeshAsaanBazSho/").then(function (data) {
                $scope.bugs = data.data["errors"];
                $scope.init();
            })
        }


    }
);


