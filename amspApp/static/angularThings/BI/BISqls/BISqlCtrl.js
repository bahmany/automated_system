'use strict';


angular.module('AniTheme').controller(
    'BISqlCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope, $stateParams,
              $mdDialog,
              $location,
              $http) {


        $scope.sql = {};

        $scope.get = function () {
            if ($stateParams.id === '0') {
                return
            }
            if (!($scope.sql.def_name)) {
                $scope.sql.def_name = "";
            }
            $http.get('/api/v1/bi_sqls/' + $stateParams.id + '/').then(function (data) {
                $scope.sql = data.data;
            });
        }

        $scope.datatablesnames = {};

        $scope.get_datatable = function () {
            $http.get('/api/v1/datatable/').then(function (data) {
                $scope.datatablesnames = data.data;
            })
        }

        $scope.save = function () {
            if ($stateParams.id !== '0') {
                $http.patch('/api/v1/bi_sqls/' + $scope.sql.id + "/", $scope.sql).then(function (data) {

                });

            } else {
                $http.post('/api/v1/bi_sqls/', $scope.sql).then(function (data) {

                });

            }
        }


        $scope.get();
        $scope.get_datatable();


    })



