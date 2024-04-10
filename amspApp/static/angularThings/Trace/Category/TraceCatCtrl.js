'use strict';

angular.module('AniTheme').controller(
    'TraceCategoryCtrl',
    function ($scope,
              $translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {


        $scope.tracecat = {};
        $scope.traces = {};

        $scope.list = function () {
            $http.get("/api/v1/trace_fromto_cat/").then(function (data) {
                $scope.traces = data.data;
            })

        };

        $scope.list();


        $scope.post = function (ev) {

            if ($scope.tracecat.id) {
                $http.patch("/api/v1/trace_fromto_cat/" + $scope.tracecat.id + "/", $scope.tracecat).then(function (data) {
                    $scope.list();
                    $scope.tracecat = {};
                })

            } else {
                $http.post("/api/v1/trace_fromto_cat/", $scope.tracecat).then(function (data) {
                    $scope.list();
                    $scope.tracecat = {};
                })
            }

        }

        $scope.editItem = function (ev, item) {
            $http.get("/api/v1/trace_fromto_cat/" + item.id + "/").then(function (data) {
                $scope.tracecat = data.data;
            })
        }


        $scope.add = function () {
            $scope.tracecat = {};
        }


        $scope.isHakTrue = false;
        $scope.$watch("tracecat.exp.hamkaranCode", function (old, newv) {
            $scope.isHakTrue = false;
            if (!($scope.tracecat.exp)) {
                return
            }

            if ($scope.tracecat.exp.hamkaranCode > -1 && $scope.tracecat.exp.hamkaranCode < 100) {
                $http.get("/api/v1/trace_fromto_cat/" + $scope.tracecat.exp.hamkaranCode + "/getH/").then(function (data) {
                    if (data.data.id) {
                        $scope.catHamk = data.data.title;
                        $scope.isHakTrue = true;
                    } else {

                    }
                })
            }
        })

    });