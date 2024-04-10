'use strict';
var globalxml = '';


angular.module('AniTheme')
    .controller('messageProcessCtrl', function ($scope, $http, $translate, $state, $rootScope, $modal, $location, messageProcessService, bpmnService) {

        $scope.bpmns = {};
        $scope.current = {};
        $scope.bpmn = {};
        $scope.oldBpmn = {};
        $scope.timeouts = [];
        $scope.currentPage = 1;
        $scope.selectedMsgProcessId = '';
        $scope.maxSize = 5;
        $scope.itemsPerPage = 14;

        // it's for get edit form field data
        //$scope.createLunchedProcess = function () {
        //
        //    var modalInstance = $modal.open({
        //        animation: true,
        //        templateUrl: 'GenericModalTaskCreate.html',
        //        controller: 'ModalLunchedProcessCreateInstanceCtrl',
        //        size: '',
        //        resolve: {}
        //    });
        //
        //    modalInstance.result.then(function (res) {
        //        $scope.getLunchedProcessList();
        //    }, function () {
        //
        //    });
        //};

        $scope.retrieveMessageProcess = function (MessageProcessId, item) {
            // debugger;
            if (item.hasOwnProperty("seen")) {
                item.seen = 1;
            }
            $scope.selectedMsgProcessId = MessageProcessId;
            $state.go("doMessage", {messageProcessId: MessageProcessId});

        };

        $scope.getMessageProcessList = function () {
            messageProcessService.listMessages($scope.currentPage, $scope.searchInput, $scope.itemsPerPage, "Inbox").then(function (data) {
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
        $scope.$watchGroup(["currentPage", "itemsPerPage"], function () {
            $scope.getMessageProcessList();
        });

        $scope.clearAllTimeouts = function () {
            for (var i = 0; i < $scope.timeouts.length; i++) {
                clearTimeout($scope.timeouts[i])
            }
        };
        $scope.searchMessageProcess = function () {
            $scope.clearAllTimeouts();
            $scope.timeouts.push(
                setTimeout($scope.getMessageProcessList, 1500)
            );

        };
        //$scope.getMessageProcessList();

    }
)
;
//angular.module('AniTheme').controller('ModalLunchedProcessCreateInstanceCtrl', function ($scope, $modalInstance, $http, bpmnService, $translate, LunchedProcessService) {
//
//    $scope.bpmns = {};
//    $scope.current = {};
//    $scope.lunchedProcess = {};
//    $scope.listBpmns = function (current) {
//        bpmnService.listBpmns(current.company, 1, undefined, 99).then(function (data) {
//            $scope.bpmns = data['results'];
//
//        });
//    };
//    bpmnService.getCurrent(0).then(function (data) {
//        $scope.current = data;
//        $scope.listBpmns(data);
//    });
//
//    $scope.saveLunchedProcess = function () {
//        LunchedProcessService.createLunchedProcess($scope.lunchedProcess).then(function (data) {
//            $modalInstance.close('u did it with success');
//        }).catch(function (data) {
//            $scope.errors = data.message;
//        });
//    };
//    $scope.cancel = function () {
//        $modalInstance.dismiss('cancel');
//    };
//});