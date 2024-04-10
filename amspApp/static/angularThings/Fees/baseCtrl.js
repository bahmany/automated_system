'use strict';


angular.module('AniTheme').controller(
    'FeeBaseCtrl',
    function ($scope,
              $translate,
              $q, $http,
              $rootScope,
              $modal) {


        $scope.percentTable = [];

        $scope.setting = {
            formulas: true,
            licenseKey: 'non-commercial-and-evaluation',
            afterInit: function () {
                $scope.hot.instance = this;
            }
        }


    });




