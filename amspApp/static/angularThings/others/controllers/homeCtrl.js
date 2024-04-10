'use strict';

/**
 * @ngdoc function
 * @name AniTheme.controller:HomeCtrl
 * @description
 * # HomeCtrl
 * Controller of AniTheme
 */
angular.module('AniTheme').controller('HomeCtrl', function ($scope, $cookies, $timeout, $http, dashService, $rootScope) {

    $scope.boxes = {};
    $scope.MSTemplates = [];

    // if (!($cookies.sessionid)){
    //     window.location.href = "/login";
    // }


    var originatorEv;
    $scope.openMenu = function ($mdOpenMenu, ev) {
        originatorEv = ev;
        $mdOpenMenu(ev);
    };


    $scope.getCurrentMSBoxes = function () {
        dashService.getMSBoxes().then(function (data) {
            $scope.boxes = data.data;
        });
    };
    $scope.MSTemplatesList = function () {
        dashService.getMSTemplates().then(function (data) {
            $scope.MSTemplates = data.data;
        });
    };

    $scope.ChangeBox = {};
    $scope.changeCurrentMSBoxes = function (newId, boxNumber) {
        $scope.ChangeBox.new = newId;
        $scope.ChangeBox.boxPos = boxNumber;
        dashService.changeMSBox($scope.ChangeBox).then(function (data) {
            $scope.getCurrentMSBoxes();
        });

    };
    // $scope.getCurrentMSBoxes();


    $scope.profile = {};
    $scope.GetDashboard = function () {
        $http.get("/api/v1/forced/getDashboard/").then(function (data) {
            $scope.profile = data.data;
            $scope.firstTimeChanged = true;
            $scope.$watchCollection($scope.profile, function (newVal, oldVal) {
                if ($scope.firstTimeChanged == false) {
                    //console.log("changed");
                }
                $scope.firstTimeChanged = true;
            })

        })
    };
    $scope.backColors = [
        '#00bcd4',
        '#8bc34a',
        '#ff9800',
        '#607d8b'
    ];

    $scope.SetStaticForBlock = function (blockItem, staticItem) {
        //blockItem.static_id = staticItem.id;
        //$http.post("/api/v1/forced/setDashboard/", $scope.profile).then(function (data) {
        //    $scope.profile = data;
        //})
    };


    $scope.GetDashboard();
    $scope.MSTemplatesList();


});