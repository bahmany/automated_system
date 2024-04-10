'use strict';


angular.module('AniTheme').controller(
    'bodyCtrl',
    function ($scope,
              $injector,
              $timeout,
              $location,
              $state,
              $http) {

        $scope.gotoHome = function () {
            $state.go('dashboard');
            // angular.element(document.querySelector('#main-menu')).fadeOut(100)
        }

        $scope.gotoLetter = function () {
            $state.go('inbox');

        }


    })