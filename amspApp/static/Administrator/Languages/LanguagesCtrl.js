'use strict';




angular.module('RahsoonAdminApp')
    .controller("LanguagesController", function ($scope, $http, $timeout, $log) {
        $scope.items = [];
        $scope.search = "";
        $scope.new = {};

        $scope.list = function () {
            $http.get("/api/v1/languages/").then(function (data) {
                $scope.items = data.data;
            })
        };

        $scope.add = function (item) {
            $http.post("/api/v1/languages/", item).then(function () {
                $scope.list();
                $scope.new = {};

            })
        }

        $scope.update = function (item) {
            $http.patch("/api/v1/languages/" + item.id + "/", item).then(function () {

            })
        };

        $scope.remove = function (item) {
            $http.delete("/api/v1/languages/" + item.id + "/").then(function () {
                $scope.list();
            })
        };

        $scope.list();

    });

