'use strict';

angular.module('AniTheme').controller(
    'TopNavCtrl',
    function ($scope,
              $translate,
              $q,
              $http, $mdDialog,
              $location,
              $rootScope,
              $timeout) {

        $scope.status = '  ';
        $scope.customFullscreen = false;

        $scope.selectedStuff = {};
        $rootScope.$on("showBasket", function (event, args) {
            $scope.selectedStuff = args.item;
            $scope.showBasket(event, args.openAdd);
        });

        $rootScope.$on("refreshBasket", function (event, args) {
            $scope.getAllBasket();
        });


        $scope.showBasket = function (ev, asAdd) {
            $mdDialog.show({
                controller: BasketController,
                templateUrl: '/page/saleaddbasket/',
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                stuff: $scope.selectedStuff,
                addItem: asAdd,
                fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
            })
                .then(function (answer) {
                    $scope.getAllBasket();
                }, function () {
                    $scope.getAllBasket();
                });
        };


        $scope.basketItems = {};
        $scope.getAllBasket = function () {
            $http.get("/api/v1/saleBasket/").then(function (data) {
                $scope.basketItems = data.data;
            })
        };
        $scope.getAllBasket();


        function BasketController($scope, $mdDialog, $http, stuff, addItem) {

            $scope.basketItem = stuff;
            $scope.addPanel = addItem;
            // debugger;
            //


            $scope.delFromBasket = function (ev, item) {
                if (confirm("آبا از حذف آیتم انتخاب شده از سبد مورد نظر اطمینان دارید ؟")) {
                    $http.delete("/api/v1/saleBasket/" + item.id + "/").then(function () {
                        $scope.getAllBasket();
                    })
                }
            }


            $scope.addToBasket = function () {

                if ($scope.basketItem.desc.itemID.length != 14) {
                    alert('کد محصول را صحیح وارد نمایید');
                    return
                }

                if ($scope.basketItem.id) {
                    $http.patch("/api/v1/saleBasket/" + $scope.basketItem.id + "/", $scope.basketItem).then(function (data) {
                        if (data.data.id) {
                            $scope.showList();
                        } else {
                            alert("مقدار انتخابی شما بیش از موجودی است")
                        }
                    }).catch(function () {
                        alert("مقدار انتخابی شما بیش از موجودی است")
                    })
                } else {
                    $http.post("/api/v1/saleBasket/", $scope.basketItem).then(function (data) {
                        if (data.data.id) {
                            $scope.showList();
                        } else {
                            alert("مقدار انتخابی شما بیش از موجودی است")
                        }
                    }).catch(function () {
                        alert("مقدار انتخابی شما بیش از موجودی است")
                    })
                }
            };

            $scope.basketItemEdit = function (item) {
                $scope.basketItem = item;
                $scope.addPanel = true;
            }

            $scope.showList = function () {
                $scope.getAllBasket();
                $scope.addPanel = false;
            };

            $scope.basketItems = {};
            $scope.getAllBasket = function () {
                $http.get("/api/v1/saleBasket/").then(function (data) {
                    $scope.basketItems = data.data;
                })
            };
            $scope.getAllBasket();

            $scope.showBasketItems = function () {

            };


            $scope.hide = function () {
                $mdDialog.hide();
            };

            $scope.cancel = function () {
                $mdDialog.cancel();
            };

            $scope.answer = function (answer) {
                $mdDialog.hide(answer);
            };
        }


    });
