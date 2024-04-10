'use strict';

var globalxml = "";
angular.module('AniTheme')
    .controller('BAMCtrl', function ($scope, $http, $translate, $rootScope, $state, $stateParams, $location, $modal, bamService) {


        $scope.bam = {};
        $scope.globalpos = '';
        $scope.current = {};
        $scope.bpmn = {};
        $scope.oldBpmn = {};
        $scope.timeouts = [];
        $scope.currentPage = 1;
        $scope.maxSize = 5;
        $scope.itemsPerPage = 14;
        $scope.lunchedProcess = {};


        $scope.selectedShakhesId = "";


        $scope.showShakhes = function (shakhesId, item) {
            $scope.selectedShakhesId = shakhesId;
            $state.go("company.bam.shakhes", {companyid: $stateParams.companyid, shakhesId: shakhesId});


        };
        $scope.newBAM = function (shakhesId, item) {
            $state.go("company.bam.new", {companyid: $stateParams.companyid});

        };


        $scope.editShakhes = function (shakhesId, item) {
            $scope.shakhesId = shakhesId;
            $state.go("company.bam.edit", {shakhesId: shakhesId});
        };

        $scope.destroyShakhes = function (shakhesObj) {
            swal({
                title: "آیا به حذف این شاخص مطمئن هستید؟ ",
                text: "این شاخص از سیستم حذف خواهد شد, وقابل بازگرداندن نخواهد بود. ",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "بله, حذف کن!",
                showLoaderOnConfirm: true,
                closeOnConfirm: false
            }, function () {
                bamService.hideShakhes($stateParams.companyid, shakhesObj.id).then(function (data) {

                    swal("خذف شد!", "شاخص از سیستم حذف شد.", "success");
                    $scope.getShakhesList();
                    $state.go("company.bam");
                });


            });

        };


        $scope.retrieveShakhes = function (id) {
            bamService.retrieveShakhes(id).then(function (data) {
                $scope.bam.name = data.data['name'];
            });
        };


        $scope.getShakhesList = function () {
            bamService.listShakhes($stateParams.companyid, $scope.currentPage, $scope.searchInput, $scope.itemsPerPage).then(function (data) {
                $scope.data = data.data;
                $scope.totalItems = data.data.count;
                if (($scope.searchInput == undefined) || ($scope.searchInput == '')) {
                    $scope.totalItemsCount = data.data.count;
                }
                $scope.itemsFrom = ($scope.currentPage - 1) * $scope.itemsPerPage;

                $scope.itemsFrom += 1;

                $scope.itemsTo = $scope.itemsFrom + $scope.itemsPerPage - 1;
                if ($scope.itemsTo > $scope.totalItems) {
                    $scope.itemsTo = $scope.totalItems;
                }

                $scope.foundedItemsCount = data.data.count;
            });

        };
        $scope.getShakhesList();
        $scope.$on('refreshList', function (event, args) {

            $scope.getShakhesList();
        });

        $scope.clearAllTimeouts = function () {
            for (var i = 0; i < $scope.timeouts.length; i++) {
                clearTimeout($scope.timeouts[i])
            }
        };

    });
