'use strict';

angular.module('AniTheme').controller(
    'RialiAvaleDorehCtrl',
    function ($scope,
              //$translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {

        $scope.BPs = {};

        var table;
        $scope.init = function () {
            $http.get("/Financial/api/v1/GardesheKol/getDatatableCols/").then(function (bbdata) {
                table = $('#divTableAvalieh').DataTable({
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


        $scope.Coil77Zero = [];
        $scope.selectTashimAvaleDorehKalayeNimehSakhtehKeSefrHastand = function () {
            $http.get("/Financial/api/v1/Coil66Tolid/selectTashimAvaleDorehKalayeNimehSakhtehKeSefrHastand/").then(function (data) {
                $scope.Coil77Zero = data.data;
            })
        }
        // $scope.selectTashimAvaleDorehKalayeNimehSakhtehKeSefrHastand();
        $scope.PostCoil77Avalieh = function (item) {
            $http.post("/Financial/api/v1/Coil66Tolid/postMeghdateRialiAvaleDoreh/", item).then(function (data) {
                if (data.data.id) {

                }
            })
        }
        $scope.getCalcStep1 = function () {
            $http.get("/Financial/api/v1/Coil66Tolid/xGetKol_xdflighghghruiwyreighueiwbrvoqeupqwoerhfqwbgoqweufhiwefjgfowfim/?format=json").then(function (data) {
                // $scope.Calc77 = data.data;
                // $.json2table(data.data, "testData").appendTo("tbl77");
                $.jsontotable(data.data, {
                    header: true,
                    id: "#tbl77",
                    className: "table table-hover"
                });
            })
        }

        $scope.Refresh66 = function () {
            if (confirm("تمامی اطلاعات گردش کالا پاک شده و از همکاران منتقل می شود اطمینان دارید ؟")) {
                $http.get("/Financial/api/v1/GardesheKol/RecieveAll/").then(function (data) {
                    if (data.result) {
                        if (data.result === "ok") {
                            table.ajax.reload();
                        }
                    }
                })
            }
        }
    });
