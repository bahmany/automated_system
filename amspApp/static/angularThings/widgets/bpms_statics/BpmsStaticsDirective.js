'use strict';

angular.module('AniTheme')
    .directive('dashboardBpmsStatics', function () {
        return {
            templateUrl: '/static/angularThings/widgets/bpms_statics/BSD_temp1.html',
            restrict: 'E',
            scope: {
                it: "="
            },
            replace: true,
            controller: function ($scope,
                                  $q,
                                  $http,
                                  $timeout,
                                  $state,
                                  $mdToast,
                                  $$$,
                                  $stateParams,
                                  $templateCache,
                                  $translate,
                                  $location,
                                  $attrs,
                                  $element,
                                  $rootScope) {
                //debugger;

                //console.log($scope.it);


                //var lineChartData = {
                //    labels: ["", "", "", "", "", "", ""],
                //    datasets: [
                //        {
                //            fillColor: "rgba(220,220,220,0.5)",
                //            strokeColor: "rgba(220,220,220,1)",
                //            pointColor: "rgba(220,220,220,1)",
                //            pointStrokeColor: "#fff",
                //            data: [65, 59, 90, 81, 56, 55, 40]
                //        },
                //        {
                //            fillColor: "rgba(151,187,205,0.5)",
                //            strokeColor: "rgba(151,187,205,1)",
                //            pointColor: "rgba(151,187,205,1)",
                //            pointStrokeColor: "#fff",
                //            data: [28, 48, 40, 19, 96, 27, 100]
                //        }
                //    ]
                //
                //};

                // getting data ids to http request
                $scope.dataIds = [];
                $scope.statics = {};
                $scope.GetDatas = function () {
                    var labels = [];
                    if (!($scope.it.data_id)) {
                        return
                    }
                    var gettingIds = [];
                    for (var i = 0; i < $scope.it.data_id.length; i++) {
                        gettingIds.push($scope.it.data_id[i].static_id);
                    }
                    var it = $scope.it;
                    $http.post("/api/v1/statistics/GetSmallStaticContrastive/", gettingIds).then(function (data) {

                        $scope.statics = data.data;

                        // creating datas
                        var ds = {};
                        ds.labels = data.data.labels;
                        ds.datasets = [];
                        for (var i = 0; i < $scope.it.data_id.length; i++) {
                            for (var y = 0; y < data.data.datasets.length; y++) {
                                if ($scope.it.data_id[i].static_id == data.data.datasets[y].tmpl.id) {
                                    var lbl = "";
                                    if ($scope.it.data_id[i].name) {
                                        lbl = $scope.it.data_id[i].name
                                    } else {
                                        lbl = data.data.datasets[y].tmpl.name
                                    }
                                    $scope.statics.datasets[y].backColor = $scope.it.data_id[y].static_color;
                                    ds.datasets.push({
                                            data: data.data.datasets[y].values.map(function (value, index) {
                                                return value.value
                                            }),
                                            label: lbl,
                                            borderWidth: 2,
                                            borderColor: $scope.it.data_id[i].static_color

                                        }
                                    )
                                }
                            }
                        }

                        // getting max and min
                        var max = 0,
                            min = 100000000000,
                            top = 0, botton = 0,
                            sumall = 0, count = 0;

                        for (var i = 0; data.data.datasets.length > i; i++) {
                            for (var y = 0; data.data.datasets[i].values.length > y; y++) {
                                // debugger;

                                if (data.data.datasets[i].values[y].value) {

                                    sumall += data.data.datasets[i].values[y].value;
                                    count += 1;
                                    if (max < data.data.datasets[i].values[y].value) {
                                        max = data.data.datasets[i].values[y].value
                                    }
                                    if (min > data.data.datasets[i].values[y].value) {
                                        min = data.data.datasets[i].values[y].value
                                    }
                                }
                            }
                        }
                        // getting suggestedMax, suggestedMin
                        // debugger;
                        top = parseInt((sumall / count) + (sumall / count));
                        if (min != 0) {
                            botton = parseInt((min / count) - (min / count));
                        } else {
                            botton = 0;
                        }


                        var ctx = $($($element).find(".canvbpm")[0])[0].getContext("2d");


                        var maxmin = data.data.datasets[0].tmpl.exp;
                        if (maxmin) {
                            maxmin = [{
                                "y": maxmin.max,
                                "style": "rgba(255, 0, 0, .3)",
                                "text": "max"
                            }, {
                                "y": maxmin.min,
                                "text": "min"
                            }]
                        } else {
                            maxmin = []
                        }


                        var myChart = new Chart(ctx, {
                            type: 'line',
                            data: {
                                labels: ds.labels,
                                datasets: ds.datasets
                            },
                            options: {
                                horizontalLine: maxmin,
                                scales: {
                                    yAxes: [{
                                        display: true,
                                        ticks: {
                                            max: top,
                                            min: botton,
                                            beginAtZero: false,
                                            callback: function (value, index, values) {
                                                return value.toLocaleString();
                                            }
                                        }
                                    }],
                                    xAxes: [{}]
                                },
                                title: {
                                    display: false,
                                    text: ''
                                },
                                legend: {
                                    display: true
                                }
                            }
                        });
                        // var myChart = new Chart(ctx, {
                        //     type: 'line',
                        //     data: {
                        //         labels: ds.labels,
                        //         datasets: ds.datasets
                        //     },
                        //     options: {
                        //         scales: {
                        //             // paddingLeft: 20,
                        //             // paddingRight: 20,
                        //             // paddingTop: 20,
                        //             // paddingBottom: 20,
                        //             yAxes: [{
                        //                 display: true,
                        //                 ticks: {
                        //                     beginAtZero: false,
                        //
                        //                     // ,
                        //                     max: 300000000,
                        //                     min: 140000000,
                        //                     suggestedMin: 150000000,
                        //                     suggestedMax: 270000000
                        //                     // showLabelBackdrop: false
                        //                 }
                        //                 // rectTop: 200000000,
                        //                 // rectBottom: 150000000
                        //                 // display: false
                        //             }],
                        //             // threshold: [
                        //             //     {
                        //             //         min: 150000000,
                        //             //         max: 23000000,
                        //             //         backgroundColor: 'rgba(0, 192, 0, 0.1)',
                        //             //         borderWidth: 3,
                        //             //         borderColor: 'rgba(0, 192, 0, 0.1)',
                        //             //         borderCapStyle: 'butt',
                        //             //         borderDash: [],
                        //             //         borderDashOffset: 0.0,
                        //             //         borderJoinStyle: 'miter',
                        //             //         fill: true,
                        //             //         labelString: 'Normal Range',
                        //             //         hAlign: 'left',
                        //             //         vAlign: 'top',
                        //             //         paddingTop: 6,
                        //             //         paddingBottom: 6,
                        //             //         paddingLeft: 6,
                        //             //         paddingRight: 6
                        //             //     }
                        //             // ],
                        //             xAxes: [{
                        //
                        //                 // display: false
                        //
                        //             }]
                        //
                        //
                        //         },
                        //         // fill: false,
                        //         // pointDot: false,
                        //         // bezierCurve: false,
                        //         // scaleShowVerticalLines: false,
                        //         title: {
                        //             display: false,
                        //             text: ''
                        //             // fontColor: '#fff'
                        //
                        //         },
                        //         legend: {
                        //             display: true
                        //             // labels: {
                        //             //     fontColor: 'rgb(255, 99, 132)'
                        //             // }
                        //         }
                        //     }
                        // });

                        // debugger;
                        //$scope.dataIds.push({
                        //    label: data.name,
                        //    borderWidth: 2,
                        //    data: data.itemsJV,
                        //    borderColor: $scope.it.data_id[i].static_color,
                        //    dto_compl: data.items,
                        //    sid: data.id
                        //})
                    });


                    for (var i = 0; i < $scope.dataIds.length; i++) {
                        //console.log($scope.dataIds[i]);
                    }

                };

                $scope.GetDatas();


            }
        }
    });