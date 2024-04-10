'use strict';

angular.module('RahsoonApp').controller(
    'step7Ctrl',
    function ($scope,
              $translate,
              $q, $location,
              $http,
              $rootScope,
              $timeout) {

        var model_name = "Job";
        var model_id = "7";

        $scope[model_name] = {};
        $scope[model_name].items = [];
        $scope[model_name + "Item"] = {};
        LoadSteps($rootScope, $scope, $http, $location);
        $scope.Get(model_id, model_name);
        $scope.AddToList = function (item) {
            if (!($scope[model_name].hasOwnProperty("items"))) {
                $scope[model_name].items = [];
            }
            $scope[model_name].items.push(item);
            $scope[model_name + "Item"] = {};
        };
        $scope.itemEdit = function (item, index) {
            $scope[model_name + "Item"] = item;
            $scope[model_name].items.splice(index, 1);
        };
    })