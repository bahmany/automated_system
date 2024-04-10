'use strict';


angular.module('AniTheme').controller(
    'SecSideCtrl',
    function ($scope,
              $translate,
              $q,$stateParams,
              $rootScope,
              $modal,
              $http,
              SecSideService) {

        ActivateSelectSec($scope, $http, $stateParams);



    });