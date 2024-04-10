'use strict';


angular.module('AniTheme').controller(
    'BIGroupsCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope, $stateParams,
              $mdDialog,
              $location,
              $http) {

        $scope.group = {};
        $scope.groups = [];
        $scope.listGroup = function () {
            $http.get('/api/v1/bi_group/').then(function (data) {
                $scope.groups = data.data;
            }).catch(function (data) {

            });
        };

        $scope.listGroup();
        $scope.createGroup = function () {
            swal({
                title: 'گروه جدید',
                text: 'نام گروه جدید را وارد نمایید',
                type: "input",
                inputValue: $scope.group.title,
                showCancelButton: true,
                closeOnConfirm: false,
                animation: "slide-from-top",
                inputPlaceholder: 'نام گروه'
            }, function (inputValue) {
                if (inputValue === false) return false;
                if (inputValue === "") {
                    swal.showInputError('نامی را وارد نمایید');
                    return false
                }
                $scope.group.groupTitle = inputValue;
                $http.post("/api/v1/bi_group/", $scope.group).then(function (data) {
                    swal('پیام', 'با موفقیت ثبت شد', "success");
                    $scope.listGroup();
                    // $scope.listGroup();
                }).catch(function (data) {
                    swal('خطا', 'نام گروه ثبت نشد بدلیل خطا', "error");
                });
            });
        };
        $scope.editGroup = function (group) {

            swal({
                title: 'ویرایش',
                text: 'نام گروه را ویرایش نمایید',
                type: "input",
                inputValue: group.groupTitle,
                showCancelButton: true,
                closeOnConfirm: false,
                animation: "slide-from-top",
                inputPlaceholder: 'نام گروه'
            }, function (inputValue) {
                if (inputValue === false) return false;
                if (inputValue === "") {
                    swal.showInputError('نامی را وارد نمایید');
                    return false
                }

                group.groupTitle = inputValue;

                $http.patch("/api/v1/bi_group/" + group.id + "/", group).then(function (data) {
                    if (data.data.id) {
                        swal('پیام', 'با موفقیت ثبت شد', "success");
                        $scope.listGroup();
                    } else {
                        swal('خطا', 'نام گروه ثبت نشد بدلیل خطا', "error");
                    }
                }).catch(function (data) {

                });
            });

        };
        $scope.deleteGroup = function (event, group) {
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

                $http.delete("/api/v1/bi_group/" + group.id + "/").then(function (data) {
                    if (data.data.msg) {
                        swal('خطا', 'ابتدا اعضا را حذف نمایید', "error");
                        return

                    }
                    swal('حذف شد', 'با موفقیت حذف شد', "success");
                    $scope.listGroup();

                });
            });
        };


        $scope.userGroup = function (event, group) {
            $scope.showAdvanced(event, group);

        }


        $scope.showAdvanced = function (ev, group) {

            $mdDialog.show({
                locals: {
                    selectedGroup: group
                },
                onComplete: function (s, e) {
                    // $(e).find('input').first().focus()
                },
                controller: BIGroupMemeberPartialCtrl,
                templateUrl: '/page/bigroupspartialmembers/',
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
            })
                .then(function (answer) {

                    $scope.listGroup();

                }, function () {
                    // $scope.status = 'You cancelled the dialog.';
                });
        };


    })