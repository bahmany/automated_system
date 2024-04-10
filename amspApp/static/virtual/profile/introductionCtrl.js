'use strict';

angular.module('RahsoonApp').controller(
    'introductionCtrl',
    function ($scope,
              $translate,
              $q, $location,
              $http,
              $rootScope,
              $timeout) {


        $scope.jobs = {};


        $scope.getJobs = function () {
            $http.get("/reg/api/v1/jobs/").then(function (data) {
                $scope.jobs = data.data;
            });
        }
        $scope.getProfileLevel = function () {
            $http.get("/reg/api/v1/users/GetProfileLevel/").then(function (data) {
                $scope.level = data.data;
            })
        };
        $scope.getProfileLevel();
        $scope.getJobs();


    });