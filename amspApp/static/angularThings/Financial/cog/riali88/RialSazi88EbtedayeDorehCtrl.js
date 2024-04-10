'use strict';

angular.module('AniTheme').controller(
    'RialSazi88EbtedayeDorehCtrl',
    function ($scope,
              //$translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {


        var editor;
        var table;
        var selected_row;
        var DT_RowId;
        var editedRow;


        // Activate an inline edit on click of a table cell
        $('#divTable88').on('click', 'tbody td:not(:first-child)', function (e) {
            editor.inline(table.cell(this).index(), {
                onBlur: 'submit'
            });
            selected_row = table.row(e.currentTarget.parentElement).data().id;
            editedRow = table.row(e.currentTarget.parentElement);

            DT_RowId = table.row(e.currentTarget.parentElement).data().DT_RowId;
        });

        $scope.init = function () {
            $http.get("/Financial/api/v1/Coil88Tolid/getDatatableColWinoutMablagheAvaliehs/").then(function (bbdata) {

                $http.get("/Financial/api/v1/Coil88Tolid/getDatatableColWinoutMablagheAvaliehsEdit/").then(function (bssbdata) {


                    editor = new $.fn.dataTable.Editor({
                        "processing": true,
                        "serverSide": true,
                        ajax: {
                            type: "PUT",
                            url: "/Financial/api/v1/Coil88Tolid/get88WinoutMablagheAvaliehUpdate/",
                            data: function (d) {
                                d.id = selected_row;
                                d.DT_RowId = DT_RowId;
                            }
                        },
                        table: "#divTable88",
                        fields: bssbdata.data
                    });

                    editor.on('submitSuccess', function (e, json, data) {
                        editedRow.data(json);
                    });

                    table = $('#divTable88').DataTable({
                        "processing": true,
                        "serverSide": true,
                        "language": {
                            "decimal": "-",
                            "thousands": "."
                        },
                        "order": [[0, "desc"]],
                        "ajax": {
                            "url": "/Financial/api/v1/Coil88Tolid/get88WinoutMablagheAvalieh/",
                            "type": "GET"
                        },
                        select: {
                            style: 'os',
                            selector: 'td:first-child'
                        },
                        buttons: [
                            {extend: "create", editor: editor},
                            {extend: "edit", editor: editor},
                            {extend: "remove", editor: editor}
                        ],

                        "columns": bbdata.data
                    });
                })


            })
        }

        $scope.init();

        $scope.postBulk = function (item) {
            $http.post("/Financial/api/v1/Coil88Tolid/postBulkRiali88AvaleDoreh/", {psb: $scope.bulkInsert}).then(function (data) {
                if (data.data.id) {

                }
            })
        }


    });


