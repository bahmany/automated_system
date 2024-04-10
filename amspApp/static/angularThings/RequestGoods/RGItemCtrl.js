'use strict';

angular.module('AniTheme').controller(
    'RGItemCtrl',
    function ($scope,
              $translate,
              $q,
              $state,
              $http,
              $location, $mdDialog,
              $rootScope, $stateParams,
              $timeout) {

        $scope.status = '  ';
        $scope.customFullscreen = false;
        $scope.requestItems = [];
        $scope.request = {};
        $scope.draft = true;
        $scope.selectedWorkflow = 0;
        $scope.selectedWorkflowEngine = {};
        $scope.tableOfSigns = [];
        $scope.flatSigns = [];
        $scope.approve = [];
        $scope.allitem = {};

        //
        // oonhayee ke bayad zakhireh shavand
        //
        //
        $scope.getTable = function () {
            $http.get("/api/v1/rg/listOfRequest/").then(function (data) {
                if (data.data.s) {
                    $scope.tableOfSigns = data.data.s;
                    $scope.flatSigns = data.data.flat;
                    $scope.refreshSigns();
                    if ($scope.draft === false) {
                        $scope.selectedSign = $scope.flatSigns.filter(function (d) {
                            return d.value === $scope.selectedWorkflow;
                        })[0];

                    }

                }
                // $scope.goodItems = data.data;
            })
        }


        $scope.addNewItem = function () {
            $scope.requestItems.push({})
        }


        $scope.init = function () {
            if ($stateParams.idof !== "1") {
                $http.get("/api/v1/rg/" + $stateParams.idof + "/").then(function (data) {
                    if (data.data.id) {
                        $scope.allitem = data.data;
                        $scope.pite = data.data;
                        $scope.selectedWorkflow = data.data.rgType;
                        $scope.requestItems = data.data.exp.requestItems;
                        $scope.draft = data.data.draft;
                        $scope.approve = data.data.signs;
                        $scope.getTable();

                    }
                })
            } else {
                $scope.getTable();
                $scope.allitem = {};
                $scope.selectedWorkflow = 0;
                $scope.requestItems = [];
                $scope.draft = true;
                $scope.approve = [];
            }
        }

        $scope.init();


        $scope.uploadDarkhastKharid = function () {
            $http.post("/api/v1/rg/" + $stateParams.idof + "/uploadDarkhastKharid/", $scope.allitem.exp).then(function (data) {
                if (data.data.errcode) {
                    sweetAlert("خطا", data.data.msg, "warning");
                }
                if (data.data.id) {
                    $scope.init();
                }

            }).catch(function (e) {

            })
        }
        $scope.requesterGetThis = function () {
            $http.get("/api/v1/rg/" + $stateParams.idof + "/requesterGetThis/").then(function (data) {
                if (data.data.errcode) {
                    sweetAlert("خطا", data.data.msg, "warning");
                }
                if (data.data.id) {
                    $scope.init();
                }

            }).catch(function (e) {

            })
        }

        $scope.taminAcceptedDates = function () {
            $http.post("/api/v1/rg/" + $stateParams.idof + "/taminAcceptedDates/", $scope.allitem.exp).then(function (data) {
                if (data.data.errcode) {
                    sweetAlert("خطا", data.data.msg, "warning");
                }
                if (data.data.id) {
                    $scope.init();
                }

            }).catch(function (e) {

            })
        }


        $scope.thisMustTamin = function () {
            $http.get("/api/v1/rg/" + $stateParams.idof + "/thisMustTamin/").then(function (data) {
                if (data.data.errcode) {
                    sweetAlert("خطا", data.data.msg, "warning");
                }
                if (data.data.id) {
                    $scope.init();
                }

            }).catch(function (e) {

            })
        }

        $scope.postDraftFirstStep = function () {
            $http.post("/api/v1/rg/postDraftFirstStep/", {
                "selectedItem": $scope.selectedWorkflow,
                "requestItems": $scope.requestItems,
                "id": $stateParams.idof
            }).then(function (data) {
                if (data.data.id) {
                    $scope.init();
                }

            }).catch(function (err) {

            });
        }
        $scope.postStartFirstStep = function () {
            $http.post("/api/v1/rg/postStartFirstStep/", {
                "selectedItem": $scope.selectedWorkflow,
                "requestItems": $scope.requestItems,
                "id": $stateParams.idof
            }).then(function (data) {
                if (data.data.errcode) {
                    sweetAlert("خطا", data.data.msg, "warning");
                }
                if (data.data.id) {
                    $state.go("request-goods-item", {idof: data.data.id});
                }

            }).catch(function (err) {
                sweetAlert("خطا", "لطفا صفحه را رفرش کنید", "warning");

            });
        }


        $scope.changeWork = function (newVal) {
            $scope.selectedWorkflow = newVal;
        }

        $scope.refreshSigns = function () {
            if ($scope.flatSigns.length > 0) {
                for (var i = 0; i < $scope.flatSigns.length; i++) {
                    if ($scope.flatSigns[i].value === $scope.selectedWorkflow) {
                        $scope.selectedWorkflowEngine = $scope.flatSigns[i];
                    }
                }
            }
        }

        $scope.$watch("selectedWorkflow", (prev, next) => {
            $scope.refreshSigns()
        });

        var thisItem;
        $scope.uploadfile = function (item) {
            document.getElementById("fileUpload").click();
            thisItem = item;

        }


        $scope.removeFile = function (item) {
            item.exp.files = null;
        }


        $("#fileUpload").change(function () {
            if ($("#fileUpload").val()) {
                var frmData = new FormData();
                frmData.append("pic", fileUpload.files[0]);

                $.ajax({
                    url: '/api/v1/file/upload/',
                    type: 'POST',
                    data: frmData,
                    contentType: false,
                    processData: false,
                    success: function (data) {
                        if (!(thisItem.exp)) {
                            thisItem.exp = {};
                        }
                        thisItem.exp.files = {
                            link: "/api/v1/file/upload?q=" + data.name,
                            thumb: "/api/v1/file/upload?q=thmum200_" + data.name
                        }
                        $scope.$apply();

                    },
                    error: function (data) {
                        swal("خطا", "لطفا فایل دیگری را انتخاب کنید", "error")
                    }
                });
            }
        });

        $scope.showGoods = function (ev, item) {
            var thisItem = item;
            $mdDialog.show({
                controller: DialogController,
                templateUrl: '/page/RGgoods/',
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                currentLine: item,
                fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
            })
                .then(function (selected_item) {
                    if (!(thisItem['exp'])) {
                        thisItem['exp'] = {};
                    }
                    thisItem.exp.selectedItem = selected_item;
                    // $scope.status = item;
                }, function () {
                    $scope.status = 'You cancelled the dialog.';
                });
        };

        $scope.removeGoods = function (ev, item, index) {
            $scope.requestItems.splice(index, 1);
        }

        function DialogController($scope, $http, $mdDialog, currentLine) {
            $scope.hide = function () {
                $mdDialog.hide();
            };

            $scope.cancel = function () {
                $mdDialog.cancel();
            };

            $scope.answer = function (answer) {
                $mdDialog.hide(answer);
            };


            $scope.selectIt = function (item) {
                $mdDialog.hide(item);
            }


            $scope.viewMojoodi = function (item) {
                item.item.mojoodi = 0;
                $http.get("/api/v1/rg/" + item.item.PartRef + "/getMojoodi/").then(function (data) {
                    item.item.mojoodi = data.data.sumQty;
                })
            }

            $scope.goodItems = {};
            $scope.isEditing = false;
            $scope.getLatestStocks = function () {
                $scope.isEditing = true;
                $http.get("/api/v1/rg/goodsRefresh/").then(function (data) {
                    $scope.isEditing = false;
                    // $scope.goodItems = data.data;
                }).catch(function (err) {
                    $scope.isEditing = false;

                })
            }


            $scope.$watch("searchStr", (prev, next) => {
                $scope.goodsHamkaranList();
            });
            $scope.searchStr = "";
            $scope.goodsHamkaranList = function () {
                $http.get("/api/v1/rg/goodsHamkaranList/?q=" + $scope.searchStr).then(function (data) {
                    $scope.goodItems = data.data;
                })

            }

            // $scope.goodsHamkaranList();

        }

// -------------------------------------------------------------------
// -------------------------------------------------------------------
// -------------------------------------------------------------------
// -------------------------------------------------------------------
// -------------------------------------------------------------------

        $scope.sign = function (stepNum, ev) {

            $scope.showAdvanced($stateParams.idof, stepNum, ev);
        };

        $scope.makeqrcode = function (signID) {
            return "http://app.****.ir/qr/3_" + signID + "/"
            // return "http://127.0.0.1:8000/qr/3_" + signID + "/"
        }

        $scope.showAdvanced = function (idof, stepID, ev) {
            $mdDialog.show({
                locals: {
                    dataToSend: {
                        stepID: stepID,
                        signType: 1,
                        httppost: '/api/v1/rg/signDarkhast/',
                        idof: idof
                    }
                },
                controller: signBodyCtrl,
                templateUrl: '/page/rgShowSignBodyPrc/',
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
            })
                .then(function (answer) {

                    $http.get('/api/v1/rg/' + idof + '/getDetailSigns/').then(function (data) {
                        $scope.init();
                        // approve.signs = data.data;


                    })

                }, function () {
                    $scope.status = 'You cancelled the dialog.';
                });
        };

// -------------------------------------------------------------------
// -------------------------------------------------------------------
// -------------------------------------------------------------------
// ------------------------------------------------------------------
    })
;
