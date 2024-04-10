'use strict';
// The restrict option is typically set to:
// 'A' - only matches attribute name
// 'E' - only matches element name
// 'C' - only matches class name
// 'M' - only matches comment
angular.module('AniTheme').directive('biChart', function () {

    return {
        templateUrl: '/static/angularThings/BI/BICharts/directives/bi_chart.html',
        restrict: 'E',
        scope: {
            chartid: '=chartid'
        },
        replace: true,
        controller: ['$scope', '$element', '$attrs', '$transclude', '$http',
            function ($scope, $element, $attrs, $transclude, $http) {


                $scope.request = {};
                $scope.chart_data = {};
                $scope.chart = {};
                $scope.chart_data_history = [];
                $scope.request.level = 0;
                $scope.is_loading_data = false;
                let current_canvas;
                let current_chart;

                $scope.init = function () {
                    $http.get('/api/v1/bi_chart/' + $scope.chartid + "/").then(function (data) {
                        $scope.chart = data.data;

                        $scope.render_chart();

                    });


                }


                $scope.get_request_data = function (is_referesh = false) {
                    if ($scope.is_loading_data) {
                        return;
                    }
                    if ($scope.chart_data) {
                        if ($scope.chart_data) {
                            if ($scope.request.level >= $scope.chart_data.max_level) {
                                console.log('max level .. !');
                                return;

                            }

                        }
                    }
                    $scope.is_loading_data = true;
                    $http.post('/api/v1/bi_chart/' + $scope.chartid + "/get_chart_with_request/", $scope.request).then(
                        function (data) {
                            $scope.is_loading_data = false;
                            $scope.chart_data = data.data;
                            $scope.update_chart($scope.chart_data);
                            if (is_referesh === false) {
                                $scope.chart_data_history.push($scope.chart_data);
                            }
                        }).catch(function (data) {
                        $scope.is_loading_data = false;

                    });
                }

                $scope.go_to_level = function (index) {
                    if (index === $scope.chart_data_history.length - 1) {
                        $scope.get_request_data(true);
                    } else {
                        $scope.request.level = $scope.chart_data_history[index].level;
                        $scope.chart_data = $scope.chart_data_history[index];
                        $scope.update_chart($scope.chart_data_history[index]);
                        $scope.chart_data_history.splice(index + 1, $scope.chart_data_history.length);

                    }

                }


                $scope.update_chart_just_option = function () {

                    current_chart.options = chart_option_1(current_chart, $scope);
                    current_chart.update();

                }


                $scope.update_chart = function (data) {
                    current_chart.data = data;
                    current_chart.options = chart_option_1(current_chart, $scope);
                    current_chart.update();
                }

                $scope.render_chart = function () {
                    if (current_canvas === undefined) {
                        current_canvas = $element.find("#chart_preview")[0].getContext('2d');
                        current_chart = new Chart(current_canvas, {
                            type: $scope.chart.details.chart_type,
                            data: {},
                            plugins: [ChartDataLabels],
                            option: {}
                        });

                    }
                    $scope.get_request_data();


                    // $scope.init_chart();


                }

                $scope.init();


            }
        ],


    }
});
