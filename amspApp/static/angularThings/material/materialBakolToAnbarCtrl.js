'use strict';


angular.module('AniTheme').controller(
    'MaterialBakolToAnbarCtrl',
    function ($scope,
              $translate,
              $http, $filter,
              $q, $mdDialog,
              $rootScope,toastConfirm,
              $modal) {

        let urlOfBarcodes = "/api/v1/barcodes/";

        $scope.goods = [];
        $scope.list = function () {
            $http.get(urlOfBarcodes + "list_unlocated_goods/").then(function (data) {
                $scope.goods = data.data;
            })
        }

        $scope.http = $http;

        $scope.search_barcode = '';


        $scope.$watch('search_barcode', function (data) {
            $scope.list();
        })


        $scope.init = function () {
            $scope.list();
        }

        $scope.qcmustsee = function (item, ev, $index) {
            $mdDialog.show({
                controller: findQC_Claim,
                templateUrl: 'findQC_Claim',
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                currentSelection: item,
                fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
            })
                .then(function (answer) {
                    if (answer === 'good_stay_in_location_with_QC_argue') {
                        $scope.list();
                        // $scope.goods.splice($index, 1);
                    }
                    if (answer === 'good_moved_another_location_with_QC_argue') {
                        $scope.list();
                        // $scope.goods.splice($index, 1);
                    }
                    // $scope.status = 'You said the information was "' + answer + '".';
                }, function () {
                    // $scope.status = 'You cancelled the dialog.';
                });
        }

        $scope.GoodStayInLocation = function (item, $index) {
           toastConfirm.showConfirm("آیا شما اطمینان دارید ؟").then(function () {
                $http.get("/api/v1/warehouse/" + item.barcode + "/good_stay_in_location/").then(
                    function (data) {
                        if (data.data.result) {
                            $rootScope.$broadcast("showToast", "با موفقیت انجام شد");
                            $scope.list();
                        }
                    }
                )


            })

        }


        $scope.testws = function () {
            $http.get(urlOfBarcodes + "send_test_ws/").then(
                function (data) {

                }
            )

        }

        $scope.removeByNotification = function (id) {
            let index = -1;

            for (let i = 0; $scope.goods.length > i; i++) {
                if ($scope.goods[i]['id'] === id) {
                    index = i;
                }
            }

            if (index !== -1) {
                $scope.goods.splice(index, 1);
            }
        }

        $scope.addToAnbarList = function (barcode) {
            $http.get("/api/v1/barcodes/" + barcode + "/").then(function (data) {
                if (data.data.id) {
                    $scope.goods.push(data.data)
                }

            })
        }

        function findQC_Claim($scope, $mdDialog, $http, currentSelection) {


            $scope.good_stay_in_location_with_QC_argue = function () {

                $http.get("/api/v1/warehouse/" + currentSelection.barcode + "/good_stay_in_location_with_QC_argue/").then(function (data) {
                    if (data.data.result) {
                        $mdDialog.hide('good_stay_in_location_with_QC_argue');

                    }
                })
            }

            $scope.good_moved_another_location_with_QC_argue = function () {

                $http.get("/api/v1/warehouse/" + currentSelection.barcode + "/good_moved_another_location_with_QC_argue/").then(function (data) {
                    if (data.data.result) {
                        $mdDialog.hide('good_moved_another_location_with_QC_argue');

                    }
                })
            }


            $scope.cancel = function () {
                $mdDialog.cancel();
            };
        }


        $scope.init();

        $scope.getChar = function (charpos) {
            var stt = "";
            if (charpos > 90) {
                return (String.fromCharCode(charpos - 26) + String.fromCharCode(charpos - 26))
            }
            return (String.fromCharCode(charpos))
        }
        $scope.checkIntAnbar = function (anbar) {
            if (anbar === undefined) {
                return "-"
            }
            if (anbar < 10) {
                return '0' + anbar.toString();
            }
            return anbar.toString();
        }


    })