'use strict';

var globalxml = "";
angular.module('AniTheme')
    .controller('BAMShowShakhesCtrl', function ($scope, $http, $translate, $rootScope, $state, $stateParams, $location, $modal, bamService) {


        $scope.shakhes = {};
        $scope.bam = {};
        $scope.monitorRes = {};
        $scope.globalposid = '';
        $scope.selectedShakhesId = "";

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
                        backgroundColor: 'rgba(2, 136, 209,0.3)',

                        borderColor: 'rgba(2, 136, 209,1)',

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

        $scope.createChart = function () {
                bamService.shakhesReport($stateParams.companyid,$stateParams.shakhesId).then(function (res2) {

                    $scope.monitorRes=res2.data.monitorRes;
                    $scope.bam.runningCount=res2.data.totalRunning;
                    $scope.bam.doneCount=res2.data.totalDone;
                    $scope.bam.name=res2.data.name;
                    $scope.bam.bpmn_name=res2.data.bpmn_name;
                    $scope.generateBarChart(res2.data.repRunning, 'barChartRunning', 'وضعیت فعالیت های جاری');
                    $scope.generateBarChart(res2.data.repDone, 'barChartDone', 'وضعیت فعالیت های فرایندهای پایان یافته');
                    //$scope.bam.runningCount = res2.totalRunning;
                });
        };


        $scope.createChart();

        $scope.clearAllTimeouts = function () {
            for (var i = 0; i < $scope.timeouts.length; i++) {
                clearTimeout($scope.timeouts[i])
            }
        };

    });
