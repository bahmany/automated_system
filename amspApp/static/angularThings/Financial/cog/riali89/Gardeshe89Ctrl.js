'use strict';

angular.module('AniTheme').controller(
    'Gardesh89Ctrl',
    function ($scope,
              //$translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {

        var table;


        $scope.list = function () {
            $http.get("/Financial/api/v1/cog_89/getDatatableCols/").then(function (bbdata) {
                table.ajax.reload();
            })
        }

        $scope.init = function () {
            $http.get("/Financial/api/v1/cog_89/getDatatableCols/").then(function (bbdata) {

                for (var i = 0; bbdata.data.length > i; i++) {
                    if (bbdata.data[i]['type'] === "num-fmt") {
                        bbdata.data[i]['render'] = $.fn.dataTable.render.number(',', '.', 1, '')
                    }
                }

                table = $('#divTablecog_89').DataTable({
                    "processing": true,
                    "serverSide": true,
                    "order": [[0, "desc"]],
                    "ajax": {
                        "url": "/Financial/api/v1/cog_89/",
                        "type": "GET"
                    },
                    "columns": bbdata.data
                });
            });
        }

        $scope.init();

        $scope.bugs = [];
        $scope.StartGardeshProcess = function () {
            $http.get("/Financial/api/v1/cog_89/startCalcGardeshChaap/").then(function (data) {
                $scope.list();
                $scope.bugs = data.data["errors"];
            })
        }


    });


