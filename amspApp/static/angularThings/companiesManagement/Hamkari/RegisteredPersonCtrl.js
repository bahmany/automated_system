'use strict';
angular.module('AniTheme')
    .controller('RegisteredPersonCtrl', function ($scope, $window, $http, $translate, $rootScope, $stateParams, $location, $$$, $filter) {

        $scope.page = 1;
        $scope.wait = false;

        $scope.personPageTo = function (page) {
            $scope.wait = true;

            if (page) {
                $http.get(page).then(function (data) {
                    $scope.wait = false;

                    $scope.jobItems = data.data;
                }).catch(function () {
                    $scope.wait = false;

                });
            }
        }
        $scope.personsSearchText = "";


        $scope.$watch("personsSearchText", function () {
            $scope.list();
        });


        var baseUrl = "/api/v1/companies/" + $stateParams.companyid + "/hamkari/" + $stateParams.item + "/registeredToHire/";
        $scope.persons = {};
        $scope.list = function () {
            $scope.wait = true;
            $http.get(baseUrl + "?q=" + $scope.personsSearchText + "&page=" + $scope.page.toString() + "&page_size=10").then(function (data) {
                $scope.wait = false;
                $scope.persons = data.data;
                $scope.page = data.data.current_page;
            }).catch(function () {
                $scope.wait = false;

            })
        };

        // getting list of registered
        $scope.list();

        $scope.OpenResume = function (item) {

            $window.open("/#/dashboard/previewResume/" + item.id);


        }


        $scope.Seen = function (item) {
            item.profile.extra.seen = !(Boolean(item.profile.extra.seen));

            $http.post(baseUrl + "Seen/", {invID: item.id, pos: item.profile.extra.seen}).then(function (data) {
                
            })
        }
        $scope.Fail = function (item) {
            item.profile.extra.fail = !(Boolean(item.profile.extra.fail));

            $http.post(baseUrl + "Fail/", {invID: item.id, pos: item.profile.extra.fail}).then(function (data) {
            })
        }
        $scope.Accept = function (item) {
            item.profile.extra.accept = !(Boolean(item.profile.extra.accept));

            $http.post(baseUrl + "Accept/", {invID: item.id, pos: item.profile.extra.accept}).then(function (data) {
            })
        }
    });
