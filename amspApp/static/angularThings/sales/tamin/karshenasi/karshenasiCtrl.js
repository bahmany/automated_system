'use strict';
angular.module('AniTheme')
    .controller(
        'karshenasiCtrl',
        function ($scope, $window, $http, $translate, $rootScope, $stateParams, $location, $timeout, $filter, $mdDialog) {


            $scope.customer = {};
            $scope.customer.desc = {};
            $scope.requests = {};

            $scope.addNew = function (ev) {
                $scope.customer = {};
                $scope.customer.desc = {};

                $scope.showModal(ev)
            }


            $scope.updateFromGoogle = function () {
                $http.get("/api/v1/salesProfileSizes/createShamsiDate/").then(function (data) {

                })
            }

            var tablePercent;
            tablePercent = $('#table2').DataTable({
                // fnPageChange: tablePageChange,
// نام مشتری	نام مشتری همکاران	ضخامت (mm)	عرض (mm)	طول برش (mm)	میزان (تن)	تمپر	زمان مصرف	شرایط پرداخت	تاریخ ثبت	شماره ثبت
                //custom datatable options
                "aLengthMenu": [[10, 50, 100, 200], [10, 50, 100, 200]],
                "bProcessing": true,
                "sAjaxSource": '/api/v1/salesProfileSizes/getForDataTables/',
                "bServerSide": true,
                "iSearchDelay": 500,
                "aoColumns": [
                    {"mData": "profileLink.name", "sTitle": "نام مشتری"},
                    {"mData": "desc.zekhamat", "sTitle": "ضخامت", "sType": "numeric"},
                    {"mData": "desc.arz", "sTitle": "عرض", "sType": "numeric"},
                    {"mData": "desc.tool", "sTitle": "طول برش", "sType": "numeric"},
                    {"mData": "desc.temper", "sTitle": "تمپر", "sType": "numeric"},
                    {"mData": "desc.qty", "sTitle": "میزان", "sType": "numeric"},
                    {"mData": "desc.sayType", "sTitle": "زمان مصرف"},
                    {"mData": "desc.payType", "sTitle": "شرایط پرداخت"},
                    {"mData": "dateOfPost", "sTitle": "تاریخ سیستم" },
                    {"mData": "desc.tarikheSabt", "sTitle": "تاریخ درخواست", "bSearchable": false},
                    {"mData": "desc.letterID", "sTitle": "شماره ثبت"},
                    {
                        "mData": "id",
                        "bSearchable": false,
                        "sTitle": "عملیات",
                        "mRender": function (data, type, full) {
                            return "<button onclick='karshEdit(\"" + data + "\");'>ویرایش</button> " +
                                "<button onclick='karshDel(\"" + data + "\");'>حذف</button> " +
                                "<button onclick='karshDup(\"" + data + "\");'>dup</button> "

                        }
                    }
                    // "sDefaultContent": "<button onclick='hiii(this);'>...</button>"}
                    // {"mData": "row.z_MeghdareMandePayamDoreh", "sTitle": "مقداری مانده پایان دوره", "sType": "numeric"},
                    // {"mData": "row.z_MablagheMandePayamDoreh", "sTitle": "ریالی مانده پایان دوره", "sType": "numeric"},
                    // {"mData": "row.z_MeghdareKhaleseTolidi", "sTitle": "مقداری خالص مصرف تولیدی", "sType": "numeric"},
                    // {"mData": "row.z_MablagheKhaleseTolidi", "sTitle": "ریالی خالص مصرف تولیدی", "sType": "numeric"}
                ]
            })


            // $scope.dataTableOpt = ;
// -----------------------------------------------------------------------
// -----------------------------------------------------------------------
// -----------------------------------------------------------------------
            // Searching Customers
// -----------------------------------------------------------------------
// -----------------------------------------------------------------------
            var customer = {};
            $scope.showModal = function (ev) {
                // $scope.customer = {};
                // $scope.customer.desc = {};
                // $scope.requests = {};
                // customer = $scope.customer;
                $mdDialog.show({
                    controller: DialogController,
                    templateUrl: '/page/salesKarshenasiAddNew',
                    parent: angular.element(document.body),
                    targetEvent: ev,
                    clickOutsideToClose: true,
                    customer: $scope.customer,
                    fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
                })
                    .then(function (jobItem) {
                        angular.element($("select[name='table2_length']")).change();

                    }, function () {
                        $scope.status = 'You cancelled the dialog.';
                    });
            };

            function DialogController($scope, $mdDialog, $http, customer) {
                $scope.customer = customer;
                $scope.SelectedProfileInfo = {};
                if (customer.id) {
                    $scope.SelectedProfileInfo.name = $scope.customer.profileLink.name;
                    $scope.SelectedProfileInfo.hamkaranCode = $scope.customer.profileLink.hamkaranCode;
                }

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
                };
                $scope.CustomersSearchText = "";
                $scope.$watch("CustomersSearchText", function () {
                    $scope.getCustomers();
                });
                $scope.setCustomer = function (customer) {
                    $scope.SelectedProfileInfo = customer;
                    $scope.customer.profileLink = customer.id;
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
                $scope.saveRequest = function () {
                    if ($scope.customer.id) {
                        // debugger;
                        if ($scope.customer.profileLink.id) {
                            $scope.customer.profileLink = $scope.customer.profileLink.id;
                        }
                        $http.patch("/api/v1/salesProfileSizes/" + $scope.customer.id + "/", $scope.customer).then(function (data) {
                            // $scope.list();
                            angular.element($("select[name='table2_length']")).change();
                            $scope.hide();

                        })
                    } else {
                        $http.post("/api/v1/salesProfileSizes/", $scope.customer).then(function (data) {
                            // $scope.list();
                            angular.element($("select[name='table2_length']")).change();
                            $scope.hide();

                        })
                    }
                }
            }


// -----------------------------------------------------------------------
// -----------------------------------------------------------------------
// -----------------------------------------------------------------------
// -----------------------------------------------------------------------
// -----------------------------------------------------------------------

            $scope.list = function () {
                $http.get("/api/v1/salesProfileSizes/getForDataTables/").then(function (data) {
                    $scope.requests = data.data;
                });
            };
            $scope.list();

            $scope.edit = function (id) {
                $http.get("/api/v1/salesProfileSizes/" + id + "/").then(function (data) {
                    $scope.customer = data.data;
                    customer = $scope.customer;
                    $scope.showModal()
                })

            };
            $scope.del = function (id) {
                if (confirm("آیا می خواهید خذف کنید ؟")) {
                    $http.delete("/api/v1/salesProfileSizes/" + id + "/").then(function (data) {
                        // debugger;
                        angular.element($("select[name='table2_length']")).change();
                    });
                }
            };
            $scope.dup = function (id) {
                    $http.get("/api/v1/salesProfileSizes/" + id + "/dup/").then(function (data) {
                        // debugger;
                        angular.element($("select[name='table2_length']")).change();
                    });
            };
            // $scope.downExcel = function () {
            //         $http.get("/api/v1/salesProfileSizes/downloadExcel/").then(function (data) {
            //             debugger;
            //             angular.element($("select[name='table2_length']")).change();
                    // });
            // };
        });


function karshEdit(id) {
    var scope = angular.element($("#hahahahahaha")).scope();
    scope.edit(id);

}

function karshDel(id) {
    var scope = angular.element($("#hahahahahaha")).scope();
    scope.del(id);
}

function karshDup(id) {
    var scope = angular.element($("#hahahahahaha")).scope();
    scope.dup(id);
}

