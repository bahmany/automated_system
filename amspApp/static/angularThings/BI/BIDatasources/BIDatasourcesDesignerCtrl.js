'use strict';


angular.module('AniTheme').controller(
    'BIDatasourcesDesignerCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope, $stateParams,
              $mdDialog,
              $location,
              $http) {

        $scope.datasource = {};
        $scope.get_current_source = function () {
            $http.get('/api/v1/bi_datasources/' + $stateParams.id + "/").then(function (data) {
                $scope.datasource = data.data;
            })
        }


        $scope.get_current_source()


    })