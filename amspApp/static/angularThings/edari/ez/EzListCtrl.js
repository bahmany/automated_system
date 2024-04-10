'use strict';


angular.module('AniTheme').controller(
    'EZListCtrl',
    function ($scope,
              $translate, $stateParams,
              $q, $http, $state,
              $rootScope,
              $modal) {

        $scope.gotodetails = function (id) {
            $state.go("ezitem", {id: id});
        }

        $scope.filter = {
            taeed_nashodeha: true,
            taeed_shodeha: false,
            draftha: false
        }

        $scope.$watchCollection('filter', (prev, next) => {

            if (table) {
                table.ajax.url("/api/v1/ez/?taeed_nashodeha=" + $scope.filter.taeed_nashodeha +
                    "&taeed_shodeha=" + $scope.filter.taeed_shodeha +
                    "&draftha=" + $scope.filter.draftha).load();
                // table.ajax.reload();

            }
        });


        $scope.new = function () {
            $state.go("ezitem", {id: '0'});

        }

        $scope.delete = function (id) {
            swal({
                title: "حذف درفت",
                text: "آیا از حذف اطمینان دارید ؟",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "بله",
                closeOnConfirm: true,
                showLoaderOnConfirm: true
            }, function () {
                $http.delete("/api/v1/ez/" + id + "/").then(function (data) {
                    if (data.data.message) {
                        $rootScope.$broadcast("showToast", data.data.message);
                    } else {
                        table.ajax.reload();
                    }
                })
            })
        }


        var table;

        $scope.init = function () {

            $http.get("/api/v1/ez/getDatatableCols/").then(function (bbdata) {

                bbdata.data.push({
                    'data': "id",
                    "searchable": false,
                    "title": "عملیات",
                    "render": function (data, type, full) {
                        let aa = "";
                        aa = "<button onclick='editEz(\"" + data + "\")'>         " +
                            "ویرایش" +
                            "     </button>";

                        if (full.typeOf !== 'درفت') {
                            aa = "<button onclick='editEz(\"" + data + "\")'>         " +
                                "ورود به فرآیند" +
                                "     </button>"
                        }
                        if (full.typeOf === 'درفت') {
                            aa += "<button onclick='removeEz(\"" + data + "\")'>         " +
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
                        "url": "/api/v1/ez/?taeed_nashodeha=" + filter.taeed_nashodeha +
                            "&taeed_shodeha=" + filter.taeed_shodeha +
                            "&draftha=" + filter.draftha,
                        "type": "GET"
                    },
                    "columns": bbdata.data,
                    "initComplete": function (settings) {


                        // $('#divTable77 thead tr').clone(true).appendTo('#divTable77 thead');
                        // $('#divTable77 thead tr:eq(1) th').each(function (i) {
                        //     $(this).unbind();
                        //     var title = $(this).text();
                        //     $(this).html('<input type="text" style="width: 50px;"  />');
                        // });


                    }
                });
            })


        }

        $scope.init();


    });

function editEz(data) {
    var scope = angular.element($("#divEZListCtrl")).scope();
    scope.gotodetails(data);

}

function removeEz(data) {
    var scope = angular.element($("#divEZListCtrl")).scope();
    scope.delete(data);

}



