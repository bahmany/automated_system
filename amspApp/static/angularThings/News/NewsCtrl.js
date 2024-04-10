'use strict';


angular.module('AniTheme').controller(
    'NewsCtrl',
    function ($scope,
              $translate,
              $http,
              $q, $mdDialog,
              $rootScope,
              $modal) {


        $scope.filter = {};
        $scope.Newses = {};
        $scope.list = function () {
            $http.get("/api/v1/news/?q="+$scope.filter.search).then(function (data) {
                $scope.Newses = data.data;
            });
        }

        $scope.list();

    });