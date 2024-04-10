'use strict';

angular.module('AniTheme').controller(
    'ReportMorekhsiRoozanehListCtrl',
    function ($scope,
              $translate,
              $q, $http,
              $rootScope,
              $modal) {


        $scope.result2 = {};
        $scope.init = function () {
            $http.get('/api/v1/morekhasi_saati/get_mandeh_report_detail/').then(function (data) {
                $scope.result2 = data.data;
            });


        }
        $scope.init();


    });





