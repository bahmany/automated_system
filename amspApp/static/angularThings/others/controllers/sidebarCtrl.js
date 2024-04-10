'use strict';

/**
 * @ngdoc function
 * @name AniTheme.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of AniTheme
 */
angular.module('AniTheme').controller('sidenavCtrl', function ($scope, $http, $rootScope, $interval, $location, $$$, menu, $mdSidenav, $cookies) {
    $scope.selectedMenu = 'dashboard';
    $scope.collapseVar = 0;
    $scope.statistics = {};


    $scope.OpenDash = function () {
        $location.url("/");
    }




    var vm = $scope;
    //functions for menu-link and menu-toggle
    vm.isOpen = isOpen;
    vm.toggleOpen = toggleOpen;
    vm.autoFocusContent = false;
    vm.menu = menu;
    // $scope.initMenu = function () {
    $http.get("scripts/directives/menu/", function (data) {
        vm.menu.sections = data.data;
    })


    // };
    // $scope.initMenu();


    $scope.isProfileBtnsClose = false;

    $scope.openProfileBtns = function () {
        $scope.isProfileBtnsClose = !$scope.isProfileBtnsClose;
    }




    $scope.close = function () {
        // Component lookup should always be available since we are not using `ng-if`
        $mdSidenav('left').close()
            .then(function () {
            });
    };


    vm.status = {
        isFirstOpen: true,
        isFirstDisabled: false
    };

    function isOpen(section) {
        return menu.isSectionSelected(section);
    }

    function toggleOpen(section) {
        menu.toggleSelectSection(section);
    }

    $scope.logout = function () {
        $http.get('/api/v1/auth/logout/').then(function (data) {
            window.location.href = "/";
        });
    };


    $scope.check = function (x) {

        if (x == $scope.collapseVar)
            $scope.collapseVar = 0;
        else
            $scope.collapseVar = x;
    };

    $scope.multiCheck = function (y) {

        if (y == $scope.multiCollapseVar)
            $scope.multiCollapseVar = 0;
        else
            $scope.multiCollapseVar = y;
    };
    $scope.currentUser = {};
    $scope.getUserInfo = function () {
        $http.get("/api/v1/users/GetUserInfo/").then(function (data) {
            $scope.currentUser = data.data;
        })
    };
    $scope.getUserInfo();

});
