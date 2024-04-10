'use strict';

angular.module('AniTheme').controller(
    'ReportMyTaradodCtrl',
    function ($scope,
              $translate,
              $q, $http,
              $rootScope,
              $modal) {


        $scope.result = '';
        $scope.filter = {
            year: 0,
            month: 0
        };

        $scope.getTaradod = function () {
            $scope.result = "";
            $http.post('/api/v1/hz/getTaradod/', $scope.filter).then(function (data) {
                $scope.result = data.data;
                $scope.KarkardViewModel = data.data;
            });



        };

        $scope.getTaradod(1399, 6);

    });




