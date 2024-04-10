'use strict';

angular.module('RahsoonApp').controller(
    'baseCtrl',
    function ($scope,
              $translate,
              $q, $mdToast,
              $http,
              $rootScope,
              $timeout) {


        $scope.logout = function () {
            $http.get('/api/v1/auth/logout/').then(function (data) {
                window.location.href = "/";
            });

        };


        $scope.getProfileLevel = function () {
            $http.get("/api/v1/users/GetProfileLevel/").then(function (data) {
                $scope.level = data.data;
            })
        };
        $scope.getProfileLevel();

        var last = {
            bottom: true,
            top: false,
            left: true,
            right: false
        };
        $scope.toastPosition = angular.extend({}, last);
        $scope.getToastPosition = function () {
            sanitizePosition();
            return Object.keys($scope.toastPosition)
                .filter(function (pos) {
                    return $scope.toastPosition[pos];
                })
                .join(' ');
        };

        function sanitizePosition() {
            var current = $scope.toastPosition;
            if (current.bottom && last.top) current.top = false;
            if (current.top && last.bottom) current.bottom = false;
            if (current.right && last.left) current.left = false;
            if (current.left && last.right) current.right = false;
            last = angular.extend({}, current);
        }

        $scope.showActionToast = function (msg) {
            var toast = $mdToast.simple()
                .textContent(msg)
                .action('OK')
                .highlightAction(true)
                .position($scope.getToastPosition());
            $mdToast.show(toast).then(function (response) {
                if (response.data == 'ok') {

                }
            });
        };


        $rootScope.showActionToast = function (msg) {
            var toast = $mdToast.simple()
                .textContent(msg)
                .action('OK')
                .highlightAction(true)
                .position($scope.getToastPosition());
            $mdToast.show(toast).then(function (response) {
                if (response.data == 'ok') {

                }
            });
        };

        $rootScope.$on("showToast", function (event, args) {
            $scope.showActionToast(args);
        });
    });