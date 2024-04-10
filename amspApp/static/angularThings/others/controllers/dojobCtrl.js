'use strict';

angular.module('AniTheme')
    .controller('dojobCtrl', function ($scope, $http, $translate, $rootScope, $stateParams, $modal, $location, taskService, bpmnService) {
        $scope.sendingData={};
        $scope.completeTask = function () {
            taskService.completeJob($stateParams.taskId,$scope.sendingData).then(function (data) {
            });

        };

        $scope.renderForm = function () {
            taskService.retrieveTask($stateParams.taskId).then(function (data) {
                bpmnService.retrieveBpmn(data.data['bpmnId']).then(function (dataBpmn) {

                    dataBpmn.data['form'].some(function (element, index, array) {
                        if (element["bpmnObjID"] == data.data["thisStep"]) {
                            $scope.formSchema = element['schema'];

                        }
                    });
                });
            });
        };

        $scope.renderForm();
    });

