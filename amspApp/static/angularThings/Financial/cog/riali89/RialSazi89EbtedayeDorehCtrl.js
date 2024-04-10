'use strict';

angular.module('AniTheme').controller(
    'RialSazi89EbtedayeDorehCtrl',
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
        $('#divTablecog_89').on('click', 'tbody td:not(:first-child)', function (e) {
            editor.inline(table.cell(this).index(), {
                onBlur: 'submit'
            });
            selected_row = table.row(e.currentTarget.parentElement).data().id;
            editedRow = table.row(e.currentTarget.parentElement);

            DT_RowId = table.row(e.currentTarget.parentElement).data().DT_RowId;
        });

        $scope.init = function () {
            $http.get("/Financial/api/v1/cog_89/getDatatableColWinoutMablagheAvaliehs/").then(function (bbdata) {

                $http.get("/Financial/api/v1/cog_89/getDatatableColWinoutMablagheAvaliehsEdit/").then(function (bssbdata) {


                    editor = new $.fn.dataTable.Editor({
                        "processing": true,
                        "serverSide": true,
                        ajax: {
                            type: "PUT",
                            url: "/Financial/api/v1/cog_89/get89WinoutMablagheAvaliehUpdate/",
                            data: function (d) {
                                d.id = selected_row;
                                d.DT_RowId = DT_RowId;
                            }
                        },
                        table: "#divTablecog_89",
                        fields: bssbdata.data
                    });

                    editor.on('submitSuccess', function (e, json, data) {
                        editedRow.data(json);
                    });

                    table = $('#divTablecog_89').DataTable({
                        "processing": true,
                        "serverSide": true,
                        "language": {
                            "decimal": "-",
                            "thousands": "."
                        },
                        "order": [[0, "desc"]],
                        "ajax": {
                            "url": "/Financial/api/v1/cog_89/get89WinoutMablagheAvalieh/",
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
            $http.post("/Financial/api/v1/cog_89/postBulkRiali89AvaleDoreh/", {psb: $scope.bulkInsert}).then(function (data) {
                if (data.data.id) {

                }
            })
        }


    });


