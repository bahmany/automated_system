'use strict';


angular.module('AniTheme').controller(
    'sample_page_for_ceo_ctrl',
    function ($scope,
              $translate,
              $q,
              $rootScope, $stateParams,
              $mdDialog,
              $location,
              $http) {

        let delayed;

        // Chart.register(ChartDataLabels);


        function buildToggler(navID) {
            return function () {
                $mdSidenav(navID)
                    .toggle()
                    .then(function () {
                        $log.debug("toggle " + navID + " is done");
                    });
            };
        }

        $scope.toggleLeft = buildToggler('right');

        $scope.previous_chart = null;
        const chart_foroosh_ghal = document.getElementById('chart_foroosh_ghal').getContext('2d');
        const myChart_foroosh_ghal = new Chart(chart_foroosh_ghal,
            {
                type: 'line',
                data: {},

                options: {
                    aspectRatio: 2,
                    onHover: (event, chartElement) => {
                        event.native.target.style.cursor = chartElement[0] ? 'pointer' : 'default';
                    },
                    onClick: (event, chartElement) => {
                        if (chartElement[0]) {
                            if (chartElement[0].datasetIndex === 1) {
                                $scope.previous_chart = $scope.get_faactor_1_for_foroosh
                                $scope.get_faactor_1_2_for_foroosh(chartElement[0].index);
                            }
                        }
                    },
                    animation: {
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
                    },
                    locale: 'fa-IR',
                    plugins: {
                        title: {
                            display: true,

                            text: "فاکتورهای صادره",
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
                            text: 'فاکتورهای صادره تمامی محصولاتی که تناژی محاسبه می شوند بع جز ضایعات',
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
                    },
                    scales: {
                        y: {

                            beginAtZero: true,
                            ticks: {
                                font: {
                                    family: "'Yekan'"
                                }
                            }

                        },
                        x: {
                            beginAtZero: true,
                            ticks: {
                                font: {
                                    family: "'Yekan'"
                                }
                            }

                        }
                    },
                }
            });

        // function clickHandler(click){
        //         console.log("hoooooo");
        //     const points = myChart_foroosh_ghal.getElementsAtEventForMode(click, 'nearest', {intersect: true}, true);
        //     if (points.length){
        //         const firstPoint = points[0];
        //         console.log("hoooooo");
        //     }
        // }

        // chart_foroosh_ghal.onclick = clickHandler;

        // const chart_foroosh_ghal_khadamaat = document.getElementById('chart_foroosh_ghal_khadamaat').getContext('2d');
        // const myChart_foroosh_ghal_khadamaat = new Chart(chart_foroosh_ghal_khadamaat, {
        //     type: 'bar',
        //     plugins: [ChartDataLabels],
        //     data: {
        //         labels: ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'],
        //         datasets: [{
        //             label: 'تناژ تولیدی',
        //             data: [12, 19, 3, 5, 2, 3, 12, 19, 3, 5, 2, 3],
        //             backgroundColor: [
        //                 'rgb(6,89,141)',
        //                 'rgb(6,89,141)',
        //                 'rgb(6,89,141)',
        //                 'rgb(6,89,141)',
        //                 'rgb(6,89,141)',
        //                 'rgb(6,89,141)',
        //                 'rgb(6,89,141)',
        //                 'rgb(6,89,141)',
        //                 'rgb(6,89,141)',
        //                 'rgb(6,89,141)',
        //                 'rgb(6,89,141)',
        //                 'rgb(6,89,141)',
        //
        //             ],
        //
        //         }]
        //     },
        //     options: {
        //         animation: {
        //             onComplete: () => {
        //                 delayed = true;
        //             },
        //             delay: (context) => {
        //                 let delay = 0;
        //                 if (context.type === 'data' && context.mode === 'default' && !delayed) {
        //                     delay = context.dataIndex * 300 + context.datasetIndex * 100;
        //                 }
        //                 return delay;
        //             },
        //         },
        //         locale: 'fa-IR',
        //         plugins: {
        //
        //             datalabels: {
        //                 align: 'top',
        //                 anchor: 'end',
        //                 labels: {
        //                     title: {
        //                         font: {
        //                             family: "'Yekan'"
        //                         }
        //                     }
        //                 }
        //             },
        //
        //
        //             title: {
        //                 display: true,
        //
        //                 text: "فروش سال جاری قلع اندود - خدماتی",
        //                 font: {
        //                     family: "'Yekan'",
        //                     size: 14
        //                 }
        //             },
        //             elements: {
        //                 bar: {
        //                     borderRadius: 3,
        //                 }
        //
        //             },
        //             tooltip: {
        //                 bodyFont: {
        //                     family: "'Yekan'",
        //                     size: 14
        //                 },
        //                 footerFont: {
        //                     family: "'Yekan'",
        //                     size: 14
        //                 },
        //                 titleFont: {
        //                     family: "'Yekan'",
        //                     size: 14
        //                 },
        //                 rtl: true,
        //             },
        //             subtitle: {
        //                 display: true,
        //                 text: 'آخرین بروز رسانی : ۱۴۰۰/۱۰/۱۲',
        //                 font: {
        //                     family: "'Yekan'",
        //
        //                 }
        //             },
        //
        //             legend: {
        //                 display: true,
        //
        //                 labels: {
        //                     font: {
        //                         family: "'Yekan'"
        //                     }
        //                 }
        //             }
        //         },
        //         scales: {
        //             y: {
        //
        //                 beginAtZero: true,
        //                 ticks: {
        //                     font: {
        //                         family: "'Yekan'"
        //                     }
        //                 }
        //
        //             },
        //             x: {
        //                 beginAtZero: true,
        //                 ticks: {
        //                     font: {
        //                         family: "'Yekan'"
        //                     }
        //                 }
        //
        //             }
        //         },
        //     }
        // });

        const chart_foroosh_ghal_daily = document.getElementById('chart_foroosh_ghal_daily').getContext('2d');
        const myChart_chart_foroosh_ghal_daily = new Chart(chart_foroosh_ghal_daily, {
            type: 'bar',
            plugins: [ChartDataLabels],
            data: {
                labels: [
                    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30
                ],
                datasets: [
                    {
                        label: 'تناژ ',
                        data: [
                            12, 19, 3, 5, 2, 3, 12, 19, 3, 5, 2,
                            12, 19, 3, 5, 2, 3, 12, 19, 3, 5, 2,
                            12, 19, 3, 5
                        ],
                        backgroundColor: [
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',
                            'rgb(4,110,10)',

                        ],

                    },
                    {
                        label: 'برنامه ',
                        type: 'line',
                        data: [
                            10, 11, 12, 13, 14, 15, 16, 9, 9, 8,
                            12, 19, 3, 5, 2, 3, 12, 19, 3, 5, 2,
                            12, 19, 3, 5, 2, 3, 12, 19, 3, 5, 2,
                        ],
                        backgroundColor: [
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',
                            'rgb(81,49,145)',

                        ],

                    }
                ]
            },
            options: {
                animation: {
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
                },
                locale: 'fa-IR',
                plugins: {

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

                        text: "فروش روزانه ماه جاری",
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
                        text: 'آخرین بروز رسانی : ۱۴۰۰/۱۰/۱۲',
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
                },
                scales: {
                    y: {

                        beginAtZero: true,
                        ticks: {
                            font: {
                                family: "'Yekan'"
                            }
                        }

                    },
                    x: {
                        beginAtZero: true,
                        ticks: {
                            font: {
                                family: "'Yekan'"
                            }
                        }

                    }
                },
            }
        });


        var gauge_tamine_emsaal = document.getElementById("gauge_tamine_emsaal").getContext("2d");
        var Chartgauge_tamine_emsaal = new Chart(gauge_tamine_emsaal, {
            type: 'gauge',
            data: {
                datasets: [{
                    value: 0.5,
                    minValue: 0,
                    data: [1, 2, 3, 4],
                    backgroundColor: ['green', 'yellow', 'orange', 'red'],
                }]
            },
            options: {
                needle: {
                    radiusPercentage: 2,
                    widthPercentage: 3.2,
                    lengthPercentage: 80,
                    color: 'rgba(0, 0, 0, 1)'
                },
                valueLabel: {
                    display: true,
                    formatter: (value) => {
                        return '$' + Math.round(value);
                    },
                    color: 'rgba(255, 255, 255, 1)',
                    backgroundColor: 'rgba(0, 0, 0, 1)',
                    borderRadius: 5,
                    padding: {
                        top: 10,
                        bottom: 10
                    }
                }
            }
        });

        var gauge_tamine_khreji_een_mah = document.getElementById("gauge_tamine_khreji_een_mah").getContext("2d");
        var Chartgauge_tamine_khreji_een_mah = new Chart(gauge_tamine_khreji_een_mah, {
            type: 'gauge',
            data: {
                datasets: [{
                    value: 0.5,
                    minValue: 0,
                    data: [1, 2, 3, 4],
                    backgroundColor: ['green', 'yellow', 'orange', 'red'],
                }]
            },
            options: {
                needle: {
                    radiusPercentage: 2,
                    widthPercentage: 3.2,
                    lengthPercentage: 80,
                    color: 'rgba(0, 0, 0, 1)'
                },
                valueLabel: {
                    display: true,
                    formatter: (value) => {
                        return '$' + Math.round(value);
                    },
                    color: 'rgba(255, 255, 255, 1)',
                    backgroundColor: 'rgba(0, 0, 0, 1)',
                    borderRadius: 5,
                    padding: {
                        top: 10,
                        bottom: 10
                    }
                }
            }
        });


        var gauge_tamine_dakheli_een_maah = document.getElementById("gauge_tamine_dakheli_een_maah").getContext("2d");
        var Chartgauge_tamine_dakheli_een_maah = new Chart(gauge_tamine_dakheli_een_maah, {
            type: 'gauge',
            data: {
                datasets: [{
                    value: 0.5,
                    minValue: 0,
                    data: [1, 2, 3, 4],
                    backgroundColor: ['green', 'yellow', 'orange', 'red'],
                }]
            },
            options: {
                needle: {
                    radiusPercentage: 2,
                    widthPercentage: 3.2,
                    lengthPercentage: 80,
                    color: 'rgba(0, 0, 0, 1)'
                },
                valueLabel: {
                    display: true,
                    formatter: (value) => {
                        return '$' + Math.round(value);
                    },
                    color: 'rgba(255, 255, 255, 1)',
                    backgroundColor: 'rgba(0, 0, 0, 1)',
                    borderRadius: 5,
                    padding: {
                        top: 10,
                        bottom: 10
                    }
                }
            }
        });

        var gauge_tamine_navarde_een_mah = document.getElementById("gauge_tamine_navarde_een_mah").getContext("2d");
        var Chartgauge_tamine_navarde_een_mah = new Chart(gauge_tamine_navarde_een_mah, {
            type: 'gauge',
            data: {
                datasets: [{
                    value: 0.5,
                    minValue: 0,
                    data: [1, 2, 3, 4],
                    backgroundColor: ['green', 'yellow', 'orange', 'red'],
                }]
            },
            options: {
                needle: {
                    radiusPercentage: 2,
                    widthPercentage: 3.2,
                    lengthPercentage: 80,
                    color: 'rgba(0, 0, 0, 1)'
                },
                valueLabel: {
                    display: true,
                    formatter: (value) => {
                        return '$' + Math.round(value);
                    },
                    color: 'rgba(255, 255, 255, 1)',
                    backgroundColor: 'rgba(0, 0, 0, 1)',
                    borderRadius: 5,
                    padding: {
                        top: 10,
                        bottom: 10
                    }
                }
            }
        });


        $scope.amare_forooshe_koli = {}
        $scope.get_total_factors = function () {
            // $http.get("/api/v1/bi_sqls/convert_old/").then(function (data){
            $http.get("/api/v1/bi_sqls/get_foroosh/").then(function (data) {
                $scope.amare_forooshe_koli = data.data;
            })
        }

        $scope.get_total_factors();

        $scope.get_faactor_1_for_foroosh = function () {
            $http.get("/api/v1/bi_sqls/get_faactor_1_for_foroosh/").then(function (data) {
                $scope.previous_chart = null;
                myChart_foroosh_ghal.data = data.data;
                myChart_foroosh_ghal.update();

            })
        }

        $scope.get_faactor_1_2_for_foroosh = function (month) {
            $http.get("/api/v1/bi_sqls/get_faactor_1_2_for_foroosh/?month=" + month).then(function (data) {
                myChart_foroosh_ghal.data = data.data;
                myChart_foroosh_ghal.update();

            })
        }


        $scope.get_faactor_1_for_foroosh();

    })


