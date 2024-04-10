'use strict';

var globalxml = "";
angular.module('AniTheme')
    .controller('BAMNewCtrl', function ($scope, $http, $translate, $rootScope, $state, $stateParams, $location, $modal, bamService) {


        $scope.bam = {};
        $scope.bpmns = [];
        $scope.steps = [];
        $scope.globalposid = '';
        $scope.selectedShakhesId = "";
        $scope.selectedBpmn = "";
        $scope.bam.time_period = '0';
        $scope.bam.don_or_run = '';
        $scope.cancelNewBAM = function () {
            $state.go("company.bam", {companyid: $stateParams.companyid});
        };

        $scope.getBpmns = function () {
            bamService.getBpmns($stateParams.companyid).then(function (res) {
                $scope.bpmns = res.data;
            });
        };
        $scope.getSteps = function () {
            bamService.getSteps($stateParams.companyid, $scope.bam.bpmn_id).then(function (res) {
                $scope.steps = res.data;
                $scope.steps.unshift({name: 'تمامی فعالیت ها', id: 0});
                $scope.bam.step_id = 0;

            });
        };


        $scope.saveIt = function () {
            for (var invx = 0; invx < $scope.bpmns.length; invx++) {
                if ($scope.bpmns[invx].id == $scope.bam.bpmn_id) {
                    $scope.bam.bpmn_name = $scope.bpmns[invx].name;
                    invx = $scope.bpmns.length;
                }
            }
            for (var invwx = 0; invwx < $scope.steps.length; invwx++) {
                if ($scope.steps[invwx].id == $scope.bam.step_id) {
                    $scope.bam.step_name = $scope.steps[invwx].name;
                    invwx = $scope.steps.length;
                }
            }
            bamService.bamCreate($stateParams.companyid, $scope.bam).then(function (data) {
                $scope.bpmn = data.data;
                $rootScope.$broadcast('refreshList');
                $state.go("company.bam", {companyid: $stateParams.companyid});

            }).catch(function (data) {
                $scope.errors = data.data;
                $scope.errors = $scope.errors.message;
            });
        };

        $scope.getBpmns();
        $scope.clearAllTimeouts = function () {
            for (var i = 0; i < $scope.timeouts.length; i++) {
                clearTimeout($scope.timeouts[i])
            }
        };

    });
