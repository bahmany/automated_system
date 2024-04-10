'use strict';

angular.module('RahsoonApp').controller(
    'HamkariDetailsCtrl',
    function ($scope, $mdDialog,
              $translate, $stateParams,
              $q, $location,
              $http,
              $rootScope,
              $timeout) {


        $scope.hamkari = {};
        $scope.jobs = {};


        $scope.getJobs = function () {
            $http.get("/reg/api/v1/jobs/" + $stateParams.hamkariID + "/").then(function (data) {
                $scope.hamkari = data.data;

                $http.get("/reg/api/v1/jobs/" + $stateParams.hamkariID + "/items/").then(function (data) {
                    $scope.jobs = data.data;
                })
            });

        };

        $scope.getJobs();


        $scope.status = '  ';
        $scope.customFullscreen = false;
        var jobItem = {};

        function DialogController($scope, $mdDialog) {
            $scope.jobItem = jobItem;
            $scope.hide = function () {
                $mdDialog.hide();
            };
            $scope.cancel = function () {
                $mdDialog.cancel();
            };
            $scope.confirmCancel = function () {
                $scope.jobItem.removeIt = true;
                jobItem.registered = false;

                $mdDialog.hide($scope.jobItem);
            }
            $scope.confirm = function () {
                jobItem.registered = true;
                $mdDialog.hide($scope.jobItem);
            };

        }

        $scope.jobItem = {};
        $scope.getJobDetails = function (ev, item) {
            $scope.jobItem = item;
            $scope.showModal(ev)
        }

        $scope.showModal = function (ev) {
            jobItem = $scope.jobItem;
            $mdDialog.show({
                controller: DialogController,
                templateUrl: '/reg/page/hamkariDetailsItemModal',
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                jobItem: $scope.jobItem,
                fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
            })
                .then(function (jobItem) {
                    // if (jobItem.id){
                    // $http.post("/reg/api/v1/jobs/removeRegisterForJob/", jobItem).then(function (data) {
                    //
                    // })
                    // } else {
                    // $http.post("/reg/api/v1/jobs/registerForJob/", jobItem).then(function (data) {
                    //
                    // })
                    //
                    // }
                    $http.post("/reg/api/v1/jobs/registerForJob/", jobItem).then(function (data) {

                    })

                }, function () {
                    $scope.status = 'You cancelled the dialog.';
                });
        };


    });