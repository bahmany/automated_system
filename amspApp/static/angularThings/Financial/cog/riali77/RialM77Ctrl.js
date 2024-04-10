'use strict';

angular.module('AniTheme').controller(
    'RialM77Ctrl',
    function ($scope,
              //$translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {


        $scope.init = function () {
            $http.get("/Financial/api/v1/GardesheKol/getDatatableCols/").then(function (bbdata) {
                $('#divTable77').DataTable({
                    "processing": true,
                    "serverSide": true,
                    "language": {
                        "decimal": "-",
                        "thousands": "."
                    },
                    "order": [[0, "desc"]],
                    "ajax": {
                        "url": "/Financial/api/v1/GardesheKol/",
                        "type": "GET"
                    },
                    "columns": bbdata.data
                });
            })
        }

        $scope.init();



        $scope.Refresh77 = function () {
            if (confirm("تمامی اطلاعات گردش کالا پاک شده و از همکاران منتقل می شود اطمینان دارید ؟")) {
                $http.get("/Financial/api/v1/GardesheKol/transferGardesh77FromHamkaran/").then(function (data) {
                    if (data.result) {
                        if (data.result === "ok") {

                        }
                    }
                })
            }
        }


    });


