'use strict';


angular.module('AniTheme').controller(
    'BIPageCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope, $stateParams,
              $mdDialog,
              $location,
              $http) {


        $scope.page = {};


        $scope.get_page = function () {
            $scope.page = {};
            $scope.page.details = {};
            $scope.page.details.rows = [];
            $scope.page.previous_page = [];
            $scope.page.groups_allowed = [];
            $scope.page.users_allowed = [];

            $http.get("/api/v1/bi_dashboard_page/" + $stateParams.id + "/").then(function (data) {
                $scope.page = data.data;
                if (!($scope.page.details.rows)) {
                    $scope.page.details.rows = [];
                }
            })
        }

        $scope.get_page();





    })