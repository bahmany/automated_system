'use strict';

angular.module('AniTheme')
    .directive('dashboardStatics', function () {
        return {
            templateUrl: '/static/angularThings/widgets/dashboard_statitics/SDS_template1.html',
            restrict: 'E',
            scope: {
                staticid: "="
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
                                  $rootScope,
                                  httpService,
                                  pendingRequests,
                                  companiesManagmentService) {


                $scope.valueMouseOn = 0;


                //$scope.SetStaticForBlockNull = function (currentID) {
                //    // $scope.current.static_id = null;
                //    $http.post("/api/v1/forced/setStaticDashboard/", {
                //        id: currentID
                //    }).then(function (data) {
                //
                //        $scope.$parent.$parent.$parent.$parent.GetDashboard();
                //    })
                //};


                $scope.current = {};
                $http.get("/api/v1/statistics/" + $scope.staticid + "/GetSmallStatic/").then(function (data) {
                    // sparkLineBar($element, data, '45px', 3, '#fff', 2);
                    $scope.current = data.data;

                    var ctx = $($($element).find(".chartPlace")[0])[0];

                    var maxmin = data.data.exp;
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
                            labels: data.data.items.map(function (obj) {
                                return obj["dt"]
                            }),
                            datasets: [{
                                lineTension: 0.1,
                                label: '',
                                data: data.data.items.map(function (obj) {
                                    return obj["val"]
                                }),
                                borderWidth: 3,
                                borderColor: '#fff'

                            }]
                        },
                        options: {
                            horizontalLine: maxmin,
                            scales: {
                                paddingLeft: 20,
                                paddingRight: 20,
                                paddingTop: 20,
                                paddingBottom: 20,
                                yAxes: [{
                                    ticks: {
                                        beginAtZero: true,
                                        showLabelBackdrop: false

                                    },
                                    display: false
                                }],
                                xAxes: [{

                                    display: false

                                }]


                            },
                            fill: true,
                            pointDot: false,
                            bezierCurve: false,
                            scaleShowVerticalLines: false,
                            title: {
                                display: true,
                                text: data.name,
                                fontColor: '#fff'

                            },
                            legend: {
                                display: false,
                                labels: {
                                    fontColor: 'rgb(255, 99, 132)'
                                }
                            }
                        }
                    });
                });


                // //console.log($attrs);


            }
        }
    });