'use strict';
angular.module('AniTheme')
    .controller(
        'HavalehForooshTraceCtrl',
        function (
            $scope,
            $window,
            $http,
            $translate,
            $rootScope,
            $stateParams,
            $location,
            $$$,
            $filter
        ) {

            $scope.is_loading = false;

            $scope.get_trace_report = function (report_type) {
                $scope.is_loading = true;

                $http.get('/api/v1/hamkaranKhorooj/get_trace_report/?typeof=' + report_type).then(function (data) {
                    $scope.report_trace_result = data.data;
                    $scope.report1 = false;
                    $scope.report2 = true;
                    $scope.is_loading = false;
                }).catch(function () {
                    $scope.is_loading = false;

                });

            }

            $scope.get_trace_report('5');


        })