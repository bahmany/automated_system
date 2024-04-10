'use strict';
angular.module('AniTheme')
    .controller(
        'SalesProfilePhonesCtrl',
        function ($scope, $window, $http, $translate, $rootScope, $stateParams, $location, $$$, $filter) {

            $scope.mobiles = {};
            $scope.list = function (page, search, page_size) {
                $http.get("/api/v1/salesProfile/listMobs/?page=" + page.toString() + "&search=" + search + "&page_size=" + page_size.toString()).then(function (data) {
                    $scope.mobiles = data.data;
                })
            };
            // $scope.list(1, '', 20);

            $scope.postcell = function (cell) {
                $http.patch("/api/v1/salesProfile/" + cell.id + "/", cell).then(function (data) {
                    $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");

                    // $scope.mobiles = data.data;
                })

            };

            $scope.profilesSearchText = "";
            $scope.$watch("profilesSearchText", function () {
                $scope.list(1, $scope.profilesSearchText, 20);
            });

            $scope.gotopage = function (url) {
                $http.get(url).then(function (data) {
                    $scope.mobiles = data.data;
                })

            }

        });

