'use strict';


angular.module('AniTheme').controller(
    'BIAmareRoozanehCtrl',
    function ($scope,
              $translate,
              $element,
              $q,
              $rootScope, $stateParams,
              $mdDialog,
              $location,
              $http) {


        $scope.today_exit_just_number = 0;
        $scope.get_today_exit = function () {
            $http.get("/api/v1/hamkaranKhorooj/get_today_exit_number/").then(function (data) {
                $scope.today_exit_just_number = data.data;
            })
        }


        $scope.showTables = function () {
            $element.find('.bi-under-table').toggle()
        }

        $scope.get_today_exit_for_chart = function () {
            $http.get("/api/v1/hamkaranKhorooj/get_today_exit_today_for_chart/").then(function (data) {
                $scope.today_exit_chart = data.data;
                let canvas = $element.find("#today_exit_chart")[0].getContext('2d');
                let myChart = new Chart(canvas, {
                    type: 'bar',
                    data: data.data,
                    plugins: [],
                    option: {},
                })
                myChart.options = {
                    animation: chart_option_animation_1(),
                    plugins: chart_option_plugin_1('خروج امروز', 'بر اساس نام مشتری - کالاهایی با سنجه وزن'),
                    scales: chart_option_scales_1(), locale: 'fa-IR',
                    responsive: true,
                    maintainAspectRatio: false,
                }
                myChart.update()
            })
        }
        $scope.get_today_exit_for_chart_by_product = function () {
            $http.get("/api/v1/hamkaranKhorooj/get_today_exit_today_for_chart_by_product/").then(function (data) {
                $scope.today_exit_chart_product = data.data;
                let canvas = $element.find("#today_exit_chart_by_prod")[0].getContext('2d');
                let myChart = new Chart(canvas, {
                    type: 'bar',
                    data: data.data,
                    plugins: [],
                    option: {},
                })
                myChart.options = {
                    animation: chart_option_animation_1(),
                    plugins: chart_option_plugin_1('خروج امروز', 'بر اساس کالا - کالاهایی با سنجه وزن'),
                    scales: chart_option_scales_1(), locale: 'fa-IR',
                    responsive: true,
                    maintainAspectRatio: false,
                }
                myChart.update()
            })
        }
        $scope.get_week_exit_for_chart = function () {
            $http.get("/api/v1/hamkaranKhorooj/get_today_exit_week_for_chart/").then(function (data) {
                $scope.get_week_exit_for_chart_table = data.data;
                let canvas = $element.find("#today_exit_chart_week")[0].getContext('2d');
                let myChart = new Chart(canvas, {
                    type: 'bar',
                    data: data.data,
                    plugins: [],
                    option: {},
                })
                myChart.options = {
                    animation: chart_option_animation_1(),
                    plugins: chart_option_plugin_1('خروج این هفته', 'بر اساس نام مشتری - کالاهایی با سنجه وزن'),
                    scales: chart_option_scales_1(), locale: 'fa-IR',
                    responsive: true,
                    maintainAspectRatio: false,
                }
                myChart.update()
            })
        }
        $scope.get_week_exit_for_chart_by_product = function () {
            $http.get("/api/v1/hamkaranKhorooj/get_today_exit_week_for_chart_by_product/").then(function (data) {
                $scope.get_week_exit_for_chart_by_product_table = data.data;
                let canvas = $element.find("#today_exit_chart_by_prod_week")[0].getContext('2d');
                let myChart = new Chart(canvas, {
                    type: 'bar',
                    data: data.data,
                    plugins: [],
                    option: {},
                })
                myChart.options = {
                    animation: chart_option_animation_1(),
                    plugins: chart_option_plugin_1('خروج این هفته', 'بر اساس کالا - کالاهایی با سنجه وزن'),
                    scales: chart_option_scales_1(), locale: 'fa-IR',
                    responsive: true,
                    maintainAspectRatio: false,
                }
                myChart.update()
            })
        }

        // $scope.get_amar_1 = function (amar_id){
        //     $http.get("/api/v1/dataForMS/"+amar_id+"/getLastEntery/").then(function (data){
        //         $scope.amar_1_values = data.data;
        //     })
        // }
        //
        // $scope.get_amar_2 = function (amar_id){
        //     $http.get("/api/v1/dataForMS/"+amar_id+"/getLastEntery/").then(function (data){
        //         $scope.amar_2_values = data.data;
        //     })
        // }
        // $scope.get_amar_3 = function (amar_id){
        //     $http.get("/api/v1/dataForMS/"+amar_id+"/getLastEntery/").then(function (data){
        //         $scope.amar_3_values = data.data;
        //     })
        // }


        $scope.init = function () {

            $scope.get_today_exit();
            $scope.get_today_exit_for_chart();
            $scope.get_today_exit_for_chart_by_product();
            $scope.get_week_exit_for_chart();
            $scope.get_week_exit_for_chart_by_product();
            // $scope.get_amar_1('579cdbe249dc912959982722');
            // $scope.get_amar_2('61913f9319c16c0e08fcfee6');
            // $scope.get_amar_3('6191402b19c16c0e08fcff29');

        }

        function chart_option_plugin_1(chart_title, subtutle,) {
            return {
                datalabels: {
                    align: 'top',
                    anchor: 'end',
                    labels: {
                        title: {
                            font: {
                                family: "'Yekan'"
                            }
                        }
                    }
                },
                title: {
                    display: true,

                    text: chart_title,
                    font: {
                        family: "'Yekan'",
                        size: 14
                    }
                },
                elements: {
                    bar: {
                        borderRadius: 3,
                    }

                },
                tooltip: {
                    bodyFont: {
                        family: "'Yekan'",
                        size: 14
                    },
                    footerFont: {
                        family: "'Yekan'",
                        size: 14
                    },
                    titleFont: {
                        family: "'Yekan'",
                        size: 14
                    },
                    rtl: true,
                },
                subtitle: {
                    display: true,
                    text: subtutle,
                    font: {
                        family: "'Yekan'",
                    }
                },
                legend: {
                    display: true,
                    labels: {
                        font: {
                            family: "'Yekan'"
                        }
                    }
                }
            }
        }
        function chart_option_animation_1() {
            let delayed;
            return {
                onComplete: () => {
                    delayed = true;
                },
                delay: (context) => {
                    let delay = 0;
                    if (context.type === 'data' && context.mode === 'default' && !delayed) {
                        delay = context.dataIndex * 300 + context.datasetIndex * 100;
                    }
                    return delay;
                },
            }
        }
        function chart_option_scales_1() {
            return {
                y: {

                    beginAtZero: true,
                    ticks: {
                        font: {
                            family: "'Yekan'"
                        }
                    }

                },
                x: {
                    title: {
                        display: false,
                        text: 'dsfasdfasdf'
                    },
                    beginAtZero: true,
                    ticks: {
                        font: {
                            family: "'Yekan'"
                        }
                    }

                }
            }
        }
        $scope.init();

    })