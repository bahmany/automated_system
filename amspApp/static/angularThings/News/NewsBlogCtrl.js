'use strict';


angular.module('AniTheme').controller(
    'NewsBlogCtrl',
    function ($scope,
              $translate,
              $http,
              $q, $mdDialog,
              $rootScope,
              $modal) {


        $scope.filter = {};
        $scope.News = {};
        $scope.list = function () {
            $http.get("/api/v1/news/?q="+$scope.filter.search).then(function (data) {
                $scope.News = data.data;
            });
        }

        $scope.list();

    });