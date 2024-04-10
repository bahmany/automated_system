'use strict';


angular.module('AniTheme').controller(
    'BIShowPagesCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope, $stateParams,
              $mdDialog,
              $location,
              $http) {


        $scope.page = {};
        $scope.get_page = function () {
            $http.get("/api/v1/bi_dashboard_page/" + $stateParams.id + "/get_page/").then(function (data) {
                $scope.page = data.data;
            })
        }

        $scope.get_page();

        $scope.init_cell = function (event, col){
            console.log(col);
        }


    })