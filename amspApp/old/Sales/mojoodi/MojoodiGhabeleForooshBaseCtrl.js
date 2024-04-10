'use strict';
angular.module('AniTheme')
    .controller(
        'MojoodiGhabeleForooshBaseCtrl',
        function ($scope, $window, $http,
                  $mdDialog,
                  $translate, $rootScope, $stateParams, $location, $$$, $filter) {


            $scope.update_from_rahkaraan = function () {
                $http.get('/api/v1/mojoodiGhabeleForoosh/update_from_rahkaraan/').then(function (data) {
                    $scope.get_anbar_cardex();
                })
            }

            $scope.filter = {};
            $scope.cardex_anbar = [];
            $scope.get_anbar_cardex = function () {
                $http.post('/api/v1/mojoodiGhabeleForoosh/get_anbar_cardex/', $scope.filter).then(function (data) {
                    $scope.cardex_anbar = data.data;
                })
            }

            $scope.get_anbar_cardex();


            $scope.add_sefaresh = function (item) {

            }


            $scope.edit_keifi_issue = function (item) {

            }

            $scope.delete_keifi_issue = function (item) {
                if (confirm("آیا از حذف عکس مورد نظر اطمینان دارید ؟")) {
                    $http.post('/api/v1/mojoodiGhabeleForoosh/' + item.id + "/remove_keifi/", item).then(
                        function (data) {
                            $scope.get_anbar_cardex();


                        });
                    // $scope["provider"]["frm" + $stateParams.formIndex]['files' + inputID].splice(fileID, 1);
                }

            }

            $scope.add_keifi_issue = function (ev, item) {
                $mdDialog.show({
                    locals: {
                        selectedItem: item
                    },
                    onComplete: function (s, e) {
                        // $(e).find('input').first().focus()
                    },
                    controller: SaleMojoodiGhabeleForooshKeifiCtrl,
                    templateUrl: '/page/MojoodiGhabeleForooshpartial_nokteh_keifi',
                    parent: angular.element(document.body),
                    targetEvent: ev,
                    clickOutsideToClose: true,
                })
                    .then(function (answer) {

                        $scope.get_anbar_cardex();

                    }, function () {
                        // $scope.status = 'You cancelled the dialog.';
                    });
            }
            $scope.add_sefaresh = function (ev, item) {
                $mdDialog.show({
                    locals: {
                        selectedItem: item
                    },
                    onComplete: function (s, e) {
                        // $(e).find('input').first().focus()
                    },
                    controller: SaleMojoodiGhabeleForooshSefareshCtrl,
                    templateUrl: '/page/MojoodiGhabeleForooshpartial_sefaresh',
                    parent: angular.element(document.body),
                    targetEvent: ev,
                    clickOutsideToClose: true,
                })
                    .then(function (answer) {

                        $scope.listMenus();

                    }, function () {
                        // $scope.status = 'You cancelled the dialog.';
                    });
            }
            $scope.toggle_setareh = function (item) {
                if (item.details.details.star === undefined) {
                    item.details.details.star = true;
                } else {
                    if (item.details.details.star === false) {
                        item.details.details.star = true;

                    } else {
                        if (item.details.details.star === true) {
                            item.details.details.star = false;

                        }
                    }
                }
                $http.post('/api/v1/mojoodiGhabeleForoosh/' + item.details.id + "/toggle_setareh/", item).then(function (data) {

                });
            }
            $scope.change_aneal = function (item) {
                $http.post('/api/v1/mojoodiGhabeleForoosh/' + item.details.id + "/change_aneal/", item).then(function (data) {

                });
            }

            $scope.mandeh_from_pish = {};
            $scope.get_pish_from_rahkaraan = function () {
                $http.get('/api/v1/mojoodiGhabeleForoosh/get_pishfactors_mandeh/').then(function (data) {
                    $scope.mandeh_from_pish = data.data;

                });
            }

            $scope.add_aniling = function (ev, item) {
                $mdDialog.show({
                    locals: {
                        selectedItem: item
                    },
                    onComplete: function (s, e) {
                        // $(e).find('input').first().focus()
                    },
                    controller: SaleMojoodiGhabeleForooshAnilingCtrl,
                    templateUrl: '/page/MojoodiGhabeleForooshpartial_aniling',
                    parent: angular.element(document.body),
                    targetEvent: ev,
                    clickOutsideToClose: true,
                })
                    .then(function (answer) {

                        $scope.listMenus();

                    }, function () {
                        // $scope.status = 'You cancelled the dialog.';
                    });
            }
            $scope.add_tozihat = function (ev, item) {
                $mdDialog.show({
                    locals: {
                        selectedItem: item
                    },
                    onComplete: function (s, e) {
                        // $(e).find('input').first().focus()
                    },
                    controller: SaleMojoodiGhabeleForooshTozihatCtrl,
                    templateUrl: '/page/MojoodiGhabeleForooshpartial_tozihat',
                    parent: angular.element(document.body),
                    targetEvent: ev,
                    clickOutsideToClose: true,
                })
                    .then(function (answer) {

                        // $scope.listMenus();

                    }, function () {
                        // $scope.status = 'You cancelled the dialog.';
                    });
            }


            function SaleMojoodiGhabeleForooshKeifiCtrl($scope,
                                                        $http, $mdDialog,
                                                        selectedItem) {
                $scope.keifi = {};
                $scope.add = function () {
                    $http.post('/api/v1/mojoodiGhabeleForoosh/' + selectedItem.details.id + "/add_keifi/", $scope.keifi).then(
                        function (data) {
                            if (data.data.id) {
                                $mdDialog.hide();
                            }
                        });
                }
            }

            function SaleMojoodiGhabeleForooshSefareshCtrl($scope,
                                                           $http, $mdDialog,
                                                           selectedItem) {

            }

            function SaleMojoodiGhabeleForooshSetarehCtrl($scope,
                                                          $http, $mdDialog,
                                                          selectedItem) {

            }

            function SaleMojoodiGhabeleForooshAnilingCtrl($scope,
                                                          $http, $mdDialog,
                                                          selectedItem) {

            }

            function SaleMojoodiGhabeleForooshTozihatCtrl($scope,
                                                          $http, $mdDialog,
                                                          selectedItem) {

            }


        });



