'use strict';
var globalxml = '';


angular.module('AniTheme')
    .controller('DoneProcessArchiveCtrl', function ($scope, $http, $translate, $rootScope, $state, $modal, $location, LunchedProcessService, bpmnService) {

        $scope.bpmns = {};
        $scope.current = {};
        $scope.bpmn = {};
        $scope.oldBpmn = {};
        $scope.searchData = {};
        $scope.timeouts = [];
        $scope.currentPage = 1;
        $scope.maxSize = 5;
        $scope.itemsPerPage = 14;
        $scope.reviewMyProcess = function (LunchedProcessId) {
            $state.go("trackDoneProcess", {lunchedProcessId: LunchedProcessId});
        };
        // it's for get edit form field data

        //$scope.doJob = function (LunchedProcessId) {
        //    $location.url('/dashboard/dojob/' + LunchedProcessId);
        //};
        $scope.destroyDoneProcess = function (LunchedProcessObj) {
            swal({
                title: "Are you sure?",
                text: "You will not be able to recover this imaginary file!",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Yes, delete it!",
                showLoaderOnConfirm: true,
                closeOnConfirm: false
            }, function () {
                bpmnService.getCurrent(0).then(function (res) {
                    $scope.current = res.data;
                    if (res.data.positionDocument == LunchedProcessObj.position_id) {
                        LunchedProcessService.hideDoneProcess(LunchedProcessObj.id).then(function (data) {

                            swal("Deleted!", "Your imaginary file has been deleted.", "success");
                            $scope.DoneProcessArchiveList();
                        });
                    } else {
                        swal("Permission!", "You're nor be able to delete this process.", "error");

                    }
                });

            });

        };
        $scope.retrieveLunchedProcess = function (id) {
            bpmnService.retrieveProcess(id, 'DoneProcessArchive').then(function (data) {
                $scope.bpmn.name = data.data['name'];
                $scope.bpmn.xml = data.data['xml'];
                $scope.bpmn.description = data.data['description'];
                $scope.bpmn.id = data.data['id'];
                globalxml = data.data['xml'];
            });
        };

        $scope.buildForm = function (id) {
            $rootScope.id = id;
            $location.url('/dashboard/buildForm');
        };
        $scope.lunchedProcessDelete = function (id) {
            var modalInstance = $modal.open({
                animation: true,
                templateUrl: 'GenericModalAreYouSure.html',
                controller: 'ModalAreYouSureInstanceCtrl',
                size: '',
                resolve: {}
            });
            modalInstance.result.then(function (selectedItem) {
                bpmnService.lunchedProcessDelete(id).then(function (data) {

                    $scope.DoneProcessArchiveList();
                }).catch(function (data) {
                    var modalInstance = $modal.open({
                        animation: true,
                        templateUrl: 'GenericModalPermissionDenied.html',
                        controller: 'ModalPermissionDeniedInstanceCtrl',
                        size: '',
                        resolve: {}
                    });
                });

            }, function () {
            });

        };

        $scope.DoneProcessArchiveList = function () {
            bpmnService.getCurrent(0).then(function (res) {
                $scope.globalposid = res.data.positionDocument;
                LunchedProcessService.listDoneProcessArchive($scope.currentPage, $scope.searchInput, $scope.itemsPerPage, $scope.searchData, "DoneProcessArchive").then(function (data) {
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
            });
        };
        $scope.$watchGroup(["searchData.bpmn","currentPage","itemsPerPage","searchData.name","searchData.receive","searchData.starter","searchData.fromDate","searchData.toDate"], function () {
            $scope.searchLunchedProcess();
        });

        $scope.clearAllTimeouts = function () {
            for (var i = 0; i < $scope.timeouts.length; i++) {
                clearTimeout($scope.timeouts[i])
            }
        };
        $scope.searchLunchedProcess = function () {
            $scope.clearAllTimeouts();
            $scope.timeouts.push(
                setTimeout($scope.DoneProcessArchiveList, 1500)
            );

        };
    });