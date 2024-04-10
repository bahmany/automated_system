'use strict';

angular.module('AniTheme')
    .controller('ReportsCtrl', function ($scope, $http, $translate, $rootScope, $stateParams, $state, $modal, $location, ReportsService) {
        $scope.selectedBpmn = 'فرآیند را انتخاب نمایید...';
        $scope.searchData = {};
        $scope.searchData.isDone = "2";
        $scope.bpmns = [];
        $scope.currentPage = 1;
        $scope.maxSize = 5;
        $scope.itemsPerPage = 14;
        $scope.selectedIDs = [];
        $scope.selectedNames = [];
        $scope.fieldsList = [];
        $scope.dataList = [];
        $scope.selected = {};
        $scope.totalItems = 0;
        $scope.listBpmns = function () {
            ReportsService.getListBpmns().then(function (data) {
                $scope.bpmns = data.data;
            });

        };
        $scope.changeBpmn = function () {
            $scope.selectedBpmn = $('#bpmnSe option:selected').text();
            ReportsService.getFieldsList($scope.searchData.bpmn).then(function (data) {
                $scope.fieldsList = data.data;

            });

        };
        $scope.dlXlsFile = function () {
            $scope.records = $.grep($scope.fieldsList, function (itm) {
                return $scope.selected[itm.name];
            });
            $scope.selectedIDs = [];
            $scope.selectedNames = [];
            for (var i = 0; i < $scope.records.length; i++) {
                $scope.selectedIDs.push($scope.records[i].name);
                $scope.selectedNames.push($scope.records[i].displayName);
            }
            ReportsService.getXlsFile($scope.searchData.bpmn, JSON.stringify($scope.selectedNames), JSON.stringify($scope.selectedIDs), $scope.searchData);
        };
        $scope.ShowReport = function () {
            $scope.records = $.grep($scope.fieldsList, function (itm) {
                return $scope.selected[itm.name];
            });
            $scope.selectedIDs = [];
            $scope.selectedNames = [];
            for (var i = 0; i < $scope.records.length; i++) {
                $scope.selectedIDs.push($scope.records[i].name);
                $scope.selectedNames.push($scope.records[i].displayName);
            }
            if ($scope.searchData.bpmn != undefined) {
                ReportsService.getDataList($scope.searchData.bpmn, JSON.stringify($scope.selectedIDs), $scope.searchData, $scope.currentPage).then(function (data) {
                    $scope.dataList = data.data;
                    $scope.totalItems = data.data.count;

                    $scope.itemsFrom = ($scope.currentPage - 1) * $scope.itemsPerPage;

                    $scope.itemsFrom += 1;

                    $scope.itemsTo = $scope.itemsFrom + $scope.itemsPerPage - 1;
                    if ($scope.itemsTo > $scope.totalItems) {
                        $scope.itemsTo = $scope.totalItems;
                    }

                });
            }
        };
        $scope.$watchGroup(["currentPage","itemsPerPage"], function () {
            $scope.ShowReport();
        });
        $scope.listBpmns();
    });

