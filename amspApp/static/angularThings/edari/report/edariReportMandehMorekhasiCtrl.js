'use strict';

angular.module('AniTheme').controller(
    'edariReportMandehMorekhasiCtrl',
    function ($scope,
              $translate,
              $q, $http,
              $rootScope,
              $modal) {


        $scope.asd = {};
        $scope.init = function () {
            $http.get('/api/v1/morekhasi_saati/get_mandeh_morekhasi_koli/').then(function (data) {
                $scope.asd = data.data;
            })


        }
        $scope.init();


    });




