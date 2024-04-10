'use strict';

angular.module('AniTheme').controller(
    'RialSazi88Ctrl',
    function ($scope,
              //$translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {

        $scope.bugs = [];
        $scope.StartGardeshProcess = function () {
            $http.get("/Financial/api/v1/Coil88Gardesh/startCalcGardesh88/").then(function (data) {
                $scope.bugs = data.data["errors"]
            })
        }


        var table;
        $scope.init = function () {
            $http.get("/Financial/api/v1/Coil88Gardesh/getDatatableCols/").then(function (bbdata) {

                for (var i = 0; bbdata.data.length > i; i++) {
                    if (bbdata.data[i]['type'] === "num-fmt") {
                        bbdata.data[i]['render'] = $.fn.dataTable.render.number(',', '.', 1, '')
                    }
                }

                table = $('#divTable88').DataTable({
                    "processing": true,
                    "serverSide": true,
                    "order": [[0, "desc"]],
                    "ajax": {
                        "url": "/Financial/api/v1/Coil88Gardesh/",
                        "type": "GET"
                    },
                    "columns": bbdata.data
                });
            });
        }

        $scope.init();


    });


