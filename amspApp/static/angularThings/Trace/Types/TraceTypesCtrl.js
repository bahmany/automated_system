'use strict';

angular.module('AniTheme').controller(
    'TraceTypesCtrl',
    function ($scope,
              $translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {


        $scope.tracetype = {};
        $scope.tracetypes = {};
        $scope.tracetype.permittedUsers = [];
        $scope.selectedPosition = {};
        $scope.searchText = "";


        $scope.new = function () {
            $scope.tracetype = {};
            $scope.tracetype.permittedUsers = [];
            $scope.selectedPosition = {};
            $scope.searchText = "";
        }

        $scope.post = function () {

            if ($scope.tracetype.id) {
                $http.patch("/api/v1/trace_type/" + $scope.tracetype.id + "/", $scope.tracetype).then(function (data) {
                    if (data.data.id) {
                        $scope.tracetype = {};
                        $scope.tracetype.permittedUsers = [];
                        $scope.selectedPosition = {};
                        $scope.searchText = "";
                        // $scope.dests = [];
                        // $scope.srcs = [];
                        $scope.list();
                    }


                });


            }
            else {
                $http.post("/api/v1/trace_type/", $scope.tracetype).then(function (data) {
                    if (data.data.id) {
                        $scope.tracetype = {};
                        $scope.tracetype.permittedUsers = [];
                        $scope.selectedPosition = {};
                        $scope.searchText = "";
                        // $scope.dests = [];
                        // $scope.srcs = [];
                        $scope.list();
                    }


                });
            }
            ;
        }


        $scope.editItem = function (ev, item) {
            $http.get("/api/v1/trace_type/" + item.id + "/ret/").then(function (data) {
                $scope.tracetype = data.data;
            })
        }

        $scope.list = function () {
            $http.get("/api/v1/trace_type/").then(function (data) {
                $scope.tracetypes = data.data;
            })
        }

        $scope.list();


        $scope.addToPermittedList = function () {
            $scope.tracetype.permittedUsers.push($scope.selectedPosition);
        }

        $scope.removeFromList = function (index) {
            $scope.tracetype.permittedUsers.splice(index, 1);
        }

        $scope.dests = [];
        $scope.getDests = function () {
            $http.get("/api/v1/trace_fromto_cat/get_dest/").then(function (data) {
                $scope.dests = data.data;
            })

        }

        $scope.srcs = [];
        $scope.getSources = function () {
            $http.get("/api/v1/trace_fromto_cat/get_source/").then(function (data) {
                $scope.srcs = data.data;

            })
        };

        $scope.getDests();
        $scope.getSources();


    })
;