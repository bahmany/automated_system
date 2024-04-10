'use strict';

angular.module('AniTheme').controller(
    'dashCtrl',
    function ($scope,
              $translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {


        // checking if authenticated


        $timeout(function () {
            $.material.init();
        }, 1200);

    });
