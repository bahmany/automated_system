'use strict';

angular.module('AniTheme').controller(
    'ReportMorekhasiSaatiCtrl',
    function ($scope,
              $translate,
              $q, $http,
              $rootScope,
              $modal) {

        $scope.result = [];
        $scope.asd = {};
        $scope.get_current_year_morekhasi = function () {
            $http.get('/api/v1/morekhasi_saati/get_mandeh_morekhasi_current_year/').then(function (data) {
                $scope.result = data.data;
            });




        }

        $scope.get_current_year_morekhasi();
    });




