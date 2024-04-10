'use strict';

angular.module('AniTheme')
    .controller('DoMessageProcessCtrl', function ($scope, $http, $translate, $rootScope, $stateParams, $state, $modal, $location, messageProcessService, bpmnService) {
        $scope.sendingData = {};
        $scope.current = {};
        $scope.userOptions = [];
        $scope.chartOptions = [];
        $scope.chartSelected = [];
        $scope.userSelected = [];
        $scope.messagePData = {};
        //var viewer;
        //viewer = new BpmnModule({container: '#bpmn-viewer'});


        $scope.listCharts = function (companyId) {
            bpmnService.listCharts(companyId).then(function (data) {
                $scope.sendingData.formData.chartOptions = data.data.results;
                $scope.sendingData.formData.chartOptions.shift();
            });

        };
        $scope.listUsers = function (companyId, chartId) {
            if (!((companyId == undefined) || (chartId == undefined))) {
                bpmnService.listUsers(companyId, chartId).then(function (data) {
                    $scope.sendingData.formData.userOptions = data.data.results;
                });
            }
        };
        $scope.initUsers = function () {
            bpmnService.getCurrent(0).then(function (data) {
                $scope.current = data.data;
                $scope.listCharts($scope.current.company);

            });
        };
        $scope.$watch("sendingData.formData.chartSelected", function (newVal, oldVal) {
            $scope.listUsers($scope.current.company, newVal);
        });

        $scope.completeIt = function () {

            messageProcessService.destroyMessage($stateParams.messageProcessId).then(function (data) {

                swal({
                    title: "پیام از قسمت پیام ها حذف شد.",
                    text: "این پیام در قسمت پایش کار یا بایگانی قابل مشاهده است",
                    type: "success"
                }, function () {
                    $state.go("message-process-dashboard");
                });

            });
        };

        $scope.current = {};
        $scope.bpmn = {};
        $scope.renderForm = function () {
            messageProcessService.retrieveMessageProcess($stateParams.messageProcessId).then(function (data) {
                        $scope.messagePData = data.data;
                bpmnService.getCurrent(0).then(function (dataCurrnet) {
                    $scope.current = dataCurrnet.data;
                        $scope.bpmn = data.data['bpmn'];
                        data.data['bpmn']['form'].some(function (element, index, array) {
                            if (element["bpmnObjID"] == data.data["thisStep"]) {
                                $scope.formSchema = element['schema'];

                            }
                        });
                        $scope.sendingData.formData = data.data.formData;
                        if (!($scope.sendingData.formData.chartSelected)) {

                            $scope.initUsers();
                        }
                });

            });
        };

        $scope.renderForm();


    });

