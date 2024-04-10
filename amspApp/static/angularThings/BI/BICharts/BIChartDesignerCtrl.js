'use strict';


angular.module('AniTheme').controller(
    'BIChartDesignerCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope, $stateParams,
              $mdDialog, $element,
              $location, $filter,
              $http) {


        $scope.sqls = [];
        $scope.chart = {};
        $scope.chart.details = {};
        $scope.chart.details.sql = {};
        $scope.chart.details.sql.table_spec = []

        $scope.get_sqls = function () {
            $http.get('/api/v1/bi_sqls/bi_get_sqls_brief/').then(function (data) {
                $scope.sqls = data.data;
            })
        }

        $scope.editorOptionsSql = {
            lineWrapping: false,
            theme: 'twilight',
            // readOnly: 'nocursor',
            lineNumbers: true,
            // readOnly: 'nocursor',
            mode: 'sql'
        };

        $scope.test_data = function () {
            // $http.get('/api/v1/bi_sqls/' + $scope.chart.details.sql.id + "/get_mssql_table_info/").then(function (data) {
            //     $scope.chart.details.sql.table_spec = data.data;
            $scope.get_sql_script();
            // });
        }

        $scope.get_table_data = function () {
            $http.get('/api/v1/bi_chart/' + $scope.chart.id + "/preview_table_by_chartID/").then(function (data) {
                $.jsontotable(data.data, {
                    header: true,
                    id: "#tbl77",
                    className: "table table-bordered table-striped mini table-hover"
                });
            })
        }

        $scope.down = function (item, index) {
            let index_current = -1;
            let index_next = -1;
            let itemsSorted = $filter('orderBy')($scope.chart.details.sql.table_spec, 'order')

            for (let i = 0; itemsSorted.length > i; i++) {
                if (itemsSorted[i].COLUMN_NAME === item.COLUMN_NAME) {
                    index_current = itemsSorted[i].order;
                }
            }
            for (let i = 0; itemsSorted.length > i; i++) {
                if (itemsSorted[i].order > index_current) {
                    index_next = itemsSorted[i].order;
                    item.order = index_next;
                    itemsSorted[i].order = index_current;
                    break;
                }
            }
        }

        $scope.up = function (item, index) {
            let index_current = -1;
            let index_prev = -1;
            // let itemsFiltered  = $filter('filter')($scope.chart.details.sql.table_spec, 'order')
            let itemsSorted = $filter('orderBy')($scope.chart.details.sql.table_spec, 'order')
            for (let i = 0; itemsSorted.length > i; i++) {
                if (itemsSorted[i].COLUMN_NAME === item.COLUMN_NAME) {
                    index_current = itemsSorted[i].order;
                    break;
                }
            }
            for (let i = itemsSorted.length - 1; -1 < i; i--) {
                if (itemsSorted[i].order < index_current) {
                    index_prev = itemsSorted[i].order;
                    item.order = index_prev;
                    itemsSorted[i].order = index_current;
                    break;
                }
            }
        }

        $scope.get_distinct_value = function (field) {
            if (field.DATA_TYPE === 'varchar' || field.DATA_TYPE === 'nvarchar') {
                if (!(field.available_values)) {
                    $http.post('/api/v1/bi_chart/' + $stateParams.id + '/get_distinct/', field).then(function (data) {
                        field.available_values = data.data;
                    });
                }
            }
        }

        $scope.get_sql_script = function () {
            $http.post('/api/v1/bi_chart/' + $stateParams.id + "/get_charting_tsql/", $scope.chart.details.sql).then(function (data) {
                $scope.chart.details.sql.script = data.data.sql;
                $scope.get_table_data();
            })
        }

        $scope.get_selected_chart = function () {
            let has_select_sql_script = false;
            let has_sqls = false;
            let has_table_spec = false;

            $http.get('/api/v1/bi_chart/' + $stateParams.id + "/").then(function (data) {
                $scope.chart = data.data;
                if ($scope.chart.details.sql) {
                    if ($scope.chart.details.sql.id) {
                        has_select_sql_script = true;
                    }

                    if ($scope.chart.details.sql.script) {
                        has_sqls = true;
                    }
                    if ($scope.chart.details.sql.table_spec) {
                        has_table_spec = true;
                    }
                }

                if (has_select_sql_script === true) {
                    if (has_sqls === false) {
                        $scope.get_sql_script();
                    }
                    if (has_table_spec === false) {
                        $scope.sql_change();
                    }
                }


            })
        }

        $scope.sql_change = function () {
            $http.get('/api/v1/bi_chart/' + $stateParams.id + '/get_mssql_table_info/').then(function (data) {
                $scope.chart.details.sql.table_spec = data.data;
            })
        }

        let init = function () {
            $scope.get_sqls();
            $scope.get_selected_chart();

        }

        $scope.save = function () {
            $http.patch('/api/v1/bi_chart/' + $stateParams.id + "/", $scope.chart).then(function (data) {

            });
        }

        init();


        // ------------------------------------------------------
        // ------------------------------------------------------
        // ------------------------ charting --------------------
        // ------------------------------------------------------
        $scope.request = {};
        $scope.chart_data = {};
        $scope.chart_data_history = [];
        $scope.request.level = 0;
        $scope.is_loading_data = false;
        let current_canvas;
        let current_chart;
        $scope.init_chart = function () {

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
            $http.post('/api/v1/bi_chart/' + $stateParams.id + "/get_chart_with_request/", $scope.request).then(
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
                if ($element.find("#chart_preview")[0]) {
                    current_canvas = $element.find("#chart_preview")[0].getContext('2d');
                    current_chart = new Chart(current_canvas, {
                        type: $scope.chart.details.chart_type,
                        data: {},
                        plugins: [ChartDataLabels],
                        option: {}
                    });

                }

            }
            $scope.get_request_data();


            // $scope.init_chart();


        }


        // ------------------------------------------------------
        // ------------------------------------------------------
        // ------------------------------------------------------
        // ------------------------------------------------------


    })