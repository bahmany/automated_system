'use strict';

angular.module('AniTheme').controller(
    'baseCtrl',
    function ($scope,
              $translate,
              $q, $mdToast,
              $http,
              $rootScope,
              $timeout) {

        var last = {
            bottom: false,
            top: true,
            left: false,
            right: true
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
                // if (response.data == 'ok') {
                //
                // }
            });
        };


        $rootScope.$on("showToast", function (event, args) {
            $scope.showActionToast(args);
        });

        $rootScope.previousState;
        $rootScope.currentState;
        $rootScope.$on('$stateChangeSuccess', function (ev, to, toParams, from, fromParams) {
            $rootScope.previousState = from.name;
            $rootScope.currentState = to.name;
            console.log('Previous state:' + $rootScope.previousState)
            console.log('Current state:' + $rootScope.currentState)
        });

    });