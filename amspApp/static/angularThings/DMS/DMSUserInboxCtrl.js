'use strict';

angular.module('AniTheme').controller('DMSUserInboxCtrl', function ($q, $location, $http, $scope, $state, $stateParams, $rootScope, Upload, DMSManagementService) {

    $scope.currentNavItem = 'page1';


    $scope.listDMS = [];
    $scope.searchData = {};
    $scope.searchData.isDone = "2";
    $scope.bpmns = [];
    $scope.currentPage = 1;
    $scope.maxSize = 5;
    $scope.itemsPerPage = 14;
    $scope.totalItems = 0;
    $scope.getlistDMS = function () {
        DMSManagementService.getDMSListForUser($scope.currentPage).then(function (data) {
            $scope.listDMS = data.data.results;
            $scope.totalItems = data.data.count;

            $scope.itemsFrom = ($scope.currentPage - 1) * $scope.itemsPerPage;

            $scope.itemsFrom += 1;

            $scope.itemsTo = $scope.itemsFrom + $scope.itemsPerPage - 1;
            if ($scope.itemsTo > $scope.totalItems) {
                $scope.itemsTo = $scope.totalItems;
            }
        }).catch(function (data) {

        });
    };
    $scope.getlistDMS();
});

