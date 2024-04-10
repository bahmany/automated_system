'use strict';


angular.module('AniTheme').controller(
    'EZItemCtrl',
    function ($scope,
              $translate, $stateParams,
              $q, $http, $state,
              $rootScope,
              $modal) {


        $scope.ez = {};
        $scope.ez.desc = {};
        $scope.ez.desc.listOf = [];
        $scope.ez.desc.pers = []


        $scope.loadUsers = function () {
            if ($stateParams.id === "0") {
                $http.get("/api/v1/ez/getPersonelList/").then(function (data) {
                    $scope.ez.desc.pers = data.data;
                });
            }
        }


        $scope.save_sharhe_eghdamaat = function () {
            $http.post('/api/v1/ez/' + $stateParams.id + '/sharheEghdam/', $scope.ez).then(function (data) {
                if (data.data.id) {
                    $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                } else {
                    if (data.data.message) {
                        $rootScope.$broadcast("showToast", data.data.message);
                    } else {
                        $rootScope.$broadcast("showToast", "خطایی رخ داده است");
                    }
                }
            })
        }

        $scope.remove_approved_ez = function () {
            swal({
                title: "اطمینان دارید",
                text: "آیا از حذف این فرآیند اضافه کاری اطمنیان دارید ؟",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "بله",
                closeOnConfirm: true,
                showLoaderOnConfirm: true
            }, function () {
                $http.get('/api/v1/ez/' + $stateParams.id + '/removeApprovedEz/').then(function (data) {
                    if (data.data.message) {
                        $rootScope.$broadcast("showToast", data.data.message);
                    } else {
                        if (data.data.ok) {
                            $state.go("ezlist", {id: $scope.ez.id});
                            $rootScope.$broadcast("showToast", 'با موفقیت حذف شد');
                        } else {
                            $rootScope.$broadcast("showToast", 'خطایی پیش آمده است');
                        }
                    }
                })
            })
        }

        var table;
        $scope.approve = function (typeOfApprove) {
            swal({
                title: "تایید اضافه کار",
                text: "آیا این اضافه کاری را تایید میکنید ؟ پس از تایید امکان بازگشت وجود ندارد",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "بله",
                closeOnConfirm: true,
                showLoaderOnConfirm: true
            }, function () {

                $http.post('/api/v1/ez/' + $stateParams.id + '/saveApprove/', {typeOfApprove}).then(function (data) {
                    if (data.data.id) {
                        $rootScope.$broadcast("showToast", "امضای شما ثبت شد");
                        $scope.ez = data.data;
                    } else {
                        if (data.data.message) {
                            $rootScope.$broadcast("showToast", data.data.message);
                        } else {
                            $rootScope.$broadcast("showToast", "خطایی رخ داده است");
                        }
                    }

                }).catch(function (err) {
                    $rootScope.$broadcast("showToast", err.message);
                })
            });
        }

        $scope.init = function () {
            $scope.loadUsers();
            if ($stateParams.id !== "0") {
                $http.get("/api/v1/ez/" + $stateParams.id + "/").then(function (data) {
                    if (data.data.id) {
                        $scope.ez = data.data;
                    }
                });
            }
        }

        $scope.init();

        $scope.save_draft = function () {
            $http.post("api/v1/ez/saveDraft/", $scope.ez).then(function (data) {
                if (data.data.id) {
                    $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                    $state.go("ezitem", {id: data.data.id});
                }
            });
        }

        $scope.comment = function (approve) {
            let a = prompt("لطفا کامنت خود را وارد نمایید")

            if (a) {
                $http.post("/api/v1/ez/" + $stateParams.id + "/postComment/", {
                    'approve': approve,
                    'comment': a
                }).then(function (data) {
                    if (data.data.id) {
                        $scope.ez = data.data;
                        $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");

                    } else {
                        $rootScope.$broadcast("showToast", data.data.message);

                    }
                }).catch(function (err) {

                })
            }


        }


        $scope.save_pers = function (per) {
            $http.post("/api/v1/ez/" + $stateParams.id + "/savePers/", {ez: $scope.ez, per: per}).then(function (data) {
                if (data.data.id) {
                    $rootScope.$broadcast("showToast", "تغییرات ثبت شد");
                    $scope.ez = data.data;
                } else {
                    $rootScope.$broadcast("showToast", data.data.message);
                }
            }).catch(function (err) {

            })
        }


        $scope.addtohz = function () {
            $http.get("/api/v1/ez/" + $stateParams.id + "/writeToKaraweb/").then(function (data) {

            })

        }

        $scope.remove_pers = function (per) {
            swal({
                title: "حذف شخص از اضافه کاری",
                text: "آیا اطمینان دارید که میخواهید این شخص را لیست اضافه کاری حذف کنید ؟",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "بله",
                closeOnConfirm: true,
                showLoaderOnConfirm: true
            }, function () {
                $http.post("/api/v1/ez/" + $stateParams.id + "/removePerFromList/", per).then(function (data) {
                    if (data.data.id) {
                        $rootScope.$broadcast("showToast", "حذف شد");
                        $scope.ez = data.data;
                    } else {
                        $rootScope.$broadcast("showToast", data.data.message);
                    }
                }).catch(function (err) {

                })
            })
        }


        $scope.start_ez = function () {
            let a_per_checked = false;
            for (var i = 0; $scope.ez.desc.pers.length > i; i++) {
                if ($scope.ez.desc.pers[i]) {
                    if ($scope.ez.desc.pers[i].check === true) {
                        a_per_checked = true;
                        if ($scope.ez.desc.pers[i].personnel_code === "") {
                            $rootScope.$broadcast("showToast", "خطا - لطفا کد پرسنلی ها رو کنترل نمایید");
                            return;
                        }
                        if ($scope.ez.desc.pers[i].personnel_code === undefined) {
                            $rootScope.$broadcast("showToast", "خطا - لطفا کد پرسنلی ها رو کنترل نمایید");
                            return;
                        }
                        if ($scope.ez.desc.pers[i].personnel_code === null) {
                            $rootScope.$broadcast("showToast", "خطا - لطفا کد پرسنلی ها رو کنترل نمایید");
                            return;
                        }

                        if (!(moment($scope.ez.desc.pers[i].az, 'HH:mm', true).isValid())) {
                            $rootScope.$broadcast("showToast", "خطا - لطفا در ورود ساعت شروع اضافه کار دقت نمایید");
                            return;
                        }
                        if (!(moment($scope.ez.desc.pers[i].ta, 'HH:mm', true).isValid())) {
                            $rootScope.$broadcast("showToast", "خطا - لطفا در ورود ساعت پایان اضافه کار دقت نمایید");
                            return;
                        }
                    }
                }
            }


            if (!a_per_checked) {
                $rootScope.$broadcast("showToast", "خطا - حداقل یک پرسنل را انتخاب کنید");
                return;
            }

            $http.post("api/v1/ez/start/", $scope.ez).then(function (data) {
                if (data.data.id) {
                    $rootScope.$broadcast("showToast", "با اجرا شد");
                    $scope.ez = data.data;
                    $state.go("ezitem", {id: $scope.ez.id});
                } else {
                    $rootScope.$broadcast("showToast", data.data.message);
                }
            })
        }

    });




