'use strict';


angular.module('AniTheme').controller(
    'MorekhasiSaatiListCtrl',
    function ($scope,
              $translate,
              $http,
              $q, $mdDialog, $state,
              $rootScope,
              $modal) {

        $scope.filter = {
            taeed_nashodeha: true,
            taeed_shodeha: false,
            draftha: false
        }

        var table;

        $scope.list = function () {
            $http.get("/api/v1/morekhasi_saati/getDatatableCols/").then(function (bbdata) {

                bbdata.data.push({
                    'data': "id",
                    "searchable": false,
                    "title": "عملیات",
                    "render": function (data, type, full) {
                        let aa = "";
                        aa = "<button onclick='editMs(\"" + data + "\")'>         " +
                            "ویرایش" +
                            "     </button>";

                        if (full.typeOf !== 'درفت') {
                            aa = "<button onclick='editMs(\"" + data + "\")'>         " +
                                "ورود به فرآیند" +
                                "     </button>"
                        }
                        if (full.typeOf === 'درفت') {
                            aa += "<button onclick='removeMs(\"" + data + "\")'>         " +
                                "حذف" +
                                "     </button>"
                        }
                        return aa
                    }
                })
                var filter = $scope.filter;

                table = $('#divTable77').DataTable({
                    "processing": true,
                    "serverSide": true,
                    "language": {
                        "decimal": "-",
                        "thousands": "."
                    },
                    "order": [[0, "desc"]],
                    "ajax": {
                        "url": "/api/v1/morekhasi_saati/?taeed_nashodeha=" + filter.taeed_nashodeha +
                            "&taeed_shodeha=" + filter.taeed_shodeha +
                            "&draftha=" + filter.draftha,
                        "type": "GET"
                    },
                    "columns": bbdata.data,
                    "initComplete": function (settings) {
                        
                    }
                });
            })

        }

        $scope.init = function () {
            $scope.list();
        }

        $scope.init();

        $scope.gotodetails = function (id) {
            $state.go("morekhasi-saati-add", {morekhasiID: id});
        }


    });


function editMs(data) {
    var scope = angular.element($("#divMorekhasiSaatiListCtrl")).scope();
    scope.gotodetails(data);

}

function removeMs(data) {
    var scope = angular.element($("#divMorekhasiSaatiListCtrl")).scope();
    scope.delete(data);

}
