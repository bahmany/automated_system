'use strict';

angular.module('RahsoonApp').controller(
    'step11resultsCtrl',
    function ($scope,
              $translate,
              $q, $location,
              $http,
              $rootScope,
              $timeout) {

// getting all registered jobs
        $scope.regJobs = [];
        $scope.GetRegisteredJobs = function () {
            $http.get("/reg/api/v1/login/get_reg_jobs/").then(function (data) {
                $scope.regJobs = data.data;
            })
        };

        $scope.GetRegisteredJobs();


        $scope.CheckIsSelectedClicked = function (item) {
            for (var i = 0; item.extra.requests.length > i; i++) {
                if (item.extra.requests[i].is_selected) {
                    return true
                }
            }
            return false
        }

    });