'use strict';


angular.module('AniTheme').controller(
    'QCManualsController',
    function ($scope,
              $translate,
              $http,
              $q, $mdDialog,
              $rootScope,
              $modal) {


        $scope.searchText = "";

        $scope.$watch("searchText", function () {
            $scope.startSearch();
        });

        $scope.wait = false;
        $scope.startSearch = function () {
            $scope.wait = true;
            $http.get("/api/v1/qc/searchref/?q=" + $scope.searchText).then(function (data) {
                $scope.searchResult = data.data;
                $scope.wait = false;
            }).catch(function () {
                $scope.wait = false;
            })
        };

        $scope.getImg = function (item) {
            if (item) {
                if (item.img) {
                    return "/api/v1/file/upload?q=thmum700_" + item.img

                }

            }
        };
        $scope.getImgFull = function (item) {
            if (item) {
                if (item.img) {
                    return "/api/v1/file/upload?q=" + item.img

                }

            }
        };

        $scope.OpenManualByOutline = function (item) {
            $scope.current = item;
        };
        $scope.OpenManual = function (item) {
            $scope.current = item;

            $("#search").fadeOut(function () {
                $("#pageViewer").fadeIn();
            })
        };

        $scope.return = function () {
            $("#pageViewer").fadeOut(function () {
                $("#search").fadeIn();
            })

        };

        $scope.Download = function (item) {
            downloadURL("/api/v1/file/upload?q=" + item.img);
        };

    });