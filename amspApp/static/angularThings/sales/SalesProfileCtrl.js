'use strict';
angular.module('AniTheme')
    .controller(
        'SalesProfileCtrl',
        function ($scope, $window, $http, $translate, $element, $rootScope, $stateParams, $location, $$$, $filter, $mdDialog) {


            $scope.profiles = {};
            $scope.profile = {};

            $scope.addNew = function (ev) {
                $scope.profile = {};
                $scope.showModal(ev)
            };
            $scope.edit = function (ev, profile) {
                // $scope.profile = profile;
                $scope.profile = profile;

                $scope.showModal(ev);
            };

            // var profile = {};
            $scope.showModal = function (ev) {
                // debugger;
                // profile = $scope.profile;
                $mdDialog.show({
                    controller: DialogController,
                    templateUrl: '/page/salesAddCustomerProfile',
                    parent: angular.element(document.body),
                    targetEvent: ev,
                    clickOutsideToClose: true,
                    locals: {
                        profile: $scope.profile
                    },
                    // profile: $scope.profile,
                    fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
                })
                    .then(function (jobItem) {
                        $scope.list();
                    }, function () {
                        $scope.status = 'You cancelled the dialog.';
                    });
            };

            function DialogController($scope, $mdDialog, $http, profile) {
                // debugger;
                $scope.searchCustomers = "";

                $scope.$watch("searchCustomers", function () {
                    $scope.getCustomers($scope.searchCustomers);
                });

                $scope.getCustomers = function (txt) {
                    $http.get("/api/v1/salesConv/getCustomerNames/?searchText=" + txt).then(function (data) {
                        $scope.Customers = data.data;
                    })
                };

                $scope.profile = profile;

                $scope.clearSearchTerm = function () {
                    $scope.searchTerm = '';
                };
                $element.find('#searchCustomer').on('keydown', function (ev) {
                    ev.stopPropagation();
                });

                // $scope.profile = {};
                $scope.setCustomer = function (customer) {
                    $scope.profile.name = customer.CustomerName;
                    $scope.profile.hamkaranCode = customer.CustomerID;
                };

                $scope.hide = function () {
                    $mdDialog.hide();
                };

                $scope.cancel = function () {
                    $mdDialog.cancel();
                };
                $scope.confirmCancel = function () {
                    $mdDialog.hide($scope.profile);
                };
                $scope.confirm = function () {
                    if (!($scope.profile.id)) {
                        $http.post("/api/v1/salesProfile/", $scope.profile).then(function () {
                            $mdDialog.hide($scope.profile);
                        })
                    } else {
                        $http.patch("/api/v1/salesProfile/" + $scope.profile.id + "/", $scope.profile).then(function () {
                            $mdDialog.hide($scope.profile);
                        })
                    }
                };
            }




            $scope.list = function () {
                $http.get("/api/v1/salesProfile/?&search=" + $scope.profilesSearchText + "&page=" + $scope.page.toString() + "&page_size=20").then(function (data) {
                    $scope.profiles = data.data;
                })
            };

            $scope.page = 1;
            $scope.wait = false;
            $scope.profilesPageTo = function (page) {
                $scope.wait = true;
                if (page) {
                    $http.get(page).then(function (data) {
                        $scope.wait = false;
                        $scope.profiles = data.data;
                    }).catch(function () {
                        $scope.wait = false;
                    });
                }
            };
            $scope.profilesSearchText = "";
            $scope.$watch("profilesSearchText", function () {
                $scope.list();
            });

            $scope.delete = function (ev, item) {
                var confirm = $mdDialog.confirm()
                    .title('حذف پروفایل')
                    .textContent('پروفایل مورد نظر حذف شود ؟')
                    .ariaLabel('حذف پروفایل')
                    .targetEvent(ev)
                    .ok('حذف شود')
                    .cancel('انصراف');

                $mdDialog.show(confirm).then(function (result) {
                    $http.delete("/api/v1/salesProfile/" + item.id + "/").then(function () {
                        $scope.list();
                    })
                }, function () {
                    $scope.status = 'You didn\'t name your dog.';
                });

            }


        });