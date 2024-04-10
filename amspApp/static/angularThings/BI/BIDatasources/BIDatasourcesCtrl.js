'use strict';


angular.module('AniTheme').controller(
    'BIDatasourcesCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope, $stateParams,
              $mdDialog,
              $location,
              $http) {


        $scope.datasources = [];
        $scope.datasource = {};
        $scope.listdatasources = function () {
            $http.get('/api/v1/bi_datasources/').then(function (data) {
                $scope.datasources = data.data;
            })
        }
        // $scope.listdatasources();
        $scope.create_or_edit_datasource = function (ev, datasource) {
            $mdDialog.show({
                controller: DialogController,
                templateUrl: '/page/bidatasourcesmodal/',
                locals: {
                    datasource: datasource
                },
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                currentScope: $scope // Only for -xs, -sm breakpoints.
            })
                .then(function (answer) {
                    $scope.listdatasources();

                }, function () {
                    $scope.status = 'You cancelled the dialog.';
                });
        }


        function DialogController($scope, $mdDialog, $http, datasource) {
            $scope.hide = function () {
                $mdDialog.hide();
            };
            $scope.cancel = function () {
                $mdDialog.cancel();
            };
            $scope.answer = function (answer) {
                $mdDialog.hide(answer);
            };
            $scope.providers = {};
            $scope.provider = {};
            $scope.connection = {};
            $scope.set_provider = function (__provider) {
                $scope.provider = __provider;
                $scope.connection.conn_type = __provider.package_name;
            }
            $scope.get_list_of_providers = function () {
                $http.get('/api/v1/bi_datasources/get_providers/').then(function (data) {
                    $scope.providers = data.data;
                })
            }

            $scope.cancel_connection = function () {
                $mdDialog.hide();
            }

            $scope.init = function (){
                if (datasource != null){
                    $scope.connection = datasource;
                }
            }

            $scope.save_connection = function () {
                $http.post('/api/v1/bi_datasources/', $scope.connection).then(function (data) {
                    if (data.data.airflow_connection_id) {
                        $mdDialog.hide();
                        $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                    } else {
                        $rootScope.$broadcast("showToast", "خطا در ثبت لطفا اطلاعات ورودی را کنترل نمایید");
                    }
                }).catch(function (data) {
                    $rootScope.$broadcast("showToast", "ثبت نشد");
                })
            }

            $scope.get_list_of_providers();
            $scope.init();

            $scope.cats = [];


            $scope.selectIt = function (item) {
                $mdDialog.hide(item);

            }
        }

        $scope.testdatasource = function (event, datasource) {
            $http.get('/api/v1/bi_datasources/' + datasource.id + '/test_connection/').then(function (data) {
                if (data.data.msg === 'succ') {
                    swal('پیام', 'با موفقیت متصل شد', "success");
                } else {
                    swal('عدم ارتباط !!!', 'error')
                }

            })
        }


        $scope.renamedatasource = function (event, datasource) {
            swal({
                title: 'تغییر نام',
                text: 'نام مورد نظر را وارد نمایید',
                type: "input",
                inputValue: datasource.datasourceTitle,
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


                datasource.datasourceTitle = inputValue
                $http.patch("/api/v1/bi_datasources/" + datasource.id + '/change_name/', datasource).then(function (data) {
                    if (data.data.id) {
                        swal('پیام', 'با موفقیت ثبت شد', "success");
                        $scope.get_list();

                    } else {
                        swal('پیام', 'این نام قبلا استفاده شده است', "error");

                    }
                    // $scope.listGroup();
                }).catch(function (data) {
                    swal('خطا', 'نام چارت ثبت نشد بدلیل خطا', "error");
                });
            });
        }
        $scope.deletedatasource = function (event, datasource) {
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

                $http.delete("/api/v1/bi_datasources/" + datasource.id + "/").then(function (data) {
                    if (data.data.msg) {
                        swal('خطا', 'ابتدا اعضا را حذف نمایید', "error");
                        return

                    }
                    swal('حذف شد', 'با موفقیت حذف شد', "success");
                    $scope.get_list();

                });
            });
        };


        $scope.get_list = function () {
            $http.get('/api/v1/bi_datasources/get_list/').then(function (data) {
                $scope.datasources = data.data;
            })
        }

        $scope.get_list();


    })