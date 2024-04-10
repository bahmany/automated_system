'use strict';


angular.module('AniTheme').controller(
    'BIMenuCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope, $stateParams,
              $mdDialog,
              $location,
              $http) {

        $scope.menu = {};
        $scope.menus = [];
        $scope.listMenus = function () {
            $http.get('/api/v1/bi_menus/').then(function (data) {
                $scope.menus = data.data;
            }).catch(function (data) {

            });
        };

        $scope.listMenus();
        $scope.createMenu = function () {
            swal({
                title: 'منو جدید',
                text: 'نام منو جدید را وارد نمایید',
                type: "input",
                inputValue: $scope.menu.title,
                showCancelButton: true,
                closeOnConfirm: false,
                animation: "slide-from-top",
                inputPlaceholder: 'نام منو'
            }, function (inputValue) {
                if (inputValue === false) return false;
                if (inputValue === "") {
                    swal.showInputError('نامی را وارد نمایید');
                    return false
                }
                $scope.menu.title = inputValue;
                $http.post("/api/v1/bi_menus/", $scope.menu).then(function (data) {
                    if (data.data.id) {
                        swal('پیام', 'با موفقیت ثبت شد', "success");

                    } else {
                        swal('خطا', 'بدلیل تکراری بودن نام منو ، ثبت نشد', "error");

                    }
                    $scope.listMenus();
                    // $scope.listGroup();
                }).catch(function (data) {
                    swal('خطا', 'نام منو ثبت نشد بدلیل خطا', "error");
                });
            });
        };
        $scope.editMenu = function (menu) {

            swal({
                title: 'ویرایش',
                text: 'نام منوی را ویرایش نمایید',
                type: "input",
                inputValue: menu.title,
                showCancelButton: true,
                closeOnConfirm: false,
                animation: "slide-from-top",
                inputPlaceholder: 'نام منو'
            }, function (inputValue) {
                if (inputValue === false) return false;
                if (inputValue === "") {
                    swal.showInputError('نامی را وارد نمایید');
                    return false
                }

                menu.title = inputValue;

                $http.patch("/api/v1/bi_menus/" + menu.id + "/", menu).then(function (data) {
                    if (data.data.id) {
                        swal('پیام', 'با موفقیت ثبت شد', "success");
                        $scope.listMenus();
                    } else {
                        swal('خطا', 'بدلیل تکراری بودن نام منو ، ثبت نشد', "error");
                    }
                }).catch(function (data) {
                    swal('خطا', 'نام منو ثبت نشد بدلیل خطا', "error");

                });
            });

        };
        $scope.deleteMenu = function (event, menu) {
            swal({
                title: 'حذف',
                text: 'آیا اطمینان دارید ؟',
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: 'بله حذف شود',
                showLoaderOnConfirm: true,
                closeOnConfirm: false
            }, function () {

                $http.delete("/api/v1/bi_menus/" + menu.id + "/").then(function (data) {
                    if (data.data.msg) {
                        swal('خطا', 'ابتدا اعضا را حذف نمایید', "error");
                        return

                    }
                    swal('حذف شد', 'با موفقیت حذف شد', "success");
                    $scope.listMenus();


                });
            });
        };


        $scope.userGroupMenu = function (event, menu) {
            $scope.showAdvanced(event, menu);
        }

        $scope.userUserMenu = function (event, menu) {
            $scope.showAdvancedUser(event, menu);
        }
        $scope.duplicateMenu = function (event, menu) {
            swal({
                title: 'نام جدید',
                text: 'نام مورد نظر را وارد نمایید',
                type: "input",
                inputValue: menu.title,
                showCancelButton: true,
                closeOnConfirm: false,
                animation: "slide-from-top",
                inputPlaceholder: 'نام چارت'
            }, function (inputValue) {
                if (inputValue === false) return false;
                if (inputValue === "") {
                    swal.showInputError('نامی را وارد نمایید');
                    return false
                }
                menu.title = inputValue
                $http.post("/api/v1/bi_menus/dup_menu/", menu).then(function (data) {
                    if (data.data.id) {
                        swal('پیام', 'با موفقیت ثبت شد', "success");
                    } else {
                        swal('خطا', 'بدلیل تکراری بودن نام منو ، ثبت نشد', "error");
                    }
                    $scope.listMenus();
                    // $scope.listGroup();
                }).catch(function (data) {
                    swal('خطا', 'نام منو ثبت نشد بدلیل خطا', "error");
                });
            });
        }

        $scope.showAdvancedUser = function (ev, menu) {

            $mdDialog.show({
                locals: {
                    selectedMenu: menu
                },
                onComplete: function (s, e) {
                    // $(e).find('input').first().focus()
                },
                controller: BIMenuMemeberUsersPartialCtrl,
                templateUrl: '/page/bimenuspartialmembersusers/',
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
            })
                .then(function (answer) {

                    $scope.listMenus();

                }, function () {
                    // $scope.status = 'You cancelled the dialog.';
                });
        };
        $scope.showEditItems = function (ev, menu) {

            $mdDialog.show({
                locals: {
                    selectedMenu: menu
                },
                onComplete: function (s, e) {
                    // $(e).find('input').first().focus()
                },
                controller: BIMenuItemsPartialCtrl,
                templateUrl: '/page/bimenuspartialitems/',
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
            })
                .then(function (answer) {

                    $scope.listMenus();

                }, function () {
                    // $scope.status = 'You cancelled the dialog.';
                });
        };

        $scope.showAdvanced = function (ev, menu) {

            $mdDialog.show({
                locals: {
                    selectedMenu: menu
                },
                onComplete: function (s, e) {
                    // $(e).find('input').first().focus()
                },
                controller: BIMenuMemeberPartialCtrl,
                templateUrl: '/page/bimenuspartialmembers/',
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
            })
                .then(function (answer) {

                    $scope.listMenus();

                }, function () {
                    // $scope.status = 'You cancelled the dialog.';
                });
        };

    })