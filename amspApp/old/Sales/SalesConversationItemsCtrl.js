'use strict';
angular.module('AniTheme')
    .controller(
        'SalesConversationItemsCtrl',
        function ($scope, $window, $http, $q, $log, $element, $translate, $rootScope, $stateParams, $location, $$$, $filter, $mdDialog, Upload) {


            $scope.currentProfile = {};
            $scope.getConv = function () {
                $http.get("/api/v1/salesConv/" + $stateParams.ConvID + "/").then(function (data) {
                    $scope.currentConv = data.data;
                    $http.get("/api/v1/salesProfile/" + $scope.currentConv.customerLink.id + "/").then(function (data) {
                        $scope.customer = data.data;
                        $scope.getFactors();
                    });
                });
            };
            $scope.getConv();


            $scope.factors = [];
            $scope.getFactors = function () {
                if ($scope.customer.hamkaranCode) {
                    $http.get("/api/v1/salesProfile/" + $scope.customer.hamkaranCode + "/getCustomerHamkaran/").then(function (data) {
                        $scope.factors = data.data;
                    })
                }
            };

            $scope.getFromBasket = function () {
                $http.get("/api/v1/salesItems/" + $stateParams.ConvID + "/addFromBasket/").then(function () {
                    $scope.listProduct();
                    $rootScope.$emit("refreshBasket", {});

                })
            };


            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            $scope.UploadedFiles = [];
            $scope.Scans = {};
            $scope.Scan = {};
            loadUploader($scope, $http, Upload);
            $scope.showUploader = function () {
                $("#divFiles").fadeOut(function () {
                    $("#divUploader").fadeIn();
                });
            };
            $scope.cancelFiles = function () {

                $("#divUploader").fadeOut(function () {
                    $("#divFiles").fadeIn();
                });

            }
            $scope.RemoveFromUploaded = function (ev, index) {

                var confirm = $mdDialog.confirm()
                    .title('حذف فایل')
                    .textContent('فایل مورد نظر حذف شود ؟')
                    .ariaLabel('حذف فایل')
                    .targetEvent(ev)
                    .ok('حذف شود')
                    .cancel('انصراف');

                $mdDialog.show(confirm).then(function (result) {

                    $scope.currentConv.Files.uploaded.splice(index, 1);

                    $http.patch("/api/v1/salesConv/" + $scope.currentConv.id + "/", {
                        Files: {
                            uploaded: $scope.currentConv.Files.uploaded
                        }
                    }).then(function () {

                    })
                }, function () {
                    $scope.status = 'You didn\'t name your dog.';
                });


            }
            $scope.saveFiles = function () {
                var final = [];
                angular.forEach($scope.UploadedFiles, function (value, key) {
                    final.push(value);
                });
                final = angular.copy($scope.UploadedFiles);
                if ($scope.currentConv.Files) {
                    if ($scope.currentConv.Files.uploaded) {
                        for (var i = 0; $scope.currentConv.Files.uploaded.length > i; i++) {
                            final.push($scope.currentConv.Files.uploaded[i]);
                        }
                    }
                }


                $http.patch("/api/v1/salesConv/" + $scope.currentConv.id + "/", {
                    Files: {
                        uploaded: final
                    }
                }).then(function () {
                    $scope.currentConv.Files = {};
                    $scope.currentConv.Files.uploaded = final;
                    $("#divUploader").fadeOut(function () {
                        $("#divFiles").fadeIn();
                    });
                })
            };


            $scope.addNewProduct = function () {
                $("#ProductsList").fadeOut(function () {
                    $("#divAddEditProduct").fadeIn();
                });
            };
            $scope.addNewConv = function () {
                $("#convTimeLine").fadeOut(function () {
                    $("#addConv").fadeIn();
                });
            };
            $scope.currentConv = {};
            $scope.getCustomerName = function () {
                $http.get("/api/v1/salesConv/" + $stateParams.ConvID + "/").then(function (data) {
                    $scope.currentConv = data.data;
                    if ($scope.currentConv.uploaded) {
                        $scope.UploadedFiles = $scope.currentConv.uploaded;
                    }
                })
            };
            $scope.getCustomerName();
            $scope.$watchCollection("products", function () {
                if ($scope.products) {
                    if ($scope.products.results) {
                        $scope.sum = 0;
                        var sum = 0;
                        for (var i = 0; $scope.products.results.length > i; i++) {
                            sum += (($scope.products.results[i].amount * $scope.products.results[i].fee) - $scope.products.results[i].off)
                            $scope.sum = sum;
                        }
                    }

                }
            });


            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            $scope.conv = {};
            $scope.postConv = function () {
                $scope.conv.saleConversationLink = $stateParams.ConvID;
                if ($scope.conv.id) {
                    $http.patch("/api/v1/salesComments/" + $scope.conv.id + "/", $scope.conv).then(function (data) {

                        $scope.conv = {};
                        $scope.listConv();
                    })

                } else {

                    $http.post("/api/v1/salesComments/", $scope.conv).then(function (data) {
                        // $("#addConv").fadeOut(function () {
                        //     $("#convTimeLine").fadeIn();
                        // });
                        $scope.conv = {};
                        $scope.listConv();
                    })

                }
            };
            $scope.Convs = {};
            $scope.listConv = function () {
                $http.get("/api/v1/salesComments/?convID=" + $stateParams.ConvID).then(function (data) {
                    $scope.Convs = data.data;
                })
            };
            $scope.listConv();
            $scope.editConv = function (item) {
                $("#convTimeLine").fadeOut(function () {
                    $("#addConv").fadeIn();
                });
                $scope.conv = item;
            };
            $scope.cancelConv = function () {
                $scope.conv = {};
            };
            $scope.deleteConv = function (ev, conv) {
                var confirm = $mdDialog.confirm()
                    .title('حذف نظر')
                    .textContent('نظر مورد نظر حذف شود ؟')
                    .ariaLabel('حذف نظر')
                    .targetEvent(ev)
                    .ok('حذف شود')
                    .cancel('انصراف');

                $mdDialog.show(confirm).then(function (result) {
                    $http.delete("/api/v1/salesComments/" + conv.id + "/").then(function () {
                        $scope.listConv();
                    })
                }, function () {
                    $scope.status = 'You didn\'t name your dog.';
                });

            };
            $scope.listReplays = function (item) {
                $http.get("/api/v1/salesComments/" + item.id + "/getReplays/").then(function (data) {
                    item.replays = data.data;
                })
            }
            $scope.removeReplay = function (parentItem, item, ev) {

                var confirm = $mdDialog.confirm()
                    .title('حذف نظر')
                    .textContent('نظر مورد نظر حذف شود ؟')
                    .ariaLabel('حذف نظر')
                    .targetEvent(ev)
                    .ok('حذف شود')
                    .cancel('انصراف');
                $mdDialog.show(confirm).then(function (result) {
                    $http.get("/api/v1/salesComments/removeReplay/?replayID=" + item.id).then(function () {
                        $scope.listReplays(parentItem);
                    })
                }, function () {
                    $scope.status = 'You didn\'t name your dog.';
                });
            }
            $scope.replayConv = function (ev, conv) {

                // Appending dialog to document.body to cover sidenav in docs app
                var confirm = $mdDialog.prompt()
                    .title('نظر شما')
                    .textContent('نظر خود را وارد نمایید')
                    .placeholder('نظر')
                    .ariaLabel('نظر')
                    .initialValue('')
                    .targetEvent(ev)
                    .ok('تایید')
                    .cancel('انصراف');

                $mdDialog.show(confirm).then(function (result) {
                    $http.post("/api/v1/salesComments/" + conv.id + "/AddToReplay/", {
                        comment: result.data
                    }).then(function (data) {
                        $scope.listReplays(conv)

                    })

                    $scope.status = 'You decided to name your dog ' + result.data + '.';
                }, function () {
                    $scope.status = 'You didn\'t name your dog.';
                });


            }

            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            setupAutoComplete($scope, $http, $q, $log, "selectedItem");
            $scope.product = {};
            $scope.selectedItem = {};
            $scope.removeHamkaran = function () {
                $scope.selectedItem.PartCode = "";
                $scope.selectedItem.PartName = "";
            }
            $scope.AddToList = function () {
                $scope.product.saleConversationLink = $stateParams.ConvID;
                $scope.product.itemID = $scope.selectedItem.PartCode;
                $scope.product.itemName = $scope.selectedItem.PartName;
                // if (!($scope.selectedItem.PartCode)) {
                //     swal("خطا", "لطفا کالا را انتخاب نمایید", "error");
                //     return
                // }
                if ($scope.product.id) {
                    $http.patch("/api/v1/salesItems/" + $scope.product.id + "/?convID=" + $stateParams.ConvID, $scope.product).then(function (data) {
                        $("#divAddEditProduct").fadeOut(function () {
                            $("#ProductsList").fadeIn();
                        });

                        $scope.listProduct();
                        $scope.product = {};
                    })
                } else {
                    $http.post("/api/v1/salesItems/", $scope.product).then(function (data) {
                        $("#divAddEditProduct").fadeOut(function () {
                            $("#ProductsList").fadeIn();
                        });

                        $scope.listProduct();
                        $scope.product = {};
                    })
                }
            }
            $scope.products = {};
            $scope.wait = false;
            $scope.listProduct = function () {
                $scope.wait = true;
                $http.get("/api/v1/salesItems/?convID=" + $stateParams.ConvID).then(function (data) {
                    $scope.wait = false;
                    $scope.products = data.data;
                })
            }
            $scope.editProduct = function (product) {
                $scope.product = product;
                $scope.selectedItem = {};
                $scope.selectedItem.PartName = product.itemName;
                $scope.selectedItem.PartCode = product.itemID;
                $("#ProductsList").fadeOut(function () {
                    $("#divAddEditProduct").fadeIn();
                });

            }
            $scope.CancelProduct = function () {
                $scope.product = {};
                $scope.selectedItem = {};
                $("#divAddEditProduct").fadeOut(function () {
                    $("#ProductsList").fadeIn();
                });

            }
            $scope.listProduct();
            $scope.deleteProduct = function (ev, product) {
                var confirm = $mdDialog.confirm()
                    .title('حذف کالا')
                    .textContent('کالای مورد نظر حذف شود ؟')
                    .ariaLabel('حذف کالا')
                    .targetEvent(ev)
                    .ok('حذف شود')
                    .cancel('انصراف');

                $mdDialog.show(confirm).then(function (result) {
                    $http.delete("/api/v1/salesItems/" + product.id + "/").then(function () {
                        $scope.listProduct();
                    })
                }, function () {
                    $scope.status = 'You didn\'t name your dog.';
                });

            }
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------


        });