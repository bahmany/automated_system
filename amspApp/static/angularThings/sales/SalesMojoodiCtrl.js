'use strict';
angular.module('AniTheme')
    .controller(
        'SalesMojoodiCtrl',
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


            $scope.MojoodiSort = [];
            $scope.sortIt = function (columnName) {

                var found = false;
                console.log($scope.MojoodiSort);
                for (var i = 0; $scope.MojoodiSort.length > i; i++) {
                    if ($scope.MojoodiSort[i] == columnName) {
                        found = true;
                        $scope.MojoodiSort[i] = "-" + columnName;
                        return
                    }
                    if ($scope.MojoodiSort[i] == "-" + columnName) {
                        found = true;
                        $scope.MojoodiSort[i] = "";
                        $scope.MojoodiSort = $scope.MojoodiSort.filter(function (n) {
                            return n != ""
                        });
                        return
                    }
                }
                if (!(found)) {
                    $scope.MojoodiSort.push(columnName)
                }

                $scope.MojoodiSort = $scope.MojoodiSort.filter(function (n) {
                    return n != ""
                });
            }

            $scope.getSortIcon = function (columnName) {
                for (var i = 0; $scope.MojoodiSort.length > i; i++) {
                    if ($scope.MojoodiSort[i] == columnName) {
                        return "+";
                    }
                    if ($scope.MojoodiSort[i] == "-" + columnName) {
                        return "-";
                    }
                }
                return "";
            }


            $scope.$watchCollection("MojoodiSort", function () {
                $scope.getCurrentMojoodi()
            })


            $scope.AddToBasket = function (ev, item) {
                // debugger;
                // if (item.PartCode.length != 14) {
                //     alert('کد محصول را صحیح وارد نمایید');
                //     return
                // }
                var currentItem = {};
                currentItem.desc = {};
                currentItem.desc.itemID = item.PartCode;
                currentItem.desc.itemName = item.PartName;
                currentItem.desc.amount = 0;
                currentItem.desc.fee = 0;
                currentItem.desc.off = 0.0;
                $rootScope.$emit("showBasket", {ev: ev, item: currentItem, openAdd: true});
            }

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
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------


            $scope.IgnorePish = function (item) {

                $http.post("/api/v1/salesConv/IgnorePish/", {
                    isAccountable: item.isAccountable,
                    details: item
                }).then(function (data) {
                    item.leve3Pish = data.data;
                })
            }

            $scope.level3Pish = {};


            $scope.openPishFactors = function (i, it, item) {
                // getting pishfactors by 5 opts
                // sath - temper - arz - zekhamat - tool - 66/77/88


                var filter = {
                    sath: item.sath,
                    temper: item.temper,
                    arz: item.arz,
                    zekhamat: item.zekhamat,
                    tool: i.tool,
                    noe: it.noe
                };

                item.showPishLevel3 = !(item.showPishLevel3);
                item.leve3Pish = {};
                $http.post("/api/v1/salesConv/getPishLevel3/", filter).then(function (data) {
                    item.leve3Pish = data.data;
                })
            }


            $scope.openCardex = function (i, it, item) {
                // getting pishfactors by 5 opts
                // sath - temper - arz - zekhamat - tool - 66/77/88

                // debugger;
                var filter = {
                    partCode: item.PartCode,
                    noe: it.noe,
                    tool: i.tool
                };


                item.showCardex = !(item.showCardex);
                item.cardex = {};
                $http.post("/api/v1/salesConv/getCardex/", filter).then(function (data) {
                    item.cardex = data.data;
                })
            }

            $scope.getMojoodiExcel = function () {
                $http.get("/api/v1/salesConv/getMojoodiExcel/").then(function (data) {
                })
            }

            $scope.getMojoodiCsv = function () {
                $http.get("api/v1/download_service/21312323556768634523424234/").then(function (data) {
                })
            }


            $scope.openConv = function (i, it, item) {
                // getting pishfactors by 5 opts
                // sath - temper - arz - zekhamat - tool - 66/77/88


                var filter = {
                    details: {
                        item: item,
                        it: item,
                        i: item
                    },
                    sath: item.sath,
                    temper: item.temper,
                    arz: item.arz,
                    zekhamat: item.zekhamat,
                    tool: i.tool,
                    noe: it.noe
                };

                item.showConvLevel3 = !(item.showConvLevel3);
                item.leve3Pish = {};
                $http.post("/api/v1/salesConv/getConvLevel3/", filter).then(function (data) {
                    item.leve3Pish = data.data;
                })
            }


// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------// ------------------------------------------------------------------
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
            $scope.Mojoodi.page = 1;
            $scope.Mojoodi.page_size = 20;
            $scope.getCurrentMojoodi = function () {
                $scope.wait = true;
                $http.post("/api/v1/salesConv/getMojoodies/?page_size=" + $scope.Mojoodi.page_size.toString() + "&page=" + $scope.Mojoodi.page.toString() + "&sort=" + $scope.MojoodiSort.join(","), $scope.searchProduct).then(function (data) {
                    if (data.data.msg) {
                        $scope.Mojoodi = data.data;

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
            // $scope.getCurrentMojoodiToExcel = function () {
            //     $scope.wait = true;
            //     $http.get("/api/v1/salesConv/getMojoodiExcel/?page_size=" + $scope.Mojoodi.page_size.toString() + "&page=" + $scope.Mojoodi.page.toString() + "&sort=" + $scope.MojoodiSort.join(",")).then(function (data) {
            //         $scope.wait = true;
            //     })
            //
            // };


            $scope.PageNext = function (lst) {
                // debugger;
                if ($scope.Mojoodi.page <= $scope.Mojoodi.page_count) {
                    $scope.Mojoodi.page = $scope.Mojoodi.page + 1;
                    $scope.getCurrentMojoodi();
                }
            }
            $scope.PagePrev = function (lst) {
                if ($scope.Mojoodi.page > 1) {
                    $scope.Mojoodi.page = $scope.Mojoodi.page - 1;
                    $scope.getCurrentMojoodi();
                }
            }
            $scope.updateCache = function (ev) {
                if ($scope.wait) {
                    return
                }
                $scope.wait = true;
                $http.get("/api/v1/salesConv/refreshCache/").then(function (data) {
                    if (data.data.msg) {

                        $scope.wait = false;

                        $rootScope.$broadcast("showToast", "با موفقیت بروز شد");
                        $scope.getCurrentMojoodi();
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
                    .cancel('انطراف');

                $mdDialog.show(confirm).then(function (result) {
                    $http.patch("/api/v1/salesConv/" + item.id + "/", {
                        PrefactorID: result.data
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

        }
    );