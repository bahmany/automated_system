'use strict';

angular.module('AniTheme').controller(
    'sahmHakaranBaseCtrl',
    function ($scope,
              //$translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {

        $scope.result = {};

            $scope.callHamkranSahm = function () {
                $http.get("/Financial/api/v1/tashbasehamk/updateFromSG/").then(function (data) {
                    if (data.data.result) {
                        $scope.result = data.data.result;
                    }
                })
            }

    });
