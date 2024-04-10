'use strict';
angular.module('AniTheme')
    .controller(
        'ConvCtrl',
        function ($scope, $window, $mdMenu, $http, $translate, $rootScope, $stateParams, $location, $$$, $filter, $element, $mdDialog) {




// $scope.getProfile = function () {
//     $http.get("/api/v1/salesProfile/"+$stateParams.)
// }

            $scope.bindfilter = {};
            $scope.bindfilter.temper = true;
            $scope.bindfilter.sath = true;
            $scope.bindfilter.zekhamat = true;
            $scope.bindfilter.arz = true;
            $scope.bindfilter.tool = false;
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------


            $scope.tatboghsearchCustomers = "";
            $scope.$watch("tatboghsearchCustomers", function () {
                $scope.tatboghgetCustomers($scope.tatboghsearchCustomers);
            });
            $scope.tatboghgetCustomers = function () {
                $http.get("/api/v1/salesProfile/?search=" + $scope.tatboghCustomersSearchText + "&page=" + $scope.tatboghpage.toString() + "&page_size=20").then(function (data) {
                    $scope.tatboghCustomers = data.data;
                })
            };
            $scope.tatboghpage = 1;
            $scope.tatboghwait = false;
            $scope.tatboghCustomersPageTo = function (page) {
                $scope.tatboghwait = true;
                if (page) {
                    $http.get(page).then(function (data) {
                        $scope.tatboghwait = false;
                        $scope.tatboghCustomers = data.data;
                    }).catch(function () {
                        $scope.tatboghwait = false;
                    });
                }
            }
            $scope.tatboghCustomersSearchText = "";
            $scope.$watch("tatboghCustomersSearchText", function () {
                $scope.tatboghgetCustomers();
            });
            $scope.tatboghclearSearchTerm = function () {
                $scope.tatboghsearchTerm = '';
            }


            // $scope.hamkaranCustomer = {};
            $scope.tatboghsetCustomer = function (customer) {
                $scope.tatboghConv = customer;
            };


            $scope.tatabogByCustomer = {};
            $scope.wait = false;
            $scope.options = {};
            $scope.tatboghsetTataboghCustomer = function (item) {
                $scope.wait = true;

                $http.get("/api/v1/salesConv/" + item.id + "/getTataboghByCustomer/?f=" +
                    $scope.bindfilter.temper.toString() + "_" +
                    $scope.bindfilter.sath.toString() + "_" +
                    $scope.bindfilter.zekhamat.toString() + "_" +
                    $scope.bindfilter.arz.toString() + "_" +
                    $scope.bindfilter.tool.toString()).then(function (data) {
                    $scope.tatabogByCustomer = data.data;
                    $scope.wait = false;

                })
            };

// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------

            $scope.searchProduct = {};
            $scope.$watchCollection("searchProduct", function () {
                $scope.getCurrentMojoodi();
            });
            $scope.Mojoodi = {};
            $scope.Futures = {};
            $scope.getCurrentMojoodi = function () {
                $scope.wait = true;
                $http.post("/api/v1/salesConv/getMojoodies/", $scope.searchProduct).then(function (data) {
                    if (data.data.msg) {
                        $scope.Mojoodi = data.data.results;
                    }
                    $scope.wait = false;
                })
                $http.post("/api/v1/salesConv/getFutures/", $scope.searchProduct).then(function (data) {
                    if (data.data.msg) {
                        $scope.Futures = data.data.results;
                    }
                    $scope.wait = false;
                })
            };
            $scope.updateCache = function (ev) {
                if ($scope.wait) {
                    return
                }
                $scope.wait = true;
                $http.get("/api/v1/salesConv/refreshCache/").then(function (data) {
                    if (data.data.msg) {

                        $scope.wait = false;

                        $rootScope.$broadcast("showToast", "با موفقیت بروز شد");
                    }
                })
            };

// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------

            $scope.filter = {};
            $scope.filter.active = true;
            $scope.filter.noactive = true;
            $scope.filter.withpish = true;
            $scope.filter.nopish = true;
            $scope.Conv = {};
            $scope.Convs = {};
            $scope.addNew = function (ev) {
                $scope.Conv = {};
                $scope.showModal(ev)
            };

            function DialogController($scope, $mdDialog, $http) {
                $scope.searchCustomers = "";
                $scope.$watch("searchCustomers", function () {
                    $scope.getCustomers($scope.searchCustomers);
                });
                $scope.getCustomers = function () {
                    $http.get("/api/v1/salesProfile/?search=" + $scope.CustomersSearchText + "&page=" + $scope.page.toString() + "&page_size=20").then(function (data) {
                        $scope.Customers = data.data;
                    })
                };
                $scope.page = 1;
                $scope.wait = false;
                $scope.CustomersPageTo = function (page) {
                    $scope.wait = true;
                    if (page) {
                        $http.get(page).then(function (data) {
                            $scope.wait = false;
                            $scope.Customers = data.data;
                        }).catch(function () {
                            $scope.wait = false;
                        });
                    }
                }
                $scope.CustomersSearchText = "";
                $scope.$watch("CustomersSearchText", function () {
                    $scope.getCustomers();
                });


                $scope.Conv = Conv;
                $scope.clearSearchTerm = function () {
                    $scope.searchTerm = '';
                }
                $element.find('#searchCustomer').on('keydown', function (ev) {
                    ev.stopPropagation();
                });

                // $scope.hamkaranCustomer = {};
                $scope.setCustomer = function (customer) {
                    $scope.Conv = customer;
                };

                $scope.hide = function () {
                    $mdDialog.hide();
                };
                $scope.cancel = function () {
                    $mdDialog.cancel();
                };
                $scope.confirmCancel = function () {
                    $mdDialog.hide($scope.Conv);
                };
                $scope.confirm = function () {
                    var cc = {};

                    cc.customerLink = $scope.Conv.id;
                    cc.CustomerName = $scope.Conv.name;
                    cc.HamkaranCode = $scope.Conv.hamkaranCode;

                    if (!(Conv.id)) {
                        $http.post("/api/v1/salesConv/", cc).then(function () {
                            $mdDialog.hide($scope.Conv);
                        })
                    } else {
                        $http.patch("/api/v1/salesConv/" + Conv.id + "/", cc).then(function () {
                            $mdDialog.hide($scope.Conv);
                        })
                    }
                };
            };

            $scope.delete = function (ev, item) {
                var confirm = $mdDialog.confirm()
                    .title('حذف مذاکره')
                    .textContent('مذاکره مورد نظر حذف شود ؟')
                    .ariaLabel('حذف مذاکره')
                    .targetEvent(ev)
                    .ok('حذف شود')
                    .cancel('انصراف');

                $mdDialog.show(confirm).then(function (result) {
                    $http.delete("/api/v1/salesConv/" + item.id + "/").then(function () {
                        $scope.list();
                    })
                }, function () {
                    $scope.status = 'You didn\'t name your dog.';
                });

            };
            var Conv = {};
            $scope.edit = function (ev, Conv) {
                $scope.Conv = Conv;
                $scope.showModal(ev);
            };
            $scope.status = '  ';
            $scope.customFullscreen = false;
            $scope.showModal = function (ev) {
                Conv = $scope.Conv;
                $mdDialog.show({
                    controller: DialogController,
                    templateUrl: '/page/salesConversationsAddNew',
                    parent: angular.element(document.body),
                    targetEvent: ev,
                    clickOutsideToClose: true,
                    Conv: $scope.Conv,
                    fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
                })
                    .then(function (jobItem) {
                        $scope.list();

                    }, function () {
                        $scope.status = 'You cancelled the dialog.';
                    });
            };
            $scope.list = function () {
                $scope.wait = true;
                var filter =
                    ($scope.filter.active).toString() + "-" +
                    ($scope.filter.noactive).toString() + "-" +
                    ($scope.filter.withpish).toString() + "-" +
                    ($scope.filter.nopish).toString();
                $http.get("/api/v1/salesConv/?filter=" + filter + "&search=" + $scope.ConvsSearchText + "&page=" + $scope.page.toString() + "&page_size=20").then(function (data) {
                    $scope.Convs = data.data;
                    $scope.wait = false;
                }).catch(function () {
                    $scope.wait = false;
                })
            };
            $scope.page = 1;
            $scope.wait = false;
            $scope.ConvsPageTo = function (page) {
                $scope.wait = true;
                if (page) {
                    $http.get(page).then(function (data) {
                        $scope.wait = false;

                        $scope.Convs = data.data;
                    }).catch(function () {
                        $scope.wait = false;
                    });
                }
            };
            $scope.ConvsSearchText = "";
            $scope.$watch("ConvsSearchText", function () {
                $scope.list();
            });
            $scope.ignore = function (ev, item) {
                if (!(item.Open)) {
                    $http.patch("/api/v1/salesConv/" + item.id + "/", {
                        Open: true
                    }).then(function () {
                        $scope.list();
                    })
                } else {
                    var confirm = $mdDialog.confirm()
                        .title('رد مذاکره')
                        .textContent('مذاکره مورد نظر رد شود ؟')
                        .ariaLabel('رد مذاکره')
                        .targetEvent(ev)
                        .ok('رد شود')
                        .cancel('انصراف');
                    $mdDialog.show(confirm).then(function (result) {
                        $http.patch("/api/v1/salesConv/" + item.id + "/", {
                            Open: false
                        }).then(function () {
                            $scope.list();
                        })
                    }, function () {
                        $scope.status = 'You didn\'t name your dog.';
                    });

                }


            };
            $scope.completed = function (ev, item) {
                var confirm = $mdDialog.prompt()
                    .title('تکمیل سفارش')
                    .textContent('کد پیش فاکتور را وارد نمایید')
                    .placeholder('شماره پیش فاکتور همکاران')
                    .ariaLabel('پیش فاکتور')
                    .initialValue('')
                    .targetEvent(ev)
                    .ok('تایید')
                    .cancel('انصراف');

                $mdDialog.show(confirm).then(function (result) {
                    $http.patch("/api/v1/salesConv/" + item.id + "/", {
                        PrefactorID: result
                    }).then(function () {
                        $scope.list();
                    })
                }, function () {
                    $scope.status = 'You didn\'t name your dog.';
                });
            };
            $scope.$watchCollection("filter", function () {
                $scope.list();
            });

// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------

        });