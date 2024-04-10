'use strict';

angular.module('AniTheme')
    .controller('GetDiagramProcessCtrl', function ($scope, $http, $translate, $rootScope, $stateParams, $state, $modal, $location, LunchedProcessService, bpmnService) {
        $scope.sendingData = {};
        $scope.current = {};
        $scope.userOptions = [];
        $scope.chartOptions = [];
        $scope.chartSelected = [];
        $scope.userSelected = [];
        $scope.lunchedPData = {};
        var viewer;
        viewer = new BpmnModule({container: '#bpmn-viewer'});
        $scope.current = {};
        $scope.bpmn = {};
        $scope.renderDiagram = function () {
            LunchedProcessService.retrieveLunchedProcessDiagram($stateParams.lunchedProcessId).then(function (data) {
                $scope.lunchedPData = data.data;
                bpmnService.getCurrent(0).then(function (dataCurrnet) {
                    $scope.current = dataCurrnet.data;
                    $scope.current.taskId = $scope.lunchedPData.curAndPrevSteps.taskId;
                    $scope.bpmn.xml = data.data['xml'];
                    viewer.importXML($scope.bpmn.xml, function (err) {

                        var canvas = viewer.get('canvas');
                        
                        $scope.lunchedPData.bpmnForm.some(function (element) {
                            $scope.lunchedPData.thisSteps.some(function (element2) {
                                if (element["bpmnObjID"] == element2[$scope.current.positionDocument]) {
                                    canvas.addMarker(element2[$scope.current.positionDocument], 'thisstep');
                                }
                            });
                        });
                        $scope.lunchedPData.pastSteps.shift();
                        $scope.lunchedPData.pastSteps.forEach(function (obj, index) {
                            if (obj) {
                                if (obj.split(".").length == 1) {
                                    canvas.addMarker(obj, 'finished');

                                }

                            }

                        });
                        if (err) {
                            ////console.log('error rendering', err);
                        }
                    });
                });

            });
        };

        $scope.renderDiagram();


    });

