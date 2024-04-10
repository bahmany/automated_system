'use strict';

var globalxml = "";
angular.module('AniTheme')
    .controller('BAMDashboardCtrl', function ($scope, $http, $translate, $rootScope, $state, $stateParams, $location, $modal, bamService) {


        $scope.bam = {};
        $scope.doneData = [];
        $scope.runningData = [];
        $scope.globalposid = '';
        $scope.selectedShakhesId = "";

        $scope.newBAM = function () {
            $state.go("company.bam.new", {companyid: $stateParams.companyid});
        };
        $scope.generateBarChart = function (chartdata, elmId, datalabel) {
            var reportValues = [], names = [];
            for (var indxfr = 0; indxfr < chartdata.length; indxfr += 1) {
                names.push(chartdata[indxfr].name);
                reportValues.push(chartdata[indxfr].value);
            }
            var ctx = document.getElementById(elmId).getContext("2d");
            var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: names,
                    datasets: [{
                        label: datalabel,
                        data: reportValues,
                        backgroundColor: 'rgba(255, 159, 64, 0.2)',

                        borderColor: 'rgba(255,99,132,1)',

                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });
        };

        $scope.createRunningChart = function () {
            bamService.getCurrent(0).then(function (res) {
                $scope.globalposid = res.data.positionDocument;
                bamService.allRunningReport($stateParams.companyid).then(function (res2) {
                    $scope.generateBarChart(res2.data.report, 'barChartRunning', 'تعداد فرایندهای درحال اجرا');
                    $scope.bam.runningCount = res2.data.totalRunning;
                });
            });

        };


        $scope.createDoneChart = function () {
            bamService.getCurrent(0).then(function (res) {
                $scope.globalposid = res.data.positionDocument;
                bamService.allDoneReport($stateParams.companyid).then(function (res2) {
                    $scope.generateBarChart(res2.data.report, 'barChartDone', 'تعداد فرایندهای پایان یافته');
                    $scope.bam.doneCount = res2.data.totalDone;
                });
            });

        };
        $scope.createRunningChart();
        $scope.createDoneChart();

        $scope.clearAllTimeouts = function () {
            for (var i = 0; i < $scope.timeouts.length; i++) {
                clearTimeout($scope.timeouts[i])
            }
        };

    });
