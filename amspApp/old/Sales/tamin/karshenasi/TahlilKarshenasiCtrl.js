'use strict';
angular.module('AniTheme')
    .controller(
        'TahlilKarshenasiCtrl',
        function ($scope, $window, $http, $translate, $rootScope, $stateParams, $location, $timeout, $filter, $mdDialog) {

            var fontSize = 16;
            var fontStyle = 'normal';
            var fontFamily = 'Yekan';
            $scope.getLastWeek = function () {
                $http.get("/api/v1/salesProfileSizes/getTop10/").then(function (data) {
                    Chart.defaults.global.defaultFontFamily = "Yekan, cent";
                    Chart.helpers.merge(Chart.defaults.global, {
                        aspectRatio: 4 / 3,
                        tooltips: false,
                        layout: {
                            padding: {
                                top: 42,
                                right: 16,
                                bottom: 0,
                                left: 8
                            }
                        },
                        elements: {
                            line: {
                                fill: true
                            },
                            point: {
                                hoverRadius: 7,
                                radius: 5
                            }
                        },
                        plugins: {
                            legend: true,
                            title: true
                        }
                    });
                    var barChartData = {
                        labels: data.data.details.map(function (v) {
                            return v.dateStr
                        }),

                        datasets: [{
                            label: 'کیلوگرم',
                            font: Chart.helpers.fontString(fontSize, fontStyle, fontFamily),
                            borderWidth: 1,
                            data: data.data.details.map(function (v) {
                                return v.sumOfQty
                            }),
                            datalabels: {
                                align: 'start',
                                anchor: 'end'
                            }

                        }]
                    }

                    var ctx = document.getElementById('canvas').getContext('2d');
                    window.myBar = new Chart(ctx, {
                        type: 'bar',
                        tooltips: {
                            enabled: true
                        },
                        data: barChartData,
                        options: {
                            tooltips: {
                                enabled: true
                            },
                            display: true,
                            responsive: false,
                            legend: {
                                position: 'top',
                            },
                            title: {
                                display: true,
                                text: 'میزان کل درخواست در روز'
                            }
                        }
                    });
                })
            };
            $scope.getLastWeek();


            // };

        });




