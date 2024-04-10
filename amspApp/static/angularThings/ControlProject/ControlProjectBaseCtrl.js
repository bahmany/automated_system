'use strict';


angular.module('AniTheme').controller(
    'ControlProjectBaseCtrl',
    function ($scope,
              $translate,
              $http,
              $q, $mdDialog,
              $rootScope,
              $modal) {

        $scope.selectedTest = null;

        $scope.$watch("selectedTest", function () {
            console.log($scope.selectedTest);
        })

    })