'use strict';

angular.module('AniTheme').controller(
    'CAToDavayereTolidiCtrl',
    function ($scope,
              //$translate,
              $q,
              $http, $window,
              $location,
              $rootScope, hotRegisterer,
              $timeout) {

        $scope.JsonOfPercent = "";
        $scope.storePercent = function () {
            // جهت ذخیره بصورت بالک از تکتس باکس
            $http.post("/Financial/api/v1/ca/saveSetting/", {
                'values': {stringJson: $scope.JsonOfPercent},
                "name": "PercentOfMavad"
            }).then(function (data) {

            })
        }


        /*
        * {
  "110101": {
    "AccNo": 110101,
    "AccTitle": "خط قلع اندود",
    "خط قلع اندود": 100,
    "آند سازی": null,
    "خط برش": null,
    "خط برش2": null,
    "چاپ": null,
    "لاک": null,
    "آسان بازشو": null,
    "قوطی سازی": null
        * */

        var tablePercent;
        var editor;
        var selected_row;
        var DT_RowId;
        var editedRow;
        $scope.convertJsonToArray = function (jsonAsText) {
            // var obj = JSON.parse(jsonAsText);
            // var jsonArr = Object.keys(obj).map(key => obj[key]);

            $http.get("/Financial/api/v1/ca_to_davayereh_tolidi/getTashimPercentCols/").then(function (data) {


                editor = new $.fn.dataTable.Editor({
                    "processing": true,
                    "serverSide": true,
                    ajax: {
                        type: "PUT",
                        url: "/Financial/api/v1/ca_to_davayereh_tolidi/getTashimPercentUpdate/",
                        data: function (d) {
                            d.id = selected_row;
                            d.DT_RowId = DT_RowId;
                        }
                    },
                    table: "#divTablePers",
                    fields: data.data.tble
                });

                editor.on('submitSuccess', function (e, json, data) {
                    // editedRow.data(json);
                    tablePercent.ajax.reload();
                });


                tablePercent = $('#divTablePers').DataTable({
                    processing: true,
                    serverSide: true,
                    order: [[0, "desc"]],
                    pageLength: 100,
                    ajax: {
                        url: "/Financial/api/v1/ca_to_davayereh_tolidi/getTashimPercent/",
                        type: "GET",

                    },
                    dom: 'Bfrtip',
                    columns: data.data.tbl,
                    select: true,
                    buttons: [
                        {text: 'ایجاد', extend: "create", editor: editor},
                        {text: 'ویرایش', extend: "edit", editor: editor},
                        {text: 'حذف', extend: "remove", editor: editor}
                    ],
                });


                // $('#divTablePers').on('click', 'tbody td:not(:first-child)', function (e) {
                //     editor.inline(table.cell(this).index(), {
                //         onBlur: 'submit'
                //     });
                //
                //     selected_row = table.row(e.currentTarget.parentElement).data().id;
                //     editedRow = table.row(e.currentTarget.parentElement);
                //     DT_RowId = table.row(e.currentTarget.parentElement).data().DT_RowId;
                // });

            })


        }

        $scope.callPercent = function () {
            $http.get("/Financial/api/v1/ca/PercentOfMavad/callSetting/").then(function (data) {
                if (data.data.err) {
                    return
                }
                $scope.JsonOfPercent = data.data.details.stringJson;
                $scope.jsonPr = $scope.convertJsonToArray(data.data.details.stringJson);
            })
        }

        var table;
        $scope.init = function () {

            $scope.GetTable();


            // $http.get("/Financial/api/v1/ca_to_davayereh_tolidi/getDatatableCols/").then(function (data) {
            //     for (var i = 0; data.data.length > i; i++) {
            //         if (data.data[i]['type'] === "num-fmt") {
            //             data.data[i]['render'] = $.fn.dataTable.render.number('/', '.', 0, '')
            //         }
            //
            //         if (data.data[i]['it_is_percent'] === true) {
            //
            //         }
            //         if (data.data[i]['it_is_percent'] === false) {
            //
            //         }
            //
            //     }
            //
            //     table = $('#divTable77').DataTable({
            //         "processing": true,
            //         "serverSide": true,
            //         "order": [[0, "desc"]],
            //         "pageLength": 100,
            //         "ajax": {
            //             "url": "/Financial/api/v1/ca_to_davayereh_tolidi/",
            //             "type": "GET",
            //
            //         },
            //         "columns": data.data
            //     });
            // });
            // $scope.callPercent();


        }

        $scope.hot = {};
        $scope.setting = {
            formulas: true,
            licenseKey: 'non-commercial-and-evaluation',
            afterInit: function () {
                $scope.hot.instance = this;
            }
        }

        $scope.percentTable = [];
        var hotInstance = document.getElementById('catable');
        $scope.GetTable = function () {
            // HotRegisterer.getInstance(hotInstance);
            // debugger;

            $http.get("/Financial/api/v1/ca_to_davayereh_tolidi/GetSahmbariTable/").then(function (data) {
                // table.ajax.reload();
                $scope.percentTable = data.data;
                // $scope.generateHandson($scope.percentTable.cols, $scope.percentTable.data);
            })
        }

        $scope.calcSums = function () {
            let colcount = $scope.hot.instance.countCols();
            let sums = {};
            let colHeader = $scope.hot.instance.getColHeader();
            let colData = $scope.hot.instance.getDataAtRow($scope.hot.instance.countRows() - 1);
            for (var i = 0; colHeader.length > i; i++) {
                sums[colHeader[i]] = colData[i];
            }
            return sums


        }


        $scope.StoreTable = function () {
            $scope.percentTable.sums = $scope.calcSums();
            $http.post("/Financial/api/v1/ca_to_davayereh_tolidi/SaveSahmbariTable/", $scope.percentTable).then(function (data) {
                // $scope.percentTable = data.data;
            })
        }
        $scope.ResetTable = function () {
            $http.get("/Financial/api/v1/ca_to_davayereh_tolidi/ResetSahmbariTable/").then(function (data) {
                if (data.data.data) {
                    $window.location.reload();
                }
            })
        }


        $scope.AddToTablePercent = function () {
            $http.get("/Financial/api/v1/ca_to_davayereh_tolidi/add_percent_to_table/").then(function (data) {
                table.ajax.reload();

            })
        }


        // $scope.generateHandson = function (cols, data) {
        // example2 = document.getElementById('example2');

        //     hot2 = new Handsontable(example2, {
        //         data: data,
        //         colHeaders: true,
        //         rowHeaders: true,
        //         contextMenu: true,
        //         formulas: true,
        //         columns: cols
        //     });
        // }
        $scope.init();


        $scope.storeSahmbari = function () {

        }


    });


