'use strict';

angular.module('RahsoonApp').controller(
    'step1Ctrl',
    function ($scope,
              $translate,
              $q, $location,
              $http,
              $rootScope,
              $timeout) {


        $scope.Shenasnameh = {};
        LoadSteps($rootScope, $scope, $http, $location);
        $scope.Get("1", "Shenasnameh");


    })