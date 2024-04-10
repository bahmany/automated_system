'use strict';
angular.module('AniTheme')
    .controller(
        'KhoroojRep1Ctrl',
        function ($scope, $window, $http, $translate, $rootScope, $stateParams, $location, $$$, $filter) {

            $scope.report_result = []

            $scope.report1 = false;
            $scope.report2 = false;

            $scope.get_report = function (report_type) {

                $http.get('/api/v1/hamkaranKhorooj/get_report/?typeof=' + report_type).then(function (data) {
                    $scope.report_result = data.data;
                    $scope.report1 = true;
                    $scope.report2 = false;
                });
            }
            $scope.get_trace_report = function (report_type) {

                $http.get('/api/v1/hamkaranKhorooj/get_trace_report/?typeof=' + report_type).then(function (data) {
                    $scope.report_trace_result = data.data;
                    $scope.report1 = false;
                    $scope.report2 = true;
                });
            }

        });