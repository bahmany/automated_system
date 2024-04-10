'use strict';


angular.module('AniTheme').controller(
    'ReadNewsCtrl',
    function ($scope,
              $translate,
              $http, $stateParams,
              $q, $mdDialog,
              $rootScope,
              $modal) {


        $scope.GetNews = function () {
            $http.get("/api/v1/news/" + $stateParams.NewsID + "/read/").then(function (data) {
                $scope.news = data.data;
            })
        }


        $scope.GetNews();

    });