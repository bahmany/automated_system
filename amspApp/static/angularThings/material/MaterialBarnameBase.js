'use strict';


angular.module('AniTheme').controller(
    'MaterialBarnameCtrl',
    function ($scope,
              $translate,
              $http, $filter,
              $q, $mdDialog,
              $rootScope, $timeout,
              $modal) {
        var table;
        var drawSeach = 0;
        $scope.onClick = function (points, evt) {
            console.log(points, evt);
        };
        $scope.OpenBasket = function (ev) {

            $mdDialog.show({
                controller: DialogController,
                templateUrl: '/Material/page/materialBasket/',
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                currentScope: $scope // Only for -xs, -sm breakpoints.
            })
                .then(function (answer) {
                    table.ajax.reload();
                    $scope.basket = [];

                }, function () {
                    $scope.status = 'You cancelled the dialog.';
                });


        }

        function DialogController($scope, $http, $mdDialog, currentScope) {

            $scope.order = {};
            $scope.order.items = currentScope.basket;


            $scope.confirm = function () {

                $http.post("/api/v1/barcodes/saveTolid/", $scope.order).then(function (data) {
                    if (data.data.error) {
                        $scope.order = data.data.error
                    } else {
                        $mdDialog.hide();
                    }
                })
            }

            $scope.cancel = function () {
                $mdDialog.cancel();
            }


            var triggerAssgned = false;
            $scope.AddFileUpload = function () {

                if (!($scope.order.files)) {
                    $scope.order.files = [];
                }

                if (triggerAssgned === false) {
                    $scope.attachChangeEvent();
                }
                $("#UploadFile").click();
            }
            $scope.attachChangeEvent = function () {
                if (Boolean($("#UploadFile")[0])) {
                    triggerAssgned = true;
                    $("#UploadFile").change(function () {
                        if ($("#UploadFile").val()) {

                            $("#UploadFile")[0].files.forEach(function (file) {
                                let frmData = new FormData();
                                frmData.append('file', file);
                                $("#waitForUpload").html("<i id='dsadasdasdafreg' class='fa fa-refresh fa-5x fa-spin'></i> ");
                                $.ajax({
                                    url: '/api/v1/file/upload/',
                                    type: 'POST',
                                    data: frmData,
                                    contentType: false,
                                    processData: false,
                                    cache: false,
                                    success: function (data) {
                                        if (data.name) {
                                            $scope.order.files.push(data);

                                            $("#waitForUpload").html('');
                                        } else {
                                            $scope.barcode.barnamehUrl = '';
                                            $("#waitForUpload").html('');
                                        }
                                    }, error: function () {
                                        $("#waitForUpload").html('');
                                    }
                                })
                                ;
                            })


                        }
                    });

                }

            }


            $scope.changePriority = function (move_type, index) {
                let count = $scope.order.items.length;
                if (move_type == 1) { // up
                    if ($scope.order.items[index].priority == 1) {
                        return
                    }
                    $scope.order.items[index - 1].priority = $scope.order.items[index - 1].priority + 1;
                    $scope.order.items[index].priority = $scope.order.items[index].priority - 1;
                }
                if (move_type == 2) { // down

                }
            }
        }

        $scope.search = {};
        $scope.search.start_date = "";
        $scope.search.end_date = "";
        $scope.search.days_arrow = "1";
        $scope.search.day1 = 0;
        $scope.search.day2 = 0;
        $scope.search.correct = true;
        $scope.search.scrap = true;
        $scope.search.scrap_and_store = true;
        $scope.$watchCollection("search", function () {
            if (table) {
                table.ajax.reload();
            }
        })
        $scope.init = function () {
            $http.get("/api/v1/barcodes/getBarcodeWithDetailsForBarnameRiziColumns/").then(function (data) {
                var cols = data.data;

                cols.push({
                    'data': 'id',
                    'searchable': false,
                    'title': 'عملیات',
                    'render': function (data, type, full) {
                        let cc = "";
                        if (full.baghimandeh > 0) {
                            cc = "<button onclick=\"addToBasket('" + full.barcode + "')\">Add</button>";

                        } else {
                            cc = "";

                        }
                        return cc
                    }
                })


                table = $('#divTableBarcode').on('preXhr.dt', function (e, settings, json, xhr) {
                    json['search'] = $scope.search;
                })

                    .on('xhr.dt', function (e, settings, json, xhr) {
                        $scope.barcodes = json;
                        $scope.labels = json.chart_graph.labels;
                        $scope.series = json.chart_graph.labels;
                        $scope.data = json.chart_graph.data;
                        $scope.labels66 = json.chart_graph66.labels;
                        $scope.series66 = json.chart_graph66.labels;
                        $scope.data66 = json.chart_graph66.data;
                        $scope.labels65 = json.chart_graph65.labels;
                        $scope.series65 = json.chart_graph65.labels;
                        $scope.data65 = json.chart_graph65.data;

                    }).DataTable({
                        "processing": true,
                        "serverSide": true,
                        "order": [[0, "desc"]],
                        "ajax": {
                            "url": "/api/v1/barcodes/getBarcodeWithDetailsForBarnameRizi/",
                            "type": "POST"
                        },
                        "columns": cols,

                        "initComplete": function (settings) {
                            if (drawSeach === 0) {
                                drawSeach = 1;
                                $('#divTableBarcode thead tr').clone(true).appendTo('#divTableBarcode thead');
                                $('#divTableBarcode thead tr:eq(1) th').each(function (i) {
                                    $(this).unbind();
                                    var title = $(this).text();
                                    $(this).html('<input type="text" style="width: 50px;"  />');
                                    $('input', this).on('keyup change', function () {
                                        if (table.column(i).search() !== this.value) {
                                            table
                                                .column(i)
                                                .search(this.value)
                                                .draw();
                                        }
                                    });
                                });

                            }
                        }
                    });

            })

        };
        $scope.init();
        $scope.basket = [];
        $scope.addToBasket = function (barcode) {
            // var found = false;
            for (var i = 0; $scope.barcodes.data.length > i; i++) {
                if ($scope.barcodes.data[i]['barcode'] === barcode.toString()) {

                    $scope.barcodes.data[i]['mizane_tolid'] = $scope.barcodes.data[i].vazneKhales;
                    var newIns = angular.copy($scope.barcodes.data[i]);
                    newIns.uniqID = makeid(10);
                    newIns.desc = null;
                    $scope.basket.push(newIns);
                }
            }
        }
    });


function addToBasket(data) {
    var scope = angular.element($("#MaterialBarnameCtrl")).scope();
    scope.addToBasket(data);
}

