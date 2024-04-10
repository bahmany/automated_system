'use strict';


angular.module('AniTheme').controller(
    'BIPageDesignerCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope, $stateParams,
              $mdDialog,
              $location,
              $http) {

        // $scope.rows = [];
        $scope.current_page = {};
        $scope.current_page.details = {};
        $scope.current_page.details.rows = [];
        $scope.current_page.previous_page = [];
        $scope.current_page.groups_allowed = [];
        $scope.current_page.users_allowed = [];

        $scope.get_page = function () {
            $scope.current_page = {};
            $scope.current_page.details = {};
            $scope.current_page.details.rows = [];
            $scope.current_page.previous_page = [];
            $scope.current_page.groups_allowed = [];
            $scope.current_page.users_allowed = [];

            $http.get("/api/v1/bi_dashboard_page/" + $stateParams.id + "/").then(function (data) {
                $scope.current_page = data.data;
                if (!($scope.current_page.details.rows)) {
                    $scope.current_page.details.rows = [];
                }
            })
        }

        $scope.get_page();

        $scope.add_row = function () {
            $scope.current_page.details.rows.push({'children': [{}]});
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


        $scope.setCell = function (row, count) {
            row.count = count;
            if (count === 1) {
                row['children'] = [{'header': null, 'flex': 100}]
            }
            if (count === 2) {
                row['children'] = [{'header': null, 'flex': 50}, {'header': null, 'flex': 50}]

            }
            if (count === 3) {
                row['children'] = [{'header': null, 'flex': 32}, {'header': null, 'flex': 32}, {
                    'header': null,
                    'flex': 32
                }]

            }
            if (count === 4) {
                row['children'] = [{'header': null, 'flex': 25}, {'header': null, 'flex': 25}, {
                    'header': null,
                    'flex': 25
                }, {'header': null, 'flex': 25}]
            }
            if (count === 5) {
                row['children'] =
                    [
                        {'header': null, 'flex': 25},
                        {'header': null, 'flex': 25},
                        {'header': null, 'flex': 50}
                    ]
            }
            if (count === 6) {
                row['children'] =
                    [
                        {'header': null, 'flex': 25},
                        {'header': null, 'flex': 50},
                        {'header': null, 'flex': 25}
                    ]
            }
            if (count === 7) {
                row['children'] =
                    [
                        {'header': null, 'flex': 50},
                        {'header': null, 'flex': 25},
                        {'header': null, 'flex': 25}
                    ]
            }
        }

        $scope.setHeader = function (row) {
            var ss = prompt("لطفا عنوان را وارد نمایید", "")
            if (ss) {
                row['header'] = ss;
            }

        }

        $scope.charts = [];
        $scope.get_all_charts = function () {
            $http.get('/api/v1/bi_chart/').then(function (data) {
                $scope.charts = data.data;
            })
        }
        $scope.get_all_charts();

        $scope.save = function () {

            $http.patch("/api/v1/bi_dashboard_page/" + $scope.current_page['id'] + "/", $scope.current_page).then(function (data) {

            })


        }


    });