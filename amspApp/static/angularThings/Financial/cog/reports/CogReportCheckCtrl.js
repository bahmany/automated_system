'use strict';

angular.module('AniTheme').controller(
    'cogReportCheckCtrl',
    function ($scope,
              //$translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {



        $scope.check = {}
        $scope.getCheck = function () {
            $http.get("/Financial/api/v1/cogb/callIntegrity/").then(function (data) {
                $scope.check = data.data;
            })
        }

        $scope.getCheck();




    });
