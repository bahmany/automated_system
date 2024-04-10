'use strict';

angular.module('AniTheme').controller(
    'RialSazi85Ctrl',
    function ($scope,
              //$translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {

        $scope.bugs = [];
        $scope.StartGardeshProcess = function () {
            $http.get("/Financial/api/v1/cog_85/startCalcGardesh85/").then(function (data) {
                $scope.bugs = data.data["errors"]
            })
        }


        var table;
        $scope.init = function () {
            $http.get("/Financial/api/v1/cog_85/getDatatableCols/").then(function (bbdata) {

                for (var i = 0; bbdata.data.length > i; i++) {
                    if (bbdata.data[i]['type'] === "num-fmt") {
                        bbdata.data[i]['render'] = $.fn.dataTable.render.number(',', '.', 1, '')
                    }
                }

                table = $('#divTable85').DataTable({
                    "processing": true,
                    "serverSide": true,
                    "order": [[0, "desc"]],
                    "ajax": {
                        "url": "/Financial/api/v1/cog_85/",
                        "type": "GET"
                    },
                    "columns": bbdata.data
                });
            });
        }

        $scope.init();


    });


