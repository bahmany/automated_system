'use strict';
// The restrict option is typically set to:
// 'A' - only matches attribute name
// 'E' - only matches element name
// 'C' - only matches class name
// 'M' - only matches comment
angular.module('AniTheme').directive('bpmsRelatedChart', function () {

    return {
        templateUrl: '/static/angularThings/BI/BIPages/directives/bpms_related_chart.html',
        restrict: 'E',
        scope: {
            currentcell: '=currentcell'
        },
        replace: true,
        controller: ['$scope', '$element', '$attrs', '$transclude', '$http',
            function ($scope, $element, $attrs, $transclude, $http) {

            $scope.loading = false;


                let canvas = $element.find("canvas")[0].getContext('2d');
                let myChart = new Chart(canvas, {
                    type: 'bar',
                    plugins: [ChartDataLabels],
                    data: {},
                    option: {}

                })

                $scope.prev_data = null;
                $scope.prev_req = null;
                $scope.current_data_req = {};
                $scope.current_chart_data = {};

                $scope.step = [];
                $scope.current_step = 0; // این برای اولین شروع است

                $scope.change_source = function (source_index) {
                    if ($scope.current_step === source_index) {
                        return
                    }
                    $scope.step.splice(source_index + 1, $scope.step.length);
                    $scope.current_step = source_index;
                    $scope.apply_step_to_chart(
                        source_index
                    )
                }

                $scope.apply_step_to_chart = function (stepID) {
                    myChart.options = $scope.step[stepID].option($element, $scope,);
                    myChart.data = $scope.step[stepID].data;
                    myChart.update();
                }

                $scope.get_data = function (req) {
                    $scope.loading = true;
                    if ($scope.step.length !== 0) {
                        if ($scope.step[$scope.current_step].request.groupby_index + 1 >= $scope.step[$scope.current_step].data.max_depth) {
                            // اینجا یادم باشه یه چیزی نشون بدم که کاربر بفهمه دیگه مرحله ی آخر هست و از این بیشتر زووم نمیشه
                            $scope.loading = false;
                            return
                        }

                    } else {


                    }

                    $http.post("/api/v1/bi_dashboard_page/get_chart_data/", req).then(function (data) {
                        $scope.step.push(
                            {
                                data: data.data,
                                option: chart_option_1,
                                request: req,
                            }
                        );
                        $scope.current_step = req.groupby_index;
                        $scope.apply_step_to_chart($scope.current_step);
                            $scope.loading = false;
                    })
                }


                $scope.get_for_init = function () {
                    let req = {}
                    req['chart_id'] = $scope.currentcell.chart_id;
                    req['groupby_index'] = 0;
                    req['groupby_value'] = -1;
                    req['groupby_dataset_index'] = 0;
                    req['chart_type'] = $scope.currentcell.type;

                    $scope.get_data(req);
                }
                $scope.get_for_init();
            }
        ],


    }
});
