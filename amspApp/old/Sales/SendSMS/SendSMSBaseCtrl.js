'use strict';
angular.module('AniTheme')
    .controller(
        'SendSMSBaseCtrl',
        function ($scope, $window, $http, $translate, $rootScope, $stateParams, $location, $$$, $filter) {

            $scope.sms = {};
            $scope.send_sms = function () {
                $http.post('/api/v1/salesConv/send_free_sms/', $scope.sms).then(function (data) {

                })
            }

            $scope.send_sms_async = function () {
                $http.post('/api/v1/salesConv/send_free_sms_async/', $scope.sms).then(function (data) {

                })
            }

        })