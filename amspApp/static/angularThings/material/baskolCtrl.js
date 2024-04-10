'use strict';


angular.module('AniTheme').controller(
    'MaterialBaskolCtrl',
    function ($scope,
              $translate,
              $http, $filter,
              $q, $mdDialog, $element,
              $rootScope,
              $modal) {

        $scope.locations = [];
        $scope.tablecalled = false;


        $scope.change_z = function (index) {
            $scope.z = index + 1;
            $scope.listBarcodeBy_xyz();
        }

        $scope.light_location_info = [];
        $scope.setCurrentLocation = function (item) {
            $http.get("/api/v1/warehouse/" + item.id + "/get_location/").then(function (data) {
                $scope.currentLocation = data.data;
                $scope.listBarcodeBy_xyz();

            })
        }


        $scope.init = function () {
            $http.get("/api/v1/warehouse/list_warehouses/").then(function (data) {
                $scope.locations = data.data;
            })
        }

        $scope.http = $http;
        $scope.updateCellWS = function (barcodeInstanceID) {
            $http.get('/api/v1/barcodes/' + barcodeInstanceID + '/').then(function (data) {
                if (data.data.id) {
                    angular.element(document.getElementById("td_" + data.data.x + "_" + data.data.z + "_" + data.data.y)).scope().cr = data.data;

                    // debugger;
                    // for (let i = 0; $scope.barcodes.length > i; i++) {
                    //
                    //     if ($scope.barcodes[i]['id'] === data.data.id) {
                    //         $scope.barcodes[i] = data.data;
                    //
                    //
                    //         // if (data.data.position === 6322344 || data.data.position === 7463333) {
                    //         //     angular.element(document.getElementById("td_" + data.data.x + "_" + data.data.z + "_" + data.data.y)).scope().cr = {
                    //         //         x: data.data.x,
                    //         //         y: data.data.y,
                    //         //         z: data.data.z,
                    //         //     }
                    //         // }
                    //     }
                    // }
                }

            }, function (data) {

            })
        }

        // $scope.changeIt = function () {
        //     $http.get("/api/v1/warehouse/" + current + "/get_location/").then(function (data) {
        //         $scope.currentLocation = data.data;
        //     })
        // }

        $scope.getChar = function (charpos) {
            var stt = "";
            if (charpos > 90) {
                return (String.fromCharCode(charpos - 26) + String.fromCharCode(charpos - 26))
            }
            return (String.fromCharCode(charpos))
        }

        $scope.checkIntAnbar = function (anbar) {
            if (anbar < 10) {
                return '0' + anbar.toString();
            }
            return anbar.toString();
        }


        $scope.init();


        $scope.z = 1;
        $scope.openLocation = function (ev, x, y, locationTitle) {

            $mdDialog.show({
                controller: DialogController,
                templateUrl: '/Material/page/popupBaskol/',
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                currentLocation: $scope.currentLocation,
                location: {'x': x, "y": y, 'z': $scope.z, locationTitle},
                fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
            }).then(function (result) {
                // $scope.listBarcodeBy_xyz();
            }, function () {
                // $scope.listBarcodeBy_xyz();
            });
        }

        $scope.barcodes = [];
        $scope.listBarcodeBy_xyz = function () {
            $scope.barcodes = [];
            $scope.tablecalled = false;
            $http.get("/api/v1/warehouse/" + $scope.currentLocation.id + "/listBarcodeBy_xyz/").then(function (data) {
                // $scope.barcodes = data.data;
                // debugger;
                for (let i = 0; data.data.length > i; i++) {
                    let hhh = {};
                    hhh = data.data[i];
                    hhh.confirmVazn = data.data[i].desc.barcode.confirm_vazn;
                    hhh.partnum = data.data[i].desc.product.Code.substring(0, 9);
                    $scope.barcodes.push(hhh);
                }
                $scope.tablecalled = true;
            })
        }

        $scope.get_cell = function (x, y, z) {
            let res = $scope.barcodes.filter(function (d) {
                return d.x === x && d.y === y && d.z === z
            });

            let result = {x: x, y: y, z: z};
            if (res.length > 0) {
                result = res[0];
            }
            return result
        }

        function DialogController($scope, $mdDialog, $http, $element, $filter, currentLocation, location) {
            $scope.getAnbars = function () {
                $http.get("/api/v1/warehouse/get_anbars/").then(function (data1) { // انبارها
                    $scope.hamkaran_anbars = data1.data;
                })
            }

            var triggerAssgned = false;
            $scope.AddScanBarname = function () {
                if (triggerAssgned === false) {
                    $scope.attachChangeEvent();
                }
                $("#ScanBarnameh").click();
            }

            $scope.attachChangeEvent = function () {
                if (Boolean($("#ScanBarnameh")[0])) {
                    triggerAssgned = true;
                    $("#ScanBarnameh").change(function () {
                        if ($("#ScanBarnameh").val()) {
                            var frmData = new FormData();
                            frmData.append("pic", $("#ScanBarnameh")[0].files[0]);
                            $("#ScanBarnamehDiv").html("<i id='dsadasdasdafreg' class='fa fa-refresh fa-5x fa-spin'></i> ");
                            $.ajax({
                                url: '/api/v1/file/upload/',
                                type: 'POST',
                                data: frmData,
                                contentType: false,
                                processData: false,
                                success: function (data) {
                                    if (data.name) {
                                        $scope.barcode.barnamehUrl = data.name;
                                        $("#ScanBarnamehDiv").html('');
                                    } else {
                                        $scope.barcode.barnamehUrl = '';
                                        $("#ScanBarnamehDiv").html('');
                                    }
                                }
                            });
                        }
                    });

                }

            }


            // ------------------------------------------------------
            // ------------------------------------------------------
            // ------------------------------------------------------
            // ------------------------------------------------------

            // $scope.vegetables = ['Corn', 'Onions', 'Kale', 'Arugula', 'Peas', 'Zucchini'];
            $scope.search_acc_dls;
            $scope.clearSearchTerm = function () {
                $scope.search_acc_dls = '';
            };
            // The md-select directive eats keydown events for some quick select
            // logic. Since we have a search input here, we don't need that logic.
            $element.find('#thisissearchstop').on('keydown', function (ev) {
                ev.stopPropagation();
            });

            $scope.$watch('search_acc_dls', function (dt) {
                $scope.get_accdls()
            })

            $scope.accdls = [];
            $scope.get_accdls = function () {
                $http.get("/api/v1/warehouse/get_accdls/?q=" + $scope.search_acc_dls).then(function (data) {
                    $scope.accdls = data.data;
                })
            }
            // ------------------------------------------------------
            // ------------------------------------------------------
            // ------------------------------------------------------
            // ------------------------------------------------------


            $scope.getCurrentDate = function () {
                return $filter('jalaliDate')(currentDatetime(), 'jYYYY/jMM/jDD HH:mm');
            };

            $scope.cancel = function () {
                $mdDialog.hide();
            }


            $scope.hamkaran_anbars = [];
            $scope.init = function () {
                // $scope.get_vendors();
                // در اینجا باید واحدهای سنجنش
                // طبقات حساب
                // و نوع کالاها را دریافت کنیم
                // و همجنین لیستی از انبارها

                $scope.attachChangeEvent();

                $scope.loadedBarcode = {};
                $scope.get_accdls();
                $http.post('/api/v1/warehouse/get_barcode_by_location/', {
                    location: location,
                    currentLocation: currentLocation
                }).then(function (data) {
                    if (data.data['id']) {
                        $scope.currentPanel = 4;
                        $scope.loadedBarcode = data.data;
                    } else {
                        $http.get("/api/v1/warehouse/get_anbars/").then(function (data1) { // انبارها
                            $scope.hamkaran_anbars = data1.data;
                            $http.get("/api/v1/warehouse/get_InvMUnit/").then(function (data2) { // واحدهای وزن ها
                                $scope.units = data2.data;
                                $http.get("/api/v1/warehouse/get_InvvwPartType/").then(function (data3) { // دریافت نوع کالاها
                                    $scope.parttypes = data3.data;
                                    $http.get("/api/v1/warehouse/get_InvAccCtgry/").then(function (data4) { // دریافت طبقات حساب ها
                                        $scope.acccats = data4.data;
                                    });
                                });
                            });

                        });
                    }

                });


            }
            $scope.init();

            $scope.currentPanel = 1;

            $scope.checkBoxCallBack = function (node) {

                $http.post("/api/v1/warehouse/post_location/", {node: node, part: $scope.PART}).then(function (data) {
                    $http.get("/api/v1/warehouse/get_anbars_of_reg/?q=" + $scope.PART.Serial).then(function (data1) { // انبارها
                        $scope.hamkaran_anbars_registered = data1.data;
                    })
                });


            }

            $scope.PART = {};
            $scope.msg = {};

            $scope.deleteFromBar = function (item) {
                $http.post("/api/v1/warehouse/delete_anbars_of_reg/", item).then(function (data) {
                    $http.get("/api/v1/warehouse/get_anbars_of_reg/?q=" + $scope.PART.Serial).then(function (data1) { // انبارها
                        $scope.hamkaran_anbars_registered = data1.data;
                    })
                })
            }

            $scope.confirm = function () {
                $scope.msg = {};
                // $scope.PART.Code = $scope.Code;
                $http.post("/api/v1/warehouse/post_part/", $scope.PART).then(function (data) {
                    if (data.data.posted_data) {

                        // $scope.PART.Code = $scope.Code;
                        // debugger;
                        $scope.getByCode(data.data.posted_data);
                        $http.get("/api/v1/warehouse/get_anbars_of_reg/?q=" + data.data.posted_data.Serial).then(function (data1) { // انبارها
                            $scope.hamkaran_anbars_registered = data1.data;
                        })
                    } else {
                        console.log($scope.msg);
                        $scope.msg = {"msg": "کد کالا و یا شرح کالا قبلا ثبت شده است لطفا نام دیگری انتخاب کنید و یا از همان نام قبلی استفاده کنید"}
                    }


                }).catch(function () {
                    console.log($scope.msg);
                    $scope.msg = {"msg": "کد کالا و یا شرح کالا قبلا ثبت شده است لطفا نام دیگری انتخاب کنید و یا از همان نام قبلی استفاده کنید"}

                })
            }

            $scope.setMahal = function () {
                $http.get("/api/v1/warehouse/get_anbars_of_reg/?q=" + $scope.PART.Serial).then(function (data1) { // انبارها
                    $scope.hamkaran_anbars_registered = data1.data;
                    $scope.currentPanel = 2;
                })
            }

            $scope.setBarcode = function () {

                $scope.currentPanel = 3;

            }


            $scope.getByCode = function (ins) {

                $http.post('/api/v1/warehouse/get_PartInstance_By_PartNo/', {partno: ins.Code}).then(function (data) {
                    if (data.data.Code) {
                        $scope.PART = data.data;
                    } else {
                        $scope.PART = {};
                        // $scope.Code = ddd;

                    }
                })
            }

            $scope.PART = {};
            $scope.Code = '';

            $scope.$watch('Code', function (dtt) {
                if (dtt) {
                    if (dtt.length > 13) {
                        // if ($scope.PART.Code) {
                        $http.post('/api/v1/warehouse/get_PartInstance_By_PartNo/', {partno: dtt}).then(function (data) {
                            if (data.data.Code) {
                                $scope.PART = data.data;
                            } else {
                                $scope.PART = {};
                            }
                        })
                        // }
                    }

                }
            })


            $scope.blockLocation = function () {
                $http.post("/api/v1/warehouse/block_location/", {
                    location: location,
                    currentLocation: currentLocation
                }).then(function (data) {

                }).cache(function (data) {

                })
            }


            $scope.barcode = {};
            $scope.confirmBarcode = function () {
                if (!($scope.barcode['dateOf'])) {
                    return
                }
                if (!($scope.barcode['shomare_barnameh'])) {
                    return
                }
                if (!($scope.barcode['barnamehUrl'])) {
                    return
                }
                if (!($scope.barcode['size_varagh'])) {
                    return
                }
                if (!($scope.barcode['vazne_khales'])) {
                    return
                }
                if (!($scope.barcode['shomare_kalaf'])) {
                    return
                }

                $http.post("/api/v1/warehouse/create_barcode/",
                    {
                        barcode: $scope.barcode,
                        product: $scope.PART,
                        location: location,
                        currentLocation: currentLocation
                    }).then(function (data) {
                    if (data.data.url) {
                        // Object.assign(document.createElement('a'), { target: '_blank', href: data.data.url}).click();
                        var link = document.createElement('a');
                        link.href = data.data.url;
                        link.download = 'file.pdf';
                        link.dispatchEvent(new MouseEvent('click'));
                        $mdDialog.hide();
                        // $('a').attr('target', '_blank').get(data.data.url).click();
                        // downloadURL()
                    }

                })

            }
            $scope.printBarcodeAgain = function () {
                var link = document.createElement('a');
                link.href = '/static/barcodes/' + $scope.loadedBarcode.barcode + '.pdf';
                link.download = $scope.loadedBarcode.barcode + '.pdf';
                link.dispatchEvent(new MouseEvent('click'));

            }

            $scope.deleteBarcode = function () {
                if (confirm('آیا از حذف این بار کد اطمینان دارید ؟')) {
                    $http.delete('/api/v1/warehouse/' + $scope.loadedBarcode.barcode + '/deletebarcode/').then(
                        function (data) {
                            $mdDialog.hide();
                        });
                }

            }


            $scope.GoodStayInLocation = function () {
                $http.get("/api/v1/warehouse/" + $scope.loadedBarcode.barcode + "/good_stay_in_location/").then(
                    function (data) {
                        if (data.data.result) {
                            $mdDialog.hide();
                        }
                    }
                )

            }
            $scope.ConfirmVazn = function () {
                var vazn = prompt("وزن تایید شده را تایید نمایید", $scope.loadedBarcode.desc.barcode.vazne_khales);


                if (vazn) {
                    $http.post("/api/v1/warehouse/" + $scope.loadedBarcode.barcode + "/taeed_vazn/",
                        {vazn: $scope.loadedBarcode.desc.barcode.vazne_khales}
                    ).then(
                        function (data) {
                            if (data.data.result) {
                                $mdDialog.hide();
                            } else {
                                alert('لطفا عدد را به درستی وارد نمایید')
                            }
                        }
                    ).catch(function (data) {
                        alert('لطفا عدد را به درستی وارد نمایید')

                    })
                }


            }
        }


    });