'use strict';


angular.module('AniTheme').controller(
    'BarcodeListCtrl',
    function ($scope,
              $translate,
              $http,
              $q, $mdDialog,
              $rootScope,
              $modal) {

        let table;

        $scope.barcodes = {};
        var currentBarCode = {};
        let urlOfBarcodes = "/api/v1/barcodes/";
        $scope.init = function () {
            $http.get("/api/v1/barcodes/getDatatableCols/").then(function (bbdata) {
                var dtt = bbdata.data;
                dtt.push({
                    'data': 'id',
                    'searchable': false,
                    'title': 'عملیات',
                    'render': function (data, type, full) {
                        var cc = "";
                        if (full['hamkaranSanad']) {
                            currentBarCode = full;
                            cc = "<button onclick='TahvilBeTolid(\"" + data + "\");'>مصرف</button> ";
                        } else {
                            cc = "<button onclick='HamkaranConfirm(\"" + data + "\");'>ثبت همکاران</button> ";
                        }

                        if (full['desc']['masraf']) {
                            cc = "";
                        }

                        return cc;
                    }
                });


                table = $('#tbl_barcodes').DataTable({
                    "processing": true,
                    "serverSide": true,
                    "order": [[0, "desc"]],
                    "ajax": {
                        "url": urlOfBarcodes,
                        "type": "GET"
                    },
                    "columns": bbdata.data,
                    initComplete: function () {
                        // var sss = "";
                        // for (var v = 0; bbdata.data.length > v; v++) {
                        //     sss +=
                        // }
                        // sss = '<tr id="table_search_area">' + sss + '</tr>';
                        // $("#tbl_barcodes > thead").append(sss);

                        this.api().columns().every(function () {
                            var that = this;
                            var sss = '<br\><input class="search_table_header" type="text" placeholder="جستجو " />';
                            $(that.header()).append(sss);
                        })

                        this.api().columns().every(function () {
                            var that = this;
                            $('input', that.header()).on('keyup change clear', function () {
                                if (that.search() !== this.value) {
                                    that
                                        .search(this.value)
                                        .draw();
                                }
                            });
                        });
                    }
                });
            })
            // $http.get("/api/v1/barcodes/").then(function (data) {
            //     $scope.barcodes = data.data;
            // })

        }


        $scope.init();

        $scope.postHamkaranNo = function (barcodeID, hamkaranSanadNo) {
            // console.log(barcodeID);
            // console.log(hamkaranSanadNo);
            $http.post("/api/v1/barcodes/postHamkaranSanadNo/", {
                barcodeID: barcodeID,
                hamkaranSanad: hamkaranSanadNo

            }).then(function (data) {
                if (data.data.result) {
                    table.ajax.reload();
                } else {
                    alert("سند مورد نظر در همکاران سیستم وجود ندارد");
                }
            }).catch(function (data) {
                alert("سند مورد نظر در همکاران سیستم وجود ندارد");
            })
        }

        $scope.SodooreMasraf = function (barcodeID) {
            $http.get("/api/v1/barcodes/" + barcodeID + '/').then(function (data) {
                let ins = data.data;
                $mdDialog.show({
                    controller: DialogController,
                    templateUrl: '/Material/page/popupMasraf/',
                    parent: angular.element(document.body),
                    clickOutsideToClose: true,
                    fullscreen: $scope.customFullscreen,
                    barcodeID: barcodeID,
                    barcodeInstance: ins
                }).then(function (result) {
                    table.ajax.reload();
                })

            })
        }

        function DialogController(
            $scope, $mdDialog, $http,
            $element, $filter,
            barcodeID, barcodeInstance) {

            $scope.masraf = {};
            $scope.masraf.mizan = barcodeInstance.desc.barcode.vazne_khales;

            $scope.confirm = function () {
                $http.post('/api/v1/barcodes/' + barcodeInstance.id + '/postmasraf/', $scope.masraf).then(function (data) {
                    if (data.data.result) {
                        $mdDialog.hide()

                    } else {
                        alert("لطفا شماره سند را صحیح وارد کنید")
                    }
                }).catch(function (data) {
                    alert("لطفا شماره سند را صحیح وارد کنید")
                })
            }


        }


    });

function HamkaranConfirm(id) {
    var scope = angular.element($("#barcodelist")).scope();
    var a = prompt("شماره سند همکاران را وارد نمایید")
    if (a != null) {
        if (a !== '') {
            scope.postHamkaranNo(id, a)
        }
    }
}

function TahvilBeTolid(id) {
    var scope = angular.element($("#barcodelist")).scope();
    scope.SodooreMasraf(id);
}