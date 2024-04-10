'use strict';
angular.module('AniTheme')
    .controller(
        'KhoroojRep1Ctrl',
        function ($scope, $window, $http, $translate, $rootScope, $stateParams, $location, $$$, $filter) {

            $scope.report_result = []

            $scope.report1 = false;
            $scope.report2 = false;
            $scope.is_loading = false;

            $scope.get_report = function (report_type) {
                $scope.is_loading = true;
                $http.get('/api/v1/hamkaranKhorooj/get_report/?typeof=' + report_type).then(function (data) {
                    if (data.data.result) {
                        $scope.report_result = data.data.result;
                        $scope.startdate = data.data.startdate;
                        $scope.enddate = data.data.enddate;
                        $scope.report1 = true;
                        $scope.report2 = false;
                        $scope.total_kg = data.data.total_kg;
                        $scope.total_cnt = data.data.total_cnt;
                    }

                    $scope.is_loading = false;
                }).catch(function () {
                    $scope.is_loading = false;

                });
            }

            $scope.get_report('4');

        });