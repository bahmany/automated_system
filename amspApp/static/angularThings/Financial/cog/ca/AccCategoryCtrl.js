'use strict';

angular.module('AniTheme').controller(
    'AccCategoryCtrl',
    function ($scope,
              //$translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {


        $scope.cat = {};
        $scope.storeCats = function () {
            $http.post("/Financial/api/v1/ca/saveCats/", $scope.cat).then(function (data) {

            })
        }
        $scope.getCats = function () {
            $http.get("/Financial/api/v1/ca/getCats/").then(function (data) {
                $scope.cat = data.data;
            })
        }
$scope.getCats();

    });


