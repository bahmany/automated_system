'use strict';
var globalxml = '';


angular.module('AniTheme')
    .controller('lunchedProcessArchiveCtrl', function ($scope, $http, $translate, $rootScope, $modal, $state, $location, LunchedProcessService, bpmnService) {

        $scope.bpmns = {};
        $scope.current = {};
        $scope.bpmn = {};
        $scope.oldBpmn = {};
        $scope.timeouts = [];
        $scope.currentPage = 1;
        $scope.maxSize = 5;
        $scope.itemsPerPage = 14;

        // it's for get edit form field data

        $scope.reviewDataProcess = function (LunchedProcessId) {
            $state.go("trackLunchedProcess", {lunchedProcessId: LunchedProcessId});

        };

        $scope.destroyProcessArchive = function (LunchedProcessObj) {
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
                    if (res.positionDocument == LunchedProcessObj.position_id) {
                        LunchedProcessService.hideLunchedProcessArchive(LunchedProcessObj.id).then(function (data) {

                            swal("Deleted!", "Your imaginary file has been deleted.", "success");
                            $scope.lunchedProcessArchiveList();
                        });
                    } else {
                        swal("Permission!", "You're nor be able to delete this process.", "error");

                    }
                });


            });

        };
        $scope.retrieveLunchedProcess = function (id) {
            bpmnService.retrieveProcess(id, 'LunchedProcessArchive').then(function (data) {
                $scope.bpmn.name = data.data['name'];
                $scope.bpmn.xml = data.data['xml'];
                $scope.bpmn.description = data.data['description'];
                $scope.bpmn.id = data.data['id'];
                globalxml = data.data['xml'];
            });
        };
        $scope.starterSearchItems = [];
        $scope.bpmnSearchItems = [];
        //$scope.retrieveSearchBar = function () {
        //LunchedProcessService.retrieveSearchBar().then(function (data) {
        //    $scope.starterSearchItems = data.starters;
        //    $scope.bpmnSearchItems = data.bpmns;
        //});
        //};
        //$scope.LPAresults = [];
        //$scope.listLunchedArchiveFromStarter = function (id) {
        //    LunchedProcessService.listLunchedArchive('posId=' + id).then(function (data) {
        //        $scope.LPAresults = data;
        //    });
        //};
        //$scope.LPAresults = [];
        //$scope.listLunchedArchive = function () {
        //    LunchedProcessService.listLunchedArchive('bpmnId=' + 1).then(function (data) {
        //        $scope.LPAresults = data;
        //
        //    });
        //};
        //$scope.listLunchedArchive();

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

                    $scope.lunchedProcessArchiveList();
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
        $scope.searchData = {};
        $scope.lunchedProcessArchiveList = function () {
            bpmnService.getCurrent(0).then(function (res) {
                $scope.globalposid = res.data.positionDocument;
                LunchedProcessService.listLunchedProcessArchive($scope.currentPage, $scope.searchInput, $scope.itemsPerPage, $scope.searchData, "LunchedProcessArchive").then(function (data) {
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

        $scope.$watchGroup(["searchData.bpmn","searchData.name","searchData.receive","searchData.starter","searchData.fromDate","searchData.toDate","currentPage","itemsPerPage"], function () {
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
                setTimeout($scope.lunchedProcessArchiveList, 1500)
            );

        };
    });
angular.module('AniTheme').controller('ModalLunchedProcessCreateInstanceCtrl', function ($scope, $modalInstance, $http, bpmnService, $translate, LunchedProcessService) {

    $scope.bpmns = {};
    $scope.current = {};
    $scope.lunchedProcess = {};
    bpmnService.getCurrent(0).then(function (data) {
        $scope.current = data.data;

    });
    bpmnService.listBpmns($scope.current.company, 1, undefined, 99).then(function (data) {
        $scope.bpmns = data.data['results'];

    });
    $scope.saveLunchedProcess = function () {
        LunchedProcessService.createLunchedProcess($scope.lunchedProcess).then(function (data) {
            $modalInstance.close('u did it with success');
        }).catch(function (data) {
            $scope.errors = data.message;
        });
    };
    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});