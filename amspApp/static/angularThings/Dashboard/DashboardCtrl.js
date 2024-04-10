'use strict';


$(".block-header").hide();

angular.module('AniTheme').controller(
    'DashboardCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope,
              $http,
              $modal,
              $location,
              $log,
              $timeout,
              $mdSidenav) {


        $scope.images = [];
        $scope.infos = {};
        $scope.getImages = function () {
            $http.get("/api/v1/file/images/?t=200").then(function (data) {
                $scope.infos = data.data;
                $scope.images = data.data.results;
            })
        };


        $scope.LoadMorePic = function () {
            $http.get($scope.infos.next).then(function (data) {
                $scope.infos = data.data;
                $scope.images.push.apply($scope.images, data.data.results)

            })
        };


        $scope.selectedPics = [];
        $scope.SelectPic = function (item) {

        }

        $scope.getImages();



    }
);