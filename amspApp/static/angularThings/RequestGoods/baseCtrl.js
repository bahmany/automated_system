'use strict';

angular.module('AniTheme').controller(
    'baseRGCtrl',
    function ($scope,
              $translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {

        // RGgoods

        $scope.filter = {
            not_finished: true,
            has_roll: false,
            archive: false,
            search: ""
        }

        $scope.$watchCollection("filter",function () {
            $scope.list();
        });

        $scope.requests = {};
        $scope.list = function () {
            $http.get("/api/v1/rg/?nf=" + $scope.filter.not_finished + "&hr=" + $scope.filter.not_finished + "&a=" + $scope.filter.archive + "&s=" + $scope.filter.search
            ).then(function (data) {
                $scope.requests = data.data;
            }).catch(function (err) {

            })
        }

        $scope.GoToPage = function (url) {
            if (url) {

                $http.get(url).then(function (data) {
                    $scope.requests = data.data;
                })
            }
        };


        $scope.init = function () {
        }


        $scope.init();
    })
;