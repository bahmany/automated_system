'use strict';

angular.module('AniTheme').controller(
    'Gardeshe75Ctrl',
    function ($scope,
              //$translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {

        var table;

        $scope.list = function () {
            $http.get("/Financial/api/v1/Coil75Gardesh/getDatatableCols/").then(function (bbdata) {

                for (var i = 0; bbdata.data.length > i; i++) {
                    if (bbdata.data[i]['type'] === "num-fmt") {
                        bbdata.data[i]['render'] = $.fn.dataTable.render.number(',', '.', 1, '')
                    }
                }


            });
        }

        $scope.init = function () {
            $http.get("/Financial/api/v1/Coil75Gardesh/getDatatableCols/").then(function (bbdata) {

                for (var i = 0; bbdata.data.length > i; i++) {
                    if (bbdata.data[i]['type'] === "num-fmt") {
                        bbdata.data[i]['render'] = $.fn.dataTable.render.number(',', '.', 1, '')
                    }
                }

                table = $('#divTable').DataTable({
                    "processing": true,
                    "serverSide": true,
                    "order": [[0, "desc"]],
                    "ajax": {
                        "url": "/Financial/api/v1/Coil75Gardesh/",
                        "type": "GET"
                    },
                    "columns": bbdata.data
                });
            });
        }

        $scope.init();

        $scope.bugs = [];
        $scope.StartGardeshProcess = function () {
            $http.get("/Financial/api/v1/Coil75Gardesh/startCalcGardesh75/").then(function (data) {
                $scope.bugs = data.data["errors"];
                $scope.init();
            })
        }


        $scope.getBugs = function () {
            $http.get("/Financial/api/v1/ca/CogCACoil75Bugs/callSetting/").then(function (data) {
                if (data.data['details']) {
                    $scope.bugs = data.data.details.errors;
                }
            })
        }

        $scope.getBugs();
        $scope.ghal = {};
        $scope.ghalInformation = function () {
            $http.get('/Financial/api/v1/Coil77Gardesh/ghalInformation/').then(function (data) {
                $scope.ghal = data.data
            })
        }
        $scope.ghalInformation();


    }
);


