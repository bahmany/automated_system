'use strict';

angular.module('AniTheme').controller(
    'TraceEntryCtrl',
    function ($scope,
              $translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {


        $scope.userActivities = [];
        $scope.getUserActivities = function () {
            $http.get("/api/v1/trace_entry/get_user_activities/").then(function (data) {
                $scope.userActivities = data.data;
            });
        };

        $scope.getUserActivities();


        $scope.currentItem = {};
        $scope.openItem = function (ev, item) {
            $scope.currentItem = item;
        }


        $scope.$watch("searchVch", function (old, ne) {
            $scope.getCardexByVch($scope.searchVch);
        })


        $scope.odoo_res = {};
        $scope.get_odoo_inv_details = function (id) {
            $http.get("/api/v1/trace_entry/" + id + "/get_odoo_inventory_details/").then(function (data) {
                if (data.data.stock) {
                    $scope.odoo_res = data.data;
                }
            })
        }

        $scope.$watch("entry.details.codeOdoo", function (_new, old) {
            if (!($scope.entry)) {
                return
            }
            if (!($scope.entry.details)) {
                return
            }
            if (!($scope.entry.details.codeOdoo)) {
                return
            }
            $scope.get_odoo_inv_details($scope.entry.details.codeOdoo);
        })


        $scope.hamk_res = {};
        $scope.getCardexByVch = function (searchVch) {
            $http.get("/api/v1/trace_entry/" + searchVch + "/get_cardex_vch/?stock=" + $scope.currentItem.destination.exp.hamkaranCode).then(function (data) {
                if (data.data.id) {
                    $scope.hamk_res = data.data.res;
                }
            });
        }


        $scope.CardexSelected = [];
        $scope.AddToCardexSelected = function (item) {
            $scope.CardexSelected.push(item);
        }

        $scope.entry = {};
        $scope.getEntryCode = function (ev) {
            $scope.entry.tracetype = $scope.currentItem.id;
            $http.post("/api/v1/trace_entry/", $scope.entry).then(function (data) {
                if (data.data.id) {
                    $scope.entry = data.data;
                } else {

                }
            })

        }


    })
;