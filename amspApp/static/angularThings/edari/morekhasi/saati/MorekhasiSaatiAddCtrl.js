'use strict';


angular.module('AniTheme').controller(
    'MorekhasiSaatiAddCtrl',
    function ($scope,
              $translate,
              $http,
              $q, $mdDialog,
              $rootScope, $stateParams,
              $state,
              $modal) {


        $scope.init = function () {
            $scope.morekhasi = {};
            $scope.morekhasi.exp = {};
            $scope.morekhasi.exp.typeof = 1;
            $scope.get_object($stateParams.morekhasiID);
        }

        $scope.get_personnel_info = function (typeofreq) {
            $http.get('/api/v1/morekhasi_saati/get_personnel_info/?q=1').then(function (data) {
                if (data.status === 400) {
                    swal('Error', data.data.message, "error");
                } else {
                    if ($scope.morekhasi.exp.typeof === 1) {
                        $scope.morekhasi = data.data;
                        $scope.morekhasi.exp.typeof = 1;
                        $scope.get_mandeh_morekhasi($scope.morekhasi.exp['pos_vahede_darkhat']['personnel_code']);

                    }
                }
            }).catch(function (data) {
                swal('Error', data.data.message, "error");
            })
        }

        $scope.$watchGroup(['morekhasi.exp.az', 'morekhasi.exp.taa'], function (newVals, oldVals) {
            if ($scope.morekhasi.exp.az && $scope.morekhasi.exp.taa) {
                var startTime = moment($scope.morekhasi.exp.az, "HH:mm"),
                    endTime = moment($scope.morekhasi.exp.taa, "HH:mm");
                $scope.morekhasi.exp.mizan = endTime - startTime;
                if ($scope.morekhasi.exp.mizan < 0) {
                    $scope.morekhasi.exp.mizan = 0
                } else {
                    $scope.morekhasi.exp.mizan = Math.round($scope.morekhasi.exp.mizan / 60000);
                }
            }
        })


        $scope.get_object = function (id) {
            if (id === "0") {
                $scope.get_personnel_info();

            } else {
                $http.get('/api/v1/morekhasi_saati/' + id + '/').then(function (data) {

                    if (data.status === 400) {
                        swal('Error', data.data.message, "error");

                    } else {
                        $scope.morekhasi = data.data;
                        $scope.get_mandeh_morekhasi($scope.morekhasi.exp['pos_vahede_darkhat']['personnel_code']);
                        update_notif();
                    }
                }).catch(function (data) {
                    swal('Error', data.data, "error");

                });
            }
        }

        $scope.karaweb_trace = {};
        $scope.get_mandeh_morekhasi = function (personnelID) {
            $http.get('/api/v1/morekhasi_saati/get_mandeh_morekhasi/?q=' + personnelID).then(function (data) {
                $scope.karaweb_trace = data.data;
            })
        }


        $scope.init();


        $scope.confirm = function (confirm_type) {
            $scope.morekhasi.exp.confirm_type = confirm_type;
            $http.post('/api/v1/morekhasi_saati/confirm/',
                $scope.morekhasi
            ).then(function (data) {

                if (!data.data.id) {
                    swal('Error','مجاز به این تایید نیستید', "error");

                } else {
                    $state.go('morekhasi-saati-add', {morekhasiID: data.data.id}, {reload: true});
                }
                // $scope.morekhasi = data.data;
            }).catch(function (data) {
                swal('Error', data.data, "error");


            })
        }


        $scope.get_another_personnel = function () {
            $scope.karaweb_trace = {};
            let a = prompt('کد پرسنلی را وارد نمایید مثلا 1234');
            if (a) {
                $http.post("/api/v1/morekhasi_saati/get_personnel_by_code/", {
                    personnel_code: a
                }).then(function (data) {
                    if (data.status === 400) {
                        swal('Error', data.data.message, "error");

                    } else {
                        $scope.morekhasi = data.data;
                        $scope.morekhasi.exp.typeof = 2;
                        $scope.get_mandeh_morekhasi($scope.morekhasi.exp['pos_vahede_darkhat']['personnel_code']);

                    }


                }).catch(function (data) {
                    swal('Error', data.data.message, "error");

                });
            }
        }

    })
;