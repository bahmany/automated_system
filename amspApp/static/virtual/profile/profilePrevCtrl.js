'use strict';

angular.module('RahsoonApp').controller(
    'profilePrevCtrl',
    function ($scope,
              $translate,
              $q, $location,
              $http,
              $rootScope,
              $timeout) {

        $scope.prev = {};

        $scope.GetAll = function () {
            $http.get("/reg/api/v1/login/get_prev/").then(function (data) {
                $scope.prev = data.data;
            })
        }
        $scope.GetAll();



        $scope.downloadResume =  function (str) {
            downloadURL('/api/v1/file/upload?q=' + $scope.prev.Resume.resume);
        }

    });