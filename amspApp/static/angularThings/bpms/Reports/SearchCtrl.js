'use strict';

angular.module('AniTheme')
    .controller('SearchCtrl', function ($scope, $http, $translate, $rootScope, $stateParams, $state, $modal, $location) {


        $scope.searchID = "";
        $scope.list = [];
        $scope.Search = function () {
            $http.get("/api/v1/reports/SearchID/?q=" + $scope.searchID).then(function (data) {
                if (data.data["ok"] == "ok") {
                    $scope.list = data.data["results"];
                } else {
                    $scope.list = []
                }
            });
        }
    });

