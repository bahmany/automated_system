'use strict';

angular.module('RahsoonApp').controller(
    'leftSidebarCtrl',
    function ($scope,
              $translate,
              $q,
              $http,
              $rootScope,$mdSidenav,
              $timeout) {


        $scope.colse = function () {
            $mdSidenav('left').close()
                .then(function () {
                    $log.debug("close left is done");
                })
        }

    });