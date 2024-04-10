'use strict';

var globalxml = "";
angular.module('AniTheme')
    .controller('BAMEditCtrl', function ($scope, $http, $translate, $rootScope, $state, $stateParams, $location, $modal, bamService) {


        $scope.bam = {};
        $scope.bpmns = [];
        $scope.steps = [];
        $scope.globalposid = '';
        $scope.selectedShakhesId = "";
        $scope.selectedBpmn = "";
        $scope.bam.time_period = '0';
        $scope.bam.don_or_run = '';
        $scope.times=[
            {id:0,name:'تمام مدت'},
            {id:7,name:'هفته گذشته'},
            {id:31,name:'ماه گذشته'},
            {id:93,name:'۳ ماه گذشته'},
            {id:183,name:'۶ ماه گذشته'},
            {id:365,name:'سال گذشته'}
        ];
        $scope.mhdoodes=[
            {id:0,name:'فعالیت های پایان یافته'},
            {id:1,name:'فعالیت های جاری'}
        ];

        $scope.cancelNewBAM = function () {
            $state.go("company.bam", {companyid: $stateParams.companyid});
        };

        $scope.getBpmns = function () {
            bamService.getBpmns($stateParams.companyid).then(function (res) {
                $scope.bpmns = res.data;
                $scope.getSteps();
            });
        };
        $scope.getObj = function () {
            bamService.getShakhes($stateParams.companyid, $stateParams.shakhesId).then(function (res) {
                $scope.bam = res.data;
                if ($scope.bam.done_or_run) {
                    $scope.bam.done_or_run = 1;
                } else {
                    $scope.bam.done_or_run = 0;
                }
            });
        };
        $scope.getSteps = function () {
            bamService.getSteps($stateParams.companyid, $scope.bam.bpmn_id).then(function (res) {
                $scope.steps = res.data;
                $scope.steps.unshift({name: 'تمامی فعالیت ها', id: 0});


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
            bamService.bamUpdate($stateParams.companyid,$stateParams.shakhesId, $scope.bam).then(function (data) {
                $scope.bpmn = data.data;
                $state.go("company.bam", {companyid: $stateParams.companyid});

            }).catch(function (data) {
                $scope.errors = data.data;
                $scope.errors = $scope.errors.message;
            });
        };

        $scope.getBpmns();
        $scope.getObj();
        $scope.clearAllTimeouts = function () {
            for (var i = 0; i < $scope.timeouts.length; i++) {
                clearTimeout($scope.timeouts[i])
            }
        };

    });
